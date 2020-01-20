from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import base64
import collections
import io
import os
import sys

import tensorflow
import tensorflow.compat.v1 as tf
import magenta
import magenta.music as mm
from magenta.music import midi_synth
from magenta.music import constants


import pretty_midi
import bokeh
import bokeh.plotting
from IPython import display
import numpy as np
import pandas as pd
from scipy.io import wavfile
from six.moves import urllib
import tempfile
import six

from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from magenta.music.protobuf import generator_pb2
from magenta.music.protobuf import music_pb2
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel
from magenta.models.score2perf import score2perf

from tensor2tensor import models
from tensor2tensor import problems
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.utils import decoding
from tensor2tensor.utils import trainer_lib



def note_sequence_to_midi_file(sequence, output_file,
                               drop_events_n_seconds_after_last_note=None):
    """Convert NoteSequence to a MIDI file on disk.
    Time is stored in the NoteSequence in absolute values (seconds) as opposed to
    relative values (MIDI ticks). When the NoteSequence is translated back to
    MIDI the absolute time is retained. The tempo map is also recreated.
    Args:
      sequence: A NoteSequence.
      output_file: String path to MIDI file that will be written.
      drop_events_n_seconds_after_last_note: Events (e.g., time signature changes)
          that occur this many seconds after the last note will be dropped. If
          None, then no events will be dropped.
    """
    print("파일로 변환/저장 중")
    pretty_midi_object = note_sequence_to_pretty_midi(
        sequence, drop_events_n_seconds_after_last_note)
    with tempfile.NamedTemporaryFile() as temp_file:
        pretty_midi_object.write(temp_file)
        # Before copying the file, flush any contents
        temp_file.flush()
        # And back the file position to top (not need for Copy but for certainty)
        temp_file.seek(0)
        tf.gfile.Copy(temp_file.name, output_file, overwrite=True)


def note_sequence_to_pretty_midi(
        sequence, drop_events_n_seconds_after_last_note=None):
    """Convert NoteSequence to a PrettyMIDI.
    Time is stored in the NoteSequence in absolute values (seconds) as opposed to
    relative values (MIDI ticks). When the NoteSequence is translated back to
    PrettyMIDI the absolute time is retained. The tempo map is also recreated.
    Args:
      sequence: A NoteSequence.
      drop_events_n_seconds_after_last_note: Events (e.g., time signature changes)
          that occur this many seconds after the last note will be dropped. If
          None, then no events will be dropped.
    Returns:
      A pretty_midi.PrettyMIDI object or None if sequence could not be decoded.
    """
    ticks_per_quarter = sequence.ticks_per_quarter or constants.STANDARD_PPQ

    max_event_time = None
    if drop_events_n_seconds_after_last_note is not None:
        max_event_time = (max([n.end_time for n in sequence.notes] or [0]) +
                          drop_events_n_seconds_after_last_note)

    # Try to find a tempo at time zero. The list is not guaranteed to be in order.
    initial_seq_tempo = None
    for seq_tempo in sequence.tempos:
        if seq_tempo.time == 0:
            initial_seq_tempo = seq_tempo
            break

    kwargs = {}
    if initial_seq_tempo:
        kwargs['initial_tempo'] = initial_seq_tempo.qpm
    else:
        kwargs['initial_tempo'] = constants.DEFAULT_QUARTERS_PER_MINUTE

    pm = pretty_midi.PrettyMIDI(resolution=ticks_per_quarter, **kwargs)

    # Create an empty instrument to contain time and key signatures.
    instrument = pretty_midi.Instrument(0)
    pm.instruments.append(instrument)

    # Populate time signatures.
    for seq_ts in sequence.time_signatures:
        if max_event_time and seq_ts.time > max_event_time:
            continue
        time_signature = pretty_midi.containers.TimeSignature(
            seq_ts.numerator, seq_ts.denominator, seq_ts.time)
        pm.time_signature_changes.append(time_signature)

    # Populate key signatures.
    for seq_key in sequence.key_signatures:
        if max_event_time and seq_key.time > max_event_time:
            continue
        key_number = seq_key.key
        if seq_key.mode == seq_key.MINOR:
            key_number += mm.midi_io._PRETTY_MIDI_MAJOR_TO_MINOR_OFFSET
        key_signature = pretty_midi.containers.KeySignature(
            key_number, seq_key.time)
        pm.key_signature_changes.append(key_signature)

    # Populate tempos.
    # TODO(douglaseck): Update this code if pretty_midi adds the ability to
    # write tempo.
    for seq_tempo in sequence.tempos:
        # Skip if this tempo was added in the PrettyMIDI constructor.
        if seq_tempo == initial_seq_tempo:
            continue
        if max_event_time and seq_tempo.time > max_event_time:
            continue
        tick_scale = 60.0 / (pm.resolution * seq_tempo.qpm)
        tick = pm.time_to_tick(seq_tempo.time)
        # pylint: disable=protected-access
        pm._tick_scales.append((tick, tick_scale))
        pm._update_tick_to_time(0)
        # pylint: enable=protected-access

    # Populate instrument names by first creating an instrument map between
    # instrument index and name.
    # Then, going over this map in the instrument event for loop
    inst_infos = {}
    for inst_info in sequence.instrument_infos:
        inst_infos[inst_info.instrument] = inst_info.name

    # Populate instrument events by first gathering notes and other event types
    # in lists then write them sorted to the PrettyMidi object.
    instrument_events = collections.defaultdict(
        lambda: collections.defaultdict(list))
    for seq_note in sequence.notes:
        instrument_events[(seq_note.instrument, seq_note.program,
                           seq_note.is_drum)]['notes'].append(
            pretty_midi.Note(
                seq_note.velocity, seq_note.pitch,
                seq_note.start_time, seq_note.end_time))
    for seq_bend in sequence.pitch_bends:
        if max_event_time and seq_bend.time > max_event_time:
            continue
        instrument_events[(seq_bend.instrument, seq_bend.program,
                           seq_bend.is_drum)]['bends'].append(
            pretty_midi.PitchBend(seq_bend.bend, seq_bend.time))
    for seq_cc in sequence.control_changes:
        if max_event_time and seq_cc.time > max_event_time:
            continue
        instrument_events[(seq_cc.instrument, seq_cc.program,
                           seq_cc.is_drum)]['controls'].append(
            pretty_midi.ControlChange(
                seq_cc.control_number,
                seq_cc.control_value, seq_cc.time))

    for (instr_id, prog_id, is_drum) in sorted(instrument_events.keys()):
        # For instr_id 0 append to the instrument created above.
        if instr_id > 0:
            instrument = pretty_midi.Instrument(prog_id, is_drum)
            pm.instruments.append(instrument)
        else:
            instrument.is_drum = is_drum
        # propagate instrument name to the midi file
        instrument.program = prog_id
        if instr_id in inst_infos:
            instrument.name = inst_infos[instr_id]
        instrument.notes = instrument_events[
            (instr_id, prog_id, is_drum)]['notes']
        instrument.pitch_bends = instrument_events[
            (instr_id, prog_id, is_drum)]['bends']
        instrument.control_changes = instrument_events[
            (instr_id, prog_id, is_drum)]['controls']

    return pm


def midi_file_to_note_sequence(midi_file):
    """Converts MIDI file to a NoteSequence.

    Args:
      midi_file: A string path to a MIDI file.

    Returns:
      A NoteSequence.

    Raises:
      MIDIConversionError: Invalid midi_file.
    """
    with tf.gfile.Open(midi_file, 'rb') as f:
        midi_as_string = f.read()
        return midi_to_note_sequence(midi_as_string)


def midi_to_note_sequence(midi_data):
    """Convert MIDI file contents to a NoteSequence.

    Converts a MIDI file encoded as a string into a NoteSequence. Decoding errors
    are very common when working with large sets of MIDI files, so be sure to
    handle MIDIConversionError exceptions.

    Args:
      midi_data: A string containing the contents of a MIDI file or populated
          pretty_midi.PrettyMIDI object.

    Returns:
      A NoteSequence.

    Raises:
      MIDIConversionError: An improper MIDI mode was supplied.
    """
    # In practice many MIDI files cannot be decoded with pretty_midi. Catch all
    # errors here and try to log a meaningful message. So many different
    # exceptions are raised in pretty_midi.PrettyMidi that it is cumbersome to
    # catch them all only for the purpose of error logging.
    # pylint: disable=bare-except
    if isinstance(midi_data, pretty_midi.PrettyMIDI):
        midi = midi_data
    else:
        try:
            midi = pretty_midi.PrettyMIDI(six.BytesIO(midi_data))
        except:
            raise mm.midi_io.MIDIConversionError('Midi decoding error %s: %s' %
                                      (sys.exc_info()[0], sys.exc_info()[1]))
    # pylint: enable=bare-except

    sequence = music_pb2.NoteSequence()

    # Populate header.
    sequence.ticks_per_quarter = midi.resolution
    sequence.source_info.parser = music_pb2.NoteSequence.SourceInfo.PRETTY_MIDI
    sequence.source_info.encoding_type = (
        music_pb2.NoteSequence.SourceInfo.MIDI)

    # Populate time signatures.
    for midi_time in midi.time_signature_changes:
        time_signature = sequence.time_signatures.add()
        time_signature.time = midi_time.time
        time_signature.numerator = midi_time.numerator
        try:
            # Denominator can be too large for int32.
            time_signature.denominator = midi_time.denominator
        except ValueError:
            raise mm.midi_io.MIDIConversionError('Invalid time signature denominator %d' %
                                      midi_time.denominator)

    # Populate key signatures.
    for midi_key in midi.key_signature_changes:
        key_signature = sequence.key_signatures.add()
        key_signature.time = midi_key.time
        key_signature.key = midi_key.key_number % 12
        midi_mode = midi_key.key_number // 12
        if midi_mode == 0:
            key_signature.mode = key_signature.MAJOR
        elif midi_mode == 1:
            key_signature.mode = key_signature.MINOR
        else:
            raise mm.midi_io.MIDIConversionError('Invalid midi_mode %i' % midi_mode)

    # Populate tempo changes.
    tempo_times, tempo_qpms = midi.get_tempo_changes()
    for time_in_seconds, tempo_in_qpm in zip(tempo_times, tempo_qpms):
        tempo = sequence.tempos.add()
        tempo.time = time_in_seconds
        tempo.qpm = tempo_in_qpm

    # Populate notes by gathering them all from the midi's instruments.
    # Also set the sequence.total_time as the max end time in the notes.
    midi_notes = []
    midi_pitch_bends = []
    midi_control_changes = []
    for num_instrument, midi_instrument in enumerate(midi.instruments):
        # Populate instrument name from the midi's instruments
        if midi_instrument.name:
            instrument_info = sequence.instrument_infos.add()
            instrument_info.name = midi_instrument.name
            instrument_info.instrument = num_instrument
        for midi_note in midi_instrument.notes:
            if not sequence.total_time or midi_note.end > sequence.total_time:
                sequence.total_time = midi_note.end
            midi_notes.append((midi_instrument.program, num_instrument,
                               midi_instrument.is_drum, midi_note))
        for midi_pitch_bend in midi_instrument.pitch_bends:
            midi_pitch_bends.append(
                (midi_instrument.program, num_instrument,
                 midi_instrument.is_drum, midi_pitch_bend))
        for midi_control_change in midi_instrument.control_changes:
            midi_control_changes.append(
                (midi_instrument.program, num_instrument,
                 midi_instrument.is_drum, midi_control_change))

    for program, instrument, is_drum, midi_note in midi_notes:
        note = sequence.notes.add()
        note.instrument = instrument
        note.program = program
        note.start_time = midi_note.start
        note.end_time = midi_note.end
        note.pitch = midi_note.pitch
        note.velocity = midi_note.velocity
        note.is_drum = is_drum

    for program, instrument, is_drum, midi_pitch_bend in midi_pitch_bends:
        pitch_bend = sequence.pitch_bends.add()
        pitch_bend.instrument = instrument
        pitch_bend.program = program
        pitch_bend.time = midi_pitch_bend.time
        pitch_bend.bend = midi_pitch_bend.pitch
        pitch_bend.is_drum = is_drum

    for program, instrument, is_drum, midi_control_change in midi_control_changes:
        control_change = sequence.control_changes.add()
        control_change.instrument = instrument
        control_change.program = program
        control_change.time = midi_control_change.time
        control_change.control_number = midi_control_change.number
        control_change.control_value = midi_control_change.value
        control_change.is_drum = is_drum

    # TODO(douglaseck): Estimate note type (e.g. quarter note) and populate
    # note.numerator and note.denominator.

    return sequence


def decode(ids, encoder):
    ids = list(ids)
    if text_encoder.EOS_ID in ids:
        ids = ids[:ids.index(text_encoder.EOS_ID)]
    return encoder.decode(ids)


def piano_continuation_to_note_sequence(primer):
    print('piano continuation 작곡 중...')
    primer_ns = mm.midi_file_to_note_sequence(primer)

    primer_ns = mm.apply_sustain_control_changes(primer_ns)

    targets = uncondi_encoders['targets'].encode_note_sequence(primer_ns)

    targets = targets[:-1]

    decode_length = max(0, 1024 - len(targets))
    if len(targets) >= 1024:
        print('Primer has more events than maximum sequence length; nothing will be generated.')

    sample_ids = next(uncondi_samples)['outputs']

    midi_filename = decode(sample_ids, encoder=uncondi_encoders['targets'])
    ns = mm.midi_file_to_note_sequence(midi_filename)

    # Append continuation to primer.
    return mm.concatenate_sequences([primer_ns, ns])

def music_vae_sample_to_note_sequence(model, num):
  print("music vae가 비트 작곡중")
  music_vae = TrainedModel(
        configs.CONFIG_MAP[model],
        batch_size=4,
        checkpoint_dir_or_path='./contents/'+model+'.tar')

  generated_sequences = music_vae.sample(n=num, length=80, temperature=1.0)

  return generated_sequences[0]


######################음악만들기하기전에이부분실행시키고해야하는데#################
####################################################################################
SF2_PATH = './soundfonts/Yamaha-C5-Salamander-JNv5.1.sf2'
SAMPLE_RATE = 10000

model_name = 'transformer'
hparams_set = 'transformer_tpu'
uncondi_ckpt_path = './contents/unconditional_model_16.ckpt/unconditional_model_16.ckpt'

class PianoPerformanceLanguageModelProblem(score2perf.Score2PerfProblem):
    @property
    def add_eos_symbol(self):
        return True

uncondi_problem = PianoPerformanceLanguageModelProblem()
uncondi_encoders = uncondi_problem.get_feature_encoders()

# Set up HParams.
hparams = trainer_lib.create_hparams(hparams_set=hparams_set)
trainer_lib.add_problem_hparams(hparams, uncondi_problem)
hparams.num_hidden_layers = 16
hparams.sampling_method = 'random'

# Set up decoding HParams.
decode_hparams = decoding.decode_hparams()
decode_hparams.alpha = 0.0
decode_hparams.beam_size = 1

# Create Estimator.
run_config = trainer_lib.create_run_config(hparams)
estimator = trainer_lib.create_estimator(
    model_name, hparams, run_config,
    decode_hparams=decode_hparams)

# Create input generator (so we can adjust priming and
# decode length on the fly).
def input_generator():
    global targets
    global decode_length
    while True:
        yield {
            'targets': np.array([targets], dtype=np.int32),
            'decode_length': np.array(decode_length, dtype=np.int32)
        }

# These values will be changed by subsequent cells.
targets = []
decode_length = 0

# Start the Estimator, loading from the specified checkpoint.
input_fn = decoding.make_input_fn_from_generator(input_generator())
uncondi_samples = estimator.predict(input_fn, checkpoint_path=uncondi_ckpt_path)

# "Burn" one.
_ = next(uncondi_samples)

targets = []
decode_length = 768

# Generate sample events.
sample_ids = next(uncondi_samples)['outputs']

# Decode to NoteSequence.
midi_filename = decode(
    sample_ids,
    encoder=uncondi_encoders['targets'])
uncondi_ns = mm.midi_file_to_note_sequence(midi_filename)

# 비트 만들고 드럼만 남기기
beat = music_vae_sample_to_note_sequence('hierdec-trio_16bar',1)
notes = [note for note in beat.notes if note.is_drum]
del beat.notes[:]
beat.notes.extend(notes)
####################################################################################




# tab1에서 happy에 맞는 음악 만들어달라고 할 때 (/media/happy/에 저장됨)
def tab1_happy():
    happy_sequence = music_pb2.NoteSequence()
    happy_sequence.tempos.add(qpm=150)

    happy_music = piano_continuation_to_note_sequence('./media/primer/prelude_in_c_major.mid')
    happy_time = min(happy_music.total_time * 0.7, beat.total_time)
    print(happy_time)

    for i in happy_music.notes:
        if i.end_time <= happy_time:
            print('happy로 변환')
            happy_sequence.notes.add(pitch=i.pitch, start_time=i.start_time * 0.7, end_time=i.end_time * 0.7,
                                     velocity=min(i.velocity + 5, 127), instrument=i.instrument)

    flag = 1
    for i in beat.notes:
        flag = 1 - flag
        if (i.end_time <= happy_time and flag == 0):
            print('happy에 드럼 추가')
            happy_sequence.notes.add(pitch=i.pitch, start_time=i.start_time, end_time=i.end_time,
                                     velocity=max(i.velocity - 25, 0), instrument=i.instrument, is_drum=True)

    #print(happy_sequence)

    note_sequence_to_midi_file(happy_sequence, './media/happy/my_happy.mid')
    print('happy 끝')


# tab1에서 sad에 맞는 음악 만들어달라고 할 때 (/media/sad/에 저장됨)
def tab1_sad():
    sad_sequence = music_pb2.NoteSequence()
    sad_sequence.tempos.add(qpm=60)

    sad_music = piano_continuation_to_note_sequence('moonlight_sonata.mid')
    sad_time = sad_music.total_time * 1.4

    for i in sad_music.notes:
        print('sad로 변환')
        if (i.start_time > 5.0):
            sad_sequence.notes.add(pitch=i.pitch, start_time=(i.start_time - 5.0) * 1.4,
                                   end_time=(i.end_time - 5.0) * 1.4, velocity=max(i.velocity - 15, 0),
                                   instrument=i.instrument)
    #print(sad_sequence)

    note_sequence_to_midi_file(sad_sequence, './media/sad/my_sad.mid')
    print('sad 끝')


# tab2에서 자기가 준 음악에 맞게 만들어달라고 할 때 (기존 음악 경로랑 새로 저장될 경로 넘겨줘야함)
def tab2_new(my_path, my_new_path):
    new_sequence = piano_continuation_to_note_sequence(my_path)
    note_sequence_to_midi_file(new_sequence, my_new_path)
