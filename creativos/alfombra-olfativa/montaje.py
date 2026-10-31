"""Monta el anuncio final: 5 clips 9:16 a 720x1280, textos como PNG (Pillow, con emoji en color) y música.
Uso: python3 montaje.py  -> alfombra-olfativa-humor-v1.mp4"""
import pathlib
import subprocess

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).parent
W, H = 720, 1280
BOLD = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

# (clip, inicio dentro del clip, duración, líneas de texto, posición vertical)
PLAN = [
    ("clips/c1.mp4", 0.0, 2.5, ["He's not bad.", "He's BORED."], 0.18),
    ("clips/c2.mp4", 0.5, 2.5, ["No promises."], 0.18),
    ("clips/c3.mp4", 0.0, 4.5, ["Your shoes?", "Can't guarantee. \U0001F605"], 0.18),
    ("clips/c4.mp4", 0.5, 3.0, ["His nose?", "Very busy."], 0.18),
    ("clips/c5.mp4", 0.0, 3.5, ["Sniff. Find. Snack.", "Try something new"], 0.17),
]


def caja(lineas, idx):
    f = ImageFont.truetype(BOLD, 58)
    fe = ImageFont.truetype(EMOJI, 109)  # Noto Color Emoji solo admite 109 px
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = int(H * PLAN[idx][4])
    for n, linea in enumerate(lineas):
        sub = idx == 4 and n == 1
        fnt = ImageFont.truetype(BOLD, 40) if sub else f
        txt, emo = (linea[:-1].rstrip(), linea[-1]) if ord(linea[-1]) > 0xFFFF else (linea, None)
        tw = d.textlength(txt, font=fnt)
        ew = 0
        if emo:
            e = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
            ImageDraw.Draw(e).text((0, 0), emo, font=fe, embedded_color=True)
            e = e.crop(e.getbbox()).resize((60, 60), Image.LANCZOS)
            ew = 72
        x = (W - tw - ew) / 2
        hgt = 76 if not sub else 56
        pad = 18
        d.rounded_rectangle((x - pad, y - 8, x + tw + ew + pad, y + hgt), 16,
                            fill=(255, 255, 255, 235) if not sub else (20, 120, 120, 235))
        d.text((x, y), txt, font=fnt, fill=(20, 20, 20) if not sub else (255, 255, 255))
        if emo:
            img.alpha_composite(e, (int(x + tw + 12), y + 4))
        y += hgt + 18
    p = AQUI / f"audio/../clips/txt{idx}.png"
    img.save(p)
    return p


partes = []
for i, (clip, ss, dur, lineas, _) in enumerate(PLAN):
    png = caja(lineas, i)
    seg = AQUI / f"clips/seg{i}.mp4"
    vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1[v];"
          f"[v][1:v]overlay=0:0:enable='gte(t,0.15)'")
    if i == 4:  # cierre: zoom lento sobre el plano final
        vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1,"
              f"zoompan=z='min(zoom+0.0008,1.06)':d=1:s={W}x{H}:fps=30[v];[v][1:v]overlay=0:0")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(ss), "-t", str(dur), "-i", str(AQUI / clip),
                    "-loop", "1", "-t", str(dur), "-i", str(png), "-filter_complex", vf, "-an",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", str(seg)], check=True)
    partes.append(seg)

lista = AQUI / "clips/lista.txt"
lista.write_text("".join(f"file '{p.name}'\n" for p in partes))
total = sum(p[2] for p in PLAN)
out = AQUI / "alfombra-olfativa-humor-v1.mp4"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
                "-i", str(AQUI / "audio/musica.wav"),
                "-filter_complex", f"[1:a]atrim=0:{total},afade=t=out:st={total - 1}:d=1,volume=0.9[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", str(out)], check=True)
print(out, total, "s")
