import json
import os
import random
import subprocess
import textwrap
import base64
import sys
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
BANCO_PATH = os.path.join(BASE, "frases_banco.json")
USADAS_PATH = os.path.join(BASE, "usadas.json")
FONT600 = os.path.join(BASE, "fonts", "caveat600.woff2")
FONT700 = os.path.join(BASE, "fonts", "caveat700.woff2")
CHROME = os.environ.get(
    "CHROME_BIN",
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
    if os.path.exists("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    else r"C:\Program Files\Google\Chrome\Application\chrome.exe",
)

HASHTAGS = {
    "mujeres_empoderadas": "#mujeresempoderadas #mujerpoderosa #empoderamientofemenino #mujeresquesuperan",
    "mujeres_cabronas": "#mujerescabronas #actitud #reinacabrona #nomeimporta",
    "frases_motivacionales": "#frasesmotivadoras #motivacion #exito #disciplina",
    "fuerza": "#fuerzainterior #mujeresfuertes #resiliencia #levantate",
}
BASE_HASHTAGS = "#fraseschingonasoficial #frasesenespanol #frasesparamujeres #reflexiones"

APERTURAS = [
    "Guarda esta frase para cuando se te olvide lo chingona que eres.",
    "Etiqueta a alguien que necesita leer esto hoy.",
    "Lee esto las veces que necesites.",
    "Para ti, que sigues aqui a pesar de todo.",
    "Esta va dedicada a la que no se rinde.",
    "Guardala. La vas a necesitar en un mal dia.",
]

ROTATIONS = [
    "rotate(-2.2deg) translateX(-8px)",
    "rotate(1.6deg) translateX(12px)",
    "rotate(-1.4deg) translateX(-2px)",
    "rotate(1.2deg) translateX(6px)",
    "rotate(-1.8deg) translateX(-4px)",
]

TEMPLATE = """<!doctype html>
<title>post</title>
<style>
@font-face {{
  font-family: 'Caveat';
  font-style: normal;
  font-weight: 600;
  src: url(data:font/woff2;base64,{font_b64}) format('woff2');
}}
:root{{
  --bg:#0c0c0c;
  --ink:#f4f2ec;
  --ink-dim:#c9c6bd;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1080px;overflow:hidden;background:var(--bg);}}
.canvas{{
  width:1080px;
  height:1080px;
  background:var(--bg);
  position:relative;
  display:flex;
  align-items:center;
  justify-content:center;
  overflow:hidden;
}}
.quote{{
  font-family:'Caveat',cursive;
  color:var(--ink);
  font-size:{font_size}px;
  font-weight:600;
  text-align:center;
  line-height:1.32;
  max-width:820px;
}}
.quote .l{{ display:block; }}
{rotation_css}
.handle{{
  position:absolute;
  bottom:88px;
  left:0;
  right:0;
  text-align:center;
  font-family:Arial,Helvetica,sans-serif;
  font-size:14px;
  letter-spacing:5px;
  color:var(--ink-dim);
  font-weight:400;
}}
</style>
<div class="canvas">
  <div class="quote">
    {lines_html}
  </div>
  <div class="handle">@FRASESCHINGONASOFICIAL</div>
</div>
"""


def wrap_quote(text, width=22):
    lines = textwrap.wrap(text, width=width, break_long_words=False)
    return lines


def font_size_for(lines):
    n = len(lines)
    longest = max(len(l) for l in lines)
    size = 80
    if n >= 5 or longest > 26:
        size = 58
    elif n == 4 or longest > 22:
        size = 66
    elif n == 3:
        size = 76
    return size


def build_html(quote_text):
    lines = wrap_quote(quote_text)
    font_size = font_size_for(lines)
    rotation_css = ""
    lines_html = ""
    for i, line in enumerate(lines):
        cls = f"l{i+1}"
        rot = ROTATIONS[i % len(ROTATIONS)]
        rotation_css += f".quote .{cls}{{ transform:{rot}; }}\n"
        lines_html += f'<span class="l {cls}">{line}</span>\n'

    font_b64 = base64.b64encode(open(FONT600, "rb").read()).decode("ascii")

    return TEMPLATE.format(
        font_b64=font_b64,
        font_size=font_size,
        rotation_css=rotation_css,
        lines_html=lines_html,
    )


def render_png(html_path, png_path):
    win_html_path = html_path.replace("\\", "/")
    subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--window-size=1080,1080",
            f"--screenshot={png_path}",
            f"file:///{win_html_path}",
        ],
        capture_output=True,
        timeout=30,
    )


def load_banco():
    with open(BANCO_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_usadas():
    with open(USADAS_PATH, encoding="utf-8") as f:
        return set(json.load(f))


def save_usadas(usadas):
    with open(USADAS_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(usadas), f, ensure_ascii=False, indent=2)


def pick_frases(n=4):
    banco = load_banco()
    usadas = load_usadas()
    categorias = list(banco.keys())
    random.shuffle(categorias)

    elegidas = []
    intentos = 0
    cat_cycle = categorias[:]
    while len(elegidas) < n and intentos < 200:
        intentos += 1
        if not cat_cycle:
            cat_cycle = categorias[:]
        cat = cat_cycle.pop()
        disponibles = [q for q in banco[cat] if q not in usadas]
        if not disponibles:
            continue
        frase = random.choice(disponibles)
        elegidas.append((cat, frase))
        usadas.add(frase)

    save_usadas(usadas)
    return elegidas


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    today = date.today().isoformat()
    out_dir = os.path.join(BASE, "posts", today)
    os.makedirs(out_dir, exist_ok=True)

    elegidas = pick_frases(n)
    if not elegidas:
        print("No hay frases disponibles sin usar. Agrega mas al banco.")
        return

    resumen = []
    for i, (cat, frase) in enumerate(elegidas, start=1):
        html = build_html(frase)
        html_path = os.path.join(out_dir, f"post_{i}.html")
        png_path = os.path.join(out_dir, f"post_{i}.png")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        render_png(html_path, png_path)

        apertura = random.choice(APERTURAS)
        hashtags = f"{BASE_HASHTAGS} {HASHTAGS.get(cat, '')}".strip()
        caption = f"{apertura}\n\n\"{frase}\"\n\n{hashtags}"
        caption_path = os.path.join(out_dir, f"post_{i}_caption.txt")
        with open(caption_path, "w", encoding="utf-8") as f:
            f.write(caption)

        resumen.append({
            "categoria": cat,
            "frase": frase,
            "png": png_path,
            "caption_path": caption_path,
        })
        print(f"[{i}] {cat}: {frase}")
        print(f"    -> {png_path}")

    resumen_path = os.path.join(out_dir, "resumen.json")
    with open(resumen_path, "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)

    print(f"\nListo. {len(elegidas)} posts generados en {out_dir}")


if __name__ == "__main__":
    main()
