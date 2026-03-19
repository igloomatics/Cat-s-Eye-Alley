#!/usr/bin/env python3
"""
猫眼巷 — Warm Constellation Poster (Refined)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# === DIMENSIONS ===
W, H = 1600, 2260
BG = (248, 247, 244)

# === COLORS ===
C_LM = (232, 85, 134)
C_LQ = (58, 175, 85)
C_YG = (90, 126, 230)
C_DARK = (26, 26, 46)
C_MID = (107, 107, 128)
C_LIGHT = (170, 168, 162)
C_FAINT = (232, 231, 226)
C_WHITE = (255, 255, 255)

# === FONTS ===
FONT_DIR = "/Users/xuzhiyue/.claude/plugins/cache/anthropic-agent-skills/document-skills/3d5951151859/skills/canvas-design/canvas-fonts"
CN_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
CN_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"
CN_SONG = "/System/Library/Fonts/Supplemental/Songti.ttc"
EN_THIN = f"{FONT_DIR}/WorkSans-Regular.ttf"
EN_BOLD = f"{FONT_DIR}/WorkSans-Bold.ttf"
EN_MONO = f"{FONT_DIR}/GeistMono-Regular.ttf"
EN_SERIF = f"{FONT_DIR}/CrimsonPro-Regular.ttf"
EN_SERIF_BOLD = f"{FONT_DIR}/CrimsonPro-Bold.ttf"
EN_POIRET = f"{FONT_DIR}/PoiretOne-Regular.ttf"

IMG_DIR = "/Users/xuzhiyue/Downloads/猫眼巷"

def load_font(path, size, index=0):
    try:
        if path.endswith('.ttc'):
            return ImageFont.truetype(path, size, index=index)
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def circle_crop(img, size):
    img = img.resize((size*4, size*4), Image.LANCZOS)
    mask = Image.new('L', (size*4, size*4), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([0, 0, size*4-1, size*4-1], fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    img = img.resize((size, size), Image.LANCZOS)
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    return output

def draw_dashed_line(draw, x1, y1, x2, y2, color, dash=8, gap=6, width=1):
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return
    dx, dy = dx/length, dy/length
    pos = 0
    while pos < length:
        end = min(pos + dash, length)
        draw.line([x1+dx*pos, y1+dy*pos, x1+dx*end, y1+dy*end], fill=color, width=width)
        pos = end + gap

def text_center_x(draw, text, font, y, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)

def text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]

def create_poster():
    canvas = Image.new('RGBA', (W, H), BG + (255,))
    draw = ImageDraw.Draw(canvas)

    # === SOFT GRADIENT BLOBS (background atmosphere) ===
    for cx, cy, r, c in [
        (160, 350, 360, (*C_LM, 10)),
        (1440, 520, 300, (*C_YG, 8)),
        (800, 1700, 400, (*C_LQ, 6)),
        (800, 300, 500, (*C_DARK, 3)),
    ]:
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)
        ov = ov.filter(ImageFilter.GaussianBlur(radius=100))
        canvas = Image.alpha_composite(canvas, ov)

    draw = ImageDraw.Draw(canvas)

    # ============================================
    # TOP: BADGE
    # ============================================
    f_badge = load_font(EN_MONO, 12)
    text_center_x(draw, "OPENCLAW  MULTI-AGENT  COMPANION  SYSTEM", f_badge, 100, C_LIGHT)

    # Thin hairline
    draw.line([W//2 - 40, 130, W//2 + 40, 130], fill=C_FAINT, width=1)

    # ============================================
    # TITLE: 猫眼巷
    # ============================================
    f_title = load_font(CN_BOLD, 140)
    text_center_x(draw, "猫眼巷", f_title, 165, C_DARK)

    # Subtitle
    f_sub = load_font(CN_LIGHT, 28)
    text_center_x(draw, "三个青梅竹马帮你把日子过好", f_sub, 330, C_MID)

    # Three color dots
    dot_y = 385
    dot_gap = 18
    for i, c in enumerate([C_LM, C_LQ, C_YG]):
        dx = W//2 - dot_gap + i * dot_gap
        draw.ellipse([dx-3, dot_y-3, dx+3, dot_y+3], fill=c)

    # ============================================
    # THREE CHARACTER AVATARS
    # ============================================
    avatar_size = 300
    avatar_y = 460
    spacing = 440
    centers = [W//2 - spacing, W//2, W//2 + spacing]

    chars = [
        {'name': '灵猫', 'en': 'LÍNG MĀO', 'title': '生活的发现者', 'color': C_LM, 'img': f'{IMG_DIR}/灵猫.jpeg', 'num': '01'},
        {'name': '鹿青', 'en': 'LÙ QĪNG', 'title': '关系的维护者', 'color': C_LQ, 'img': f'{IMG_DIR}/鹿青.jpeg', 'num': '02'},
        {'name': '雨宫澄', 'en': 'YǓGŌNG CHÉNG', 'title': '决策的参谋', 'color': C_YG, 'img': f'{IMG_DIR}/雨宫澄.jpeg', 'num': '03'},
    ]

    for i, ch in enumerate(chars):
        cx = centers[i]
        cy = avatar_y + avatar_size // 2

        # Outer glow ring
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        for offset in range(3):
            r = avatar_size//2 + 18 + offset
            od.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(*ch['color'], 18 - offset*5), width=1)
        canvas = Image.alpha_composite(canvas, ov)
        draw = ImageDraw.Draw(canvas)

        # Number (top-right, subtle)
        f_num = load_font(EN_POIRET, 48)
        num_w = text_width(draw, ch['num'], f_num)
        draw.text((cx + avatar_size//2 - num_w + 8, avatar_y - 10), ch['num'], font=f_num, fill=(*ch['color'][:3], 35))

        # Avatar image
        try:
            img = Image.open(ch['img']).convert('RGBA')
            cropped = circle_crop(img, avatar_size)
            canvas.paste(cropped, (cx - avatar_size//2, avatar_y), cropped)
            draw = ImageDraw.Draw(canvas)
        except Exception as e:
            print(f"Error: {e}")
            draw.ellipse([cx-avatar_size//2, avatar_y, cx+avatar_size//2, avatar_y+avatar_size],
                        fill=(*ch['color'], 30))

        # Fine ring on avatar edge
        draw.ellipse([cx-avatar_size//2-1, cy-avatar_size//2-1, cx+avatar_size//2+1, cy+avatar_size//2+1],
                    outline=(*ch['color'], 50), width=1)

        # Name
        f_name = load_font(CN_BOLD, 38)
        name_y = avatar_y + avatar_size + 24
        nw = text_width(draw, ch['name'], f_name)
        draw.text((cx - nw//2, name_y), ch['name'], font=f_name, fill=ch['color'])

        # Pinyin (smaller, lighter)
        f_py = load_font(EN_THIN, 13)
        pw = text_width(draw, ch['en'], f_py)
        draw.text((cx - pw//2, name_y + 46), ch['en'], font=f_py, fill=C_LIGHT)

        # Role
        f_role = load_font(CN_LIGHT, 17)
        rw = text_width(draw, ch['title'], f_role)
        draw.text((cx - rw//2, name_y + 70), ch['title'], font=f_role, fill=C_MID)

    # Connection lines between avatars
    line_y = avatar_y + avatar_size // 2
    for a, b in [(0,1), (1,2)]:
        draw_dashed_line(draw,
            centers[a] + avatar_size//2 + 22, line_y,
            centers[b] - avatar_size//2 - 22, line_y,
            C_FAINT, dash=5, gap=7)

    # ============================================
    # DIVIDER
    # ============================================
    div_y = 900
    draw.line([W//2 - 80, div_y, W//2 + 80, div_y], fill=C_FAINT, width=1)
    # Small diamond at center
    d = 4
    draw.polygon([(W//2, div_y-d), (W//2+d, div_y), (W//2, div_y+d), (W//2-d, div_y)], fill=C_LIGHT)

    # ============================================
    # PHILOSOPHY SECTION
    # ============================================
    f_sec = load_font(CN_BOLD, 32)
    text_center_x(draw, "不是工具，是朋友", f_sec, 945, C_DARK)

    f_sec_sub = load_font(CN_LIGHT, 16)
    text_center_x(draw, "我们相信陪伴不该千篇一律", f_sec_sub, 995, C_LIGHT)

    # Three philosophy cards
    card_w = 420
    card_h = 300
    card_gap = 36
    total = card_w * 3 + card_gap * 2
    card_x0 = (W - total) // 2
    card_y = 1060

    pillars = [
        {'title': '个性化定制陪伴', 'lines': ['不是一个万能助手', '而是三个性格鲜明的朋友', '她们记住你的喜好、习惯和情绪', '陪伴越久越懂你'], 'color': C_LM},
        {'title': '接入真实生活', 'lines': ['记住你妈妈的生日', '你纠结了三天的决定', '你上周说想学的吉他', '然后在合适的时候，主动出现'], 'color': C_LQ},
        {'title': '共享记忆 自然流动', 'lines': ['你跟一个人聊过的事', '其他人也会知道', '不是监控', '是朋友之间本来就会互相关心'], 'color': C_YG},
    ]

    f_ct = load_font(CN_BOLD, 22)
    f_cd = load_font(CN_LIGHT, 15)

    for i, p in enumerate(pillars):
        cx = card_x0 + i * (card_w + card_gap)

        # Card bg
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        od.rounded_rectangle([cx, card_y, cx+card_w, card_y+card_h], radius=16, fill=(255, 255, 255, 200))
        od.rounded_rectangle([cx, card_y, cx+card_w, card_y+card_h], radius=16, outline=(*p['color'], 20), width=1)
        canvas = Image.alpha_composite(canvas, ov)
        draw = ImageDraw.Draw(canvas)

        # Top color accent bar
        draw.rounded_rectangle([cx, card_y, cx+card_w, card_y+4], radius=2, fill=(*p['color'], 60))

        # Card title
        draw.text((cx + 32, card_y + 32), p['title'], font=f_ct, fill=p['color'])

        # Small line under title
        tw = text_width(draw, p['title'], f_ct)
        draw.line([cx + 32, card_y + 64, cx + 32 + tw, card_y + 64], fill=(*p['color'], 30), width=1)

        # Description lines
        for j, line in enumerate(p['lines']):
            draw.text((cx + 32, card_y + 84 + j * 36), line, font=f_cd, fill=C_MID)

    # ============================================
    # QUOTE
    # ============================================
    quote_y = 1420
    draw.line([W//2 - 50, quote_y, W//2 + 50, quote_y], fill=C_FAINT, width=1)

    f_quote = load_font(CN_SONG, 22, index=0)
    text_center_x(draw, "「她们记住你的生活，然后主动出现」", f_quote, quote_y + 36, C_MID)

    # ============================================
    # BOTTOM SPECS
    # ============================================
    spec_y = 1540
    draw.line([140, spec_y, W - 140, spec_y], fill=C_FAINT, width=1)

    f_label = load_font(EN_MONO, 11)
    f_val = load_font(CN_LIGHT, 14)

    specs = [
        ("ARCHITECTURE", "Multi-Agent 协作系统"),
        ("MEMORY", "共享记忆池 · 个性化学习"),
        ("AGENTS", "灵猫 · 鹿青 · 雨宫澄"),
        ("VISION", "陪伴不该千篇一律"),
    ]

    spec_gap = (W - 280) // 4
    for i, (label, val) in enumerate(specs):
        sx = 140 + i * spec_gap
        draw.text((sx, spec_y + 24), label, font=f_label, fill=C_LIGHT)
        draw.text((sx, spec_y + 44), val, font=f_val, fill=C_MID)

    # ============================================
    # DECORATIVE CONSTELLATION DOTS (bottom area)
    # ============================================
    import random
    random.seed(42)
    for _ in range(30):
        dx = random.randint(100, W - 100)
        dy = random.randint(1640, 1720)
        r = random.choice([1, 2, 2, 3])
        c = random.choice([C_LM, C_LQ, C_YG])
        alpha = random.randint(15, 40)
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).ellipse([dx-r, dy-r, dx+r, dy+r], fill=(*c, alpha))
        canvas = Image.alpha_composite(canvas, ov)

    draw = ImageDraw.Draw(canvas)

    # ============================================
    # FOOTER
    # ============================================
    footer_y = H - 140
    draw.line([140, footer_y, W - 140, footer_y], fill=C_FAINT, width=1)

    f_footer = load_font(EN_MONO, 11)
    text_center_x(draw, "MAOYANXIANG  ·  OPENCLAW  PROJECT  ·  2025", f_footer, footer_y + 24, C_LIGHT)

    f_fcn = load_font(CN_LIGHT, 13)
    text_center_x(draw, "猫眼巷 — AI 生活陪伴，不该千篇一律", f_fcn, footer_y + 52, C_LIGHT)

    # ============================================
    # SAVE
    # ============================================
    final = canvas.convert('RGB')
    out = f"{IMG_DIR}/猫眼巷-海报.png"
    final.save(out, 'PNG', quality=95, dpi=(300, 300))
    print(f"Saved: {out} ({W}x{H})")

if __name__ == '__main__':
    create_poster()
