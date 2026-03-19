#!/usr/bin/env python3
"""
猫眼巷 — Warm Constellation Poster
Museum-quality promotional poster with three character avatars
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# === DIMENSIONS ===
W, H = 1600, 2260
BG = (248, 247, 244)  # #f8f7f4

# === COLORS ===
C_LM = (232, 85, 134)    # 灵猫 rose
C_LQ = (58, 175, 85)     # 鹿青 green
C_YG = (90, 126, 230)    # 雨宫澄 blue
C_DARK = (26, 26, 46)    # #1a1a2e
C_MID = (107, 107, 128)  # #6b6b80
C_LIGHT = (180, 178, 172)
C_FAINT = (230, 229, 224)

# === FONTS ===
FONT_DIR = "/Users/xuzhiyue/.claude/plugins/cache/anthropic-agent-skills/document-skills/3d5951151859/skills/canvas-design/canvas-fonts"
CN_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
CN_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"
CN_SONG = "/System/Library/Fonts/Supplemental/Songti.ttc"
EN_THIN = f"{FONT_DIR}/WorkSans-Regular.ttf"
EN_BOLD = f"{FONT_DIR}/WorkSans-Bold.ttf"
EN_MONO = f"{FONT_DIR}/GeistMono-Regular.ttf"
EN_SERIF = f"{FONT_DIR}/CrimsonPro-Regular.ttf"

# === IMAGES ===
IMG_DIR = "/Users/xuzhiyue/Downloads/猫眼巷"

def load_font(path, size, index=0):
    try:
        if path.endswith('.ttc'):
            return ImageFont.truetype(path, size, index=index)
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def circle_crop(img, size):
    """Crop image into a perfect circle with anti-aliased edges"""
    img = img.resize((size*4, size*4), Image.LANCZOS)
    mask = Image.new('L', (size*4, size*4), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([0, 0, size*4-1, size*4-1], fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    img = img.resize((size, size), Image.LANCZOS)
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    return output

def draw_circle_ring(draw, cx, cy, r, color, width=1):
    """Draw a thin circle ring"""
    for w in range(width):
        draw.ellipse([cx-r-w, cy-r-w, cx+r+w, cy+r+w], outline=color, width=1)

def draw_dashed_line(draw, x1, y1, x2, y2, color, dash=8, gap=6, width=1):
    """Draw a dashed line"""
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return
    dx, dy = dx/length, dy/length
    pos = 0
    while pos < length:
        end = min(pos + dash, length)
        draw.line([
            x1 + dx*pos, y1 + dy*pos,
            x1 + dx*end, y1 + dy*end
        ], fill=color, width=width)
        pos = end + gap

def text_center_x(draw, text, font, y, fill, canvas_width=W):
    """Draw text centered horizontally"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (canvas_width - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return tw

def create_poster():
    canvas = Image.new('RGBA', (W, H), BG + (255,))
    draw = ImageDraw.Draw(canvas)

    # === DECORATIVE BACKGROUND ELEMENTS ===

    # Subtle large circles in background (very faint)
    for cx, cy, r, c in [
        (200, 400, 300, (*C_LM, 8)),
        (1400, 600, 250, (*C_YG, 6)),
        (800, 1800, 350, (*C_LQ, 5)),
    ]:
        overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)
        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=80))
        canvas = Image.alpha_composite(canvas, overlay)

    draw = ImageDraw.Draw(canvas)

    # === TOP SECTION: BADGE + TITLE ===

    # Top thin line
    draw.line([W//2 - 60, 120, W//2 + 60, 120], fill=C_FAINT, width=1)

    # Small badge text
    f_badge = load_font(EN_MONO, 13)
    text_center_x(draw, "OPENCLAW  MULTI-AGENT  COMPANION  SYSTEM", f_badge, 140, C_LIGHT)

    # Main title - 猫眼巷
    f_title = load_font(CN_BOLD, 128)
    text_center_x(draw, "猫 眼 巷", f_title, 200, C_DARK)

    # Subtitle
    f_sub = load_font(CN_LIGHT, 30)
    text_center_x(draw, "三个青梅竹马帮你把日子过好", f_sub, 348, C_MID)

    # Decorative dots under subtitle
    dot_y = 408
    for i in range(3):
        colors = [C_LM, C_LQ, C_YG]
        draw.ellipse([W//2 - 20 + i*20, dot_y, W//2 - 14 + i*20, dot_y + 6], fill=colors[i])

    # === THREE CHARACTER PORTRAITS ===

    avatar_size = 260
    avatar_y = 520
    spacing = 420
    centers = [W//2 - spacing, W//2, W//2 + spacing]

    chars = [
        {
            'name': '灵猫',
            'en': 'LÍNG MĀO',
            'title': '生活的发现者',
            'color': C_LM,
            'img': f'{IMG_DIR}/灵猫.jpeg',
            'num': '01',
        },
        {
            'name': '鹿青',
            'en': 'LÙ QĪNG',
            'title': '关系的维护者',
            'color': C_LQ,
            'img': f'{IMG_DIR}/鹿青.jpeg',
            'num': '02',
        },
        {
            'name': '雨宫澄',
            'en': 'YǓGŌNG CHÉNG',
            'title': '决策的参谋',
            'color': C_YG,
            'img': f'{IMG_DIR}/雨宫澄.jpeg',
            'num': '03',
        },
    ]

    for i, ch in enumerate(chars):
        cx = centers[i]
        cy = avatar_y + avatar_size // 2

        # Outer decorative ring (faint)
        ring_color = (*ch['color'], 40)
        overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        r_outer = avatar_size // 2 + 20
        od.ellipse([cx-r_outer, cy-r_outer, cx+r_outer, cy+r_outer], outline=(*ch['color'], 30), width=1)
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)

        # Number label (top-left of avatar)
        f_num = load_font(EN_MONO, 14)
        draw.text((cx - avatar_size//2 - 5, avatar_y - 24), ch['num'], font=f_num, fill=(*ch['color'],))

        # Avatar image
        try:
            img = Image.open(ch['img']).convert('RGBA')
            cropped = circle_crop(img, avatar_size)
            paste_x = cx - avatar_size // 2
            paste_y = avatar_y
            canvas.paste(cropped, (paste_x, paste_y), cropped)
            draw = ImageDraw.Draw(canvas)
        except Exception as e:
            print(f"Error loading {ch['img']}: {e}")
            draw.ellipse([cx-avatar_size//2, avatar_y, cx+avatar_size//2, avatar_y+avatar_size],
                        fill=(*ch['color'], 30))

        # Inner ring on avatar edge
        draw_circle_ring(draw, cx, cy, avatar_size//2 + 2, (*ch['color'][:3], 60), width=1)

        # Character name
        f_name = load_font(CN_BOLD, 36)
        name_y = avatar_y + avatar_size + 28
        bbox = draw.textbbox((0, 0), ch['name'], font=f_name)
        nw = bbox[2] - bbox[0]
        draw.text((cx - nw//2, name_y), ch['name'], font=f_name, fill=ch['color'])

        # Pinyin
        f_py = load_font(EN_THIN, 13)
        bbox = draw.textbbox((0, 0), ch['en'], font=f_py)
        pw = bbox[2] - bbox[0]
        draw.text((cx - pw//2, name_y + 44), ch['en'], font=f_py, fill=C_LIGHT)

        # Title/role
        f_role = load_font(CN_LIGHT, 18)
        bbox = draw.textbbox((0, 0), ch['title'], font=f_role)
        rw = bbox[2] - bbox[0]
        draw.text((cx - rw//2, name_y + 70), ch['title'], font=f_role, fill=C_MID)

    # === CONNECTION LINES BETWEEN AVATARS ===
    # Thin dashed lines connecting the three
    line_y = avatar_y + avatar_size // 2
    dash_color = (*C_FAINT,)
    draw_dashed_line(draw, centers[0] + avatar_size//2 + 24, line_y,
                     centers[1] - avatar_size//2 - 24, line_y, dash_color, dash=6, gap=8)
    draw_dashed_line(draw, centers[1] + avatar_size//2 + 24, line_y,
                     centers[2] - avatar_size//2 - 24, line_y, dash_color, dash=6, gap=8)

    # === DIVIDER ===
    div_y = 940
    draw.line([W//2 - 100, div_y, W//2 + 100, div_y], fill=C_FAINT, width=1)

    # === PHILOSOPHY SECTION: THREE PILLARS ===

    section_y = 990
    f_section_title = load_font(CN_BOLD, 28)
    text_center_x(draw, "不是工具，是朋友", f_section_title, section_y, C_DARK)

    # Three philosophy cards
    card_y = 1070
    card_w = 400
    card_h = 280
    card_gap = 40
    total_cards_w = card_w * 3 + card_gap * 2
    card_start_x = (W - total_cards_w) // 2

    pillars = [
        {
            'title': '个性化定制陪伴',
            'desc': '不是一个万能助手\n而是三个性格鲜明的朋友\n她们记住你的喜好、习惯和情绪\n陪伴越久越懂你',
            'color': C_LM,
            'accent': '✦',
        },
        {
            'title': '接入真实生活',
            'desc': '记住你妈妈的生日\n你纠结了三天的决定\n你上周说想学的吉他\n然后在合适的时候，主动出现',
            'color': C_LQ,
            'accent': '✦',
        },
        {
            'title': '共享记忆 自然流动',
            'desc': '你跟一个人聊过的事\n其他人也会知道\n不是监控\n是朋友之间本来就会互相关心',
            'color': C_YG,
            'accent': '✦',
        },
    ]

    f_card_title = load_font(CN_BOLD, 22)
    f_card_desc = load_font(CN_LIGHT, 16)
    f_accent = load_font(EN_SERIF, 20)

    for i, p in enumerate(pillars):
        cx = card_start_x + i * (card_w + card_gap)

        # Card background (very subtle)
        overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h],
                            radius=16, fill=(255, 255, 255, 180))
        od.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h],
                            radius=16, outline=(*p['color'], 25), width=1)
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)

        # Top accent line
        draw.line([cx + 28, card_y + 24, cx + 28 + 32, card_y + 24], fill=p['color'], width=2)

        # Card title
        draw.text((cx + 28, card_y + 40), p['title'], font=f_card_title, fill=p['color'])

        # Card description
        lines = p['desc'].split('\n')
        for j, line in enumerate(lines):
            draw.text((cx + 28, card_y + 82 + j * 32), line, font=f_card_desc, fill=C_MID)

    # === QUOTE SECTION ===
    quote_y = 1420
    draw.line([W//2 - 60, quote_y, W//2 + 60, quote_y], fill=C_FAINT, width=1)

    f_quote = load_font(CN_SONG, 20, index=0)
    text_center_x(draw, "「她们记住你的生活，然后主动出现」", f_quote, quote_y + 30, C_MID)

    # === BOTTOM SECTION: TECH BADGE ===

    bottom_y = 1530

    # Thin separator
    draw.line([120, bottom_y, W - 120, bottom_y], fill=C_FAINT, width=1)

    # Technical specs in a minimal grid
    f_label = load_font(EN_MONO, 11)
    f_val = load_font(CN_LIGHT, 14)

    specs = [
        ("ARCHITECTURE", "Multi-Agent 协作系统"),
        ("MEMORY", "共享记忆池 · 个性化学习"),
        ("AGENTS", "灵猫 · 鹿青 · 雨宫澄"),
        ("PHILOSOPHY", "陪伴不该千篇一律"),
    ]

    spec_y = bottom_y + 30
    spec_x_start = 160
    spec_gap = 340

    for i, (label, val) in enumerate(specs):
        sx = spec_x_start + (i % 4) * spec_gap
        sy = spec_y
        draw.text((sx, sy), label, font=f_label, fill=C_LIGHT)
        draw.text((sx, sy + 22), val, font=f_val, fill=C_MID)

    # === DECORATIVE BOTTOM ELEMENTS ===

    # Small constellation dots
    dot_positions = [
        (200, 1660, C_LM), (220, 1675, C_LM),
        (800, 1680, C_LQ), (815, 1665, C_LQ),
        (1380, 1670, C_YG), (1400, 1685, C_YG),
    ]
    for dx, dy, c in dot_positions:
        draw.ellipse([dx, dy, dx+4, dy+4], fill=(*c, 80))

    # Connecting thin lines between dot pairs
    draw_dashed_line(draw, 204, 1662, 222, 1677, (*C_LM, 40), dash=3, gap=4)
    draw_dashed_line(draw, 802, 1682, 817, 1667, (*C_LQ, 40), dash=3, gap=4)
    draw_dashed_line(draw, 1382, 1672, 1402, 1687, (*C_YG, 40), dash=3, gap=4)

    # === FOOTER ===
    footer_y = H - 120
    draw.line([120, footer_y, W - 120, footer_y], fill=C_FAINT, width=1)

    f_footer = load_font(EN_MONO, 11)
    text_center_x(draw, "MAOYANXIANG  ·  OPENCLAW PROJECT  ·  2025", f_footer, footer_y + 20, C_LIGHT)

    f_footer_cn = load_font(CN_LIGHT, 13)
    text_center_x(draw, "猫眼巷 — AI 生活陪伴，不该千篇一律", f_footer_cn, footer_y + 48, C_LIGHT)

    # === SAVE ===
    final = canvas.convert('RGB')
    output_path = f"{IMG_DIR}/猫眼巷-海报.png"
    final.save(output_path, 'PNG', quality=95, dpi=(300, 300))
    print(f"Poster saved to: {output_path}")
    print(f"Size: {W}x{H}px")

if __name__ == '__main__':
    create_poster()
