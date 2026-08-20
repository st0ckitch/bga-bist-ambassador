#!/usr/bin/env python3
"""Generate the Circle brand marks as SVG.

Every mark is built from arcs on one construction circle so the family stays
geometrically consistent: centre (50,50) in a 100x100 viewBox, radius 36.

Round line caps extend half the stroke width past the arc endpoint, which eats
into the gaps. That overhang is ~ (stroke/2)/radius radians, so a 40 degree
geometric gap with a 12 unit stroke shows as roughly 21 degrees of daylight.
The sweeps below are chosen so the visible gap stays close to one stroke width
- wide enough to read as deliberate at 22px in the nav, tight enough that the
ring still closes as a single shape.
"""

import math
from pathlib import Path

OUT = Path(__file__).parent

NAVY = "#0D1B3E"
GOLD = "#F2B32C"
GOLD_DEEP = "#D99A14"   # the darker stop of the card gradient already on the site
CREAM = "#F6F4EE"
WHITE = "#FFFFFF"

CX = CY = 50.0
R = 36.0


def point(angle_deg, radius=R):
    a = math.radians(angle_deg)
    return CX + radius * math.cos(a), CY + radius * math.sin(a)


def arc(start_deg, end_deg, color, stroke, radius=R):
    """One arc, drawn clockwise on screen from start to end (y grows downward)."""
    sweep = (end_deg - start_deg) % 360
    x1, y1 = point(start_deg, radius)
    x2, y2 = point(end_deg, radius)
    large = 1 if sweep > 180 else 0
    return (
        f'<path d="M {x1:.3f} {y1:.3f} A {radius} {radius} 0 {large} 1 '
        f'{x2:.3f} {y2:.3f}" fill="none" stroke="{color}" '
        f'stroke-width="{stroke}" stroke-linecap="round"/>'
    )


def svg(body, view="0 0 100 100", size=None, title="Circle"):
    dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}"{dims} '
        f'role="img" aria-label="{title}">\n  '
        + "\n  ".join(body)
        + "\n</svg>\n"
    )


# --- Primary: two arcs, one circle ------------------------------------------
# Gaps of 40 degrees centred on the upper-right (315) and lower-left (135)
# diagonal. Each arc sweeps 140 degrees. Navy holds the upper-left, gold the
# lower-right, so the split reads as two forms completing one ring.
STROKE = 12.0
ARC_A = (155.0, 295.0)   # upper-left
ARC_B = (335.0, 115.0)   # lower-right


def two_arcs(c_a, c_b, stroke=STROKE):
    return [arc(*ARC_A, c_a, stroke), arc(*ARC_B, c_b, stroke)]


def write(name, content):
    (OUT / name).write_text(content)
    print(f"  {name}")


print("marks:")
write("circle-mark.svg", svg(two_arcs(NAVY, GOLD)))
write("circle-mark-reverse.svg", svg(two_arcs(CREAM, GOLD), title="Circle (reversed)"))
write("circle-mark-navy.svg", svg(two_arcs(NAVY, NAVY), title="Circle (one colour)"))
write("circle-mark-gold.svg", svg(two_arcs(GOLD, GOLD), title="Circle (one colour)"))

# Small optical cut, for use at 32px and below on cream or white.
# Two changes from the standard cut, both measured rather than guessed:
# the stroke goes up so the arcs survive rasterisation, and the gold drops to
# the deeper stop of the card gradient because #F2B32C on #F6F4EE loses the
# lower arc at nav size - the mark reads lopsided instead of circular.
write(
    "circle-mark-small.svg",
    svg(two_arcs(NAVY, GOLD_DEEP, stroke=14.0), title="Circle (small sizes)"),
)

# --- Favicon: navy tile, cropped tighter so the ring fills the square --------
# Stroke 16 on a radius-30 ring: at 16px this is the lightest weight where both
# arcs and both gaps still resolve. Thinner mushes into a blob, wider gaps stop
# reading as one closed ring.
favicon = [f'<rect width="100" height="100" rx="20" fill="{NAVY}"/>'] + [
    arc(*ARC_A, CREAM, 16.0, radius=30),
    arc(*ARC_B, GOLD, 16.0, radius=30),
]
write("circle-favicon.svg", svg(favicon, title="Circle"))

# --- Badge chip: drops into the gold card chip slot in the navy band ---------
chip = [
    f'<rect width="58" height="38" rx="7" fill="{GOLD}"/>',
    '<g transform="translate(16 6) scale(0.26)">',
    "  " + arc(*ARC_A, NAVY, 13.5),
    "  " + arc(*ARC_B, NAVY, 13.5),
    "</g>",
]
write("circle-chip.svg", svg(chip, view="0 0 58 38", size=(58, 38), title="Circle card"))

# --- Alternate 1: segmented ring, one segment per partner category ----------
CATS = 7
SLOT = 360.0 / CATS
SEG = 28.0
seg_stroke = 9.0
segments = []
for i in range(CATS):
    centre = -90.0 + i * SLOT
    color = GOLD if i == 1 else NAVY
    segments.append(arc(centre - SEG / 2, centre + SEG / 2, color, seg_stroke))
write("circle-segmented.svg", svg(segments, title="Circle (segmented)"))

# --- Alternate 2: C-monogram that resolves into a closed circle -------------
mono = [arc(65.0, 295.0, NAVY, STROKE), arc(-30.0, 30.0, GOLD, STROKE)]
write("circle-monogram.svg", svg(mono, title="Circle (monogram)"))

# --- Lockup: mark + wordmark ------------------------------------------------
# Sora is not installed here, so the wordmark stays live text with a fallback
# stack. On the site itself the lockup is built in HTML from the same webfont
# the page already loads; this file is the reference artwork.
MARK = 32.0
lockup = [
    f'<g transform="translate(4 4) scale({MARK / 100:.4f})">',
    "  " + arc(*ARC_A, NAVY, STROKE),
    "  " + arc(*ARC_B, GOLD, STROKE),
    "</g>",
    f'<text x="50" y="29.4" fill="{NAVY}" font-family="Sora, Manrope, '
    'system-ui, sans-serif" font-weight="800" font-size="26" '
    'letter-spacing="5.72">CIRCLE</text>',
]
write("circle-lockup.svg", svg(lockup, view="0 0 190 40", title="Circle"))

# --- Geometry report --------------------------------------------------------
cap_deg = math.degrees((STROKE / 2) / R)
gap_deg = (ARC_B[0] - ARC_A[1]) % 360
visible = gap_deg - 2 * cap_deg
print(
    f"\nprimary: stroke {STROKE:.0f}, arc sweep "
    f"{(ARC_A[1] - ARC_A[0]) % 360:.0f} deg, gap {gap_deg:.0f} deg geometric "
    f"-> {visible:.1f} deg visible ({math.radians(visible) * R:.1f} units, "
    f"{math.radians(visible) * R / 100 * 22:.1f}px at 22px)"
)
