"""Generate 3 animated pixel-art header SVGs for the GitHub profile concepts."""
import base64, io, random, sys
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

HERE = Path(__file__).parent
FONTS = HERE / "fonts"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE

USED = set()


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=12, fill="#fff", font="G", anchor="start", cls="", extra=""):
    if font in ("G", "GB"):
        USED.update(s)
    c = f' class="{cls}"' if cls else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{c} {extra}>{esc(s)}</text>')


def sprite(grid, pal, x, y, s=1, cls=""):
    """Pixel grid -> rects, merging horizontal runs."""
    out = []
    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == "." or ch == " ":
                c += 1
                continue
            start = c
            while c < len(row) and row[c] == ch:
                c += 1
            out.append(f'<rect x="{x + start * s}" y="{y + r * s}" width="{(c - start) * s}" height="{s}" fill="{pal[ch]}"/>')
    body = "".join(out)
    return f'<g class="{cls}">{body}</g>' if cls else f"<g>{body}</g>"


def font_face(name, path, chars=None):
    f = TTFont(path)
    if chars is not None:
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = []
        sub = subset.Subsetter(opts)
        sub.populate(text="".join(sorted(chars)))
        sub.subset(f)
    f.flavor = "woff2"
    buf = io.BytesIO()
    f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:{name};src:url(data:font/woff2;base64,{b64}) format('woff2');}}"


def wrap(body, css, w=420, h=180):
    return body, css, w, h


# ---------------------------------------------------------------- sprites
DEV = [
    "...hhhhh....",
    "..hhhhhhh...",
    "..hhhhhhhh..",
    "..sshhhhhh..",
    "..kshhhhh...",
    "..sssshhh...",
    "...ssss.....",
    "..bbbbbbb...",
    ".abbbbbbbb..",
    "aabbbbbbbb..",
    "..bbbbbbbb..",
    "..pppppppp..",
    "..pppppppppp",
    "..pp.....pp.",
    "..pp.....pp.",
    "..kk.....kk.",
]
DEV_B = DEV[:7] + [
    "..bbbbbbb...",
    "aabbbbbbbb..",
    ".abbbbbbbb..",
    "..bbbbbbbb..",
] + DEV[11:]
DEV_PAL = dict(h="#2b1d14", s="#f5c9a0", k="#1a1a1a", b="#3b82c4", a="#f5c9a0", p="#30343f")

CAT_A = [
    ".......k.k",
    ".......kkk",
    "k......kwk",
    ".k.kkkkkkk",
    "..kkkkkkk.",
    "..k.k.k.k.",
]
CAT_B = CAT_A[:5] + [".k.k...k.k"]
CAT_PAL = dict(k="#3a3a3a", w="#ffe066")

PLANE = [
    "......w......",
    ".....www.....",
    ".....www.....",
    "..wwwwwwwww..",
    "wwwwwwwwwwwww",
    "......w......",
    ".....www.....",
    "....wwwww....",
]
BALLC = [
    "...pppp...",
    ".ppwwpppp.",
    ".pwwppppp.",
    "pppppppppp",
    "pppppppppp",
    ".pppppppp.",
    "..pppppp..",
    "...gggg...",
    "..gggggg..",
    ".gggggggg.",
]
MOLE = [
    "...bbbb...",
    "..bbbbbb..",
    ".bkbbbbkb.",
    ".bbbppbbb.",
    ".bbbbbbbb.",
    "dddddddddd",
    "dddddddddd",
]
SNAKE = [
    "......ggg.",
    ".....gkggr",
    "gg...ggg..",
    "ggg.ggg...",
    ".ggggg....",
    "..ggg.....",
]
SOCCER = [
    "..kkkk..",
    ".kwwwwk.",
    "kwwkkwwk",
    "kwkkkkwk",
    "kwwkkwwk",
    "kwwwwwwk",
    ".kwwwwk.",
    "..kkkk..",
]
FACE = [
    "...hhhhhh...",
    "..hhhhhhhh..",
    ".hhhhhhhhhh.",
    ".hhsssssshh.",
    ".hssssssssh.",
    ".ssksssskss.",
    ".ssssssssss.",
    "..sssrrsss..",
    "...ssssss...",
    "....ssss....",
    "..bbbbbbbb..",
    ".bbbbbbbbbb.",
]
RUN_A = [
    "..hhhh..",
    ".hhhhhh.",
    ".hsssss.",
    "..ssss..",
    ".rrrrrr.",
    "srrrrrrs",
    "s.rrrr.s",
    "..wwww..",
    "..w..w..",
    "..s..s..",
    "..s..s..",
    ".kk..kk.",
]
RUN_B = RUN_A[:8] + [
    ".ww..ww.",
    ".s....s.",
    "s......s",
    "k......k",
]
COIN = [
    ".yyyy.",
    "yyooyy",
    "yoyyoy",
    "yoyyoy",
    "yyooyy",
    ".yyyy.",
]


# ---------------------------------------------------------------- A: game dev story
def concept_a():
    b, css = [], []
    W = 420
    # wall / floor
    b.append('<rect width="420" height="180" fill="#f2dfb4"/>')
    b.append('<rect y="100" width="420" height="10" fill="#d9b98a"/>')
    b.append('<rect y="110" width="420" height="32" fill="#a8703f"/>')
    for i, y in enumerate((118, 126, 134)):
        b.append(f'<rect y="{y}" width="420" height="1" fill="#93602f"/>')
        off = 0 if i % 2 == 0 else 20
        for x in range(off, 420, 40):
            b.append(f'<rect x="{x}" y="{y - 8}" width="1" height="8" fill="#93602f"/>')
    # window with drifting clouds
    b.append('<clipPath id="win"><rect x="33" y="33" width="74" height="44"/></clipPath>')
    b.append('<rect x="30" y="30" width="80" height="50" fill="#8a5a2b"/>')
    b.append('<rect x="33" y="33" width="74" height="44" fill="#7ec8f2"/>')
    cloud = '<rect x="0" y="4" width="18" height="5" fill="#fff"/><rect x="4" y="0" width="10" height="5" fill="#fff"/>'
    b.append(f'<g clip-path="url(#win)"><g class="clouds"><g transform="translate(10,40)">{cloud}</g><g transform="translate(60,52)">{cloud}</g><g transform="translate(110,44)">{cloud}</g></g>'
             + f'<g class="jet">{sprite(PLANE, dict(w="#ffffff"), 0, 0, 1)}</g></g>')
    b.append('<rect x="69" y="33" width="2" height="44" fill="#8a5a2b"/><rect x="33" y="54" width="74" height="2" fill="#8a5a2b"/>')
    css.append(".clouds{animation:drift 24s linear infinite}@keyframes drift{from{transform:translateX(0)}to{transform:translateX(-100px)}}")
    css.append(".jet{animation:jet 10s steps(40) infinite}@keyframes jet{0%{transform:translate(110px,70px) rotate(0)}100%{transform:translate(-20px,30px)}}")
    # poster
    b.append('<rect x="286" y="32" width="46" height="38" fill="#c0392b"/><rect x="289" y="35" width="40" height="32" fill="#fff8e7"/>')
    b.append(sprite(PLANE, dict(w="#2e86de"), 302, 40, 1))
    b.append(text(309, 63, "AIRPORT", 5, "#c0392b", "P", "middle"))
    # bookshelf with game boxes
    b.append('<rect x="352" y="36" width="54" height="74" fill="#7a4a22"/>')
    for sy in (58, 82, 106):
        b.append(f'<rect x="352" y="{sy}" width="54" height="4" fill="#5c3517"/>')
    random.seed(7)
    for sy in (40, 64, 88):
        x = 356
        while x < 400:
            w = random.choice((5, 6, 7))
            hgt = random.choice((14, 16, 18))
            col = random.choice(("#e74c3c", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6", "#e67e22"))
            b.append(f'<rect x="{x}" y="{sy + 18 - hgt}" width="{w}" height="{hgt}" fill="{col}"/>')
            x += w + 1
    # plant
    b.append('<rect x="126" y="96" width="10" height="14" fill="#c0692b"/>')
    b.append(sprite(["..g.g..", ".gggggg", "ggg.ggg", ".ggggg.", "..ggg.."], dict(g="#3fa34d"), 124, 82, 2))
    # desk
    b.append('<rect x="150" y="92" width="96" height="6" fill="#8b5a2b"/><rect x="154" y="98" width="4" height="22" fill="#6b4220"/><rect x="238" y="98" width="4" height="22" fill="#6b4220"/>')
    # monitor
    b.append('<rect x="182" y="86" width="10" height="6" fill="#444"/><rect x="176" y="90" width="22" height="2" fill="#444"/>')
    b.append('<rect x="160" y="54" width="54" height="34" fill="#2b2b2b"/><rect x="163" y="57" width="48" height="27" fill="#10243a"/>')
    cols = ("#7ee787", "#79c0ff", "#ffa657", "#d2a8ff", "#7ee787", "#79c0ff")
    widths = (22, 34, 18, 28, 38, 14)
    for i, (c, w) in enumerate(zip(cols, widths)):
        ind = (i % 3) * 4
        b.append(f'<rect class="ln{i}" x="{166 + ind}" y="{60 + i * 4}" width="{w}" height="2" fill="{c}"/>')
        s = 4 + i * 9
        css.append(f".ln{i}{{animation:ln{i} 10s steps(1) infinite}}@keyframes ln{i}{{0%,{s}%{{opacity:0}}{s + 1}%,95%{{opacity:1}}96%,100%{{opacity:0}}}}")
    b.append('<rect class="cur" x="166" y="84" width="4" height="2" fill="#fff"/>')
    css.append(".cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}")
    b.append('<rect x="162" y="89" width="30" height="3" fill="#dcdcdc"/>')
    # mug + steam
    b.append('<rect x="200" y="84" width="7" height="8" fill="#fff"/><rect x="207" y="86" width="2" height="4" fill="#fff"/>')
    b.append('<g class="steam"><rect x="202" y="78" width="1" height="2" fill="#bbb"/><rect x="204" y="74" width="1" height="2" fill="#bbb"/></g>')
    css.append(".steam{animation:steam 2s steps(4) infinite}@keyframes steam{from{transform:translateY(0);opacity:1}to{transform:translateY(-6px);opacity:0}}")
    # chair + dev typing
    b.append('<rect x="244" y="70" width="6" height="40" fill="#c0392b"/><rect x="220" y="102" width="30" height="4" fill="#c0392b"/><rect x="232" y="106" width="3" height="14" fill="#333"/><rect x="224" y="118" width="20" height="2" fill="#333"/>')
    b.append(sprite(DEV, DEV_PAL, 218, 72, 2, "fa"))
    b.append(sprite(DEV_B, DEV_PAL, 218, 72, 2, "fb"))
    css.append(".fa{animation:fa .5s steps(1) infinite}.fb{animation:fb .5s steps(1) infinite}@keyframes fa{50%{opacity:0}}@keyframes fb{0%{opacity:0}50%{opacity:1}}")
    # walking cat
    b.append(f'<g class="cat">{sprite(CAT_A, CAT_PAL, 0, 0, 2, "fa")}{sprite(CAT_B, CAT_PAL, 0, 0, 2, "fb")}</g>')
    css.append(".cat{animation:cat 16s linear infinite}@keyframes cat{from{transform:translate(-30px,124px)}to{transform:translate(440px,124px)}}")
    # floating stat pops (the Kairosoft signature)
    pops = [("재미 +12", 0), ("그래픽 +8", 22), ("기획 +15", 44), ("사운드 +6", 62)]
    for i, (s, start) in enumerate(pops):
        b.append(text(188, 50, s, 12, "#ff7a00", "GB", "middle", f"pop{i}",
                      'stroke="#fff" stroke-width="3" paint-order="stroke" stroke-linejoin="round"'))
        e = start + 14
        css.append(f".pop{i}{{opacity:0;animation:pop{i} 10s steps(14) infinite}}@keyframes pop{i}{{0%,{start}%{{opacity:0;transform:translateY(6px)}}{start + 1}%{{opacity:1;transform:translateY(6px)}}{e}%{{opacity:1;transform:translateY(-10px)}}{e + 1}%,100%{{opacity:0}}}}")
    # top bar
    b.append('<rect width="420" height="18" fill="#233a66"/><rect y="18" width="420" height="2" fill="#0f1d38"/>')
    b.append(text(6, 13, "채웅 게임즈", 12, "#fff", "GB"))
    b.append(text(210, 13, "자금 1,500만", 12, "#ffd84d", "G", "middle"))
    b.append(text(414, 13, "2026년 10월 3주", 12, "#fff", "G", "end"))
    # bottom panel
    b.append('<rect y="142" width="420" height="38" fill="#233a66"/><rect x="3" y="145" width="414" height="32" fill="none" stroke="#fff" stroke-width="2"/>')
    b.append('<g class="dev">' + text(12, 160, "개발 중", 12, "#9fd0ff", "GB")
             + text(62, 160, "「도트 축구 매니저」(가제)", 12, "#fff", "G")
             + '<rect x="12" y="165" width="230" height="7" fill="#0f1d38"/><rect class="bar" x="12" y="165" width="230" height="7" fill="#ffd84d"/>'
             + text(408, 172, "기획 → 개발 → 출시", 12, "#9fd0ff", "G", "end") + "</g>")
    b.append('<g class="rel">' + text(210, 166, "★ 신작 출시! 대히트 예감 ★", 12, "#ffd84d", "GB", "middle") + "</g>")
    css.append(".bar{transform-box:fill-box;transform-origin:left;animation:bar 10s steps(12) infinite}@keyframes bar{0%{transform:scaleX(0)}70%,100%{transform:scaleX(1)}}")
    css.append(".dev{animation:dev 10s steps(1) infinite}@keyframes dev{72%,100%{opacity:0}}")
    css.append(".rel{opacity:0;animation:rel 10s steps(1) infinite}@keyframes rel{0%,71%{opacity:0}72%,76%,80%,84%,88%,92%,96%{opacity:1}74%,78%,82%,86%,90%,94%,98%{opacity:.25}}")
    return b, css


MOLE2 = [
    "....oooooo....",
    "...obbbbbbo...",
    "..obbbbbbbbo..",
    "..obkwbbkwbo..",
    "..obkkbbkkbo..",
    ".obbbbnnbbbbo.",
    ".obllbnnbllbo.",
    ".oblllttlllbo.",
    "ppobllllllbopp",
    "ppobllllllbopp",
    "dddddddddddddd",
    "dhhhhhhhhhhhhd",
    ".dddddddddddd.",
]
BALL2 = [
    "....oooo....",
    "..oowwwwoo..",
    ".owwwwwwwwo.",
    ".owwwkkwwwo.",
    "owwwkkkkwwwo",
    "okwwkkkkwwko",
    "okkwwkkwwkko",
    "owwwwwwwwwgo",
    ".owkwwwwkgo.",
    ".owkkwwkkgo.",
    "..oowwggoo..",
    "....oooo....",
]

BALL3 = [
    "........oooooo........",
    "......ooooowwwoo......",
    "....ooooooowwwwwoo....",
    "...oowooooowwwwwwoo...",
    "..oowwowwwwowwwoowoo..",
    "..owwwowwwwowwoooowo..",
    ".owwwwowwwwwooooooowo.",
    ".owwwowwwwwwwoooooowo.",
    "oswwwowwwwwwowooooowwo",
    "osswoowwwwwowwwowwwowo",
    "ossoooowwoowwwwowwwooo",
    "osooooooowwwwwowwwwooo",
    "osoooooowwwwwwowwwoooo",
    "ossooooowwwwwwowwwoooo",
    ".ososwwwowwwwoowwwwoo.",
    ".ososwwwwowwoooowwowo.",
    "..ossswwwwoooooooowo..",
    "..oosssswwwoooooowoo..",
    "...oosssssssoooowoo...",
    "....oosssssssossoo....",
    "......oossssosoo......",
    "........oooooo........",
]

# ---------------------------------------------------------------- B: arcade
def concept_b():
    b, css = [], []
    b.append('<rect width="420" height="180" fill="#0d0a1f"/>')
    random.seed(3)
    for i in range(40):
        x, y = random.randrange(420), random.randrange(180)
        if 60 < x < 360 and 4 < y < 158:
            continue
        d = random.choice((0, 1, 2, 3))
        b.append(f'<rect class="tw{d}" x="{x}" y="{y}" width="1" height="1" fill="#fff"/>')
    for d in range(4):
        css.append(f".tw{d}{{animation:tw 3s steps(1) {-d * 0.75}s infinite}}")
    css.append("@keyframes tw{0%,40%{opacity:1}41%,100%{opacity:.2}}")
    # cabinet sides
    b.append('<rect x="56" y="4" width="308" height="176" fill="#1d1640"/><rect x="60" y="4" width="300" height="176" fill="#251b52"/>')
    # marquee
    b.append('<defs><filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
             '<pattern id="scan" width="4" height="2" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000"/></pattern></defs>')
    b.append('<rect x="70" y="10" width="280" height="32" fill="#12082b" stroke="#ff3fa4" stroke-width="2"/>')
    b.append(f'<g class="neon" filter="url(#glow)">{text(210, 33, "CHAE ARCADE", 16, "#ffd6f0", "P", "middle", "", "")}</g>')
    css.append(".neon{animation:neon 5s steps(1) infinite}@keyframes neon{0%,62%,66%,70%,100%{opacity:1}63%,68%{opacity:.25}}")
    # timeline: 0-2.2s coin spins, 2.2-2.5 drops in, 2.5-4 PRESS START, 4-14 game select
    T = 14
    pc = lambda t: round(t / T * 100, 2)
    def show(cls, t0, t1):
        """visible only between t0 and t1 seconds of the loop"""
        kf = (f"0%,{pc(t0) - .01}%{{opacity:0}}" if t0 > 0 else "") + f"{pc(t0)}%,{pc(t1) - .01}%{{opacity:1}}" + (f"{pc(t1)}%,100%{{opacity:0}}" if t1 < T else "")
        css.append(f".{cls}{{opacity:0;animation:{cls} {T}s steps(1) infinite}}@keyframes {cls}{{{kf}}}")
    css.append("@keyframes blink{50%{opacity:0}}.blk{animation:blink 1s steps(1) infinite}.blk2{animation:blink .5s steps(1) infinite}")
    # screen
    b.append('<rect x="74" y="50" width="272" height="104" rx="8" fill="#333"/><rect x="80" y="54" width="260" height="96" rx="6" fill="#06140d"/>')
    # attract mode
    b.append(f'<g class="att1">{text(210, 110, "INSERT COIN", 16, "#ffd166", "P", "middle", "blk")}{text(210, 130, "1 COIN  1 PLAY", 8, "#6dff9a", "P", "middle")}</g>')
    show("att1", 0, 2.5)

    b.append(f'<g class="att2">{text(210, 96, "PRESS START", 16, "#6dff9a", "P", "middle", "blk2")}{text(210, 120, "PLAYER 1  READY", 8, "#ffd166", "P", "middle")}</g>')
    show("att2", 2.5, 4)
    # game select
    m = []
    m.append(text(92, 70, "SELECT GAME", 8, "#ffd166", "P"))
    items = ["신입사원 공항 키우기", "운결 · 운세 사이트", "두더지 잡기", "모션 스네이크", "??? 축구 게임"]
    for i, s_ in enumerate(items):
        m.append(text(104, 86 + i * 13, s_, 12, "#6dff9a" if i < 4 else "#5a7d68", "G"))
    m.append(text(196, 138, "SOON", 8, "#ff5c8a", "P", "start", "blk"))
    m.append('<g class="sel"><rect x="90" y="76" width="152" height="13" fill="#6dff9a" opacity=".15"/>' + text(92, 86, "▶", 12, "#ffd166", "G") + "</g>")
    kf = "".join(f"{pc(4 + i * 2)}%,{pc(6 + i * 2) - .01}%{{transform:translateY({i * 13}px)}}" for i in range(5))
    css.append(f".sel{{animation:sel {T}s steps(1) infinite}}@keyframes sel{{0%,{pc(4) - .01}%{{transform:translateY(0)}}{kf}}}")
    m.append('<rect x="252" y="74" width="80" height="66" fill="#0b2418" stroke="#6dff9a" stroke-width="1"/>')
    previews = [
        sprite(PLANE, dict(w="#e8f4ff"), 266, 86, 4),
        sprite(BALLC, dict(p="#9b59ff", w="#fff", g="#c99a2e"), 272, 87, 4),
        sprite(MOLE2, dict(o="#3b2414", b="#7a4e33", l="#c89a72", k="#111", w="#fff", n="#ff7fa0", t="#fff", p="#f2b8a0", d="#6b4a2a", h="#1a1008"), 264, 81, 4),
        sprite(SNAKE, dict(g="#4cd964", k="#111", r="#ff4d4d"), 272, 94, 4),
        sprite(BALL3, dict(o="#11163a", w="#eef4fc", s="#b9d2ee"), 270, 85, 2),
    ]
    for i, pv in enumerate(previews):
        m.append(f'<g class="pv{i}">{pv}</g>')
        show(f"pv{i}", 4 + i * 2, 6 + i * 2)
    b.append('<g class="menu">' + "".join(m) + "</g>")
    show("menu", 4, T)
    b.append('<rect x="80" y="54" width="260" height="96" rx="6" fill="url(#scan)" opacity=".35"/>')
    # control panel: credit, coin slot, 1P
    b.append(f'<g class="cr0">{text(80, 170, "CREDIT 03", 8, "#9a8cff", "P")}</g>')
    show("cr0", 0, 2.5)
    b.append(f'<g class="cr1">{text(80, 170, "CREDIT 04", 8, "#ffd166", "P")}</g>')
    show("cr1", 2.5, T)
    b.append(f'<g class="cn6">{text(340, 170, "6 COIN", 8, "#ffd166", "P", "end")}</g>')
    show("cn6", 0, 2.5)
    b.append(f'<g class="cn5">{text(340, 170, "5 COIN", 8, "#9a8cff", "P", "end")}</g>')
    show("cn5", 2.5, T)
    b.append('<rect x="196" y="160" width="28" height="16" fill="#1a1238" stroke="#9a8cff" stroke-width="1"/>')
    b.append('<clipPath id="scrclip"><rect x="80" y="54" width="260" height="96" rx="6"/></clipPath>')
    b.append('<g clip-path="url(#scrclip)" class="att1"><g class="drop"><g class="spin">' + sprite(COIN, dict(y="#ffd166", o="#c98b00"), 198, 62, 4) + "</g></g></g>")
    b.append('<rect x="203" y="166" width="14" height="3" fill="#0d0a1f"/>')
    b.append('<rect class="flash" x="203" y="166" width="14" height="3" fill="#ffd166"/>')
    show("flash", 2.5, 3.2)
    css.append(".spin{transform-box:fill-box;transform-origin:center;animation:spin 1s steps(4) infinite}@keyframes spin{50%{transform:scaleX(.15)}}")
    css.append(f".drop{{animation:drop {T}s steps(1) infinite}}@keyframes drop{{0%,{pc(2.2)}%{{transform:translateY(0)}}{pc(2.3)}%{{transform:translateY(30px)}}{pc(2.4)}%{{transform:translateY(60px)}}{pc(2.5)}%,100%{{transform:translateY(100px)}}}}")
    return b, css


# ---------------------------------------------------------------- C: FIFA card + pitch
def concept_c():
    b, css = [], []
    b.append('<rect width="420" height="180" fill="#0f1724"/>')
    # pitch
    px, py, pw, ph = 146, 12, 266, 158
    for i, x in enumerate(range(px, px + pw, 19)):
        b.append(f'<rect x="{x}" y="{py}" width="{min(19, px + pw - x)}" height="{ph}" fill="{"#3a9d3a" if i % 2 == 0 else "#348f34"}"/>')
    b.append(f'<rect x="{px + 2}" y="{py + 2}" width="{pw - 4}" height="{ph - 4}" fill="none" stroke="#e8ffe8" stroke-width="2"/>')
    b.append(f'<rect x="{px + pw - 54}" y="52" width="52" height="78" fill="none" stroke="#e8ffe8" stroke-width="2"/>')
    b.append(f'<rect x="{px + pw - 22}" y="72" width="20" height="38" fill="none" stroke="#e8ffe8" stroke-width="2"/>')
    b.append(f'<rect x="{px + 60}" y="{py}" width="2" height="{ph}" fill="#e8ffe8"/>')
    # goal + net
    b.append('<g class="net"><rect x="408" y="74" width="8" height="34" fill="#fff" opacity=".9"/>'
             + "".join(f'<rect x="409" y="{y}" width="6" height="1" fill="#9bbf9b"/>' for y in range(76, 107, 3)) + "</g>")
    css.append(".net{animation:net 6s steps(1) infinite}@keyframes net{58%,62%,66%{transform:translateX(2px)}60%,64%,68%{transform:translateX(0)}}")
    # label
    b.append('<rect x="152" y="18" width="128" height="16" fill="#000" opacity=".55"/>')
    b.append(text(158, 30, "NEXT ▶ 도트 축구 매니저", 12, "#ffd84d", "G"))
    # keeper
    keeper_pal = dict(h="#222", s="#f5c9a0", r="#ffd84d", w="#222", k="#111")
    b.append(f'<g class="gk">{sprite(RUN_A, keeper_pal, 0, 0, 2)}</g>')
    css.append(".gk{animation:gk 6s steps(6) infinite}@keyframes gk{0%{transform:translate(384px,80px)}25%{transform:translate(384px,70px)}50%{transform:translate(384px,90px)}58%,100%{transform:translate(384px,112px)}}")
    # striker
    run_pal = dict(h="#2b1d14", s="#f5c9a0", r="#e3242b", w="#fff", k="#111")
    b.append(f'<g class="st">{sprite(RUN_A, run_pal, 0, 0, 2, "ra")}{sprite(RUN_B, run_pal, 0, 0, 2, "rb")}</g>')
    css.append(".st{animation:st 6s steps(30) infinite}@keyframes st{0%{transform:translate(166px,104px)}50%,100%{transform:translate(318px,96px)}}")
    css.append(".ra{animation:ra .3s steps(1) infinite}.rb{animation:rb .3s steps(1) infinite}@keyframes ra{50%{opacity:0}}@keyframes rb{0%{opacity:0}50%{opacity:1}}")
    # ball
    b.append(f'<g class="ball">{sprite(SOCCER, dict(k="#222", w="#fff"), 0, 0, 1)}</g>')
    css.append(".ball{animation:ball 6s steps(40) infinite}@keyframes ball{0%{transform:translate(184px,122px)}50%{transform:translate(336px,114px)}58%,100%{transform:translate(404px,86px)}}")
    # GOAL text
    b.append(f'<g class="goal">{text(274, 150, "GOAL!!", 18, "#ffd84d", "P", "middle", "", "stroke=\"#7a2a00\" stroke-width=\"4\" paint-order=\"stroke\"")}</g>')
    css.append(".goal{opacity:0;animation:goal 6s steps(1) infinite}@keyframes goal{0%,59%{opacity:0}60%,70%,80%,90%{opacity:1}65%,75%,85%,95%{opacity:.3}}")
    # player card
    b.append('<defs><linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff3a8"/><stop offset=".5" stop-color="#e9c75a"/><stop offset="1" stop-color="#b8862a"/></linearGradient>'
             '<clipPath id="card"><polygon points="24,22 44,12 104,12 124,22 124,160 74,172 24,160"/></clipPath></defs>')
    b.append('<polygon points="24,22 44,12 104,12 124,22 124,160 74,172 24,160" fill="url(#gold)"/>')
    b.append('<polygon points="28,24 46,15 102,15 120,24 120,157 74,168 28,157" fill="none" stroke="#8a6416" stroke-width="1"/>')
    b.append(text(34, 46, "77", 18, "#3b2a07", "P"))
    b.append(text(36, 60, "DEV", 12, "#3b2a07", "GB"))
    b.append(text(36, 74, "KOR", 12, "#3b2a07", "G"))
    b.append(sprite(FACE, dict(h="#2b1d14", s="#f5c9a0", k="#1a1a1a", r="#c0392b", b="#e3242b"), 66, 30, 4))
    b.append('<rect x="34" y="80" width="80" height="1" fill="#8a6416"/>')
    b.append(text(74, 96, "CHAE", 10, "#3b2a07", "P", "middle"))
    b.append('<rect x="34" y="102" width="80" height="1" fill="#8a6416"/>')
    stats = [("88", "경영"), ("90", "집념"), ("84", "기획"), ("86", "감성"), ("71", "도트"), ("69", "코딩")]
    for i, (v, k) in enumerate(stats):
        cx = 32 if i % 2 == 0 else 77
        cy = 117 + (i // 2) * 14
        b.append(text(cx, cy, v, 12, "#3b2a07", "GB") + text(cx + 18, cy, k, 12, "#3b2a07", "G"))
    b.append('<g clip-path="url(#card)"><rect class="shine" x="0" y="0" width="16" height="200" fill="#fff" opacity=".45" transform="skewX(-20)"/></g>')
    css.append(".shine{animation:shine 4s steps(20) infinite}@keyframes shine{0%{transform:translateX(-40px) skewX(-20deg)}40%,100%{transform:translateX(190px) skewX(-20deg)}}")
    return b, css


PY_ICON = [
    "...bbbbb....",
    "..bwbbbbb...",
    "..bbbbbbb...",
    "......bbb...",
    "bbbbbbbbb.y.",
    "bbbbbbbbb.yy",
    "bb.yyyyyyyyy",
    "b..yyyyyyyyy",
    "...yyy......",
    "...yyyyyyy..",
    "...yyyyywy..",
    "....yyyyy...",
]
WIN_ICON = ["rrrrr.ggggg"] * 5 + ["..........."] + ["bbbbb.yyyyy"] * 5
GIT_ICON = []
for r in range(11):
    row = ""
    for c in range(11):
        row += "o" if abs(r - 5) + abs(c - 5) <= 5 else "."
    GIT_ICON.append(row)
for (r, c) in [(3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (4, 5), (5, 6), (6, 6), (3, 3), (7, 3), (7, 5)]:
    GIT_ICON[r] = GIT_ICON[r][:c] + "w" + GIT_ICON[r][c + 1:]


FACE_M = [
    "..hhhhhhhh..",
    ".hhhhhhhhhh.",
    ".hhhhhhhhhh.",
    ".hssssssssh.",
    ".shhsssshhs.",
    ".ssksssskss.",
    ".ssssssssss.",
    "..sssmmsss..",
    "...ssssss...",
    "....ssss....",
    "..bbbbbbbb..",
    ".bbbbbbbbbb.",
]
HEART = [".rr.rr.", "rrrrrrr", "rrrrrrr", ".rrrrr.", "..rrr..", "...r..."]


def concept_player():
    b, css = [], []
    b.append('<rect width="420" height="140" fill="#0d0a1f"/>')
    b.append('<rect x="4" y="4" width="412" height="132" fill="#251b52"/><rect x="7" y="7" width="406" height="126" fill="#12082b" stroke="#6dff9a" stroke-width="1"/>')
    b.append(text(16, 22, "PLAYER STATUS", 8, "#ffd166", "P"))
    b.append(text(404, 22, "1P", 8, "#9a8cff", "P", "end"))
    b.append('<rect x="14" y="28" width="392" height="1" fill="#3a2d78"/>')
    # avatar
    b.append('<rect x="16" y="36" width="60" height="60" fill="#0b2418" stroke="#6dff9a" stroke-width="1"/>')
    b.append(f'<g class="bob">{sprite(FACE_M, dict(h="#1f1a17", s="#f5c9a0", k="#1a1a1a", m="#8a4b3a", b="#3b82c4"), 22, 42, 4)}</g>')
    css.append(".bob{animation:bob 1.2s steps(1) infinite}@keyframes bob{50%{transform:translateY(1px)}}")
    b.append(text(46, 110, "CHAE", 8, "#fff", "P", "middle"))
    for i in range(3):
        b.append(sprite(HEART, dict(r="#ff3f6c" if i < 2 else "#3a2d78"), 22 + i * 17, 118, 2))
    # level / exp
    b.append(text(92, 48, "LV.3", 10, "#fff", "P"))
    b.append(text(140, 48, "견습 게임 개발자", 12, "#6dff9a", "GB"))
    b.append(text(92, 66, "EXP", 8, "#ffd166", "P"))
    b.append('<rect x="120" y="58" width="160" height="9" fill="#0b2418" stroke="#6dff9a" stroke-width="1"/>')
    b.append('<rect class="exp" x="121" y="59" width="99" height="7" fill="#6dff9a"/>')
    b.append(text(286, 66, "62%", 8, "#fff", "P"))
    css.append(".exp{transform-box:fill-box;transform-origin:left;animation:exp 6s steps(10) infinite}@keyframes exp{0%{transform:scaleX(0)}60%,100%{transform:scaleX(1)}}")
    b.append(text(92, 86, "NEXT LV ▶ 「도트 축구」 출시", 12, "#c8bfff", "G"))
    b.append(text(92, 106, "패시브", 12, "#ff5c8a", "GB"))
    b.append(text(136, 106, "경영학 — 타이쿤 밸런스 감각 +20", 12, "#fff", "G"))
    b.append(text(92, 126, "클리어 4 · 개발 중 1 · ??? 1", 12, "#9a8cff", "G"))
    # skill slots
    b.append(text(318, 48, "SKILL", 8, "#ffd166", "P"))
    icons = [(PY_ICON, dict(b="#3b7bd8", y="#ffd43b", w="#fff"), "PY"),
             (WIN_ICON, dict(r="#f25022", g="#7fba00", b="#00a4ef", y="#ffb900"), "WIN"),
             (GIT_ICON, dict(o="#f05032", w="#fff"), "GIT")]
    for i, (ic, pal, lab) in enumerate(icons):
        x = 318 + i * 30
        b.append(f'<rect x="{x}" y="56" width="26" height="26" fill="#0b2418" stroke="#3a2d78" stroke-width="1"/>')
        n = len(ic[0])
        b.append(sprite(ic, pal, x + (26 - n * 2) // 2, 56 + (26 - len(ic) * 2) // 2, 2))
        b.append(text(x + 13, 94, lab, 6, "#c8bfff", "P", "middle"))
    b.append('<rect class="slot" x="317" y="55" width="28" height="28" fill="none" stroke="#ffd166" stroke-width="2"/>')
    css.append(".slot{animation:slot 4.5s steps(1) infinite}@keyframes slot{0%{transform:translateX(0)}33.3%{transform:translateX(30px)}66.6%{transform:translateX(60px)}}")
    b.append(text(362, 112, "MAIN", 6, "#6dff9a", "P", "middle"))
    b.append(text(362, 124, "PYTHON", 8, "#fff", "P", "middle"))
    return b, css


def build():
    parts = {"a-gamedev": concept_a(), "b-arcade": concept_b(), "c-card": concept_c(), "player": concept_player()}
    faces = (font_face("G", FONTS / "Galmuri11.woff2", USED | set(" "))
             + font_face("GB", FONTS / "Galmuri11-Bold.woff2", USED | set(" "))
             + font_face("P", FONTS / "PressStart2P.ttf"))
    for name, (body, css) in parts.items():
        hgt = 140 if name == "player" else 180
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 {hgt}" width="840" height="{hgt * 2}" shape-rendering="crispEdges">'
               f"<style>{faces}text{{text-rendering:optimizeSpeed}}{''.join(css)}</style>{''.join(body)}</svg>")
        p = OUT / f"{name}.svg"
        p.write_text(svg, encoding="utf-8")
        print(p.name, len(svg) // 1024, "KB")


if __name__ == "__main__":
    build()
