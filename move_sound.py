# create_move_sound.py
import pygame
import numpy as np
import os

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1)

# Create assets directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

# Create a simple "click" sound
duration = 0.15  # seconds
volume = 0.3
sample_rate = 44100
t = np.linspace(0, duration, int(duration * sample_rate), False)
note = 0.7 * np.sin(2 * np.pi * 800 * t) * np.exp(-5 * t)
audio = np.int16(note * 32767 * volume)

# Convert to pygame sound and save
# sound = pygame.sndarray.make_sound(audio)
# pygame.mixer.Sound.save(sound, os.path.join('assets', 'move.wav'))

# print("Move sound created successfully!")

import wave

# Save the audio as a .wav file
with wave.open(os.path.join('assets', 'move.wav'), 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16-bit
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(audio.tobytes())

print("Move sound created successfully!")