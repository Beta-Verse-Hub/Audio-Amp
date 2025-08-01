import wave
import pyaudio
import numpy as np
import keyboard

bass_boost_factor=1.0
mid_boost_factor=1.0
treble_boost_factor=1.0
playing = True

def stop():
    playing = False

def play(audio_file):
    """
    Play an audio file with optional bass, mid, and treble boosting using
    FFT-based frequency manipulation.

    Parameters
    ----------
    audio_file : str
        Path to the audio file to play.
    bass_boost_factor : float, optional
        Boost factor for bass sound, by default 1.0 (no boost).
    mid_boost_factor : float, optional
        Boost factor for mid sound, by default 1.0 (no boost).
    treble_boost_factor : float, optional
        Boost factor for treble sound, by default 1.0 (no boost).

    Notes
    -----
    Press 'z' to increase the bass boost, 'c' to decrease.
    Press 'e' to increase the mid boost, 'q' to decrease.
    Press 'd' to increase the treble boost, 'a' to decrease.
    Press 'esc' to exit.
    """
    # Global variables
    global bass_boost_factor
    global mid_boost_factor
    global treble_boost_factor

    # Open audio file
    wf = wave.open(audio_file, 'rb')
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Flag to control audio playback
    playing = True

    # Get audio file parameters
    channels = wf.getnchannels()
    sample_rate = wf.getframerate()
    sample_width = wf.getsampwidth()
    chunk_size = 1024

    # Open audio stream
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=sample_rate,
                    output=True)

    # Define EQ frequency ranges (these are approximate and can be tuned)
    bass_max_freq = 250    # Upper limit for bass frequencies
    mid_min_freq = 250     # Lower limit for mid frequencies
    mid_max_freq = 4000    # Upper limit for mid frequencies
    treble_min_freq = 4000 # Lower limit for treble frequencies

    # Read the first chunk of audio data
    data = wf.readframes(chunk_size)
    
    print("Use keyboard to adjust EQ:")
    print("Bass: 'z' (up), 'c' (down)")
    print("Mid: 'e' (up), 'q' (down)")
    print("Treble: 'd' (up), 'a' (down)")
    print("Press 'esc' to exit.")

    while data:
        # Convert bytes to numpy array
        # Reshape for multi-channel audio if applicable (samples x channels)
        audio_array = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        if channels > 1:
            audio_array = audio_array.reshape(-1, channels)
        
        # Perform Fast Fourier Transform (FFT)
        # Apply FFT along the first axis (samples) for multi-channel or single channel
        fft_spectrum = np.fft.fft(audio_array, axis=0)
        
        # Get frequencies corresponding to FFT bins
        frequencies = np.fft.fftfreq(len(audio_array), d=1.0/sample_rate)

        # Create a copy of the FFT spectrum to modify
        modified_fft_spectrum = np.copy(fft_spectrum)

        # Apply boosts based on frequency ranges for each channel
        for ch in range(channels):
            for i, freq in enumerate(frequencies):
                abs_freq = abs(freq) # Use absolute frequency for symmetric bins
                
                # Apply bass boost to frequencies below bass_max_freq
                if abs_freq <= bass_max_freq:
                    if channels > 1:
                        modified_fft_spectrum[i, ch] *= bass_boost_factor
                    else:
                        modified_fft_spectrum[i] *= bass_boost_factor
                
                # Apply mid boost to frequencies between mid_min_freq and mid_max_freq
                elif mid_min_freq < abs_freq <= mid_max_freq:
                    if channels > 1:
                        modified_fft_spectrum[i, ch] *= mid_boost_factor
                    else:
                        modified_fft_spectrum[i] *= mid_boost_factor
                
                # Apply treble boost to frequencies above treble_min_freq
                elif abs_freq > treble_min_freq:
                    if channels > 1:
                        modified_fft_spectrum[i, ch] *= treble_boost_factor
                    else:
                        modified_fft_spectrum[i] *= treble_boost_factor

        # Perform Inverse Fast Fourier Transform (IFFT)
        # Take the real part as the output must be real audio data
        modified_array = np.fft.ifft(modified_fft_spectrum, axis=0).real
        
        # Flatten the array back to 1D for writing to the audio stream if multi-channel
        if channels > 1:
            modified_array = modified_array.flatten()

        # Clip the audio samples to the valid 16-bit integer range to prevent distortion
        modified_array = np.clip(modified_array, -32768, 32767).astype(np.int16)
        
        # Write the modified audio data back to the stream
        stream.write(modified_array.tobytes())
        data = wf.readframes(chunk_size) # Read the next chunk

        # Keyboard controls for dynamic boosting adjustments
        if keyboard.is_pressed("z") and bass_boost_factor < 100:
            bass_boost_factor += 1
            print(f"Bass Boost Factor Increased: {bass_boost_factor:.1f}")
        if keyboard.is_pressed("c") and bass_boost_factor > 1:
            bass_boost_factor -= 1
            print(f"Bass Boost Factor Decreased: {bass_boost_factor:.1f}")
        if keyboard.is_pressed("e") and mid_boost_factor < 100:
            mid_boost_factor += 1
            print(f"Mid Boost Factor Increased: {mid_boost_factor:.1f}")
        if keyboard.is_pressed("q") and mid_boost_factor > 1:
            mid_boost_factor -= 1
            print(f"Mid Boost Factor Decreased: {mid_boost_factor:.1f}")
        if keyboard.is_pressed("d") and treble_boost_factor < 100:
            treble_boost_factor += 1
            print(f"Treble Boost Factor Increased: {treble_boost_factor:.1f}")
        if keyboard.is_pressed("a") and treble_boost_factor > 1:
            treble_boost_factor -= 1
            print(f"Treble Boost Factor Decreased: {treble_boost_factor:.1f}")
        if keyboard.is_pressed("esc"):
            break
        if not playing:
            break

    # Clean up audio stream and PyAudio resources
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
