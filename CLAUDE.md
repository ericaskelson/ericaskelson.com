# Claude Code Context

Notes for future Claude sessions working on this project.

## Project Overview

Personal website for Eric Askelson (actuary). Static site hosted on GitHub Pages with custom domain ericaskelson.com.

## Key Technical Details

### Windows Environment
- Use `py` instead of `python` for Python commands
- Batch files (`.bat`) need to be run via `cmd /c filename.bat` if calling from bash
- Paths use backslashes but most tools accept forward slashes

### Markdown Rendering
- Resume and About pages use **marked.js** for client-side markdown rendering
- Blog posts are pre-built to HTML via `build.py`
- The same markdown may render slightly differently between marked.js (web) and Pandoc (PDF)

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

**4. Verify paths:**
If the paths have changed, update them in `build-pdf.bat`:
```batch
set PANDOC="%LOCALAPPDATA%\Pandoc\pandoc.exe"
set PDFLATEX="%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"
```

### PDF Spacing Fix
The file `content/resume-header.tex` contains LaTeX overrides to fix spacing after h4 headers (`####` in markdown). Without this, Pandoc's default output runs headers and body text together. The key settings are:
- `parskip=0.5em` - adds space between paragraphs
- `titlesec` package - controls header spacing

### Blog Build System
- `build.py` reads markdown files from `content/blog/`
- Extracts frontmatter (title, date, excerpt)
- Generates HTML using `blog/posts/_template.html`
- Updates the `posts` array in `blog/index.html`
- Files starting with `_` are ignored (e.g., `_draft.md`)

### Git Notes
- The repo is public (required for GitHub Pages with custom domain on free plan)
- CNAME file must exist for custom domain
- GitHub Pages builds from the `main` branch root

## File Purposes

| File | Purpose |
|------|---------|
| `serve.bat` | Start local dev server, auto-opens browser |
| `build.bat` | Run blog build script |
| `build-pdf.bat` | Generate resume PDF with Pandoc |
| `build.py` | Blog post generator (Python) |
| `DEPLOY.md` | GitHub Pages setup instructions |
| `content/resume-header.tex` | LaTeX styling for PDF headers |

## Common Tasks

**User wants to update resume:** Edit `content/resume.md`, then run `build-pdf.bat`

**User wants to add blog post:** Create `content/blog/post-name.md` with frontmatter, run `build.bat`

**User wants to change colors:** Edit CSS variables in `css/styles.css` under `:root`

**PDF looks different from website:** Check `content/resume-header.tex` for LaTeX spacing settings
