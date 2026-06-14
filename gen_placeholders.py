#!/usr/bin/env python3
"""Generates named SVG placeholder images for the SAMRAU site.
Replace these files with real photographs from the presentation; keep the file names."""
import os
 
OUT = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUT, exist_ok=True)
 
LIGHT_BG = "#eef2f0"
LIGHT_BG2 = "#dfe7e2"
GRID = "#cdd8d2"
GREEN = "#00682b"
GREEN2 = "#00d56f"
INK = "#2b3a33"
 
DARK_BG = "#0e1a14"
DARK_BG2 = "#16291f"
 
 
def _rasterize_to_jpg(svg_bytes, jpg_path):
    """Render SVG bytes to a JPEG file. Requires rsvg-convert + Pillow.
    Returns True on success, False if the tools are unavailable."""
    import subprocess
    from io import BytesIO
    try:
        from PIL import Image
        png = subprocess.run(
            ["rsvg-convert", "-b", "white"],
            input=svg_bytes, capture_output=True, check=True,
        ).stdout
        Image.open(BytesIO(png)).convert("RGB").save(jpg_path, "JPEG", quality=88)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def svg(name, label, w=1200, h=800, dark=False, badge=None):
    bg1 = DARK_BG if dark else LIGHT_BG
    bg2 = DARK_BG2 if dark else LIGHT_BG2
    grid = "#23362b" if dark else GRID
    text = "#eaf4ee" if dark else INK
    sub = GREEN2 if dark else GREEN
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="{label}">'
    )
    parts.append(
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="{w}" y2="{h}" '
        f'gradientUnits="userSpaceOnUse"><stop stop-color="{bg1}"/>'
        f'<stop offset="1" stop-color="{bg2}"/></linearGradient></defs>'
    )
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#bg)"/>')
    # grid lines
    for x in range(0, w, 60):
        parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{grid}" stroke-width="1" opacity="0.5"/>')
    for y in range(0, h, 60):
        parts.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{grid}" stroke-width="1" opacity="0.5"/>')
    # corner accents
    parts.append(f'<rect x="0" y="0" width="120" height="8" fill="{sub}"/>')
    parts.append(f'<rect x="0" y="0" width="8" height="120" fill="{sub}"/>')
    parts.append(f'<rect x="{w-120}" y="{h-8}" width="120" height="8" fill="{sub}"/>')
    parts.append(f'<rect x="{w-8}" y="{h-120}" width="8" height="120" fill="{sub}"/>')
    # central gear/drill mark
    cx, cy = w // 2, h // 2 - 30
    parts.append(
        f'<circle cx="{cx}" cy="{cy}" r="70" stroke="{sub}" stroke-width="6" opacity="0.9"/>'
        f'<circle cx="{cx}" cy="{cy}" r="26" stroke="{sub}" stroke-width="6"/>'
    )
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        x1 = cx + 70 * math.cos(a)
        y1 = cy + 70 * math.sin(a)
        x2 = cx + 92 * math.cos(a)
        y2 = cy + 92 * math.sin(a)
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{sub}" stroke-width="6" stroke-linecap="round"/>')
    # label
    parts.append(
        f'<text x="{cx}" y="{cy+150}" text-anchor="middle" '
        f'font-family="Arial, sans-serif" font-size="38" font-weight="700" fill="{text}">{label}</text>'
    )
    parts.append(
        f'<text x="{cx}" y="{cy+190}" text-anchor="middle" '
        f'font-family="Arial, sans-serif" font-size="20" fill="{sub}">фото будет заменено</text>'
    )
    if badge:
        bw = 150
        parts.append(f'<rect x="32" y="32" width="{bw}" height="52" rx="8" fill="{sub}"/>')
        parts.append(
            f'<text x="{32+bw//2}" y="66" text-anchor="middle" font-family="Arial, sans-serif" '
            f'font-size="26" font-weight="800" fill="#ffffff">{badge}</text>'
        )
    parts.append("</svg>")
    data = "\n".join(parts)
    if name.endswith(".jpg"):
        jpg_path = os.path.join(OUT, name)
        if not _rasterize_to_jpg(data.encode("utf-8"), jpg_path):
            # Fallback: keep a valid placeholder even without rsvg-convert/Pillow.
            svg_path = os.path.splitext(jpg_path)[0] + ".svg"
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(data)
            print(f"warning: could not rasterize {name}; wrote {os.path.basename(svg_path)} instead")
        return
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(data)
 
 
svg("hero-burovaya-mashina.jpg", "Подземная буровая машина", 1400, 1000, dark=True)
svg("proizvodstvennaya-baza.jpg", "Производственная база")
svg("lokalizaciya-strel.svg", "Локализация стрел Troidon 66")
svg("vosstanovlenie-strel.jpg", "Восстановление стрел")
svg("proizvodstvo-komplektuyushih.jpg", "Производство комплектующих")
svg("remont-gidrocilindrov.jpg", "Ремонт гидроцилиндров")
svg("ispytaniya-gidrocilindrov.jpg", "Испытания на маслостанции")
svg("okrasochnaya-kamera.jpg", "Окрасочная камера")
 
projects = [
    "proekt-1-strela-sandvik-dd2711",
    "proekt-2-strela-mashholding-df-b1",
    "proekt-3-podatchik-mashholding-df-b1",
    "proekt-4-gidrocilindr-fambition-fl07",
    "proekt-5-gidrocilindr-oprokid-fambition-fl07",
]
for p in projects:
    svg(f"{p}-do.svg", "До ремонта", 900, 650, badge="ДО")
    svg(f"{p}-posle.svg", "После ремонта", 900, 650, badge="ПОСЛЕ")
 
print("generated", len(os.listdir(OUT)), "files")