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
  in git, so the agent edits them and the owner reviews them in VS Code; it renders **one self-contained HTML file**
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
| `talk/sections/_06-future.qmd` | What's next · Thank you |
| `talk/talk.css` | the look: colours, sizes, spacing, the boxes and cards, the Halloween decorations |
| `talk/images/` | every picture: photos and generated images (`.jpg`), the diagrams (`_*.svg`), the scripts that draw the diagrams (`make_*_svg.py`), and `CREDITS.md` |
| `talk/data/` | the numbers behind a chart, kept in git (`trim-run-2026-10-01T17-48-37.csv`) |
| `talk/_output/` | **the rendered deck** (`index.html`, about 5.6 MB) — generated, never edited, kept out of git |
| `talk/.quarto/` | Quarto's working files — generated, kept out of git |

The section files start with an underscore (`_01-intro.qmd`) on purpose: Quarto skips files whose name starts with `_`
when it renders a project, so they are rendered only once, as parts of `index.qmd`, not also as decks of their own.

**The fastest way to find a slide's text:** VS Code's search across files (Cmd-Shift-F), with a phrase you see on the
slide.

### 2.1 The deck's settings (`talk/_quarto.yml`)

```yaml
project:
  type: default
  output-dir: _output        # the rendered deck goes to talk/_output/

format:
  revealjs:
    theme: night             # the dark theme the Halloween look starts from
    width: 1280              # 16:9 — most projectors are 16:9
    height: 720
    slide-number: true       # the "7 / 30" in the bottom-right corner
    hash: true               # each slide gets its own address (…/index.html#/about-this-project)
    embed-resources: true    # one self-contained HTML file: images, fonts and scripts inside it
    css: talk.css            # our own styles, on top of the theme
    footer: "Zombie-Radio · Austin Python Meetup · October 2026"
```

`embed-resources: true` is what makes the deck work **offline**: every image and script is packed into
`_output/index.html`. The exception is the Welles clip, which plays from YouTube (§7).

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
| `.small-note` | small grey centred lines (the counts under the timeline, captions under charts, the links on the last slide) |
| `.credit` | the tiny attribution lines under pictures |
| `.centered` | centre a block (the Welles clip and its credit) |
| `.stats`, `.stat`, `.n`, `.d` | the grid of cards (Local AI only, the 3090); `.n` the big orange word, `.d` the grey detail; `.stats.two`, `.stats.compact`, `.stats.one` are variants |
| `.built-on`, `.lead`, `.smaller-lead` | a lead line under a title |
| `.channel`, `.channel-text`, `.channel-video` | the red-barred box with Steve Corbett's channel and its thumbnail |
| `.about-block`, `.about-head`, `.about-row`, `.about-card`, `.about-code`, `.about-principles`, `.about-goals` | "About this project" |
| `.provider-shots`, `.provider-caption`, `.citation` | "Why not AI APIs (2/2)": the two screenshots, the closing line, the Supreme Court citation |
| `.model-lines` | the model's lines on the grammar slide |
| `.boxed-columns` | a faint box around each column (§4.2) |

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
  director's seeded random generator).
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
old-radio photo; the Wikipedia citation on "Why not AI APIs (2/2)"); **the radio static's credits line on the last
slide is required** (CC BY includes public performance). The owner's own images are recorded as such.

## 7. The Welles clip (YouTube)

The opening clip is a YouTube player inside the slide (`<iframe data-external="1" …>` — `data-external` keeps
Quarto from trying to pack the video into the HTML). It needs:

- **the venue's internet** — if the network is down, skip the clip;
- **the deck served over HTTP**, not opened as a file (§3.3, Error 153).

## 8. Presenting

### 8.1 Keys

| Key | Does |
|---|---|
| → or Space | the next slide, or the next step of a slide (the components diagram, the highlighted code line) |
| ← | back |
| **S** | the **speaker view**: a second window with the current slide, the next slide, a clock, a timer, and the notes |
| **F** | full screen |
| **O** or Esc | the overview: every slide as a grid, to jump anywhere |

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

## 10. Publishing (not done yet)

```bash
# Publish the deck to a gh-pages branch of this repository, served by GitHub Pages — on the owner's order only
cd talk && quarto publish gh-pages
```

It makes the deck **public** on GitHub Pages; a served copy also plays the Welles clip. Not run at this writing.

## 11. Before the talk

- Recount the numbers under the timeline (discussions, experiments, tools — counted 2026-10-03).
- Check the A6000's hourly price on "One command to a GPU" (~$0.50, from the provider survey of 2026-09-13).
- Update "The 3090 at home" to wherever goal 4 stands.
- Fill in "Who I am" and the links on the last slide.
- Re-render with the network up (the fonts, §3.2); rehearse with the speaker view and the live demo against the woken
  cloud box.
