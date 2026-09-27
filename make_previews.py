"""Generate branded preview screenshots for the README.

These are placeholder previews (clearly labelled) so the README's Screenshots
section renders before real captures are added. Replace the PNG files in
static/images/screenshots/ with actual screenshots to go live.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join("static", "images", "screenshots")
os.makedirs(OUT, exist_ok=True)

W, H = 1280, 800
NAVY = (15, 23, 42)
WHITE = (255, 255, 255)
MUTED = (148, 163, 184)
INDIGO = (79, 70, 229)
VIOLET = (139, 92, 246)
CYAN = (6, 182, 212)
GREEN = (16, 185, 129)
RED = (244, 63, 94)


def font(size, bold=False):
    names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(os.path.join("C:", "\\", "Windows", "Fonts", name), size)
        except Exception:
            continue
    return ImageFont.load_default()


def gradient(size, c1, c2, angle=135):
    w, h = size
    base = Image.new("RGB", (w, h))
    px = base.load()
    for y in range(h):
        for x in range(0, w, 4):
            t = (x / w + y / h) / 2
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            for dx in range(4):
                if x + dx < w:
                    px[x + dx, y] = (r, g, b)
    return base


def browser_frame(title_text):
    img = Image.new("RGB", (W, H), (246, 247, 251))
    d = ImageDraw.Draw(img)
    # toolbar
    d.rectangle([0, 0, W, 56], fill=(255, 255, 255))
    d.line([0, 56, W, 56], fill=(226, 230, 240), width=1)
    for i, col in enumerate([RED, (255, 189, 46), GREEN]):
        x = 24 + i * 26
        d.ellipse([x, 20, x + 16, 36], fill=col)
    # address bar
    d.rounded_rectangle([120, 14, W - 24, 42], radius=8, fill=(241, 245, 249))
    d.text((136, 19), title_text, font=font(15), fill=MUTED)
    return img, d


def label_note(d, y, note):
    d.rounded_rectangle([W - 300, H - 46, W - 16, H - 14], radius=8, fill=NAVY)
    d.text((W - 288, H - 40), note, font=font(14, bold=True), fill=WHITE)


def save(img, name):
    img.save(os.path.join(OUT, name), "PNG")
    print("wrote", name)


# ---- Landing ----
img, d = browser_frame("http://127.0.0.1:5000/")
hero = gradient((W, 420), INDIGO, CYAN)
img.paste(hero, (0, 57))
d = ImageDraw.Draw(img)
d.text((70, 150), "Smart Parking", font=font(64, bold=True), fill=WHITE)
d.text((70, 224), "Management for Campuses", font=font(64, bold=True), fill=WHITE)
d.text((70, 320), "Automated slot allocation, real-time availability", font=font(22), fill=(226, 232, 240))
d.text((70, 352), "and a seamless parking experience for everyone.", font=font(22), fill=(226, 232, 240))
d.rounded_rectangle([70, 410, 260, 460], radius=10, fill=VIOLET)
d.text((100, 422), "Get Started", font=font(20, bold=True), fill=WHITE)
d.rounded_rectangle([280, 410, 400, 460], radius=10, outline=WHITE, width=2)
d.text((310, 422), "Login", font=font(20, bold=True), fill=WHITE)
d.text((70, 510), "Key Features", font=font(30, bold=True), fill=NAVY)
for i in range(6):
    cx = 70 + (i % 3) * 390
    cy = 560 + (i // 3) * 120
    d.rounded_rectangle([cx, cy, cx + 350, cy + 100], radius=12, fill=WHITE)
    d.rounded_rectangle([cx + 16, cy + 16, cx + 46, cy + 46], radius=8, fill=INDIGO)
    d.text((cx + 60, cy + 20), "Feature", font=font(18, bold=True), fill=NAVY)
    d.text((cx + 60, cy + 50), "Preview tile", font=font(14), fill=MUTED)
label_note(d, 510, "PREVIEW")
save(img, "landing.png")

# ---- Login ----
img, d = browser_frame("http://127.0.0.1:5000/login")
d.rectangle([0, 57, W, H], fill=(246, 247, 251))
cx = W // 2
d.rounded_rectangle([cx - 220, 150, cx + 220, 640], radius=20, fill=WHITE)
d.rectangle([cx - 220, 150, cx + 220, 156], fill=INDIGO)
d.rounded_rectangle([cx - 40, 190, cx + 40, 270], radius=16, fill=INDIGO)
d.text((cx - 14, 216), "P", font=font(36, bold=True), fill=WHITE)
d.text((cx - 120, 290), "Welcome Back", font=font(28, bold=True), fill=NAVY)
d.rounded_rectangle([cx - 160, 350, cx + 160, 390], radius=8, outline=(226, 230, 240), width=2)
d.text((cx - 145, 362), "Email address", font=font(16), fill=MUTED)
d.rounded_rectangle([cx - 160, 410, cx + 160, 450], radius=8, outline=(226, 230, 240), width=2)
d.text((cx - 145, 422), "Password", font=font(16), fill=MUTED)
d.rounded_rectangle([cx - 160, 480, cx + 160, 524], radius=10, fill=VIOLET)
d.text((cx - 48, 494), "Login", font=font(18, bold=True), fill=WHITE)
label_note(d, 290, "PREVIEW")
save(img, "login.png")

# ---- Register ----
img, d = browser_frame("http://127.0.0.1:5000/register")
d.rectangle([0, 57, W, H], fill=(246, 247, 251))
cx = W // 2
d.rounded_rectangle([cx - 260, 110, cx + 260, 700], radius=20, fill=WHITE)
d.rectangle([cx - 260, 110, cx + 260, 116], fill=INDIGO)
d.text((cx - 160, 140), "Create Account", font=font(28, bold=True), fill=NAVY)
fields = ["First name", "Last name", "Email address", "Phone", "Password", "Role"]
for i, f in enumerate(fields):
    col = i % 2
    row = i // 2
    x = cx - 220 + col * 230
    y = 200 + row * 80
    d.rounded_rectangle([x, y, x + 200, y + 44], radius=8, outline=(226, 230, 240), width=2)
    d.text((x + 14, y + 12), f, font=font(15), fill=MUTED)
d.rounded_rectangle([cx - 220, 560, cx + 220, 604], radius=10, fill=VIOLET)
d.text((cx - 60, 574), "Register", font=font(18, bold=True), fill=WHITE)
label_note(d, 140, "PREVIEW")
save(img, "register.png")

# ---- Dashboard ----
img, d = browser_frame("http://127.0.0.1:5000/dashboard")
d.rectangle([0, 57, W, H], fill=(246, 247, 251))
grad = gradient((W - 140, 120), INDIGO, VIOLET)
img.paste(grad, (70, 90))
d = ImageDraw.Draw(img)
d.text((96, 120), "Welcome back, Akshay", font=font(28, bold=True), fill=WHITE)
cards = [("Available", GREEN, "45"), ("Occupied", RED, "55"), ("Bookings", INDIGO, "8"), ("Revenue", CYAN, "Rs 1.2k")]
for i, (t, col, v) in enumerate(cards):
    x = 70 + i * 295
    d.rounded_rectangle([x, 240, x + 265, 360], radius=14, fill=WHITE)
    d.rounded_rectangle([x + 18, 262, x + 58, 302], radius=10, fill=col)
    d.text((x + 72, 262), v, font=font(30, bold=True), fill=NAVY)
    d.text((x + 18, 315), t, font=font(16), fill=MUTED)
d.rounded_rectangle([70, 390, 700, 720], radius=14, fill=WHITE)
d.text((96, 410), "Live Slot Map", font=font(20, bold=True), fill=NAVY)
for r in range(6):
    for c in range(8):
        x = 96 + c * 68
        y = 460 + r * 40
        col = GREEN if (r + c) % 3 else RED
        d.rounded_rectangle([x, y, x + 56, y + 32], radius=6, fill=col)
d.rounded_rectangle([730, 390, W - 70, 720], radius=14, fill=WHITE)
d.text((756, 410), "Recent Activity", font=font(20, bold=True), fill=NAVY)
label_note(d, 120, "PREVIEW")
save(img, "dashboard.png")

print("done")
