from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "poster.png"
BG = ROOT / "Mai 2026" / "background.png"
SIZE = (1055, 1491)

FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_HAND = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, y, text, fnt, fill, spacing=8):
    box = draw.multiline_textbbox((0, 0), text, font=fnt, align="center", spacing=spacing)
    x = (SIZE[0] - (box[2] - box[0])) // 2
    draw.multiline_text((x, y), text, font=fnt, fill=fill, align="center", spacing=spacing)
    return box[3] - box[1]


image = Image.open(BG).convert("RGB")
scale = max(SIZE[0] / image.width, SIZE[1] / image.height)
image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
left = (image.width - SIZE[0]) // 2
top = (image.height - SIZE[1]) // 2
image = image.crop((left, top, left + SIZE[0], top + SIZE[1])).filter(ImageFilter.GaussianBlur(0.35))

overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
card = (54, 70, 1001, 1425)
od.rounded_rectangle(card, radius=42, fill=(255, 250, 232, 232), outline=(23, 59, 94, 70), width=3)
image = Image.alpha_composite(image.convert("RGBA"), overlay)
draw = ImageDraw.Draw(image)

navy = (23, 59, 94, 255)
green = (47, 107, 47, 255)
orange = (200, 90, 28, 255)
ink = (27, 33, 29, 255)

badge = (205, 107, 850, 169)
draw.rounded_rectangle(badge, radius=30, fill=green)
centered(draw, 116, "1 Jahr Kultur am Eck", font(FONT_BOLD, 28), (255, 255, 255, 255))

centered(draw, 184, "Kultur am Eck", font(FONT_HAND, 100), navy)
centered(draw, 322, "Donnerstag, 06.08.2026", font(FONT_BOLD, 51), navy)
centered(draw, 389, "ab 18:00 Uhr", font(FONT, 43), orange)

highlight = (122, 468, 933, 609)
draw.rounded_rectangle(highlight, radius=24, fill=(255, 240, 197, 255), outline=orange, width=6)
centered(draw, 493, "Jubiläums-Highlight:\nein Kasten selbst gebrautes Bier", font(FONT_BOLD, 39), navy, spacing=7)

centered(draw, 660, "Mit Liedern, Musik, Gedichten und weiteren Beiträgen\nfür Klein und Groß", font(FONT_BOLD, 34), green, spacing=8)
centered(draw, 795, "Herzliche Einladung!", font(FONT, 34), ink)
centered(draw, 845, "Sei dabei mit einem kulturellen Beitrag, Getränk, Gebäck oder Kuchen.", font(FONT, 27), ink)
centered(draw, 900, "Dazu wieder Feuerschale, Gespräche und – je nach Wetter –\nGrillen oder Stockbrot.", font(FONT, 27), ink, spacing=7)

draw.line((135, 1115, 920, 1115), fill=orange, width=3)
centered(draw, 1160, "Findet bei jedem Wetter statt.", font(FONT_BOLD, 27), navy)
centered(draw, 1205, "Kleiner Grillrost überm Feuer verfügbar.", font(FONT, 25), navy)

image.convert("RGB").save(OUT, "PNG", optimize=True)
print(OUT)
