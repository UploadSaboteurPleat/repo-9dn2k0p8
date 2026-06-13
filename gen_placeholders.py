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
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
 
 
svg("hero-burovaya-mashina.svg", "Подземная буровая машина", 1400, 1000, dark=True)
svg("proizvodstvennaya-baza.svg", "Производственная база")
svg("lokalizaciya-strel.svg", "Локализация стрел Troidon 66")
svg("vosstanovlenie-strel.svg", "Восстановление стрел")
svg("proizvodstvo-komplektuyushih.svg", "Производство комплектующих")
svg("remont-gidrocilindrov.svg", "Ремонт гидроцилиндров")
svg("ispytaniya-gidrocilindrov.svg", "Испытания на маслостанции")
svg("okrasochnaya-kamera.svg", "Окрасочная камера")
 
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