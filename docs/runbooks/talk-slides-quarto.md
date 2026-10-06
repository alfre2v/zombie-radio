# Runbook: the talk's slides in Quarto — view, edit, check, present

*Living, undated (runbooks convention). How the deck for the Austin Python Meetup talk is built, and how to work on it
by hand: start a live preview, find the text of a slide, change it with the few pieces of Quarto syntax the deck uses,
check that it still builds and looks right, and present it. Why Quarto was chosen, and the talk's structure:
`docs/discussions/2026-10-03-the-talk.md`. The work itself: PR #26 (branch `alfre2v/talk`).*

The owner (verbatim, 2026-10-04): "Until now I have not paid attention to the quarto software, but it is handy and I
want to lear how to use it myself." — this runbook is the answer, written out in full.

## 1. What Quarto is, and how it is installed here

**Quarto** turns Markdown files (`.qmd`) into documents and slide decks. For this talk it produces a **reveal.js**
deck: HTML slides that run in any browser. The deck's source is plain text in git, reviewed in VS Code like any other
file; the deck itself is generated.

- **Installed** on the owner's Mac with Homebrew (2026-10-03), run by the owner because it asks the Mac's admin
  password:

  ```bash
  # Install Quarto (asks the Mac's admin password)
  brew install --cask quarto
  ```

  The version installed: **1.10.18** (`quarto --version`). The download was `quarto-1.10.18-macos.pkg`, 247.7 MB, from
  Quarto's GitHub releases; licence MIT "With the exceptions noted below" (the tools it bundles, such as Pandoc).
- **Why Quarto** (decided 2026-10-03, over Google Slides, Marp, a Claude Artifact deck and others): the slides are text
  in git, so the agent edits them and the owner reviews them in VS Code; it renders a **static website** (a folder)
  that runs from the laptop with **no network at the venue**; and it can be published on GitHub Pages after the talk.
  The full comparison: [discussion 2026-10-03] the-talk §2.

## 2. Where everything lives

All of the deck is in the `talk/` folder of this repository:

| File or folder | What it holds |
|---|---|
| `talk/_quarto.yml` | the deck's settings (§2.1) |
| `talk/index.qmd` | the title slide — `title`, `subtitle`, `author`, `date` — and the list of sections, each pulled in with an `include` |
| `talk/sections/_01-intro.qmd` | the intro: Orson Welles, vibe coder · Who I am · How this project came to be · A Halloween broadcast · About this project · Local AI only · Why not AI APIs (1/2) and (2/2) |
| `talk/sections/_02-tech-overview.qmd` | The machines · The components |
| `talk/sections/_03-demo.qmd` | Commands to go on air · Live demo |
| `talk/sections/_04-deep-dive.qmd` | Behind the curtain: one round · The director, in plain Python · A grammar keeps the model in format · The 32k context, and the trim · One command to a GPU · The 3090 at home |
| `talk/sections/_05-ai-pair.qmd` | Built with an AI pair: the documentation system · what went right · what went wrong (placeholders at this writing) |
| `talk/sections/_06-future.qmd` | What's next · Thank you · Credits (the rolling credits, the deck's last slide) |
| `talk/talk.css` | the look: colours, sizes, spacing, the boxes and cards, the Halloween decorations |
| `talk/images/` | every picture: photos and generated images (`.jpg`), the diagrams (`_*.svg`), the scripts that draw the diagrams (`make_*_svg.py`), and `CREDITS.md` |
| `talk/data/` | the numbers behind a chart, kept in git (`trim-run-2026-10-01T17-48-37.csv`) |
| `talk/_output/` | **the rendered deck**, a static website: `index.html`, `site_libs/` (reveal.js and its plugins), `images/`, `talk.css`, `search.json` (a site search index the deck does not use) — about 10 MB; generated, never edited, kept out of git |
| `talk/.quarto/` | Quarto's working files — generated, kept out of git |

The section files start with an underscore (`_01-intro.qmd`) on purpose: Quarto skips files whose name starts with `_`
when it renders a project, so they are rendered only once, as parts of `index.qmd`, not also as decks of their own.

**The fastest way to find a slide's text:** VS Code's search across files (Cmd-Shift-F), with a phrase you see on the
slide.

### 2.1 The deck's settings (`talk/_quarto.yml`)

```yaml
project:
  type: website              # a website project: publishing uploads the whole rendered folder (§10)
  output-dir: _output        # the rendered deck goes to talk/_output/
  render:
    - index.qmd              # render the deck only, not images/CREDITS.md as a page of its own
  resources:
    - images/favicon.svg     # the tab icon, copied into the rendered folder

format:
  revealjs:
    theme: night             # the dark theme the Halloween look starts from
    width: 1280              # 16:9 — most projectors are 16:9
    height: 720
    slide-number: true       # the "7 / 30" in the bottom-right corner
    hash: true               # each slide gets its own address (…/index.html#/about-this-project)
    embed-resources: false   # a folder, not one file: the chalkboard requires it
    css: talk.css            # our own styles, on top of the theme
    chalkboard: true         # draw on the slides (§8.1)
    footer: "Zombie-Radio · Austin Python Meetup · October 2026"
```

**The rendered deck is a static website.** `talk/_output/` holds plain HTML, CSS, JavaScript and images, no
server-side code: copy the whole folder to any web server (nginx, Apache, a storage bucket, GitHub Pages) and open
`index.html` at the server's address — the folder, not `index.html` alone, which loads its scripts and pictures from the
files beside it. It works offline, served from the laptop; the exception is the two YouTube clips (§7).

Until 2026-10-05 the deck was **one self-contained file** (`embed-resources: true`: every image and script packed into
`index.html`, about 5.6 MB). The chalkboard cannot work that way — Quarto refuses: "Reveal plugin 'RevealChalkboard is
not compatible with self-contained output" — so the owner traded the single file for the chalkboard (verbatim: "Let's
try it, if we don't like it we can revert everything in git."). The PDF export (§8.1, E) is the one-file backup.

## 3. The workflow: edit, save, look

### 3.1 The live preview (the everyday tool)

```bash
# From the repository's root: render the deck, serve it, and reload the browser on every save
cd talk && quarto preview
```

It prints an address such as `Browse at http://localhost:3626/` (the port changes each time) and opens the deck in the
browser. From then on **every time a file in `talk/` is saved, Quarto re-renders and the browser reloads by itself**.
So the loop is: edit in VS Code, save, glance at the browser. Stop it with **Ctrl-C** in its terminal.

### 3.2 A one-off render (what the agent runs to check)

```bash
# Rebuild talk/_output/index.html once, keeping only the lines that matter
cd talk && quarto render 2>&1 | grep -i -E 'warn|error|Output created'
```

`quarto render` rebuilds the deck and prints a lot of settings; the `grep` keeps only warnings, errors and the final
line. **`Output created: _output/index.html` alone means a clean build.** A broken fence or a missing image shows up
here as a warning or an error.

Rendering fetches the theme's web fonts from Google to embed them. Once (2026-10-03) the network failed and Quarto
printed `[WARNING] Could not fetch resource https://fonts.googleapis.com/…`; the deck still built, with the fonts
missing. Re-render with the network up before the talk.

### 3.3 Viewing a render without the preview

- **Serve it, don't open it as a file.** `talk/_output/index.html` opens in any browser by double-click, and everything
  works except the embedded YouTube clip: a page opened from a file (`file:///…`) sends YouTube no information about
  where it comes from, and YouTube refuses with **"Error 153 — Video player configuration error"**. Served over HTTP
  (by `quarto preview`, by a local server, or later by GitHub Pages), the clip loads.
- **The plain local server the agent uses** (no live reload; it serves the last render):

  ```bash
  # Serve the rendered deck on this laptop only (127.0.0.1), port 8020
  cd talk/_output && python3 -m http.server 8020 --bind 127.0.0.1
  # Stop it later (from anywhere)
  kill $(lsof -nP -iTCP:8020 -sTCP:LISTEN -t)
  ```

  Then open `http://127.0.0.1:8020/index.html`. Run one or the other, the preview or this server — not two copies.

## 4. The syntax the deck uses

A `.qmd` file is Markdown with a few extras. These are all the pieces the deck uses.

### 4.1 Sections, slides, text

```markdown
# Tech deep dive                    ← one # = a section's title slide

## The machines                     ← two ## = a new slide; the text after ## is its title

### October 30, 1938                ← three ### = a heading inside a slide

Plain text is a paragraph. **bold**, *italic*, `code`.

- a bullet
- another bullet

1. a numbered item
2. another
```

- A slide's **address** comes from its title: lower case, spaces become hyphens, punctuation dropped —
  "Why not AI APIs (1/2)" becomes `#/why-not-ai-apis-12`. A slide with no title gets `#/section`, `#/section-1`, ….
- A literal asterisk in text must be escaped, or Markdown reads it as italics: `Someone \*made\* this` shows
  `Someone *made* this`.

### 4.2 Styles on a whole slide

`{…}` after a slide's title sets styles for that slide:

```markdown
## A Halloween broadcast {.smaller .boxed-columns}
## Live demo {background-color="#000000"}
```

| Style | What it does |
|---|---|
| `{.smaller}` | Quarto's own: all the slide's text a size smaller |
| `{.boxed-columns}` | ours (`talk.css`): a faint box around each column, to tell two columns apart |
| `{background-color="#000000"}` | the slide's background colour (the section slides use dark tints: `#1a0000`, `#001a00`, …) |
| `{background-image="images/…" background-size="cover"}` | a picture filling the whole slide (used for a while for the CEO poster) |

### 4.3 Speaker notes

```markdown
::: {.notes}
Only the speaker sees this, in the speaker view (press S while presenting).
:::
```

Each slide's notes hold what to say, timings ("About 5 minutes."), and facts in case someone asks. The audience never
sees them (§8.2 explains when that holds).

### 4.4 Blocks and inline pieces with a style

**`:::` fences** wrap several lines in a box styled by `talk.css`. From "About this project":

```markdown
::: {.about-block .about-goals}
[Four goals]{.about-head}

1. Story coherence and improvisation
2. Emotional voices, in sync with the story
:::
```

- `::: {.name}` … `:::` — a block (a box, a card, a row). Blocks can nest: each opening fence needs its own closing
  `:::`.
- `[some text]{.name}` — a few words with a style, inside a line.
- **Change the words freely; leave the `:::` fences and the `{.names}` as they are**, unless the aim is to change the
  look. **If a slide suddenly looks broken, a missing or extra `:::` is the usual cause.**
- Centring needs a block: `text-align` has no effect on an inline `[…]{.name}`. (The counts line under the timeline was
  first written inline and stayed left-aligned; as a `::: {.small-note}` block it centred.)

The styles defined in `talk.css` and where they are used:

| Style | Used for |
|---|---|
| `.small-note` | small grey centred lines (the counts under the timeline, captions under charts, the footer of What's next) |
| `.credit` | the tiny attribution lines under pictures |
| `.centered` | centre a block (the Welles clip and its credit) |
| `.stats`, `.stat`, `.n`, `.d` | the grid of cards (Local AI only, the 3090); `.n` the big orange word, `.d` the grey detail; `.stats.two`, `.stats.compact`, `.stats.one` are variants |
| `.built-on`, `.lead`, `.smaller-lead` | a lead line under a title |
| `.channel`, `.channel-text`, `.channel-video` | the red-barred box with Steve Corbett's channel and its thumbnail |
| `.about-block`, `.about-head`, `.about-row`, `.about-card`, `.about-code`, `.about-principles`, `.about-goals` | "About this project" |
| `.provider-shots`, `.provider-caption`, `.citation` | "Why not AI APIs (2/2)": the two screenshots, the closing line, the Supreme Court citation |
| `.model-lines` | the model's lines on the grammar slide |
| `.boxed-columns` | a faint box around each column (§4.2) |
| `.next-row`, `.next-blood` | "What's next": its two rows of cards (they reuse `.about-block`), and the red card |
| `.thanks-links`, `.thanks-contact` | "Thank you": the two link cards and the contact line |
| `.credits-slide`, `.credits-roll`, `.cr-title`, `.cr-by`, `.cr-head`, `.cr-role`, `.cr-name`, `.cr-note` | "Credits": the slide (title hidden, the roll clipped and faded at top and bottom), the rolling block, and its parts — the big title, the byline, the orange headings, the small-caps roles on the left, the names on the right, the grey notes (§4.10) |

### 4.5 Columns

```markdown
::: {.columns}
::: {.column width="50%"}
Left column
:::
::: {.column width="50%"}
Right column
:::
:::
```

### 4.6 Images

```markdown
![](images/scientists-radio.jpg){.scene .nostretch fig-alt="what the picture shows, for screen readers"}
```

- **Quarto's auto-stretch:** when a slide has a single image, Quarto stretches it to fill the space left on the
  slide — that is what distorted the CEO poster, pulling it out of its 16:9 shape. **`.nostretch`** opts an image out.
  Slides with two or more images are not stretched.
- The size then comes from a class in `talk.css`: `.scene` (a fixed height, the image's own proportions), `.poster`
  (16:9 at a fixed height), `.col-img` (a picture under a column), `.finale` (the last slide's picture).
- Every picture's source and licence goes in `talk/images/CREDITS.md`; some need a credit line on the slide (§6.3).

### 4.7 Code blocks

````markdown
```bash
make ans-deploy ENV=cloud
```

```{.python code-line-numbers="|4"}
def plan_round(...):
    ...
```
````

- The language after the backticks (`bash`, `python`, `ebnf`) sets the colouring.
- `code-line-numbers="|4"` adds a **step**: the block first shows whole, then one press of → highlights line 4 (the
  director's seeded random generator). **Dropped from the director's slide on 2026-10-05.** The owner noticed the
  slide needed two presses to move on and looked the same after the first. reveal.js draws the step as a copy of the
  code laid over the original, every other line dimmed, and the slide's style made the code's background transparent, so
  the bright original showed through and the highlight was invisible. An opaque background fixed it (tested), but the
  owner chose to drop the step (verbatim): "the presentation is long enough and I don't even think we will make it to
  this slide." **The trap, for any future step:** a highlighted code block needs an opaque background on its `code`.
  A highlight with no step, as on "Commands to go on air" (`code-line-numbers="7-8,19-20,22-23"`), has no copy and no
  such trap.
- **An apostrophe in a `bash` block can break the colouring:** the highlighter takes `'` as the start of a quoted
  string, and with no closing quote everything after it turns green. That happened with `<the box's address>`;
  `<box-address>` fixed it.
- A code block that is too long gets cut off at the bottom of its frame (scrollable, which is useless on stage):
  shorten it, join two commands with `&&`, or use `{.smaller}` on the slide.

### 4.8 Diagrams included inline, and steps inside them

The diagrams are SVG files pulled into the slide's HTML (not shown as `<img>`), so that parts of them can appear one
at a time:

````markdown
```{=html}
{{< include images/_components.svg >}}
```
````

- **The path in an `include` is relative to `talk/`** (where `index.qmd` is), even inside a section file:
  `images/_components.svg`, not `../images/…`. A wrong path stops the render with "Include directive failed … could not
  find file".
- Inside the SVG, a group marked `class="fragment" data-fragment-index="1"` appears on the first press of →, `…="2"` on
  the second, and so on — that is how "The components" builds up zone by zone.

### 4.9 Dates on the title slide

```yaml
date: 2026-10-14
date-format: "MMMM YYYY"
```

Quarto **parses** the date: written as `"October 2026"` it showed "2026-10-01". A real date with a `date-format` shows
"October 2026". The talk is on 2026-10-14 in the slides (the internal docs keep 2026-10-08 as the deadline, on
purpose).

### 4.10 An animation that runs while a slide shows (the rolling credits)

The "Credits" slide opens on a big orange **CREDITS** at the centre of the screen, then rolls everything upward like a
film's end — built with CSS alone (`talk.css`):

```css
.reveal section.credits-slide.present .credits-roll {
  animation: credits-roll 62s linear infinite;
}

@keyframes credits-roll {
  0% { transform: translateY(308px); opacity: 0; }  /* CREDITS centred on the screen, invisible */
  1.61% { opacity: 1; }                             /* 1 s: faded in */
  4.84% { transform: translateY(308px); }           /* 3 s: held still, to be read */
  90.32% { transform: translateY(-1400px); }        /* 56 s: the last line has left at the top */
  100% { transform: translateY(-1400px); }          /* held there: 6 s of empty screen, then again */
}
```

- **The slide** is clipped (`overflow: hidden`) and faded at both ends with a `mask-image` gradient, so lines fade in at
  the bottom and out at the top; its `##` title is hidden. The visible title is the first item of the roll,
  `[Credits]{.cr-credits}` — a 97-pixel-tall line whose `margin-bottom: 265px` is the gap that keeps the list below the
  screen while the title sits at the centre.
- **The numbers** (measured in the browser, 2026-10-04): the roll is 1,395 pixels tall in a 720-pixel slide. At a shift
  of 308 the title's centre is at 360 (the screen's centre) and the list's first line at 673, just below the band where
  lines are visible (the bottom fade starts at 662). The roll is fully gone once its bottom passes the top edge (a shift
  of −1,398; the end is −1,400). The roll covers 1,708 pixels in 53 s — about 32 pixels a second — after a 3 s hold;
  then 6 s of empty screen (the owner asked for at least 5): a 62 s cycle. The percentages are the moments divided by
  62: 1 s = 1.61 %, 3 s = 4.84 %, 56 s = 90.32 %. **Adding lines makes the roll taller:** lower the end shift by as much,
  and lengthen the cycle to keep the speed (then recompute the percentages).
- **A trap, found by the owner (2026-10-04):** the rule was first written `.reveal .present .credits-roll` — "inside
  *anything* marked present". reveal.js also marks an outer container `present`, so the animation never stopped when
  the slide was left, and never restarted when it was entered again. **Tie such a rule to the slide itself:**
  `section.credits-slide.present`. Then leaving the slide stops the roll, and entering it starts from the beginning.
- **Checking an animation** cannot be done with one screenshot (it shows one instant). The agent froze the roll at
  given positions in a scratch copy of the page (a `transform … !important` and `animation: none`), and read the running
  animation's state in the browser pane (`element.getAnimations()[0].currentTime`).

## 5. Things never edited by hand

- **`talk/_output/`** — regenerated by every render; edits there are lost (and it is not in git).
- **The diagrams `talk/images/_*.svg`** — each is written by the script beside it. To change a diagram, change the
  script and run it, then render:

  | Script | Draws |
  |---|---|
  | `make_machines_svg.py` | "The machines" |
  | `make_components_svg.py` | "The components" (three zones, built up on key presses) |
  | `make_timeline_svg.py` | the timeline on "How this project came to be" |
  | `make_round_flow_svg.py` | "Behind the curtain: one round" |
  | `make_trim_chart_svg.py` | the trim chart; it reads the run's record from the fork's `runs/` folder when present, saves the numbers to `talk/data/trim-run-2026-10-01T17-48-37.csv`, and draws from that file — so the chart can be redrawn from this repository alone |

  ```bash
  # Redraw a diagram after changing its script (example: the machines), then render
  python3 talk/images/make_machines_svg.py
  cd talk && quarto render 2>&1 | grep -i -E 'warn|error|Output created'
  ```

  The scripts use the Python standard library only — nothing to install.

## 6. Pictures

### 6.1 The rule for the decorations: black backgrounds

The Halloween decorations on every slide — the spider web (top right), the bloody handprint (bottom right), the zombies
walking along the bottom — are the owner's images, set in `talk.css` as three backgrounds of one layer
(`.reveal::after`):

```css
background-image: url("images/spiderweb.jpg"), url("images/handprint.jpg"), url("images/zombies.jpg");
background-position: right top, right 0.6vw bottom 9vh, left bottom;
background-size: auto 36vh, auto 18vh, auto 15vh;
mix-blend-mode: lighten;
background-blend-mode: lighten;
```

- **`mix-blend-mode: lighten`** blends the layer with the slide under it: wherever a picture is pure black, the slide
  shows through. **So every decoration must have a truly black background**, or it shows as a grey box.
- **`background-blend-mode: lighten`** blends the three pictures with each other — without it, the handprint's black
  rectangle hid the zombies behind it.
- **The sizes** (`36vh`, `18vh`, `15vh`) are fractions of the screen's height: one number each to make a decoration
  bigger or smaller. `background-position` places them.
- **To hide the decorations on one slide** (done for a while for the full-screen CEO poster, then removed when the
  poster moved into its slide): give the slide `data-state="no-decor"` — reveal.js then adds the class `no-decor` to the
  page while that slide shows — and add to `talk.css` a rule `.reveal-viewport.no-decor .reveal::after { display: none; }`.
  To hide the footer and the slide number too, the rule needs `!important`, because Quarto's own script sets them with
  an inline style.

### 6.2 Preparing a new picture

The owner puts a new image next to the repositories (in `/Users/alfredo/workspace/hackTNT_2026/`); the original stays
untouched, and a cropped, scaled copy goes into `talk/images/`:

```bash
# A picture's size in pixels
sips -g pixelWidth -g pixelHeight <file>
# Scale to 1,600 pixels wide, as a JPEG (quality 4 of ffmpeg's scale, about 200 KB for a photo)
ffmpeg -v error -y -i <original> -vf scale=1600:-2 -q:v 4 talk/images/<name>.jpg
# Crop first (width:height:x:y), then scale — e.g. the zombies strip
ffmpeg -v error -y -i <original> -vf "crop=3168:440:0:735,scale=-2:180" -q:v 4 talk/images/zombies.jpg
# Darken (here to 55 %), keeping black black — for decorations that are too bright
ffmpeg -v error -y -i <original> -vf "colorlevels=romax=0.55:gomax=0.55:bomax=0.55" talk/images/<name>.jpg
```

- JPEG for photos and generated images (smaller, same look at slide size); PNG only for a real transparent background.
- To prompt an image generator for a decoration: ask for **a pure black background (#000000)**, greyscale or muted
  colours, no text, and the subject where it will sit (a web anchored in the top-right corner; a strip of figures
  along the bottom, seamless left to right).
- A picture with text that must not appear (a name, an address) can be pixelated in place — e.g. the provider's name
  in "Why not AI APIs (2/2)":
  `ffmpeg -i in.jpg -filter_complex "[0]crop=88:44:752:39,scale=11:5,scale=88:44:flags=neighbor[p];[0][p]overlay=752:39" out.jpg`.

### 6.3 Credits

`talk/images/CREDITS.md` records the source and licence of every picture. Public-domain pictures need no credit (the
slide still says "Wikimedia Commons, public domain"); **CC BY and CC BY-SA need a credit line on the slide** (the
old-radio photo; the Wikipedia citation on "Why not AI APIs (2/2)"); **the radio static's credits are required on
screen** (CC BY includes public performance) — they are on the rolling "Credits" slide, with the EARS voices
(CC BY-NC 4.0), Steve Corbett's projects, the models and the pictures (§4.10). The owner's own images are recorded as
such.

## 7. The Welles clip (YouTube)

The opening clip is a YouTube player inside the slide (`<iframe data-external="1" …>` — `data-external` keeps
Quarto from trying to pack the video into the HTML). It needs:

- **the venue's internet** — if the network is down, skip the clip;
- **the deck served over HTTP**, not opened as a file (§3.3, Error 153).

## 8. Presenting

### 8.1 Keys, and what else reveal.js can do

The owner (verbatim, 2026-10-05): "One thing that I notice is that when one opens the "notes" view (pressing "S"),
there is more to this reveal.js window that it seems at first: For once, if one presses Esc, it shows a slideshow view
map of all the slides by section, so one can jump quickly to the slide one need... What other reveal.js secrets are
worth knowing?"

Checked against the deck itself (2026-10-05): its help overlay (press **?**) and the plugins it loads (`quarto-line-
highlight`, `pdf-export`, `menu`, `quarto-support`, `mathjax2`, `notes`, `search`, `zoom`).

**Moving**

| Key | Does |
|---|---|
| → , Space, N | the next slide, or the next step of a slide (the components diagram, the highlighted code line) |
| ← , P | back |
| **Alt + ← / →** | next / previous slide **skipping the build-up steps** (past "The components" without its three zones) |
| **Shift + ← / →** | jump to the first / last slide |
| **G** | **jump to slide**: type its number, then Enter (`G 22 Enter`) |
| **Esc** or **O** | the overview: every slide as a grid by section; arrows to move, Enter to open |
| **M** | the **menu** (also the ☰ in the bottom-left corner): every slide by title, and tools. This M is the deck's; the M that mutes the static belongs to the app's page, another window — no conflict |
| **Ctrl + Shift + F** | **search** the deck's text, Enter to jump to the match — fastest when a question names something on a slide |

**On stage**

| Key | Does |
|---|---|
| **.** | **pause**: a black screen; again to come back (B, its other key, now opens the chalkboard's blackboard) |
| **F** | full screen |
| **Alt + click** | **zoom** into what is clicked; Alt + click again to zoom out — the dense diagrams, the Artificial Analysis chart, the grammar |
| **S** | the **speaker view** (below) |
| **?** | the help overlay, every key |

**Other modes**

| Key | Does |
|---|---|
| **E** | **PDF export mode**: press E, then print from the browser (Cmd-P, save as PDF) — one page per slide; a backup for a USB stick. Animations (the rolling credits, the build-ups) print as still frames |
| **R** | **scroll view**: the deck as one long scrolling page — for reviewing, not for presenting |

**The speaker view (S)** — a second window with the current slide, the next slide, that slide's notes, a clock and a
**timer** (click it to reset it when the talk starts: it shows how long you have been talking, against the plan of about
33 minutes); a layout button in its corner rearranges the panes; the slides can be driven from it, so the projector
never needs the mouse.

**The chalkboard** (enabled 2026-10-05) — draw on the slides with the mouse: circle a number on the trim chart,
underline a line of the grammar, sketch on a blank board. Keys, from the deck's help overlay:

| Key | Does |
|---|---|
| **C** | **draw on the current slide**: the cursor becomes a pen, drag to draw; C again to stop |
| **B** | **the blackboard**: a separate board over the slide, to sketch on; B again to go back |
| **X** / **Y** | next / previous pen colour |
| **Del** | clear the drawings on this slide |
| **Backspace** | clear all the drawings, on every slide |
| **D** | download the drawings (a JSON file) |

Two icons in the bottom-left corner, beside the ☰ menu — a board and a pen — open the same two modes with the mouse.
Drawings stay with their slide while moving around, until cleared; they never change the slides themselves. It needs
the deck rendered as a folder (§2.1).

### 8.2 Keeping the notes private

- **A projector (HDMI or USB-C) is a second display.** In macOS's System Settings → Displays it is either an
  **extended display** or a **mirror** of the laptop's screen. **Extended:** the slides full screen on the projector,
  the speaker view on the laptop — the audience never sees the notes (the normal way to present). **Mirrored:** both
  show the same, so the speaker view would be on the wall — do not open it then. At the venue: plug in, check that
  setting, drag the deck's window to the projector, press F.
- **Screen sharing (Zoom, Meet, Teams): share a window, or one display — never the whole screen with the notes on it.**
  The talk switches between the deck and the live show in the browser; with window sharing that means changing the
  shared window each time. Simpler: put the deck and the show's browser window on the second display (or the
  projector) and share **that display**; the speaker view stays on the laptop's screen, outside the share.
- **Sound:** plugging into a projector may move macOS's sound output to the HDMI cable. Check Sound in System Settings
  before the show — the radio play is all audio.

The venue's setup is learned on the day; the owner arrives early to work it out (owner action queue: demo-day
logistics).

### 8.3 Different screens and resolutions

The owner (verbatim, 2026-10-05): "I have no idea how this quarto presentation will behave in a different
resolution, which will probably be the case on a projector screen. What should we expect on different resolutions, how
are the slides supposed to grow and shrink?"

**How it works.** The deck is designed on a fixed canvas of 1280×720 (`width` and `height` in `_quarto.yml`, §2.1).
reveal.js scales that canvas **as one picture** to fit the window, like zooming an image: the layout never reflows —
every gap, box and line break stays where it was tuned; text grows on a big screen and shrinks on a small one, in
proportion. A screen of another shape gets the same slide, fitted inside, with empty bands.

**The exception: the decorations.** The zombies, the handprint and the spider web (§6.1) are painted on the window, not
on the slide, and sized as a share of the window's height (`vh`); the footer and the slide number are on the window too,
at a fixed pixel size. On a 16:9 screen they line up with the slide exactly as designed; on another shape they sit at
the window's edges while the slide floats inside its bands.

**Tested 2026-10-05** — the slide "Local AI only" rendered by headless Chrome at three screen sizes:

| Screen | What happened |
|---|---|
| 1920×1080 (16:9, most projectors) | identical to the 1280×720 design, 1.5 times bigger; every tuned gap holds; the footer and slide number look a little smaller, at their fixed pixel size |
| 1280×800 (16:10, many laptops, some projectors) | the same slide with a thin band above; the zombies at the window's bottom edge, lower than designed — more room between them and the content |
| 1024×768 (4:3, older projectors) | the slide shrunk to the width, wide bands above and below; the zombies and the web at the window's edges, clear of the content; text smaller but readable |

So **the layout is safe at any resolution**, and the tight spots tuned against the zombies (the channel box on "Local
AI only", the captions above their heads) are exact on any 16:9 screen and only get more room on other shapes. The cost
of a non-16:9 projector is the empty bands and slightly smaller text — nothing to fix in the deck.

**At the venue, three things matter more than the projector's resolution:**

1. **Present full screen (press F).** A browser window with its tabs and address bar is shorter than 16:9: the slide
   shrinks with bands at the sides, and the decorations shift as on a 16:10 screen. Full screen gives the deck the whole
   display.
2. **Keep the browser's zoom at 100 %** (Cmd-0 resets it). A zoomed page changes the window size reveal.js sees.
3. **Use the projector's native resolution** in System Settings → Displays, if macOS does not pick it. A scaled
   resolution can make everything blurry (the layout stays the same).

## 9. Checking an edit (the agent's four steps)

After the owner edits the slides, the agent checks with these commands — run from the repository's root:

1. **Which files changed:**

   ```bash
   git status -sb
   ```

   `M` marks a modified file, `??` a new one.
2. **What exactly changed:**

   ```bash
   git diff talk/sections/
   ```

   Lines starting with `-` were removed, lines with `+` added. It shows everything since the last commit — so with work
   of the agent's still uncommitted, its changes and the owner's appear together. VS Code's Source Control panel shows
   the same diff side by side.
3. **Does it still build cleanly:** the render of §3.2 — "Output created" alone is a clean build.
4. **Does it look right:** a screenshot with headless Chrome — the agent cannot see the owner's browser — with the deck
   served (§3.3):

   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
     --window-size=1280,720 --virtual-time-budget=4000 --screenshot=about.png \
     "http://127.0.0.1:8020/index.html#/about-this-project"
   ```

   `--window-size=1280,720` is the deck's 16:9 size; `--virtual-time-budget` gives the page time to finish loading;
   the part after `#/` is the slide's address (§4.1); adding `/2` after it (`#/the-components/2`) shows a step of a
   built-up slide. **The owner does not need this one:** `quarto preview` shows the same, live.

Then, as for every change in this repository: review in VS Code, commit only on the owner's order, the IP scan on the
staged diff (`git diff --cached | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}'` — `127.0.0.1` on the commands slide is
fine), push on the owner's order.

## 10. Publishing to GitHub Pages (first published 2026-10-05)

The owner (verbatim, 2026-10-04): "Not that I want to publish the talk yet, but I am curious how is the process of
publishing to GitHub Pages. Walk me through the steps required." — the walk-through, kept here. **Nothing in this
section had been run at this writing.** It was first run on 2026-10-05, after #26 merged; what happened, and the one
correction it needed, are in §10.4.

### 10.1 What publishing does

`quarto publish gh-pages` renders the deck and pushes the result — the `_output/` folder, about 10 MB — to a
**separate branch called `gh-pages`** in the zombie-radio repository. GitHub Pages then serves that branch as a website
at:

**https://alfre2v.github.io/zombie-radio/**

(GitHub's default address for a repository's Pages site: `<owner>.github.io/<repository>/`; it is the address already
on the "Thank you" slide.) The source — `talk/`, the `.qmd` files — stays on `main` as it is; `gh-pages` holds only the
rendered output, so it never mixes with the work branches.

### 10.2 The steps

**0. Merge #26 first, and publish from `main`.** Publishing pushes whatever is rendered *on the machine, from the
branch checked out*. Doing it from `main` after the merge makes the public deck match the repository's record.

**1. Create the empty `gh-pages` branch — once.** Quarto's documentation asks for this branch to exist before the first
publish. It is an "orphan" branch: no history shared with `main`.

```bash
# A new branch with no history
git checkout --orphan gh-pages
# Empty its staging area (destructive: commit or stash any work first)
git reset --hard
# One empty commit, so the branch exists
git commit --allow-empty -m "Initialising gh-pages branch"
# Put it on GitHub
git push origin gh-pages
# Back to work
git checkout main
```

**2. Turn on GitHub Pages — once**, in the browser: the repository's **Settings → Pages → Build and deployment →
Source: "Deploy from a branch" → Branch: `gh-pages`, folder `/ (root)` → Save.** Quarto may set this by itself; check it
either way. On 2026-10-05 nothing had to be done: after the first publish, GitHub showed Pages on, served from
`gh-pages`, folder `/`.

**3. Publish:**

```bash
# Render the deck and push it to the gh-pages branch (asks to confirm)
cd talk && quarto publish gh-pages
```

- It asks for confirmation, renders the deck, copies it into `gh-pages` — adding a `.nojekyll` file, which tells GitHub
  not to reprocess the site with its Jekyll tool — and pushes.
- Quarto's documentation says it also writes a small **`talk/_publish.yml`** recording where the deck was published (a
  new file, reviewed and committed like any other). The first publish of 2026-10-05 wrote none.

**4. Wait a minute, then check.** GitHub builds the site; the repository's **Actions** tab shows a run named "pages
build and deployment". When it is green, open `https://alfre2v.github.io/zombie-radio/`. The Welles clip plays there,
because the page is served (§3.3, §7).

**Updating later:** edit, commit, then `cd talk && quarto publish gh-pages` again — it replaces the old version.
**Taking it down:** turn Pages off in Settings → Pages, or delete the `gh-pages` branch.

### 10.3 Before publishing

- **The speaker notes become public too.** They are inside the HTML, and anyone viewing the published deck can press
  **S** and read them. Ours hold the owner's full wording, timings and reminders ("check today's price") — nothing
  sensitive at this writing, but read them with that in mind. **The owner's decision (2026-10-05): publish the notes as
  they are** — "Accept them as they are", over a pass rewriting them for the public or a deck without notes. Before
  publishing, scan the rendered file as commits are scanned:

  ```bash
  # Any machine address in the rendered deck (127.0.0.1 on the commands slide is fine)
  grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' talk/_output/index.html | sort -u
  # The AI provider the slides leave unnamed (expect nothing)
  grep -c -i -E 'gemini|google' talk/_output/index.html
  ```

  Run on 2026-10-04 against the deck as rendered that day: the only address was `127.0.0.1`, and the provider's name
  appeared 0 times (the embedded fonts carry no name either).
- **It is public at once**, and search engines may index it. The repository is public already, so nothing new is
  revealed, but the slides become easy to find.
- **It is an outward-facing action** — a new branch on GitHub and a public website — so under the working agreements it
  happens only on the owner's order; the agent asks before step 1, before step 3, and before every later re-publish.
- **An alternative not taken:** a GitHub Actions workflow that renders the deck in the cloud on every push to `main`.
  Automatic, but it needs Quarto installed in CI, more setup, and it publishes things one may not mean to publish.
  Manual publishing suits a talk deck better.

### 10.4 The first publish (2026-10-05)

The owner, after merging #26 (verbatim): "PR merged. Let's publish now the gh pages to see how it looks" — publishing
before the talk, so the address on "Thank you" works when shown; republished after any later change (the owner's
choice that day, over publishing after the talk).

1. **The `gh-pages` branch** was created as in step 1, from `main`.
2. **The scans of §10.3** on the fresh render: the only address `127.0.0.1` (five other hits were numbers inside the
   GitHub icon's drawing, not addresses); the provider's name 0 times.
3. **`quarto publish gh-pages` refused:** "The specified path (…/talk) is not a website, manuscript or book project so
   cannot be published." The deck was then a project of type `default`, and Quarto publishes a whole folder only for a
   website, a book or a manuscript.
4. **Published as a single document instead** — `quarto publish gh-pages index.qmd`. The deck went up, but **without the
   Halloween decorations**: a document's publish uploads only the files the page itself points to, and the zombies, the
   handprint and the spider web are named only in `talk.css`. On the live site they answered 404.
5. **The correction: the project became a website** (`type: website` in `_quarto.yml`, §2.1), tested first on a copy
   of `talk/`: the render folder holds the decorations, and a website's publish uploads that whole folder. The owner
   asked whether that would fix it ("would making it a website project fix the issue? How complex would that change of
   project type be?"), then: "go ahead, website type with the render line". The `render:` line keeps
   `images/CREDITS.md` from being rendered as a page of its own and published beside the deck. What else changed: the
   reveal.js files moved from `index_files/libs/` to `site_libs/`, and the render adds a `search.json`, a site search
   index the deck does not use. The slides look the same.
6. **Then republished** from `main`, once the correction merged, with the plain `cd talk && quarto publish gh-pages` of
   step 3.

## 11. Before the talk

- Recount the numbers under the timeline (discussions, experiments, tools — counted 2026-10-03).
- Check the A6000's hourly price on "One command to a GPU" (~$0.50, from the provider survey of 2026-09-13).
- Update "The 3090 at home" to wherever goal 4 stands.
- Fill in "Who I am", and the email, website and LinkedIn on "Thank you" (placeholders).
- Publish (§10), so the slides' address on "Thank you" works.
- Re-render with the network up (the fonts, §3.2); rehearse with the speaker view and the live demo against the woken
  cloud box.
