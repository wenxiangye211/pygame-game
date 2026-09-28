import pygame
import random
import sys
import json
import os
import math

pygame.init()

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def make_sound(freq, duration=0.1):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        val = int(127 * (0.6 * math.sin(2 * 3.14159 * freq * t)))
        buf.append(val + 128)
    return pygame.mixer.Sound(buffer=bytes(buf))

sound_flip = make_sound(420, 0.08)
sound_match = make_sound(680, 0.12)
sound_wrong = make_sound(220, 0.2)

CARD_WIDTH = 80
CARD_HEIGHT = 110
MARGIN = 16
TOP_PADDING = 80
BOTTOM_PADDING = 40

font_big = pygame.font.Font(None, 56)
font_title = pygame.font.Font(None, 42)
font_text = pygame.font.Font(None, 30)
font_small = pygame.font.Font(None, 26)

BG_TOP = (242, 235, 226)
BG_BOTTOM = (220, 208, 195)
CARD_BACK = (168, 180, 190)
CARD_BACK_DECO = (140, 155, 165)
CARD_FRONT = (250, 248, 242)
PAIRED_COLOR = (200, 225, 210)
TEXT_COLOR = (70, 85, 95)
WHITE = (255, 255, 255)
BTN_NORMAL = (175, 195, 185)
BTN_HOVER = (195, 218, 208)
BTN_TEXT = (50, 65, 75)

fruits = [
    {"name":"Apple","body":(215,120,115),"shadow":(180,90,85),"highlight":(240,170,165),"leaf":(135,170,130),"stem":(120,90,70),"blush":(245,185,180)},
    {"name":"Banana","body":(230,210,130),"shadow":(195,175,100),"highlight":(245,230,170),"leaf":(130,165,125),"stem":(125,100,80),"blush":(245,220,180)},
    {"name":"Orange","body":(235,170,120),"shadow":(200,135,90),"highlight":(248,205,165),"leaf":(125,160,120),"stem":(115,85,65),"blush":(248,195,150)},
    {"name":"Pear","body":(185,205,140),"shadow":(150,170,110),"highlight":(215,230,175),"leaf":(130,165,125),"stem":(120,90,70),"blush":(230,215,180)},
    {"name":"Grape","body":(155,135,175),"shadow":(120,100,145),"highlight":(185,170,205),"leaf":(125,160,120),"stem":(110,80,60),"blush":(200,185,215)},
    {"name":"Watermelon","body":(140,175,130),"shadow":(110,140,100),"highlight":(180,210,170),"leaf":(120,155,115),"stem":(115,85,65),"blush":(235,150,145)},
    {"name":"Kiwi","body":(175,190,140),"shadow":(140,155,110),"highlight":(205,220,175),"leaf":(125,160,120),"stem":(118,88,68),"blush":(225,210,170)},
    {"name":"Peach","body":(235,180,170),"shadow":(200,140,130),"highlight":(248,210,200),"leaf":(130,165,125),"stem":(120,90,70),"blush":(248,190,180)},
    {"name":"Lemon","body":(240,225,110),"shadow":(200,185,80),"highlight":(250,240,160),"leaf":(140,175,135),"stem":(122,92,72),"blush":(245,230,190)},
    {"name":"Strawberry","body":(210,85,95),"shadow":(165,55,65),"highlight":(235,140,145),"leaf":(110,160,100),"stem":(100,70,50),"blush":(230,120,130)},
    {"name":"Cherry","body":(180,45,65),"shadow":(140,20,35),"highlight":(215,110,120),"leaf":(120,165,110),"stem":(90,60,40),"blush":(200,70,85)},
    {"name":"Pineapple","body":(220,175,60),"shadow":(175,130,30),"highlight":(240,210,120),"leaf":(70,130,80),"stem":(100,70,50),"blush":(230,195,130)},
    {"name":"Mango","body":(235,150,60),"shadow":(190,110,30),"highlight":(250,195,120),"leaf":(130,170,120),"stem":(110,80,60),"blush":(245,170,90)},
    {"name":"Blueberry","body":(90,80,145),"shadow":(55,45,100),"highlight":(140,130,190),"leaf":(115,155,105),"stem":(85,55,35),"blush":(120,110,170)},
    {"name":"Coconut","body":(150,125,95),"shadow":(110,90,60),"highlight":(190,170,145),"leaf":(100,140,90),"stem":(95,65,45),"blush":(170,145,115)},
    {"name":"Plum","body":(130,70,130),"shadow":(90,40,90),"highlight":(180,120,180),"leaf":(125,160,115),"stem":(105,75,55),"blush":(160,95,160)},
]

max_level_memory = 1

def save_level(level):
    global max_level_memory
    if level > max_level_memory:
        max_level_memory = level

def load_saved_level():
    return max_level_memory

def get_level_size(level):
    base_row = 4 + (level - 1) // 3
    base_col = 4 + (level - 1) // 4
    total = base_row * base_col
    if total % 2 != 0:
        base_col += 1
    return base_row, base_col

def create_level(level):
    row, col = get_level_size(level)
    pair_count = (row * col) // 2
    shuffled_fruits = random.sample(fruits, pair_count)
    selected_fruits = []
    for fruit in shuffled_fruits:
        selected_fruits.append(fruit)
        selected_fruits.append(fruit)
    random.shuffle(selected_fruits)
    opened = [[False for _ in range(col)] for _ in range(row)]
    paired = [[False for _ in range(col)] for _ in range(row)]
    preview_time = 2000 + level * 180
    return row, col, selected_fruits, opened, paired, preview_time

def generate_fruit_pattern_tile():
    tile_size = 260
    tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    tile.fill((238, 230, 218))
    dot_color = (218, 208, 196)
    dot_pos = [
        (22,33), (66,14), (124,47), (172,22), (221,54),
        (35,92), (88,117), (144,96), (196,121), (233,86),
        (18,164), (77,188), (131,158), (184,176), (226,148),
        (44,225), (99,242), (152,219), (207,231), (241,202),
        (111,72), (166,136), (55,145), (212,204), (83,56),
        (190,61), (122,201), (23,206)
    ]
    for x,y in dot_pos:
        pygame.draw.circle(tile, dot_color, (x, y), 10)

    mini_fruits = [
        {"name": "Apple", "color": (210, 115, 110)},
        {"name": "Pear", "color": (180, 200, 135)},
        {"name": "Orange", "color": (230, 165, 115)},
        {"name": "Peach", "color": (230, 175, 165)},
        {"name": "Lemon", "color": (235, 220, 105)},
        {"name": "Grape", "color": (150, 130, 170)},
        {"name": "Cherry", "color": (175, 40, 60)},
        {"name": "Blueberry", "color": (85, 75, 140)},
    ]

    positions = [
        (40, 50), (130, 40), (200, 70),
        (60, 140), (170, 130), (230, 160),
        (30, 210), (140, 220), (210, 230),
    ]
    for i, (x, y) in enumerate(positions):
        fruit = mini_fruits[i % len(mini_fruits)]
        draw_mini_fruit(tile, x, y, fruit["name"], fruit["color"])
    return tile

def draw_mini_fruit(surface, cx, cy, name, color):
    alpha = 110
    s = pygame.Surface((60, 60), pygame.SRCALPHA)
    if name == "Apple":
        pygame.draw.circle(s, (*color, alpha), (22, 26), 14)
        pygame.draw.circle(s, (120, 170, 120, alpha), (30, 14), 5)
    elif name == "Pear":
        pygame.draw.circle(s, (*color, alpha), (24, 30), 13)
        pygame.draw.circle(s, (120, 170, 120, alpha), (32, 18), 5)
    elif name == "Orange":
        pygame.draw.circle(s, (*color, alpha), (26, 26), 14)
    elif name == "Peach":
        pygame.draw.circle(s, (*color, alpha), (24, 28), 14)
        pygame.draw.circle(s, (240, 190, 180, alpha), (18, 22), 5)
    elif name == "Lemon":
        pygame.draw.ellipse(s, (*color, alpha), (12, 18, 28, 16))
    elif name == "Grape":
        for dx, dy in [(0, 0), (14, 4), (-4, 12), (12, 14)]:
            pygame.draw.circle(s, (*color, alpha), (24 + dx, 26 + dy), 7)
    elif name == "Cherry":
        pygame.draw.circle(s, (*color, alpha), (20, 30), 8)
        pygame.draw.circle(s, (*color, alpha), (32, 28), 8)
        pygame.draw.circle(s, (120, 170, 120, alpha), (30, 16), 4)
    elif name == "Blueberry":
        pygame.draw.circle(s, (*color, alpha), (26, 28), 8)
        pygame.draw.circle(s, (*color, alpha), (18, 34), 7)
        pygame.draw.circle(s, (*color, alpha), (34, 34), 7)
    surface.blit(s, (cx - 30, cy - 30))

def draw_gradient_bg(surface):
    w, h = surface.get_size()
    tile_w, tile_h = pattern_tile.get_size()
    for y in range(0, h, tile_h):
        for x in range(0, w, tile_w):
            surface.blit(pattern_tile, (x, y))

def draw_fruit(surface, cx, cy, fruit, size=24):
    name = fruit["name"]
    body = fruit["body"]
    shadow = fruit["shadow"]
    highlight = fruit["highlight"]
    leaf = fruit["leaf"]
    stem = fruit["stem"]
    blush = fruit["blush"]
    if name == "Apple":
        pygame.draw.circle(surface, body, (cx, cy + 2), size)
        pygame.draw.circle(surface, shadow, (cx - size // 3, cy + size // 4), size // 2)
        pygame.draw.circle(surface, highlight, (cx - size // 3, cy - size // 3), size // 4)
        pygame.draw.rect(surface, stem, (cx - 2, cy - size, 4, 6))
        pygame.draw.circle(surface, leaf, (cx + 6, cy - size + 2), 5)
        pygame.draw.circle(surface, blush, (cx - 9, cy + 6), 4)
        pygame.draw.circle(surface, blush, (cx + 9, cy + 6), 4)
        pygame.draw.circle(surface, (50, 50, 50), (cx - 6, cy), 2)
        pygame.draw.circle(surface, (50, 50, 50), (cx + 6, cy), 2)
    elif name == "Banana":
        pygame.draw.ellipse(surface, body, (cx - 18, cy - 6, 36, 14))
        pygame.draw.ellipse(surface, shadow, (cx - 14, cy - 2, 28, 8))
        pygame.draw.ellipse(surface, highlight, (cx - 10, cy - 4, 16, 6))
        pygame.draw.rect(surface, stem, (cx + 14, cy - 4, 5, 4))
        pygame.draw.circle(surface, (50, 50, 50), (cx - 6, cy - 1), 1.5)
        pygame.draw.circle(surface, (50, 50, 50), (cx + 5, cy - 1), 1.5)
    elif name == "Orange":
        pygame.draw.circle(surface, body, (cx, cy), size)
        pygame.draw.circle(surface, shadow, (cx - size // 3, cy + size // 4), size // 2)
        pygame.draw.circle(surface, highlight, (cx - size // 3, cy - size // 3), size // 4)
        pygame.draw.rect(surface, stem, (cx - 2, cy - size - 2, 4, 5))
        pygame.draw.circle(surface, leaf, (cx + 6, cy - size - 4), 5)
        pygame.draw.circle(surface, blush, (cx - 8, cy + 6), 4)
        pygame.draw.circle(surface, blush, (cx + 8, cy + 6), 4)
        pygame.draw.circle(surface, (50, 50, 50), (cx - 6, cy), 2)
        pygame.draw.circle(surface, (50, 50, 50), (cx + 6, cy), 2)
    elif name == "Pear":
        pygame.draw.circle(surface, body, (cx, cy + 6), size)
        pygame.draw.circle(surface, shadow, (cx - size // 3, cy + 10), size // 2)
        pygame.draw.circle(surface, highlight, (cx - size // 3, cy - 2), size // 4)
        pygame.draw.rect(surface, stem, (cx - 2, cy - size + 4, 4, 6))
        pygame.draw.circle(surface, leaf, (cx + 6, cy - size + 2), 5)
        pygame.draw.circle(surface, blush, (cx - 8, cy + 10), 4)
        pygame.draw.circle(surface, blush, (cx + 8, cy + 10), 4)
        pygame.draw.circle(surface, (50, 50, 50), (cx - 6, cy + 4), 2)
        pygame.draw.circle(surface, (50, 50, 50), (cx + 6, cy + 4), 2)
    elif name == "Grape":
        for dx, dy in [(-10, 4), (0, -4), (10, 4), (-6, 14), (6, 14)]:
            pygame.draw.circle(surface, body, (cx + dx, cy + dy), 10)
            pygame.draw.circle(surface, shadow, (cx + dx - 3, cy + dy + 3), 4)
            pygame.draw.circle(surface, highlight, (cx + dx - 3, cy + dy - 3), 3)
        pygame.draw.rect(surface, stem, (cx - 2, cy - 12, 4, 6))
        pygame.draw.circle(surface, leaf, (cx + 8, cy - 14), 5)
    elif name == "Watermelon":
        pygame.draw.ellipse(surface, body, (cx - 22, cy - 12, 44, 24))
        pygame.draw.ellipse(surface, shadow, (cx - 18, cy - 8, 36, 16))
        pygame.draw.ellipse(surface, highlight, (cx - 14, cy - 10, 20, 8))
        pygame.draw.rect(surface, stem, (cx - 2, cy - 14, 4, 6))
        pygame.draw.circle(surface, leaf, (cx + 8, cy - 16), 5)
        pygame.draw.circle(surface, (50, 50, 50), (cx - 6, cy), 2)
        pygame.draw.circle(surface, (50, 50, 50), (cx + 6, cy), 2)
    elif name == "Kiwi":
        pygame.draw.circle(surface, body, (cx, cy), size)
        pygame.draw.circle(surface, shadow, (cx - size // 3, cy + size // 4), size // 2)
        pygame.draw.circle(surface, highlight, (cx - size // 3, cy - size // 3), size // 4)
        pygame.draw.rect(surface, stem, (cx - 2, cy - size - 2, 4, 5))
        pygame.draw.circle(surface, leaf, (cx + 6, cy - size - 4), 5)
        pygame.draw.circle(surface, blush, (cx - 8, cy + 6), 4)
        pygame.draw.circle(surface, blush, (cx + 8, cy + 6), 4)
        pygame.draw.circle(surface, (50, 50, 50), (cx - 6, cy), 2)
        pygame.draw.circle(surface, (50, 50, 50), (cx + 6, cy), 2)
    elif name == "Peach":
        pygame.draw.circle(surface, body, (cx, cy + 2), size)
        pygame.draw.circle(surface, shadow, (cx - size // 3, cy + size // 4), size // 2)
        pygame.draw.circle(surface, highlight, (cx - size // 3, cy - size // 3), size // 4)
        pygame.draw.rect(surface, stem, (cx - 2, cy - size, 4, 6))
        pygame.draw.circle(surface, leaf, (cx + 6, cy - size + 2), 5)
        pygame.draw.circle(surface, blush, (cx - 9, cy + 6), 4)
        pygame.draw.circle(surface, blush, (cx + 9, cy + 6), 4)
        pygame.draw.circle(surface, (50, 50, 50), (cx - 6, cy), 2)
        pygame.draw.circle(surface, (50, 50, 50), (cx + 6, cy), 2)
    elif name == "Lemon":
        pygame.draw.ellipse(surface, body, (cx-size, cy-size*0.8, size*2, size*1.6))
        pygame.draw.ellipse(surface, shadow, (cx-size//2, cy-size//3, size, size*0.8))
        pygame.draw.ellipse(surface, highlight, (cx-size//1.5, cy-size//2, size//2, size//1.5))
        pygame.draw.rect(surface, stem, (cx - 2, cy - size, 4, 5))
        pygame.draw.circle(surface, leaf, (cx + 6, cy - size - 2),5)
        pygame.draw.circle(surface, (50,50,50), (cx-6, cy), 2)
        pygame.draw.circle(surface, (50,50,50), (cx+6, cy), 2)
    elif name == "Strawberry":
        pygame.draw.ellipse(surface, body, (cx-16, cy-20, 32, 40))
        pygame.draw.ellipse(surface, shadow, (cx-10, cy-10, 20,25))
        pygame.draw.polygon(surface, leaf, [(cx-12, cy-20), (cx+12, cy-20), (cx, cy-32)])
        pygame.draw.circle(surface, (245,245,245), (cx-6, cy-8),2)
        pygame.draw.circle(surface, (245,245,245), (cx+5, cy+4),2)
        pygame.draw.circle(surface, (245,245,245), (cx-4, cy+10),2)
    elif name == "Cherry":
        pygame.draw.circle(surface, body, (cx-10, cy), size*0.75)
        pygame.draw.circle(surface, body, (cx+10, cy), size*0.75)
        pygame.draw.circle(surface, shadow, (cx-12, cy+4), size*0.35)
        pygame.draw.circle(surface, shadow, (cx+8, cy+4), size*0.35)
        pygame.draw.line(surface, stem, (cx-10, cy-size*0.75), (cx, cy-size*1.4),3)
        pygame.draw.line(surface, stem, (cx+10, cy-size*0.75), (cx, cy-size*1.4),3)
        pygame.draw.circle(surface, leaf, (cx, cy-size*1.4 - 4), 5)
    elif name == "Pineapple":
        pygame.draw.rect(surface, body, (cx-14, cy-12, 28, 36), border_radius=8)
        pygame.draw.rect(surface, shadow, (cx-8, cy, 16,20), border_radius=4)
        pygame.draw.polygon(surface, leaf, [(cx-12, cy-12), (cx+12, cy-12), (cx, cy-28)])
    elif name == "Mango":
        pygame.draw.ellipse(surface, body, (cx-18, cy-10, 36, 24))
        pygame.draw.ellipse(surface, shadow, (cx-10, cy, 20,12))
        pygame.draw.rect(surface, stem, (cx-2, cy-size, 4, 6))
        pygame.draw.circle(surface, leaf, (cx + 6, cy - size + 2),5)
    elif name == "Blueberry":
        pygame.draw.circle(surface, body, (cx, cy), size*0.65)
        pygame.draw.circle(surface, shadow, (cx-4, cy+4), size*0.3)
        pygame.draw.circle(surface, highlight, (cx-4, cy-4), size*0.25)
        pygame.draw.rect(surface, stem, (cx - 2, cy - size*0.65 - 4, 4,4))
    elif name == "Coconut":
        pygame.draw.circle(surface, body, (cx, cy), size)
        pygame.draw.circle(surface, shadow, (cx - size //3, cy + size//4), size//2)
        pygame.draw.circle(surface, highlight, (cx - size//3, cy - size//3), size//4)
        pygame.draw.polygon(surface, (80,60,40), [(cx-6, cy-6), (cx+6, cy-6), (cx, cy+4)])
    elif name == "Plum":
        pygame.draw.circle(surface, body, (cx, cy), size)
        pygame.draw.circle(surface, shadow, (cx - size//3, cy + size//4), size//2)
        pygame.draw.circle(surface, highlight, (cx - size//3, cy - size//3), size//4)
        pygame.draw.rect(surface, stem, (cx -2, cy - size,4,6))
        pygame.draw.circle(surface, leaf, (cx+6, cy - size + 2),5)
        pygame.draw.circle(surface, (50, 50, 50), (cx-6, cy),2)
        pygame.draw.circle(surface, (50, 50, 50), (cx+6, cy),2)

def draw_card(surface, x, y, fruit, opened_flag, is_paired):
    shadow_rect = pygame.Rect(x+4, y+4, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(surface, (0,0,0,40), shadow_rect, border_radius=16)
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    if opened_flag:
        if is_paired:
            pygame.draw.rect(surface, PAIRED_COLOR, rect, border_radius=16)
            pygame.draw.rect(surface, (150,180,160), rect, width=3, border_radius=16)
        else:
            pygame.draw.rect(surface, CARD_FRONT, rect, border_radius=16)
            pygame.draw.rect(surface, (210, 205, 190), rect, width=2, border_radius=16)
        draw_fruit(surface, x + CARD_WIDTH//2, y + CARD_HEIGHT//2, fruit, size=26)
    else:
        pygame.draw.rect(surface, CARD_BACK, rect, border_radius=16)
        pygame.draw.rect(surface, CARD_BACK_DECO, rect, width=3, border_radius=16)
        pygame.draw.rect(surface, (255,255,255,30), rect.inflate(-20,-20), border_radius=12)
        txt = font_title.render("?", True, WHITE)
        surface.blit(txt, (x + CARD_WIDTH//2 - txt.get_width()//2, y + CARD_HEIGHT//2 - txt.get_height()//2))

def draw_button(surface, rect, text, hover=False):
    shadow = pygame.Rect(rect.x, rect.y+5, rect.width, rect.height)
    pygame.draw.rect(surface, (0,0,0,35), shadow, border_radius=16)
    color = BTN_HOVER if hover else BTN_NORMAL
    pygame.draw.rect(surface, color, rect, border_radius=16)
    pygame.draw.rect(surface, WHITE, rect, width=2, border_radius=16)
    label = font_text.render(text, True, BTN_TEXT)
    surface.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))

game_state = "select"
current_level = load_saved_level()
max_saved_level = current_level
ROW, COL = 4,4
card_list = []
opened = []
paired = []
first = None
second = None
wait_timer = 0
preview = True
preview_ms = 2500
wrong_chance = 3

screen = pygame.display.set_mode((720, 520))
pattern_tile = generate_fruit_pattern_tile()
pygame.display.set_caption("Fruit Memory Match")
clock = pygame.time.Clock()

btn_start = pygame.Rect(240, 200, 240, 60)
btn_exit = pygame.Rect(240, 290, 240, 60)

def load_level(lv):
    global ROW, COL, card_list, opened, paired, preview, preview_ms, first, second, wait_timer, wrong_chance
    ROW, COL, card_list, opened, paired, preview_ms = create_level(lv)
    cards_width = COL * CARD_WIDTH + (COL - 1) * MARGIN
    cards_height = ROW * CARD_HEIGHT + (ROW - 1) * MARGIN
    game_width = cards_width + 80
    game_height = TOP_PADDING + cards_height + BOTTOM_PADDING
    win_w = max(game_width, 720)
    win_h = max(game_height, 520)
    new_screen = pygame.display.set_mode((win_w, win_h))
    pygame.display.set_caption(f"Fruit Memory Match - Level {lv}")
    preview = True
    first = None
    second = None
    wait_timer = 0
    wrong_chance = 3
    return new_screen

while True:
    draw_gradient_bg(screen)
    mx, my = pygame.mouse.get_pos()
    delta_time = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        click_pos = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = event.pos
        if event.type == pygame.FINGERDOWN:
            x = event.x * screen.get_width()
            y = event.y * screen.get_height()
            click_pos = (x, y)

        if click_pos is not None:
            mx, my = click_pos
            if game_state == "select":
                if btn_start.collidepoint(mx, my):
                    screen = load_level(current_level)
                    game_state = "play"
                elif btn_exit.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()
            elif game_state == "play":
                if preview:
                    continue
                if wait_timer>0:
                    continue
                for r in range(ROW):
                    for c in range(COL):
                        cards_width = COL * CARD_WIDTH + (COL - 1) * MARGIN
                        cards_height = ROW * CARD_HEIGHT + (ROW - 1) * MARGIN
                        start_x = (screen.get_width() - cards_width) // 2
                        start_y = TOP_PADDING + (screen.get_height() - TOP_PADDING - BOTTOM_PADDING - cards_height) // 2
                        x = start_x + c * (CARD_WIDTH + MARGIN)
                        y = start_y + r * (CARD_HEIGHT + MARGIN)
                        rect = pygame.Rect(x,y,CARD_WIDTH,CARD_HEIGHT)
                        if rect.collidepoint(mx,my) and not opened[r][c] and not paired[r][c]:
                            if first is None:
                                first = (r,c)
                                opened[r][c] = True
                                sound_flip.play()
                            elif second is None:
                                second = (r,c)
                                opened[r][c] = True
                                sound_flip.play()
                                wait_timer = 800
            elif game_state == "win":
                w = screen.get_width()
                h = screen.get_height()
                btn_next = pygame.Rect(0, 0, 240, 60)
                btn_menu = pygame.Rect(0, 0, 240, 60)
                btn_next.center = (w // 2, h // 2 - 40)
                btn_menu.center = (w // 2, h // 2 + 50)
                if btn_next.collidepoint(mx,my):
                    current_level += 1
                    if current_level>max_saved_level:
                        max_saved_level = current_level
                        save_level(max_saved_level)
                    screen = load_level(current_level)
                    game_state = "play"
                elif btn_menu.collidepoint(mx,my):
                    game_state = "select"
                    current_level = max_saved_level
            elif game_state == "lose":
                w = screen.get_width()
                h = screen.get_height()
                btn_restart = pygame.Rect(0, 0, 240, 60)
                btn_back_home = pygame.Rect(0, 0, 240, 60)
                btn_restart.center = (w // 2, h // 2 - 40)
                btn_back_home.center = (w // 2, h // 2 + 50)
                if btn_restart.collidepoint(mx,my):
                    screen = load_level(current_level)
                    game_state = "play"
                elif btn_back_home.collidepoint(mx,my):
                    game_state = "select"
                    current_level = max_saved_level

    if game_state == "select":
        title = font_big.render("Fruit Memory Match", True, TEXT_COLOR)
        sub = font_text.render("Flip cards to find matching fruit pairs", True, TEXT_COLOR)
        level_text = font_small.render(f"Your highest level: {max_saved_level}", True, TEXT_COLOR)
        w = screen.get_width()
        h = screen.get_height()
        screen.blit(title, (w//2 - title.get_width()//2, 70))
        screen.blit(sub, (w//2 - sub.get_width()//2, 140))
        screen.blit(level_text, (w//2 - level_text.get_width()//2, 380))
        draw_button(screen, btn_start, "Start Game", btn_start.collidepoint(mx,my))
        draw_button(screen, btn_exit, "Quit Game", btn_exit.collidepoint(mx,my))
        credit_text = font_small.render("weixinyue + AI-generated", True, TEXT_COLOR)
        screen.blit(credit_text, (w//2 - credit_text.get_width()//2, h - 30))

    elif game_state == "play":
        if preview:
            cards_width = COL * CARD_WIDTH + (COL - 1) * MARGIN
            cards_height = ROW * CARD_HEIGHT + (ROW - 1) * MARGIN
            start_x = (screen.get_width() - cards_width) // 2
            start_y = TOP_PADDING + (screen.get_height() - TOP_PADDING - BOTTOM_PADDING - cards_height) // 2
            for r in range(ROW):
                for c in range(COL):
                    x = start_x + c*(CARD_WIDTH + MARGIN)
                    y = start_y + r*(CARD_HEIGHT + MARGIN)
                    idx = r*COL + c
                    draw_card(screen, x,y, card_list[idx], True, False)
            tip = font_text.render(f"Level {current_level} — Memorize fruits!", True, TEXT_COLOR)
            screen.blit(tip, (screen.get_width()//2 - tip.get_width()//2, screen.get_height()-40))
            pygame.display.update()
            pygame.time.wait(preview_ms)
            for r in range(ROW):
                for c in range(COL):
                    opened[r][c] = False
            preview = False
        else:
            if wait_timer>0:
                wait_timer -= delta_time
                if wait_timer <= 0:
                    r1,c1 = first
                    r2,c2 = second
                    i1 = r1*COL + c1
                    i2 = r2*COL + c2
                    if card_list[i1]==card_list[i2]:
                        paired[r1][c1]=True
                        paired[r2][c2]=True
                        sound_match.play()
                    else:
                        opened[r1][c1]=False
                        opened[r2][c2]=False
                        wrong_chance -= 1
                        sound_wrong.play()
                        if wrong_chance <= 0:
                            game_state = "lose"
                    first=None
                    second=None
            cards_width = COL * CARD_WIDTH + (COL - 1) * MARGIN
            cards_height = ROW * CARD_HEIGHT + (ROW - 1) * MARGIN
            start_x = (screen.get_width() - cards_width) // 2
            start_y = TOP_PADDING + (screen.get_height() - TOP_PADDING - BOTTOM_PADDING - cards_height) // 2
            for r in range(ROW):
                for c in range(COL):
                    x = start_x + c * (CARD_WIDTH + MARGIN)
                    y = start_y + r * (CARD_HEIGHT + MARGIN)
                    idx = r * COL + c
                    draw_card(screen, x,y, card_list[idx], opened[r][c] or paired[r][c], paired[r][c])
            status = font_text.render(f"Level:{current_level} | Remaining wrong chances: {wrong_chance}", True, TEXT_COLOR)
            screen.blit(status, (20, 20))
        all_paired = True
        for r in range(ROW):
            for c in range(COL):
                if not paired[r][c]:
                    all_paired = False
        if all_paired:
            sound_match.play()
            game_state = "win"

    elif game_state == "win":
        w = screen.get_width()
        h = screen.get_height()
        btn_next = pygame.Rect(0, 0, 240, 60)
        btn_menu = pygame.Rect(0, 0, 240, 60)
        btn_next.center = (w // 2, h // 2 - 40)
        btn_menu.center = (w // 2, h // 2 + 50)

        title = font_big.render("Congratulations!", True, TEXT_COLOR)
        info = font_text.render(f"You completed Level {current_level}", True, TEXT_COLOR)
        screen.blit(title, (w//2-title.get_width()//2,80))
        screen.blit(info, (w//2-info.get_width()//2,150))
        draw_button(screen, btn_next, "Next Level", btn_next.collidepoint(mx,my))
        draw_button(screen, btn_menu, "Main Menu", btn_menu.collidepoint(mx,my))

    elif game_state == "lose":
        w = screen.get_width()
        h = screen.get_height()
        btn_restart = pygame.Rect(0, 0, 240, 60)
        btn_back_home = pygame.Rect(0, 0, 240, 60)
        btn_restart.center = (w // 2, h // 2 - 40)
        btn_back_home.center = (w // 2, h // 2 + 50)

        title = font_big.render("Out of chances", True, TEXT_COLOR)
        info = font_text.render("All 3 attempts used up", True, TEXT_COLOR)
        screen.blit(title, (w//2-title.get_width()//2,80))
        screen.blit(info, (w//2-info.get_width()//2,150))
        draw_button(screen, btn_restart, "Restart Level", btn_restart.collidepoint(mx,my))
        draw_button(screen, btn_back_home, "Main Menu", btn_back_home.collidepoint(mx,my))

    pygame.display.update()
