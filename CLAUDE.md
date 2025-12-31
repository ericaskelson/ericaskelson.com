# Claude Code Context

Notes for future Claude sessions working on this project.

## Project Overview

Personal website for Eric Askelson (actuary). Static site hosted on GitHub Pages with custom domain ericaskelson.com.

## Key Technical Details

### Windows Environment
- Use `py` instead of `python` for Python commands
- Batch files (`.bat`) need to be run via `cmd /c filename.bat` if calling from bash
- Paths use backslashes but most tools accept forward slashes

### Build System

The site uses a unified `build.py` script that handles all build tasks:

```
py build.py           # Build everything
py build.py blog      # Build blog posts only
py build.py pages     # Build about/resume HTML only
py build.py pdf       # Build resume PDF only
```

Or use `build.bat` which wraps the Python script.

### Static Page Generation
- About and Resume pages are **pre-built to static HTML** from markdown
- Templates live in `templates/about.html` and `templates/resume.html`
- The `{{CONTENT}}` placeholder is replaced with rendered markdown
- Requires the `markdown` Python package: `py -m pip install markdown`
- No JavaScript required for content - fully static HTML

### Blog Build System
- `build.py` reads markdown files from `content/blog/`
- Extracts frontmatter (title, date, excerpt)
- Generates HTML using `blog/posts/_template.html`
- Updates the `posts` array in `blog/index.html`
- Files starting with `_` are ignored (e.g., `_draft.md`)
- **Conditional Blog Link**: If no blog posts exist, the "Blog" nav link is automatically hidden across all pages. When you add posts, it reappears.

### Image Assets
Generated with Nano Banana Pro (Gemini image model). Located in `images/`:
- `bg-watercolor-1.png` - Hero section background (wine/gold watercolor edges)
- `bg-texture-1.png` - Subtle cream marble texture (About/Resume background)
- `bg-geometric-1.png` - Gold hexagon pattern on cream (available)
- `bg-hero-dramatic-1.png` - Bold wine splashes (alternative hero, available)
- `divider-gold-final.png` - Gold calligraphic flourish (hero divider)
- `divider-wine-final.png` - Wine line with diamond (section/title divider)

**Generating transparent images with Nano Banana:**
1. Generate on white background (not transparent checkerboard)
2. Use Python/Pillow to convert white pixels to transparent:
   ```python
   # threshold=240 catches near-white pixels
   if r >= threshold and g >= threshold and b >= threshold:
       pixels[x, y] = (r, g, b, 0)
   ```

### PDF Generation Setup

The resume PDF is generated using Pandoc with MiKTeX (LaTeX). If setting up on a new machine:

**1. Install Pandoc:**
```
winget install JohnMacFarlane.Pandoc
```
Installs to: `%LOCALAPPDATA%\Pandoc\pandoc.exe`

**2. Install MiKTeX:**
```
winget install MiKTeX.MiKTeX
```
Installs to: `%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe`

**3. First PDF build:**
On first run, MiKTeX will prompt to install missing LaTeX packages (titlesec, etc.).
Click "Install" when prompted. This is normal and only happens once per package.

### PDF Spacing Fix
The file `content/resume-header.tex` contains LaTeX overrides to fix spacing after h4 headers (`####` in markdown). Without this, Pandoc's default output runs headers and body text together. The key settings are:
- `parskip=0.5em` - adds space between paragraphs
- `titlesec` package - controls header spacing

### Git Notes
- The repo is public (required for GitHub Pages with custom domain on free plan)
- CNAME file must exist for custom domain
- GitHub Pages builds from the `main` branch root

## File Purposes

| File | Purpose |
|------|---------|
| `serve.bat` | Start local dev server, auto-opens browser |
| `build.bat` | Run unified build script (wraps build.py) |
| `build.py` | Unified build script: blog, pages, and PDF |
| `templates/` | HTML templates for about and resume pages |
| `DEPLOY.md` | GitHub Pages setup instructions |
| `content/resume-header.tex` | LaTeX styling for PDF headers |

## Common Tasks

**User wants to update resume:** Edit `content/resume.md`, then run `py build.py` (or just `py build.py pages pdf`)

**User wants to update about page:** Edit `content/about.md`, then run `py build.py pages`

**User wants to add blog post:** Create `content/blog/post-name.md` with frontmatter, run `py build.py blog`

**User wants to change colors:** Edit CSS variables in `css/styles.css` under `:root`

**PDF looks different from website:** Check `content/resume-header.tex` for LaTeX spacing settings
