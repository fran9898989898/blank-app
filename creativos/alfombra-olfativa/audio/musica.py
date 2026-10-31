"""Pista instrumental juguetona de 16 s (pizzicato + bajo + shaker), sintetizada: sin derechos de terceros.
Uso: python3 musica.py  -> musica.wav (44,1 kHz, estéreo)"""
import pathlib
import wave

import numpy as np

SR = 44100
BPM = 116
BEAT = 60 / BPM
DUR = 16.0
N = int(SR * DUR)
out = np.zeros(N)


def note(freq, t0, length, vol, kind="pluck"):
    i0 = int(t0 * SR)
    n = int(length * SR)
    if i0 >= N:
        return
    n = min(n, N - i0)
    t = np.arange(n) / SR
    if kind == "pluck":  # pizzicato / ukelele: armónicos con caída rápida
        w = (np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(4 * np.pi * freq * t) + 0.25 * np.sin(6 * np.pi * freq * t))
        env = np.exp(-t * 7) * np.minimum(1, t * 400)
    elif kind == "bass":
        w = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)
        env = np.exp(-t * 4) * np.minimum(1, t * 200)
    elif kind == "bell":
        w = np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(2 * np.pi * freq * 2.76 * t)
        env = np.exp(-t * 3) * np.minimum(1, t * 500)
    else:  # shaker
        w = np.random.default_rng(i0).uniform(-1, 1, n)
        env = np.exp(-t * 60)
    out[i0:i0 + n] += vol * w * env


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


# Progresión C - Am - F - G (2 compases cada uno por vuelta), melodía saltarina
chords = [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [55, 59, 62])]
melody = [72, 76, 79, 76, 74, 72, 74, None, 72, 69, 72, 76, 77, 76, 74, None,
          77, 76, 74, 72, 74, 76, 77, None, 79, 77, 76, 74, 72, 74, 72, None]
beats = int(DUR / BEAT)
for b in range(beats):
    t = b * BEAT
    root, triad = chords[(b // 4) % 4]
    note(hz(root), t, BEAT, 0.35, "bass")
    if b % 2 == 1:
        for m in triad:
            note(hz(m), t, BEAT * 0.5, 0.10, "pluck")
    # melodía en corcheas, entra en el beat 4 (tras el hook)
    if b >= 4:
        for h in range(2):
            m = melody[((b - 4) * 2 + h) % len(melody)]
            if m is not None:
                note(hz(m), t + h * BEAT / 2, BEAT / 2, 0.16, "pluck")
    for h in range(2):
        note(0, t + h * BEAT / 2, 0.05, 0.05 if h else 0.08, "shaker")
# campanita en el cierre (segundo 12, logo)
for k, m in enumerate([84, 88, 91, 96]):
    note(hz(m), 12.0 + k * 0.12, 1.5, 0.12, "bell")

# fade out final y normalizado
fade = int(1.2 * SR)
out[-fade:] *= np.linspace(1, 0, fade)
out = out / np.max(np.abs(out)) * 0.85
st = np.stack([out, np.roll(out, 220)], axis=1)  # leve anchura estéreo
pcm = (st * 32767).astype(np.int16)
dest = pathlib.Path(__file__).with_name("musica.wav")
with wave.open(str(dest), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(dest, DUR, "s")
