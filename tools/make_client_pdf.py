"""Builds the client direction PDF for Scene 9.

Needs reportlab (pip install reportlab). Usage:
    python tools/make_client_pdf.py docs/SOTR-Scene9-Projection-Direction.pdf
The PDF itself is gitignored, so rebuild it on each machine or copy it across.
"""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Flowable, KeepTogether, PageBreak)

import os
OUT = sys.argv[1] if len(sys.argv) > 1 else "SOTR-Scene9-Projection-Direction.pdf"
# Georgia: macOS names first, then Windows names.
_FONTS = {
    "G": ["/System/Library/Fonts/Supplemental/Georgia.ttf", "C:/Windows/Fonts/georgia.ttf"],
    "G-B": ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf", "C:/Windows/Fonts/georgiab.ttf"],
    "G-I": ["/System/Library/Fonts/Supplemental/Georgia Italic.ttf", "C:/Windows/Fonts/georgiai.ttf"],
    "G-BI": ["/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf", "C:/Windows/Fonts/georgiaz.ttf"],
}
for name, paths in _FONTS.items():
    pdfmetrics.registerFont(TTFont(name, next(p for p in paths if os.path.exists(p))))
from reportlab.lib.fonts import addMapping
addMapping("G", 0, 0, "G"); addMapping("G", 1, 0, "G-B"); addMapping("G", 0, 1, "G-I"); addMapping("G", 1, 1, "G-BI")

INK = colors.HexColor("#1f1c18")
SOFT = colors.HexColor("#5b554c")
GOLD = colors.HexColor("#9a7b3c")
RULE = colors.HexColor("#d9d2c5")
PAPER = colors.HexColor("#faf8f4")

W, H = A4
M = 22 * mm
CW = W - 2 * M

st = {
    "kicker": ParagraphStyle("kicker", fontName="G", fontSize=8.5, leading=12, textColor=GOLD, spaceAfter=10),
    "title": ParagraphStyle("title", fontName="G", fontSize=30, leading=34, textColor=INK, spaceAfter=6),
    "sub": ParagraphStyle("sub", fontName="G-I", fontSize=12.5, leading=17, textColor=SOFT, spaceAfter=16),
    "h": ParagraphStyle("h", fontName="G", fontSize=18, leading=22, textColor=INK, spaceBefore=8, spaceAfter=8),
    "num": ParagraphStyle("num", fontName="G", fontSize=8.5, leading=11, textColor=GOLD, spaceBefore=14, spaceAfter=2),
    "lead": ParagraphStyle("lead", fontName="G-I", fontSize=11.5, leading=16.5, textColor=INK, spaceAfter=9),
    "p": ParagraphStyle("p", fontName="G", fontSize=10, leading=15, textColor=INK, spaceAfter=7),
    "b": ParagraphStyle("b", fontName="G", fontSize=10, leading=15, textColor=INK, leftIndent=12, bulletIndent=0, spaceAfter=5),
    "small": ParagraphStyle("small", fontName="G-I", fontSize=9, leading=13, textColor=SOFT, spaceAfter=6),
    "cell": ParagraphStyle("cell", fontName="G", fontSize=9, leading=12.5, textColor=INK),
    "cellh": ParagraphStyle("cellh", fontName="G-B", fontSize=8.5, leading=12, textColor=SOFT),
    "sub_h": ParagraphStyle("sub_h", fontName="G-B", fontSize=10, leading=14, textColor=INK, spaceBefore=6, spaceAfter=3),
}

def P(t, s="p"): return Paragraph(t, st[s])
def B(t): return Paragraph(t, st["b"], bulletText="•")
def section(n, title): return [P(f"{n:02d}", "num"), P(title, "h")]

def table(rows, widths, header=True):
    data = [[Paragraph(c, st["cellh" if (header and i == 0) else "cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * CW for w in widths], repeatRows=1 if header else 0)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t

class Walls(Flowable):
    """Three walls at their true 4:5:4 proportion, each with a caption."""
    def __init__(self, labels, fill, text=INK, edge=None, caption=None):
        super().__init__()
        self.labels, self.fill, self.text, self.edge, self.caption = labels, fill, text, edge or RULE, caption
        self.gap = 5
        unit = (CW - 2 * self.gap) / 13.0
        self.ws = [4 * unit, 5 * unit, 4 * unit]
        self.h = 5 * unit * 3.6 / 6.0
        self.height = self.h + 16
    def wrap(self, aw, ah): return CW, self.height
    def draw(self):
        c = self.canv; x = 0
        names = ["LEFT", "CENTRE", "RIGHT"]
        for i, w in enumerate(self.ws):
            c.setFillColor(self.fill); c.setStrokeColor(self.edge); c.setLineWidth(0.6)
            c.rect(x, 16, w, self.h, fill=1, stroke=1)
            c.setFillColor(GOLD); c.setFont("G", 7.5)
            c.drawCentredString(x + w / 2, 4, names[i])
            p = Paragraph(self.labels[i], ParagraphStyle("wl", fontName="G", fontSize=8.5, leading=11.5,
                                                         textColor=self.text, alignment=TA_CENTER))
            pw, ph = p.wrap(w - 14, self.h)
            p.drawOn(c, x + 7, 16 + (self.h - ph) / 2)
            x += w + self.gap

class Swatches(Flowable):
    def __init__(self, items):
        super().__init__(); self.items = items; self.height = 26
    def wrap(self, aw, ah): return CW, self.height
    def draw(self):
        c = self.canv; x = 0
        for name, hexv in self.items:
            c.setFillColor(colors.HexColor(hexv)); c.setStrokeColor(RULE); c.setLineWidth(0.5)
            c.rect(x, 6, 16, 16, fill=1, stroke=1)
            c.setFillColor(SOFT); c.setFont("G", 8.5); c.drawString(x + 22, 10.5, name)
            x += 22 + c.stringWidth(name, "G", 8.5) + 22

def on_page(c, doc):
    c.saveState()
    c.setFillColor(PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(RULE); c.setLineWidth(0.5); c.line(M, 15 * mm, W - M, 15 * mm)
    c.setFillColor(SOFT); c.setFont("G", 7.5)
    c.drawString(M, 10.5 * mm, "Secret of the Raft  ·  Scene 9 projection direction")
    c.drawRightString(W - M, 10.5 * mm, str(doc.page))
    c.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=20 * mm, bottomMargin=22 * mm,
                      title="Scene 9 Projection Direction", author="", subject="Secret of the Raft, Scene 9")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(M, 22 * mm, CW, H - 42 * mm, id="f",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=on_page)])

s = []
s += [Spacer(1, 10 * mm), P("SECRET OF THE RAFT  ·  SCENE 9, THE AFTERMATH", "kicker"),
      P("Projection direction", "title"),
      P("The salon, the studio and the court martial. September 2026.", "sub"),
      P("This sets out where the projections for Scene 9 are heading. The look of all three worlds is "
        "now decided, the plan for how they sit on the set is in place, and the first test images are "
        "being made this week. None of this is final artwork yet. It’s the direction, so you can see "
        "what’s coming and the thinking behind it.", "lead")]

# 1
s += section(1, "The idea")
s += [P("The three worlds in Scene 9 are the three people who decide how Agnès’s story gets told. "
        "The court writes the official lie. The salon laughs at it. The studio refuses it and paints the truth."),
      P("The scene cuts between them quickly, sometimes with two on stage at once, so the audience needs to "
        "know where they are at a glance. Each world has its own kind of light and its own kind of surface, "
        "and that’s what tells them apart."),
      table([["World", "Light", "Surface", "Colour"],
             ["<b>Salon</b>", "Warm candlelight from many small flames", "Polished: gilt, mirror, silk", "Ivory and gold, a touch of crimson"],
             ["<b>Studio</b>", "One cold window, deep shadow", "Worn: raw plaster, dust, paint stains", "Grey daylight and earth browns, a touch of dried-blood red"],
             ["<b>Court</b>", "Flat and glowing, lit from behind", "None. It’s a shape, not a room", "Bone white and pure black"]],
            [0.14, 0.30, 0.28, 0.28]),
      Spacer(1, 8),
      P("The salon and the studio are both Paris interiors from the same few years, so the difference has to "
        "come from how they feel: warm and polished against cold and worn. The court sits apart from both.")]

# 2
s += [KeepTogether(section(2, "Three screens, one room") + [P("Each world is built as a real room, and each of the three surfaces is one wall of it. The centre "
        "screen is the back wall, and the two side flats are the left and right walls. The set already "
        "folds like a room, so the images don’t need to fake any depth. Every wall is shown straight on."),
      Walls(["Left wall of the room<br/>4.8 x 3.6 m", "Back wall of the room<br/>6.0 x 3.6 m", "Right wall of the room<br/>4.8 x 3.6 m"],
            colors.HexColor("#efe9df")),
      P("The three surfaces at their real proportions, as seen from the audience.", "small")]),
      Spacer(1, 4),
      B("<b>True to scale.</b> The bottom of each image is the stage floor. A rail sits at hip height and a "
        "candle sconce at head height, so an actor who walks up to the wall stands at the right size against it."),
      B("<b>The view never moves.</b> There are no pans and no drifting camera. The only movement is inside the "
        "picture: candle flames, dust in the light, a curtain stirring."),
      B("<b>Nothing is split across two screens.</b> Every object sits whole on one wall, so there’s never "
        "half a table on one flat and half on the next. Each wall works as a picture on its own. The three still "
        "read as one room because they share the same architecture, light and colour."),
      B("<b>Any world can take any wall.</b> Because each wall stands alone, the salon can hold one side while "
        "the studio builds on the other, and the court can break in over both."),
      B("<b>No people in the images.</b> The actors are the people. The only figure is the judge’s silhouette.")]

# 3
s += [PageBreak()]
s += section(3, "The salon")
s += [P("Marie-Louise’s salon is old money on show. It’s an evening in 1817, in a grand room from the "
        "century before, kept perfect by a royalist household that wants the old days back.", "lead"),
      Walls(["Portrait of Louis XVIII in a heavy gilt frame, candle sconces either side",
             "Tall gilt mirror over a white marble fireplace, reflecting the chandelier",
             "Tall window, crimson curtains drawn, a line of dusk at the edges"],
            colors.HexColor("#f3ead8"), edge=colors.HexColor("#c9ad6e")),
      Spacer(1, 6),
      B("<b>Left.</b> This is the wall behind Marie-Louise when she reads the letter, so the king is watching over "
        "her. The portrait will be the real painting from the period, placed in by hand."),
      B("<b>Centre.</b> The mirror reflects the room behind the audience, with its chandelier and candles. "
        "It’s the one place in the scene with real depth, and it puts glittering crystal right in the middle."),
      B("<b>Right.</b> A thin line of cold evening light at the curtains is the only thing in the room that isn’t warm."),
      P("Around all three walls runs carved ivory panelling picked out in gold, with pairs of candle sconces."),
      P("What moves", "sub_h"),
      P("Candle flames, light catching the gilt and the crystal, and the faintest stir in the curtains. Nothing else."),
      P("How it arrives and leaves", "sub_h"),
      P("Each wall is made in two versions, lit and dark. The salon is revealed out of the dark one candle at a "
        "time, with the gold catching first. It leaves the same way, as the candles go out."),
      P("Why this version", "sub_h"),
      P("A real salon of 1817 was paler and plainer than most people imagine. The script asks for something "
        "grander, and a room from before the Revolution, still in use, is exactly what a royalist family would "
        "have treasured. It also reads as privilege the moment it appears."),
      Swatches([("Ivory and cream", "#efe6d2"), ("Burnished gold", "#b08d3e"), ("Crimson silk", "#8e1b24")])]

# 4
s += [PageBreak()]
s += section(4, "The studio")
s += [P("Géricault’s studio is a working room, and a grim one. Paris, 1818. A big, bare rented space "
        "where he shut himself away to paint the Raft.", "lead"),
      Walls(["Shelves of plaster casts, the model of the raft, canvases leaning on the wall",
             "The great canvas, where the painting builds up through the scene",
             "Tall north window, sketches of limbs pinned around it, a candle stub on the sill"],
            colors.HexColor("#d9d6cf"), edge=colors.HexColor("#8f887b")),
      Spacer(1, 6),
      B("<b>Left.</b> The clutter of the work: casts, the small raft model the ship’s carpenter built for "
        "him, and stacked canvases."),
      B("<b>Centre.</b> The painting grows over the scene: charcoal lines first, then half painted, then almost "
        "finished by the time Géricault and Sarah step back to look at it. We use the real painting, brought "
        "in stage by stage."),
      B("<b>Right.</b> Cold grey daylight from the window lights the whole room. Studies of arms, legs and hands "
        "are pinned to the plaster, and a rag stained red lies by the candle."),
      P("What moves", "sub_h"),
      P("Dust drifting in the window light, a candle guttering, and now and then a cloud passing, so the "
        "daylight dims and comes back."),
      P("How it arrives and leaves", "sub_h"),
      P("It paints itself in, charcoal lines first and then colour, as if the artist is making it appear. It "
        "leaves by fading back to bare canvas, the edges breaking up."),
      P("Two choices worth knowing about", "sub_h"),
      P("The real canvas is about 4.9 by 7.2 metres, bigger than the centre screen. We’ve shown it smaller so "
        "the whole composition fits, including the figure waving at the top. That’s the image the scene "
        "builds to, so it needs to be seen in full."),
      P("The darker side of his research is in the sketches on the wall. The rotting head stays with the actor "
        "as a real prop, so the images don’t compete with it."),
      Swatches([("Grey daylight", "#a9aaa6"), ("Raw umber", "#5a4632"), ("Dried-blood red", "#6e1f1a")])]

# 5
s += [PageBreak()]
s += section(5, "The court martial")
s += [P("The court is the one world that isn’t a room. It’s a solid black silhouette of the judge "
        "against a pale, glowing field, like a shadow thrown on a paper screen. It gets bigger with every "
        "strike of the gavel.", "lead"),
      P("The judge is shown side-on in a long robe and tall cap, gavel raised in one hand and the verdict "
        "scroll in the other. There’s no face and no detail, just the shape of authority."),
      table([["Strike", "Moment in the script", "What the audience sees"],
             ["1", "“Order!” and finding One", "A small judge, centre screen only"],
             ["2", "Finding Two", "Twice the size"],
             ["3", "Finding Three, “Get the traitors out”", "The judge fills the centre screen"],
             ["4", "The judge loses control", "Two more judges appear, one on each side screen, and all three strike together"],
             ["5", "“...cannot be held responsible.”", "Each screen fills with a huge gavel coming down, then everything cuts to black"]],
            [0.10, 0.38, 0.52]),
      Spacer(1, 8),
      P("Each jump in size lands hard on the strike, with a jolt through the whole image. It never grows "
        "smoothly. At the fourth strike the court becomes a panel of three, which is how a real court martial "
        "sat. It also means no figure ever gets split across two screens."),
      P("The judge’s voice is pre-recorded, since the actor who plays him is on stage as Sarah."),
      Swatches([("Bone white", "#efe8da"), ("Black", "#111111")])]

# 6
s += [KeepTogether(section(6, "Moving between the worlds") + [P("Each world arrives in its own way. The salon shows off, with candles and gold. The studio makes "
        "things visible, with paint. The court imposes itself: a hard cut on the strike, no fade."),
      P("The screens themselves are the fragments. The salon mostly lives on the left and the studio on the "
        "right, and they meet in the middle, while the court breaks in across all three. This is the current "
        "plan, beat by beat. It can still change once we see it on the set."),
      KeepTogether(table([["Beat", "Moment", "Left", "Centre", "Right"],
             ["2", "Salon: the letter", "Salon, candles in", "Dark", "Dark"],
             ["3", "Court: “One!”", "Salon dims", "Court", "Dark"],
             ["4", "Studio: the head", "Dark", "Canvas, charcoal", "Studio paints in"],
             ["5", "Court: “Two!”, “Three!”", "Dark", "Court grows", "Studio fades"],
             ["6", "Studio: “Twenty!”", "Dark", "Canvas, half painted", "Studio"],
             ["7", "Court: the verdict", "Court", "Court", "Court"],
             ["8", "Salon: “Mais bien sûr”", "Salon", "Dark", "Dark"],
             ["9", "Studio: “I will bring down...”", "Dark", "Canvas, nearly finished", "Studio"]],
            [0.08, 0.32, 0.18, 0.22, 0.20]))]),
      Spacer(1, 8),
      P("All the transitions are built by hand in the edit rather than generated, so every cue can be timed "
        "exactly and repeat the same way every night.")]

# 7
s += [PageBreak()]
s += section(7, "How it gets made, and what’s next")
s += [P("The images are made with AI image and video tools, one wall at a time, then put together, timed "
        "and finished by hand. The order goes like this:"),
      table([["", "Step"],
             ["1", "A full view of each room, to settle the design before any wall is built"],
             ["2", "The three walls, each built from that view so they match"],
             ["3", "A check with all three side by side, to make sure they read as one room"],
             ["4", "Gentle movement added to each wall: flames, dust, light"],
             ["5", "Everything laid out on one wide timeline, where the transitions and the court’s strikes are timed"],
             ["6", "Final images sharpened to 4K and handed to the projection software, which fits them to the real surfaces"]],
            [0.08, 0.92]),
      Spacer(1, 10),
      P("Where things are", "sub_h"),
      P("The first test images for the salon and the studio are being made now. All three worlds are due in "
        "about a week."),
      P("Worth knowing", "sub_h"),
      B("Sound sits with the sound designer. The projection timing leads, and each key moment will be marked "
        "so the sound can land on it."),
      B("The measurements come from the current draft of the set plan. If the set changes, the images get "
        "adjusted to match."),
      B("Projecting onto the floor isn’t part of this first pass, but it could be added later.")]

doc.build(s)
print("ok", OUT)
