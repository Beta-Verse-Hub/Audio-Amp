import wave
import pyaudio
import numpy as np
import keyboard



def play_with_simple_bass_boost(audio_file, boost_factor=1.2, window_size=50):
    wf = wave.open(audio_file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(1024)
    history = np.zeros(window_size)
    history_index = 0
    frames_processed = 0
    while data:
        audio_array = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        modified_array = np.copy(audio_array)

        if frames_processed >= window_size:
            average_level = np.mean(history)
            for i in range(len(modified_array)):

                if abs(modified_array[i]) > average_level:
                    modified_array[i] *= boost_factor

        modified_array = np.clip(modified_array, -32768, 32767).astype(np.int16)
        stream.write(modified_array.tobytes())
        data = wf.readframes(1024)
        frames_processed += len(audio_array)

        if keyboard.is_pressed("z") and boost_factor < 100:
            boost_factor += 1
            print(f"Boost Factor Increased: {boost_factor:.1f}")
        if keyboard.is_pressed("c") and boost_factor > 1:
            boost_factor -= 1
            print(f"Boost Factor Decreased: {boost_factor:.1f}")
    stream.stop_stream()
    stream.close()
    p.terminate()


def play_with_simple_treble_boost(audio_file, boost_factor=1.2):
    """Plays an audio file with a very simple, real-time-like treble boost attempt."""
    wf = wave.open(audio_file, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    previous_value = 0
    data = wf.readframes(1024)
    while data:
        audio_array = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        modified_array = np.copy(audio_array)  # Make a copy to modify

        for i in range(len(modified_array)):
            # Emphasize changes compared to the previous value
            change = modified_array[i] - previous_value
            modified_array[i] += change * (boost_factor - 1)
            previous_value = audio_array[i]  # Update previous value for the next sample

        # Clip to avoid distortion
        modified_array = np.clip(modified_array, -32768, 32767).astype(np.int16)
        stream.write(modified_array.tobytes())
        data = wf.readframes(1024)

        if keyboard.is_pressed("d") and boost_factor < 100:
            boost_factor += 1
            print(boost_factor)
        if keyboard.is_pressed("a") and boost_factor > 1:
            boost_factor -= 1
            print(boost_factor)

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    audio_file = "World of Terminal.wav"
    # boost = 1
    # play_with_simple_treble_boost(audio_file, boost)
    bass_boost = 1
    window = 75
    play_with_simple_bass_boost(audio_file, bass_boost, window)