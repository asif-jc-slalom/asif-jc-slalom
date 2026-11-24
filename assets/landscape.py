"""Generates the animated footer scene: a slalom ski run under the Slalom blue palette, night in dark mode, day in light.

Run `python3 assets/landscape.py` from the repo root after editing; it rewrites both SVGs.
The run is a single Bezier slope; gates, trees, the skier and the finish banner are all placed on it by parameter t.
"""

import random
from pathlib import Path

W, H = 850, 240
BLUE = "#0C62FB"  # Slalom blue
P = [(-10, 92), (220, 98), (520, 138), (860, 198)]  # slope curve control points

THEMES = {
    "dark": {
        "layers": ["#071a4d", "#0a2a7a", "#0b46c2"],
        "snow": "#b9d0ff",
        "snow2": "#8fb2f5",
        "tree": "#06143d",
        "gate_a": BLUE,
        "gate_b": "#e6f0ff",
        "ink": "#e6edf3",
        "cable": "#5f7fc9",
        "banner": "#0b1b4d",
        "night": True,
    },
    "light": {
        "layers": ["#cfe0ff", "#9cc0ff", "#5c97ff"],
        "snow": "#f1f6ff",
        "snow2": "#d3e2ff",
        "tree": "#0a3a9a",
        "gate_a": BLUE,
        "gate_b": "#0A2A7A",
        "ink": "#0a2a7a",
        "cable": "#6b8bd0",
        "banner": "#ffffff",
        "night": False,
    },
}


def bez(t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = P
    u = 1 - t
    x = u**3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t**3 * x3
    y = u**3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t**3 * y3
    return x, y


def ridge(rng, base, amp, step, snowcap):
    """Alpine ridge as a closed path; snowcap adds a lighter triangle on each peak."""
    pts = [(x, base - rng.uniform(0.3, 1.0) * amp) for x in range(-20, W + 2 * step, step)]
    d = f"M{pts[0][0]},{H} L{pts[0][0]},{pts[0][1]:.1f}" + "".join(f" L{x},{y:.1f}" for x, y in pts[1:])
    d += f" L{pts[-1][0]},{H} Z"
    caps = ""
    if snowcap:
        for i in range(1, len(pts) - 1):
            (xa, ya), (xb, yb), (xc, yc) = pts[i - 1], pts[i], pts[i + 1]
            if yb < ya and yb < yc:
                dy = (min(ya, yc) - yb) * 0.4
                caps += f"M{xb:.0f},{yb:.1f} L{xb - (xb - xa) * 0.4:.0f},{yb + dy:.1f} L{xb + (xc - xb) * 0.4:.0f},{yb + dy:.1f} Z "
    return d, caps


def pine(x, y, s, colour):
    return (
        f'<g transform="translate({x:.0f} {y:.0f}) scale({s})" fill="{colour}">'
        '<path d="M0,-26 L7,-12 L3,-12 L10,0 L-10,0 L-3,-12 L-7,-12 Z"/><rect x="-1.2" y="0" width="2.4" height="4"/></g>'
    )


def gate(x, y, colour, ink):
    return (
        f'<g transform="translate({x:.0f} {y:.0f}) scale(1.4)"><line x1="0" y1="0" x2="0" y2="-17" stroke="{ink}" stroke-width="1.2"/>'
        f'<path d="M0,-17 L9,-14 L0,-11 Z" fill="{colour}"/></g>'
    )


def build(theme):
    t = THEMES[theme]
    rng = random.Random(11)  # fixed seed so both themes share the same geography
    far, far_caps = ridge(rng, 108, 80, 40, True)
    mid, mid_caps = ridge(rng, 140, 46, 64, True)
    slope = "M{},{} C{},{} {},{} {},{} L860,{} L-10,{} Z".format(
        P[0][0], P[0][1], P[1][0], P[1][1], P[2][0], P[2][1], P[3][0], P[3][1], H, H
    )
    drift = f"M-10,{H} L-10,205 C200,190 520,214 860,{H} Z"
    ski_path = "M{},{} C{},{} {},{} {},{}".format(
        P[0][0], P[0][1] - 4, P[1][0], P[1][1] - 4, P[2][0], P[2][1] - 4, P[3][0], P[3][1] - 4
    )
    cable_y = (30, 66)

    sky = []
    if t["night"]:
        sky.append(
            '<g class="aurora" filter="url(#blur)"><ellipse cx="300" cy="46" rx="260" ry="14" fill="#0C62FB" opacity=".35"/>'
            '<ellipse cx="520" cy="62" rx="220" ry="10" fill="#38bdf8" opacity=".22"/></g>'
        )
        for _ in range(55):
            sx, sy = rng.uniform(0, W), rng.uniform(4, 95)
            sky.append(
                f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{rng.uniform(0.5, 1.3):.1f}" fill="#e6edf3" class="star" '
                f'style="animation-delay:-{rng.uniform(0, 6):.1f}s;animation-duration:{rng.uniform(3, 7):.1f}s"/>'
            )
        sky.append(
            '<g transform="translate(700 40)"><circle r="26" fill="#e6edf3" opacity=".06"/>'
            '<circle r="13" fill="#e6edf3" opacity=".9" mask="url(#crescent)"/></g>'
            '<line x1="0" y1="0" x2="46" y2="14" stroke="url(#trail)" stroke-width="1.4" class="meteor"/>'
        )
    else:
        sky.append(
            '<g transform="translate(700 44)"><circle r="30" fill="#f2cc60" opacity=".15"/>'
            '<circle r="15" fill="#f2cc60" opacity=".85"/></g>'
        )
        for i, (by, dur, delay) in enumerate([(42, 48, 0), (56, 56, 18), (30, 64, 33)]):
            sky.append(
                f'<g class="drift" style="animation-duration:{dur}s;animation-delay:-{delay}s">'
                f'<path transform="translate(0 {by})" stroke="#57606a" stroke-width="1.3" fill="none">'
                f'<animate attributeName="d" dur="{0.9 + 0.2 * i:.1f}s" repeatCount="indefinite" '
                'values="M0,0 q4,-4 8,0 q4,-4 8,0;M0,0 q4,3 8,0 q4,3 8,0;M0,0 q4,-4 8,0 q4,-4 8,0"/></path></g>'
            )
    cloud_fill, cloud_op = ("#274690", ".35") if t["night"] else ("#ffffff", ".8")
    for cy, dur, delay, s in [(28, 140, 20, 1.0), (64, 180, 95, 0.7)]:
        sky.append(
            f'<g class="drift" style="animation-duration:{dur}s;animation-delay:-{delay}s" fill="{cloud_fill}" opacity="{cloud_op}">'
            f'<g transform="translate(0 {cy}) scale({s})"><ellipse cx="0" cy="0" rx="34" ry="8"/>'
            '<ellipse cx="-12" cy="-6" rx="16" ry="8"/><ellipse cx="10" cy="-8" rx="18" ry="9"/></g></g>'
        )

    # Gondola cable from the left peak to the right; the cabin rides it with SMIL so it works inside <img>.
    cable = (
        f'<line x1="0" y1="{cable_y[0]}" x2="{W}" y2="{cable_y[1]}" stroke="{t["cable"]}" stroke-width="1" opacity=".7"/>'
        '<g><animateMotion dur="38s" repeatCount="indefinite" '
        f'path="M0,{cable_y[0]} L{W},{cable_y[1]}"/>'
        f'<line x1="0" y1="0" x2="0" y2="7" stroke="{t["cable"]}" stroke-width="1"/>'
        f'<rect x="-6" y="7" width="12" height="8" rx="1.5" fill="{BLUE}"/>'
        '<rect x="-4" y="9" width="3" height="3" fill="#e6f0ff" opacity=".9"/>'
        '<rect x="1" y="9" width="3" height="3" fill="#e6f0ff" opacity=".9"/></g>'
    )

    trees = []
    for tt, s, dy in [(0.04, 1.1, 7), (0.09, 0.8, 5), (0.15, 1.3, 9), (0.5, 0.9, 7), (0.56, 1.2, 9),
                      (0.62, 0.8, 6), (0.93, 1.2, 9), (0.97, 0.9, 7)]:
        x, y = bez(tt)
        trees.append(pine(x, y + dy, s, t["tree"]))

    gates = []
    for i, tt in enumerate([0.14 + 0.075 * k for k in range(9)]):
        x, y = bez(tt)
        gates.append(gate(x, y + 2, t["gate_a"] if i % 2 == 0 else t["gate_b"], t["ink"]))

    # Finish banner straddling the run, the one place the brand name appears in the scene.
    bx, by = bez(0.9)
    banner = (
        f'<g transform="translate({bx:.0f} {by + 4:.0f})">'
        f'<line x1="-34" y1="0" x2="-34" y2="-30" stroke="{t["ink"]}" stroke-width="1.5"/>'
        f'<line x1="34" y1="6" x2="34" y2="-24" stroke="{t["ink"]}" stroke-width="1.5"/>'
        f'<path d="M-34,-30 L34,-24 L34,-9 L-34,-15 Z" fill="{BLUE}"/>'
        '<text x="0" y="-14" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-weight="700" '
        'font-size="12" letter-spacing="1" fill="#fff" transform="rotate(5 0 -16)">slalom</text></g>'
    )

    skier = (
        f'<g><animateMotion dur="9s" repeatCount="indefinite" rotate="auto" path="{ski_path}" keyPoints="0;1" '
        'keyTimes="0;1" calcMode="linear"/>'
        f'<g transform="scale(1.6)"><g class="carve"><circle cx="0" cy="-10" r="2.2" fill="{t["ink"]}"/>'
        f'<path d="M0,-8 L-2,-2 M-2,-2 L3,0 M0,-7 L4,-4" stroke="{BLUE}" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
        f'<line x1="-7" y1="1.5" x2="8" y2="1.5" stroke="{t["ink"]}" stroke-width="1.4" stroke-linecap="round"/></g></g></g>'
    )

    snow = "".join(
        f'<circle cx="{rng.uniform(0, W):.0f}" cy="-6" r="{rng.uniform(0.8, 1.8):.1f}" fill="{"#e6f0ff" if t["night"] else "#8fb2f5"}" '
        f'class="flake" style="animation-duration:{rng.uniform(6, 12):.1f}s;animation-delay:-{rng.uniform(0, 12):.1f}s"/>'
        for _ in range(38)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<!-- Generated by assets/landscape.py; edit that, not this. -->
<defs>
  <mask id="crescent"><circle r="13" fill="#fff"/><circle cx="6" cy="-4" r="11" fill="#000"/></mask>
  <linearGradient id="trail"><stop offset="0" stop-color="#e6edf3" stop-opacity="0"/><stop offset="1" stop-color="#e6edf3"/></linearGradient>
  <filter id="blur" x="-20%" y="-100%" width="140%" height="300%"><feGaussianBlur stdDeviation="9"/></filter>
</defs>
<style>
  .star {{ animation: twinkle ease-in-out infinite alternate; }}
  @keyframes twinkle {{ from {{ opacity: .15 }} to {{ opacity: .9 }} }}
  .drift {{ animation: drift linear infinite; }}
  @keyframes drift {{ from {{ transform: translateX(-80px) }} to {{ transform: translateX({W + 80}px) }} }}
  .meteor {{ opacity: 0; animation: meteor 11s ease-out infinite 3s; }}
  @keyframes meteor {{ 0%, 90% {{ opacity: 0; transform: translate(80px, 10px) }} 92% {{ opacity: 1 }} 100% {{ opacity: 0; transform: translate(260px, 64px) }} }}
  .aurora {{ animation: aurora 9s ease-in-out infinite alternate; }}
  @keyframes aurora {{ from {{ opacity: .5; transform: translateX(-24px) }} to {{ opacity: 1; transform: translateX(24px) }} }}
  .flake {{ animation: fall linear infinite; }}
  @keyframes fall {{ from {{ transform: translate(0, 0); opacity: .9 }} to {{ transform: translate(-30px, {H + 12}px); opacity: .2 }} }}
  .carve {{ animation: carve .9s ease-in-out infinite alternate; }}
  @keyframes carve {{ from {{ transform: translate(0, -1px) rotate(-6deg) }} to {{ transform: translate(0, -2px) rotate(6deg) }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
{"".join(sky)}
<path d="{far}" fill="{t["layers"][0]}"/>
<path d="{far_caps}" fill="{t["snow2"]}" opacity=".55"/>
<path d="{mid}" fill="{t["layers"][1]}"/>
<path d="{mid_caps}" fill="{t["snow2"]}" opacity=".5"/>
{cable}
<path d="{slope}" fill="{t["snow"]}"/>
<path d="{drift}" fill="{t["snow2"]}"/>
{"".join(trees)}
{"".join(gates)}
{banner}
{skier}
{snow}
</svg>
"""


if __name__ == "__main__":
    here = Path(__file__).parent
    for theme in THEMES:
        (here / f"landscape-{theme}.svg").write_text(build(theme))
