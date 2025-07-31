import wave
import pyaudio
import numpy as np
import keyboard



def play(audio_file, bass_boost_factor=1.2, treble_boost_factor=1.2, window_size=50):
    """
    Play an audio file with optional bass and treble boosting
    
    Parameters
    ----------
    audio_file : str
        Path to the audio file to play
    bass_boost_factor : float, optional
        Boost factor for bass sound, by default 1.2
    treble_boost_factor : float, optional
        Boost factor for treble sound, by default 1.2
    window_size : int, optional
        Window size for calculating the average level for bass boost, by default 50
    
    Notes
    -----
    Press 'z' to increase the bass boost, 'c' to decrease, 'd' to increase the treble boost, 'a' to decrease
    """
    wf = wave.open(audio_file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
                    
    data = wf.readframes(1024)
    history = np.zeros(window_size)
    frames_processed = 0
    previous_value = 0
    while data:
        audio_array = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        modified_array = np.copy(audio_array)

        # Bass boost
        if frames_processed >= window_size:
            average_level = np.mean(history)
            for i in range(len(modified_array)):
                if abs(modified_array[i]) > average_level:
                    modified_array[i] *= bass_boost_factor
        
        # Treble boost
        for i in range(len(modified_array)):
            change = modified_array[i] - previous_value
            modified_array[i] += change * (treble_boost_factor - 1)
            previous_value = audio_array[i]

        # Clip to avoid distortion
        modified_array = np.clip(modified_array, -32768, 32767).astype(np.int16)
        stream.write(modified_array.tobytes())
        data = wf.readframes(1024)
        frames_processed += len(audio_array)

        # Change boost factors using keyboard inputs
        if keyboard.is_pressed("z") and bass_boost_factor < 100:
            bass_boost_factor += 1
            print(f"Bass Boost Factor Increased: {bass_boost_factor:.1f}")
        if keyboard.is_pressed("c") and bass_boost_factor > 1:
            bass_boost_factor -= 1
            print(f"Bass Boost Factor Decreased: {bass_boost_factor:.1f}")
        if keyboard.is_pressed("d") and treble_boost_factor < 100:
            treble_boost_factor += 1
            print(f"Treble Boost Factor Increased: {treble_boost_factor:.1f}")
        if keyboard.is_pressed("a") and treble_boost_factor > 1:
            treble_boost_factor -= 1
            print(f"Treble Boost Factor Decreased: {treble_boost_factor:.1f}")

    stream.stop_stream()
    stream.close()
    p.terminate()



if __name__ == "__main__":
    audio_file = "World of Terminal.wav"
    treble_boost = 1
    bass_boost = 1
    window = 75
    play(audio_file, bass_boost, treble_boost, window)