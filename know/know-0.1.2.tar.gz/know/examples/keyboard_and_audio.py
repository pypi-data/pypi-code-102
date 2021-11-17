"""Example of processing audio and keyboard streams"""
import time
from typing import Callable, NewType, Any
import json
from stream2py.stream_buffer import StreamBuffer
from keyboardstream2py.keyboard_input import KeyboardInputSourceReader
from audiostream2py.audio import (
    PyAudioSourceReader,
    find_a_default_input_device_index,
)

from i2 import ContextFanout

AudioData = NewType('AudioData', Any)
KeyboardData = NewType('KeyboardData', Any)
AudioDataCallback = Callable[[AudioData], Any]
KeyboardDataCallback = Callable[[KeyboardData], Any]


def default_audio_callback(audio_data):
    if audio_data is not None:
        (audio_timestamp, waveform, frame_count, time_info, status_flags,) = audio_data
        print(
            f'   [Audio] {audio_timestamp}: {len(waveform)=} {type(waveform).__name__}',
            end='\n\r',
        )


def full_audio_print(audio_data):
    if audio_data is not None:
        (audio_timestamp, waveform, frame_count, time_info, status_flags,) = audio_data
        # print(f"{type(audio_data)=}")
        print(
            f'   [Audio] {audio_timestamp=}: {len(waveform)=} {type(waveform).__name__}'
            f' {frame_count=}, {time_info=}, {status_flags=}',
            end='\n\r',
        )


def default_keyboard_event_callback(keyboard_data):
    """Prints some data extracted from keyboard_data
    :param keyboard_data: Input character
    """
    if keyboard_data is not None:
        # print(f"{type(keyboard_data)=}, {len(keyboard_data)=}")
        index, keyboard_timestamp, char = keyboard_data
        print(f'[Keyboard] {keyboard_timestamp}: {char=} ({ord(char)=})', end='\n\r')
        if keyboard_data_signals_an_interrupt(keyboard_data):
            raise KeyboardInterrupt('You want to stop?')


def keyboard_data_signals_an_interrupt(
    keyboard_data, stop_signal_chars=frozenset(['\x03', '\x04', '\x1b'])
):
    """The function returns a positive stop signal (1) if the character is in the
    `stop_signal_chars` set.
    By default, the `stop_signal_chars` contains:
    * \x03: (ascii 3 - End of Text)
    * \x04: (ascii 4 - End of Trans)
    * \x1b: (ascii 27 - Escape)
    (See https://theasciicode.com.ar/ for ascii codes.)

    (1) in the form of a string specifying what the ascii code of the input character was

    :param keyboard_data: Input character
    :param stop_signal_chars: Set of stop characters
    :return:
    """
    if keyboard_data is not None:
        # print(f"{type(keyboard_data)=}, {len(keyboard_data)=}")
        index, keyboard_timestamp, char = keyboard_data
        # print(f'[Keyboard] {keyboard_timestamp}: {char=} ({ord(char)=})', end='\n\r')

        if char in stop_signal_chars:
            return f'ascii code: {ord(char)} (See https://theasciicode.com.ar/)'
        else:
            return False


def handle_input_device_index(input_device_index, verbose=1):
    if input_device_index is None:
        input_device_index = find_a_default_input_device_index()

    audio_src_info = PyAudioSourceReader.info_of_input_device_index(input_device_index)
    if verbose:
        print(f'Starting audio device: {json.dumps(audio_src_info, indent=2)}\n')

    return input_device_index


def keyboard_and_audio(
    input_device_index=None,  # find index with PyAudioSourceReader.list_device_info()
    rate=44100,
    width=2,
    channels=1,
    frames_per_buffer=44100,  # same as sample rate for 1 second intervals
    seconds_to_keep_in_stream_buffer=60,
    audio_data_callback: AudioDataCallback = default_audio_callback,
    keyboard_data_callback: KeyboardDataCallback = default_keyboard_event_callback,
):
    """Starts two independent streams: one for audio and another for keyboard inputs.
    Prints stream type, timestamp, and additional info about data:
    Shows input key pressed for keyboard and byte count for audio

    Press Esc key to quit.

    :param input_device_index: find index with PyAudioSourceReader.list_device_info()
    :param rate: audio sample rate
    :param width: audio byte width
    :param channels: number of audio input channels
    :param frames_per_buffer: audio samples per buffer
    :param seconds_to_keep_in_stream_buffer: max size of audio buffer before data falls off
    :return: None
    """

    input_device_index = handle_input_device_index(input_device_index)

    # converts seconds_to_keep_in_stream_buffer to max number of buffers of size frames_per_buffer
    maxlen = PyAudioSourceReader.audio_buffer_size_seconds_to_maxlen(
        buffer_size_seconds=seconds_to_keep_in_stream_buffer,
        rate=rate,
        frames_per_buffer=frames_per_buffer,
    )
    audio_source_reader = PyAudioSourceReader(
        rate=rate,
        width=width,
        channels=channels,
        unsigned=True,
        input_device_index=input_device_index,
        frames_per_buffer=frames_per_buffer,
    )

    audio_stream_buffer = StreamBuffer(source_reader=audio_source_reader, maxlen=maxlen)
    keyboard_stream_buffer = StreamBuffer(
        source_reader=KeyboardInputSourceReader(), maxlen=maxlen
    )

    from know.util import SlabsPushTuple
    from i2 import HandleExceptions

    slabs = ContextFanout(audio=audio_stream_buffer, keyboard=keyboard_stream_buffer)

    def audio_and_keyboard_data_callback(data):
        audio_data, keyboard_data = data
        if keyboard_data_signals_an_interrupt(keyboard_data):
            raise KeyboardInterrupt('You want to stop?')
        return audio_data_callback(audio_data), keyboard_data_callback(keyboard_data)

    def print_raw(data):
        audio_data, keyboard_data = data
        if keyboard_data_signals_an_interrupt(keyboard_data):
            raise KeyboardInterrupt('You want to stop.')
        if keyboard_data is not None:
            print(f'{keyboard_data=}\n', end='\n\r')
        full_audio_print(audio_data)

    def dict_print_raw(data):
        audio_data = data['audio']
        keyboard_data = data['keyboard']
        if keyboard_data_signals_an_interrupt(keyboard_data):
            raise KeyboardInterrupt('You want to stop.')
        if keyboard_data is not None:
            print(f'{keyboard_data=}\n', end='\n\r')
        full_audio_print(audio_data)

    from know.util import SlabsPush, IteratorExit

    ws = SlabsPush(
        slabs,
        services={
            # 'print': audio_and_keyboard_data_callback,
            'print_raw': dict_print_raw
        },
    )

    with HandleExceptions(
        {
            KeyboardInterrupt: 'You made an interrupt key combo!',
            IteratorExit: 'An iterator raised a IteratorExit',
        }
    ):
        for _ in iter(ws):
            if not ws.slabs['audio'].is_running:
                print("audio isn't running anymore!")
                break

    print(f'\nQuitting the app...\n')


if __name__ == '__main__':
    # TODO: When wrappers.py ready for it, use argh, preprocessing the function so that:
    #   specific (int expected) transformed to int (argname, annotation, or default)
    #   functional args removed, or {str: func} map provided, or inject otherwise?
    keyboard_and_audio()
