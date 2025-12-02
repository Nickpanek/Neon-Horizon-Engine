# @title 🌆 The Neon Horizon Engine (Math Edition v2.0)
# @markdown Click Play to generate 2,400 Deterministic Assets.

import os
import csv
import zipfile
import math
import time

print("Installing Audio Engine...")
!pip install mido > /dev/null
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
from google.colab import files

# ======================================================
# 1. THE EXPANDED CONSTANTS (2,400 Combinations)
# ======================================================

KEYS = {
    "A_Minor": 57, "C_Minor": 60, "D_Minor": 62,
    "E_Minor": 64, "F_Minor": 65, "G_Minor": 67
}

# Fine-tune BPMs: 85, 87, 89... up to 115 (16 Steps)
BPMS = range(85, 117, 2)

# THE BASS EQUATION: i % PERIOD < DUTY
# We added complex polyrhythms here.
BASS_MATH = [
    (4, 2),  # Driving 8ths
    (8, 3),  # Tresillo
    (16, 4), # Sparse
    (6, 3),  # Rolling Triplets
    (8, 5)   # Heavy Syncopation
]

# THE MELODY EQUATION: Index = floor( AMP * sin(t * FREQ) )
# (Amplitude, Frequency)
MELODY_MATH = [
    (5, 0.1),  # Slow Arp
    (7, 0.2),  # Fast Run
    (12, 0.05),# Wide Sweep
    (3, 0.4),  # Rapid Trill
    (9, 0.15)  # Complex Meander
]

OUTPUT_DIR = "/content/Panek_Synth_Library"

# ======================================================
# 2. THE ENGINE
# ======================================================

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_math_track(key_name, root, bpm, bass_params, mel_params, filename):
    mid = MidiFile()

    # SETUP TRACKS
    track_drums = MidiTrack(); mid.tracks.append(track_drums)
    track_bass = MidiTrack(); mid.tracks.append(track_bass)
    track_pads = MidiTrack(); mid.tracks.append(track_pads)
    track_lead = MidiTrack(); mid.tracks.append(track_lead)

    # INSTRUMENTS
    track_drums.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))
    track_bass.append(Message('program_change', program=38, time=0)) # Synth Bass
    track_pads.append(Message('program_change', program=89, time=0)) # Warm Pad
    track_lead.append(Message('program_change', program=81, time=0)) # Sawtooth

    # --- THE LOGIC ---
    bars = 8
    steps = bars * 16
    ticks = 120

    # UNPACK YOUR CONSTANTS
    bass_period, bass_duty = bass_params
    mel_amp, mel_freq = mel_params

    # Progression: i - VI - III - VII (Classic 80s)
    prog = [0, 8, 3, 10]
    scale = [0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24] # Extended Minor Pentatonic

    events_drums, events_bass, events_pads, events_lead = [], [], [], []

    for i in range(steps):
        t = i * ticks

        # CHORD LOGIC
        chord_idx = (i // 32) % 4
        current_root = root + prog[chord_idx]

        # 1. DRUMS (Standard Gated Beat)
        beat = i % 16
        if beat % 8 == 0: # Kick
            events_drums.append({'n': 36, 'v': 110, 't': t, 'd': 100})
        if beat == 4 or beat == 12: # Snare
            events_drums.append({'n': 38, 'v': 120, 't': t, 'd': 100})

        # 2. BASS (The Modulo Function)
        if i % bass_period < bass_duty:
            events_bass.append({'n': current_root - 24, 'v': 100, 't': t, 'd': 200})

        # 3. PADS (Static Math)
        if i % 32 == 0:
            # Add-9 Voicing: Root, +3, +7, +14
            for interval in [0, 3, 7, 14]:
                events_pads.append({'n': current_root + interval, 'v': 70, 't': t, 'd': 3800})

        # 4. LEAD (The Sine Wave Function)
        if i % 2 == 0: # 8th notes
            sine_val = math.sin(i * mel_freq)
            scale_idx = int((sine_val + 1) * 0.5 * mel_amp)
            scale_idx = max(0, min(scale_idx, len(scale)-1))
            note = current_root + scale[scale_idx] + 12
            events_lead.append({'n': note, 'v': 90, 't': t, 'd': 200})

    # WRITE FUNCTION
    def write(track, events):
        events.sort(key=lambda x: x['t'])
        last_t = 0
        for e in events:
            dt = max(0, e['t'] - last_t)
            track.append(Message('note_on', note=e['n'], velocity=e['v'], time=dt))
            track.append(Message('note_off', note=e['n'], velocity=0, time=e['d']))
            last_t = e['t'] + e['d']

    write(track_drums, events_drums)
    write(track_bass, events_bass)
    write(track_pads, events_pads)
    write(track_lead, events_lead)

    mid.save(filename)

# ======================================================
# 3. EXECUTION
# ======================================================

print("--- STARTING DETERMINISTIC FACTORY ---")
ensure_dir(OUTPUT_DIR)
csv_name = "/content/Panek_Synth_Manifest.csv"

with open(csv_name, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Filename", "Key", "BPM", "BassMath", "MelodyMath", "Author"])

    count = 0
    for key, root in KEYS.items():
        for bpm in BPMS:
            for b_math in BASS_MATH:
                for m_math in MELODY_MATH:
                    fname = f"Synth_{key}_{bpm}_Bass{b_math}_Mel{m_math}.mid"
                    path = os.path.join(OUTPUT_DIR, fname)

                    generate_math_track(key, root, bpm, b_math, m_math, path)
                    writer.writerow([fname, key, bpm, b_math, m_math, "Nick Panek"])
                    count += 1
                    if count % 200 == 0: print(f"Calculated {count} files...")

print(f"TOTAL: {count} assets created.")
print("--- ZIPPING ---")
zip_name = "/content/NickPanek_Synth_Collection.zip"
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(csv_name, arcname="Panek_Synth_Manifest.csv")
    for r, d, fnames in os.walk(OUTPUT_DIR):
        for f in fnames:
            z.write(os.path.join(r, f), arcname=f)

print(f"DONE. Downloading {zip_name}...")
files.download(zip_name)
