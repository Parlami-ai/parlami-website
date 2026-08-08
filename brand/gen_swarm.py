#!/usr/bin/env python3
"""Generate swarm-of-dots speech bubble mark for Parlami."""
import random, math, sys

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 42)

# Bubble geometry (matches previous mark): rounded rect 96..416 x 120..360, r=72
X0, X1, Y0, Y1, R = 96, 416, 120, 360, 72

def inside_rounded_rect(x, y):
    if not (X0 <= x <= X1 and Y0 <= y <= Y1):
        return False
    cx = min(max(x, X0 + R), X1 - R)
    cy = min(max(y, Y0 + R), Y1 - R)
    return (x - cx) ** 2 + (y - cy) ** 2 <= R * R

def circle_fits(x, y, r):
    for a in range(10):
        th = a * math.pi / 5
        if not inside_rounded_rect(x + r * math.cos(th), y + r * math.sin(th)):
            return False
    return True

# Bars (drawn separately): capsules x=196,256,316, y 298 down to 252/216/180, half-width 19
BARS = [(196, 252, 298), (256, 216, 298), (316, 180, 298)]
BAR_HW = 19
CLEAR = 5

def dist_to_bar(x, y, bar):
    bx, ytop, ybot = bar
    cy = min(max(y, ytop), ybot)
    return math.hypot(x - bx, y - cy)

def clear_of_bars(x, y, r):
    return all(dist_to_bar(x, y, b) >= BAR_HW + CLEAR + r for b in BARS)

# Color: gradient cyan -> violet along the same diagonal as before, + emerald accents
def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

CYAN, VIOLET, EMERALD, WHITE = (0x22, 0xD3, 0xEE), (0x8B, 0x5C, 0xF6), (0x34, 0xD3, 0x99), (255, 255, 255)

def color_for(x, y):
    # t=0 at bottom-left (cyan), 1 at top-right (violet); same axis as old gradient
    t = ((x - X0) / (X1 - X0) + (430 - y) / (430 - Y0)) / 2
    t = min(1, max(0, t + random.uniform(-0.08, 0.08)))
    roll = random.random()
    if roll < 0.13:
        c = EMERALD
    elif roll < 0.21:
        c = lerp(lerp(CYAN, VIOLET, t), WHITE, 0.35)  # sparkle tint
    else:
        c = lerp(CYAN, VIOLET, t)
    return "#%02x%02x%02x" % c

# Dart-throw packing, big dots first
dots = []
attempts = [(random.uniform(X0, X1), random.uniform(Y0, Y1), 4.5 + 11.5 * random.random() ** 1.3) for _ in range(150000)]
attempts.sort(key=lambda d: -d[2])
GAP = 2.5
for x, y, r in attempts:
    if not circle_fits(x, y, r) or not clear_of_bars(x, y, r):
        continue
    if all(math.hypot(x - ox, y - oy) >= r + orr + GAP for ox, oy, orr, _ in dots):
        dots.append((x, y, r, color_for(x, y)))

# Tail: trail of shrinking dots toward bottom-left tip (cyan end)
tail = [(206, 386, 21), (172, 414, 13.5), (150, 436, 8)]
for x, y, r in tail:
    dots.append((x, y, r, color_for(x, y)))

# Flyaways: small dots escaping top-right (kept inside avatar circle-crop, r<246 from center)
fly = [(424, 128, 8.5), (441, 111, 6), (448, 101, 4)]
for x, y, r in fly:
    dots.append((x, y, r, color_for(x, y)))

print(f"<!-- {len(dots)} dots -->", file=sys.stderr)
out = []
for x, y, r, c in dots:
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c}"/>')
open(sys.argv[2] if len(sys.argv) > 2 else "swarm-dots.txt", "w").write("\n".join(out))
