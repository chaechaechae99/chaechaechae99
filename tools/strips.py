"""One-line animated strips for each STAGE in the profile README."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import gen  # noqa: E402
from gen import text, sprite, font_face, FONTS, MOLE2, SOCCER, RUN_A, RUN_B  # noqa: E402

AIRPORT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
sys.path.insert(0, str(AIRPORT))
import sprites as AP  # noqa: E402  (the user's own airport game sprites)

PAL = AP.PALETTE_DAY


def ap(name, x, y, cls=""):
    """Draw a sprite from the airport game. 'h' (shadow) drawn translucent."""
    rows = AP.SPRITES[name]
    pal = dict(PAL)
    g = sprite(rows, pal, x, y, 1)
    if cls:
        g = f'<g class="{cls}">{g}</g>'
    return g


# ---------------------------------------------------------------- 1 airport
def strip_airport():
    b, css = [], []
    W, H = 420, 84
    ry = 48                                         # runway row
    from PIL import Image
    import base64, io
    img = Image.new("RGB", (W, H))
    def paste(name, x, y):
        for r, row in enumerate(AP.SPRITES[name]):
            for c, ch in enumerate(row):
                if ch != "." and 0 <= x + c < W and 0 <= y + r < H:
                    img.putpixel((x + c, y + r), tuple(int(PAL[ch][i:i + 2], 16) for i in (1, 3, 5)))
    for ty in range(0, H, 32):
        for tx in range(0, W, 32):
            paste(f"grass{(tx // 32 + ty // 32) % 4}", tx, ty)
    n = W // 32 + 1
    for i in range(n):
        paste("runway_h_w" if i == 0 else ("runway_h_e" if i == n - 1 else "runway_h"), i * 32, ry)
    for name, x in (("tree0", 0), ("terminal2_0", 40), ("terminal1_1", 74), ("hangar", 150), ("hangar_closed", 184), ("tree1", 230), ("shop1_0", 262), ("hangar_light", 330), ("tree0", 372), ("tree1", 398)):
        paste(name, x, 46 - len(AP.SPRITES[name]))
    buf = io.BytesIO(); img.save(buf, "PNG", optimize=True)
    b.append(f'<image width="{W}" height="{H}" style="image-rendering:pixelated" href="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"/>')
    # plane + shadow: lands from the left, rolls, takes off to the right
    plane, shadow = "mid_red_e", "midshadow_e"
    ph = len(AP.SPRITES[plane])
    base_y = ry + 16 - ph // 2                      # centred on the runway
    b.append(f'<g class="shd">{ap(shadow, 0, 0)}</g>')
    b.append(f'<g class="pln">{ap(plane, 0, 0)}</g>')
    T = 9
    # x positions / altitude (px up) over time
    keys = [(0, -50, 34), (25, 70, 14), (38, 130, 0), (55, 210, 0), (70, 280, 10), (100, 470, 40)]
    pk = "".join(f"{p}%{{transform:translate({x}px,{base_y - alt}px)}}" for p, x, alt in keys)
    sk = "".join(f"{p}%{{transform:translate({x + 6}px,{base_y + 4}px)}}" for p, x, alt in keys)
    css.append(f".pln{{animation:pln {T}s linear infinite}}@keyframes pln{{{pk}}}")
    css.append(f".shd{{opacity:.35;animation:shd {T}s linear infinite}}@keyframes shd{{{sk}}}")
    # caption chip
    b.append('<rect x="4" y="4" width="104" height="16" fill="#000" opacity=".55"/>')
    b.append(text(10, 16, "내 게임 실제 화면", 12, "#ffd84d", "G"))
    return b, css, W, H


# ---------------------------------------------------------------- 2 운결
SUN = [
    "....y..y....",
    ".y..yyyy..y.",
    "..yyyyyyyy..",
    "..yyoyyoyy..",
    "yyyyyyyyyyyy",
    "..yyyyyyyy..",
    "..yyorroyy..",
    ".y..yyyy..y.",
    "....y..y....",
]


def strip_fortune():
    b, css = [], []
    W, H = 420, 84
    b.append(f'<rect width="{W}" height="{H}" fill="#1c2f4f"/>')
    for i, (x, y) in enumerate(((150, 10), (390, 14), (300, 70), (40, 72), (230, 8), (360, 50))):
        b.append(f'<rect class="tw{i % 3}" x="{x}" y="{y}" width="2" height="2" fill="#e8c873"/>')
    css.append(".tw0{animation:tw 2s steps(1) infinite}.tw1{animation:tw 2s steps(1) -.7s infinite}.tw2{animation:tw 2s steps(1) -1.3s infinite}@keyframes tw{50%{opacity:.2}}")
    # tarot card flip
    cx, cy, cw, ch = 30, 8, 46, 68
    back = (f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="#24426e" stroke="#e8c873" stroke-width="2"/>'
            f'<rect x="{cx + 6}" y="{cy + 6}" width="{cw - 12}" height="{ch - 12}" fill="none" stroke="#e8c873" stroke-width="1"/>'
            + sprite(["..y..", ".yyy.", "yyyyy", ".yyy.", "..y.."], dict(y="#e8c873"), cx + 13, cy + 24, 4))
    front = (f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="#fff6dc" stroke="#e8c873" stroke-width="2"/>'
             + sprite(SUN, dict(y="#ffc93c", o="#7a4a00", r="#e0603a"), cx + 5, cy + 12, 3)
             + text(cx + cw // 2, cy + 62, "THE SUN", 6, "#7a4a00", "P", "middle"))
    b.append(f'<g class="cb">{back}</g><g class="cf">{front}</g>')
    T = 9
    css.append(f".cb,.cf{{transform-box:fill-box;transform-origin:center}}"
               f".cb{{animation:cb {T}s steps(1) infinite}}@keyframes cb{{0%,10%{{transform:scaleX(1)}}11%{{transform:scaleX(.6)}}12%{{transform:scaleX(.2)}}13%,100%{{transform:scaleX(0)}}}}"
               f".cf{{transform:scaleX(0);animation:cf {T}s steps(1) infinite}}@keyframes cf{{0%,12.9%{{transform:scaleX(0)}}13%{{transform:scaleX(.2)}}14%{{transform:scaleX(.6)}}15%,92%{{transform:scaleX(1)}}93%,100%{{transform:scaleX(0)}}}}")
    # typed reading
    lines = [("당신의 오늘 운세는…", "#c9d6ea", 16, 22),
             ("★★★★☆  재물운 상승!", "#ffd84d", 26, 46),
             ("행운의 색: 보라  ·  행운의 숫자: 7", "#e8c873", 40, 70)]
    for i, (s, col, t0, y) in enumerate(lines):
        clip = f"tp{i}"
        width = 300
        b.append(f'<clipPath id="{clip}"><rect class="ty{i}" x="96" y="{y - 14}" width="{width}" height="18"/></clipPath>')
        b.append(f'<g clip-path="url(#{clip})">{text(100, y, s, 12, col, "GB" if i == 1 else "G")}</g>')
        css.append(f".ty{i}{{transform-box:fill-box;transform-origin:left;animation:ty{i} {T}s steps(20) infinite}}"
                   f"@keyframes ty{i}{{0%,{t0}%{{transform:scaleX(0)}}{t0 + 12}%,92%{{transform:scaleX(1)}}93%,100%{{transform:scaleX(0)}}}}")
    return b, css, W, H


# ---------------------------------------------------------------- 3 두더지
MOLE_TOP = MOLE2[:10]
HAMMER = [
    ".......nn.",
    "......nn..",
    ".....nn...",
    "....nn....",
    "oooooo....",
    "orrrro....",
    "orrrro....",
    "orrrro....",
    "oooooo....",
]


def strip_mole():
    b, css = [], []
    W, H = 420, 84
    b.append(f'<rect width="{W}" height="{H}" fill="#7cc64a"/>')
    for x in range(0, W, 12):
        b.append(f'<rect x="{x + (x // 12 % 3) * 2}" y="{(x * 7) % 70 + 6}" width="2" height="2" fill="#66b33a"/>')
    holes = [40, 110, 180, 250, 320]
    T = 8
    pops = [(0, 0), (1, 2), (2, 4), (3, 1), (4, 3), (5, 0), (6, 4), (7, 2)]   # (second, hole)
    for x in holes:
        b.append(f'<rect x="{x}" y="56" width="56" height="14" fill="#3b2414"/><rect x="{x + 4}" y="58" width="48" height="10" fill="#1a1008"/>')
    for k, (sec, h) in enumerate(pops):
        x = holes[h] + 0
        mole = sprite(MOLE_TOP, dict(o="#3b2414", b="#7a4e33", l="#c89a72", k="#111", w="#fff", n="#ff7fa0", t="#fff", p="#f2b8a0"), x, 22, 4)
        b.append(f'<clipPath id="hc{k}"><rect x="{x - 8}" y="0" width="72" height="62"/></clipPath>')
        b.append(f'<g clip-path="url(#hc{k})"><g class="m{k}">{mole}</g></g>')
        a, c = sec / T * 100, (sec + .9) / T * 100
        css.append(f".m{k}{{transform:translateY(44px);animation:m{k} {T}s steps(1) infinite}}"
                   f"@keyframes m{k}{{0%,{a:.2f}%{{transform:translateY(44px)}}{a + 1.2:.2f}%{{transform:translateY(20px)}}{a + 2.4:.2f}%,{c - 4:.2f}%{{transform:translateY(0)}}{c - 2.5:.2f}%{{transform:translateY(24px)}}{c:.2f}%,100%{{transform:translateY(44px)}}}}")
        # hammer + POW
        hx = holes[h] + 14
        b.append(f'<g class="hm{k}">{sprite(HAMMER, dict(o="#3b1a10", r="#e3242b", n="#c98b4a"), hx, 0, 4)}{text(hx + 44, 16, "POW!", 8, "#fff", "P", "start", "", "stroke=\"#e3242b\" stroke-width=\"3\" paint-order=\"stroke\"")}</g>')
        hs, he = (sec + .45) / T * 100, (sec + .75) / T * 100
        css.append(f".hm{k}{{opacity:0;animation:hm{k} {T}s steps(1) infinite}}@keyframes hm{k}{{0%,{hs:.2f}%{{opacity:0}}{hs + .01:.2f}%,{he:.2f}%{{opacity:1}}{he + .01:.2f}%,100%{{opacity:0}}}}")
    # score
    b.append('<rect x="340" y="4" width="76" height="18" fill="#000" opacity=".55"/>')
    for k in range(len(pops) + 1):
        cls = f"sc{k}"
        b.append(f'<g class="{cls}">{text(410, 17, f"SCORE {k:02d}", 8, "#ffd84d", "P", "end")}</g>')
        t0 = 0 if k == 0 else (pops[k - 1][0] + .5) / T * 100
        t1 = 100 if k == len(pops) else (pops[k][0] + .5) / T * 100
        kf = (f"0%,{t0 - .01:.2f}%{{opacity:0}}" if k else "") + f"{t0:.2f}%,{t1 - .01:.2f}%{{opacity:1}}" + (f"{t1:.2f}%,100%{{opacity:0}}" if t1 < 100 else "")
        css.append(f".{cls}{{opacity:0;animation:{cls} {T}s steps(1) infinite}}@keyframes {cls}{{{kf}}}")
    return b, css, W, H


# ---------------------------------------------------------------- 4 모션 스네이크
P_BASE = [
    "....hhhh....",
    "...hhhhhh...",
    "...hsssss...",
    "...ssksks...",
    "....ssss....",
]
LEGS = [
    "....pppp....",
    "....p..p....",
    "....p..p....",
    "...kk..kk...",
]
POSES = {
    "RIGHT": P_BASE + ["...bbbb.....", "..sbbbbsssss", "..sbbbb.....", "...bbbb....."] + LEGS,
    "UP": ["..s......s..", "..s.hhhh.s..", "..shhhhhhs..", "..shsssssh..", "..ssskskss..", "...bssssb...",
           "....bbbb....", "....bbbb....", "....bbbb...."] + LEGS,
    "LEFT": P_BASE + [".....bbbb...", "ssssbbbbs...", ".....bbbbs..", ".....bbbb..."] + LEGS,
    "DOWN": P_BASE + ["...bbbbbb...", "..sbbbbbbs..", "..sbbbbbbs..", "..s.bbbb.s.."] + LEGS,
}


def strip_snake():
    b, css = [], []
    W, H = 420, 84
    b.append(f'<rect width="{W}" height="{H}" fill="#14181f"/>')
    # webcam frame with player
    b.append('<rect x="8" y="6" width="96" height="72" fill="#2a3240" stroke="#8aa0b8" stroke-width="2"/>')
    b.append('<rect x="14" y="10" width="6" height="6" fill="#ff4d4d" class="rec"/>' + text(24, 16, "CAM", 6, "#ff9f9f", "P"))
    css.append(".rec{animation:rec 1s steps(1) infinite}@keyframes rec{50%{opacity:.2}}")
    T = 12
    order = ["RIGHT", "UP", "LEFT", "DOWN"]
    dur = [4.5, 1.5, 4.5, 1.5]
    pal = dict(h="#2b1d14", s="#f5c9a0", k="#1a1a1a", b="#4cd964", p="#30343f")
    t = 0
    for name, d in zip(order, dur):
        cls = f"ps{name}"
        b.append(f'<g class="{cls}">{sprite(POSES[name], pal, 38, 24, 3)}{text(56, 72, name, 6, "#ffd84d", "P", "middle")}</g>')
        a, c = t / T * 100, (t + d) / T * 100
        kf = (f"0%,{a - .01:.2f}%{{opacity:0}}" if a else "") + f"{a:.2f}%,{c - .01:.2f}%{{opacity:1}}" + (f"{c:.2f}%,100%{{opacity:0}}" if c < 100 else "")
        css.append(f".{cls}{{opacity:0;animation:{cls} {T}s steps(1) infinite}}@keyframes {cls}{{{kf}}}")
        t += d
    b.append(text(116, 46, "▶", 12, "#4cd964", "G"))
    # board
    gx, gy, cs, cols, rows = 134, 8, 8, 34, 9
    b.append(f'<rect x="{gx}" y="{gy}" width="{cols * cs}" height="{rows * cs}" fill="#0b2418"/>')
    for c in range(cols):
        for r in range(rows):
            if (c + r) % 2 == 0:
                b.append(f'<rect x="{gx + c * cs}" y="{gy + r * cs}" width="{cs}" height="{cs}" fill="#0e2c1e"/>')
    # loop path: right 18, up 6, left 18, down 6  (cells)  -> 48 steps over T
    path = []
    x, y = 6, 7
    for dx, dy, n in ((1, 0, 18), (0, -1, 6), (-1, 0, 18), (0, 1, 6)):
        for _ in range(n):
            path.append((x, y))
            x += dx
            y += dy
    N = len(path)
    kf = "".join(f"{i / N * 100:.3f}%{{transform:translate({gx + px * cs}px,{gy + py * cs}px)}}" for i, (px, py) in enumerate(path))
    kf += f"100%{{transform:translate({gx + path[0][0] * cs}px,{gy + path[0][1] * cs}px)}}"
    css.append(f"@keyframes seg{{{kf}}}")
    APPLE = ["....g...", "...g....", ".rrrrrr.", "rrwrrrrr", "rrrrrrrr", "rrrrrrrr", ".rrrrrr.", "..rrrr.."]
    step = T / N
    eat_idx = [10, 21, 34]
    eat_t = [i * step - step / 2 for i in eat_idx]
    for k, (i, te) in enumerate(zip(eat_idx, eat_t)):
        ax, ay = gx + path[i][0] * cs, gy + path[i][1] * cs
        b.append(f'<g class="ap{k}">{sprite(APPLE, dict(r="#ff4d4d", w="#fff", g="#7a4a00"), ax, ay, 1)}</g>')
        prev = eat_t[k - 1] if k else eat_t[-1]
        a_, e_ = te / T * 100, prev / T * 100
        if k == 0:   # visible from last apple eaten (wraps) until eaten
            kf = f"0%,{a_ - .01:.2f}%{{opacity:1}}{a_:.2f}%,{e_ - .01:.2f}%{{opacity:0}}{e_:.2f}%,100%{{opacity:1}}"
        else:
            kf = f"0%,{e_ - .01:.2f}%{{opacity:0}}{e_:.2f}%,{a_ - .01:.2f}%{{opacity:1}}{a_:.2f}%,100%{{opacity:0}}"
        css.append(f".ap{k}{{animation:ap{k} {T}s steps(1) infinite}}@keyframes ap{k}{{{kf}}}")
        stroke = 'stroke="#000" stroke-width="3" paint-order="stroke"'
        b.append(f'<g class="pl{k}">' + text(ax + 4, ay - 2, "+1", 8, "#ffd84d", "P", "middle", "", stroke) + "</g>")
        css.append(f".pl{k}{{opacity:0;animation:pl{k} {T}s steps(6) infinite}}@keyframes pl{k}{{0%,{a_ - .01:.2f}%{{opacity:0;transform:translateY(0)}}{a_:.2f}%{{opacity:1;transform:translateY(0)}}{a_ + 6:.2f}%{{opacity:1;transform:translateY(-8px)}}{a_ + 6.01:.2f}%,100%{{opacity:0}}}}")
    b.append(f'<rect x="{gx + cols * cs - 66}" y="{gy + 2}" width="64" height="12" fill="#000" opacity=".6"/>')
    for k in range(4):
        t0 = 0 if k == 0 else eat_t[k - 1]
        t1 = T if k == 3 else eat_t[k]
        cls = f"cnt{k}"
        b.append(f'<g class="{cls}">{text(gx + cols * cs - 6, gy + 11, f"APPLE {k}", 6, "#ff9f9f", "P", "end")}</g>')
        kf = (f"0%,{t0 / T * 100 - .01:.2f}%{{opacity:0}}" if k else "") + f"{t0 / T * 100:.2f}%,{t1 / T * 100 - .01:.2f}%{{opacity:1}}" + (f"{t1 / T * 100:.2f}%,100%{{opacity:0}}" if k < 3 else "")
        css.append(f".{cls}{{opacity:0;animation:{cls} {T}s steps(1) infinite}}@keyframes {cls}{{{kf}}}")
    L = 7
    for k in range(L):
        col = "#7dff9a" if k == 0 else ("#4cd964" if k % 2 else "#3cb553")
        delay = -((T - k * T / N) % T) - T / N / 2
        b.append(f'<rect class="sg{k}" x="0" y="0" width="{cs}" height="{cs}" fill="{col}"/>')
        css.append(f".sg{k}{{animation:seg {T}s steps(1) {delay:.3f}s infinite}}")
    b.append(f'<rect class="sg0" x="5" y="2" width="2" height="2" fill="#111"/>')
    return b, css, W, H


# ---------------------------------------------------------------- 5 도트 축구
def strip_soccer():
    b, css = [], []
    W, H = 420, 84
    for i, x in enumerate(range(0, W, 21)):
        b.append(f'<rect x="{x}" y="0" width="21" height="{H}" fill="{"#3a9d3a" if i % 2 == 0 else "#348f34"}"/>')
    b.append(f'<rect x="2" y="2" width="{W - 4}" height="{H - 4}" fill="none" stroke="#e8ffe8" stroke-width="2"/>')
    b.append('<rect x="120" y="0" width="2" height="84" fill="#e8ffe8"/>')
    b.append('<rect x="362" y="14" width="56" height="56" fill="none" stroke="#e8ffe8" stroke-width="2"/>')
    b.append('<g class="net"><rect x="410" y="28" width="8" height="28" fill="#fff" opacity=".9"/>' + "".join(f'<rect x="411" y="{y}" width="6" height="1" fill="#9bbf9b"/>' for y in range(30, 55, 3)) + "</g>")
    T = 6
    css.append(f".net{{animation:net {T}s steps(1) infinite}}@keyframes net{{58%,62%,66%{{transform:translateX(2px)}}60%,64%,68%{{transform:translateX(0)}}}}")
    kp = dict(h="#222", s="#f5c9a0", r="#ffd84d", w="#222", k="#111")
    b.append(f'<g class="gk"><g class="dv">{sprite(RUN_A, kp, 0, 0, 2)}</g></g>')
    css.append(f".gk{{animation:gk {T}s steps(12) infinite}}@keyframes gk{{0%{{transform:translate(392px,34px)}}25%{{transform:translate(392px,28px)}}50%{{transform:translate(392px,40px)}}55%{{transform:translate(393px,34px)}}58%,95%{{transform:translate(394px,30px)}}100%{{transform:translate(392px,34px)}}}}")
    css.append(f".dv{{transform-box:fill-box;transform-origin:50% 100%;animation:dv {T}s steps(1) infinite}}@keyframes dv{{0%,50%{{transform:rotate(0)}}53%{{transform:rotate(-12deg)}}56%,95%{{transform:rotate(-24deg) scaleY(1.1)}}96%,100%{{transform:rotate(0)}}}}")
    rp = dict(h="#2b1d14", s="#f5c9a0", r="#e3242b", w="#fff", k="#111")
    b.append(f'<g class="st">{sprite(RUN_A, rp, 0, 0, 2, "ra")}{sprite(RUN_B, rp, 0, 0, 2, "rb")}</g>')
    css.append(f".st{{animation:st {T}s steps(30) infinite}}@keyframes st{{0%{{transform:translate(60px,40px)}}50%,100%{{transform:translate(320px,34px)}}}}")
    css.append(".ra{animation:ra .3s steps(1) infinite}.rb{animation:rb .3s steps(1) infinite}@keyframes ra{50%{opacity:0}}@keyframes rb{0%{opacity:0}50%{opacity:1}}")
    b.append(f'<g class="ball">{sprite(SOCCER, dict(k="#222", w="#fff"), 0, 0, 1)}</g>')
    css.append(f".ball{{animation:ball {T}s steps(40) infinite}}@keyframes ball{{0%{{transform:translate(78px,58px)}}50%{{transform:translate(338px,52px)}}58%,100%{{transform:translate(410px,29px)}}}}")
    b.append(f'<g class="goal">{text(240, 50, "GOAL!!", 16, "#ffd84d", "P", "middle", "", "stroke=\"#7a2a00\" stroke-width=\"4\" paint-order=\"stroke\"")}</g>')
    css.append(f".goal{{opacity:0;animation:goal {T}s steps(1) infinite}}@keyframes goal{{0%,59%{{opacity:0}}60%,70%,80%,90%{{opacity:1}}65%,75%,85%,95%{{opacity:.3}}}}")
    b.append('<rect x="6" y="6" width="86" height="16" fill="#000" opacity=".55"/>' + text(12, 18, "COMING SOON", 6, "#ffd84d", "P"))
    return b, css, W, H


def main():
    parts = {"stage1-airport": strip_airport(), "stage2-unkyeol": strip_fortune(), "stage3-mole": strip_mole(),
             "stage4-snake": strip_snake(), "stage5-soccer": strip_soccer()}
    faces = (font_face("G", FONTS / "Galmuri11.woff2", gen.USED | set(" "))
             + font_face("GB", FONTS / "Galmuri11-Bold.woff2", gen.USED | set(" "))
             + font_face("P", FONTS / "PressStart2P.ttf"))
    for name, (body, css, W, H) in parts.items():
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W * 2}" height="{H * 2}" shape-rendering="crispEdges">'
               f"<style>{faces}text{{text-rendering:optimizeSpeed}}{''.join(css)}</style>{''.join(body)}</svg>")
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
        print(name, len(svg) // 1024, "KB")


if __name__ == "__main__":
    main()
