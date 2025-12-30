# Eric Askelson's Personal Website

A personal website hosted on GitHub Pages at [ericaskelson.com](https://ericaskelson.com).

## Site Structure

```
personal-website/
├── index.html              # Home page
├── about.html              # About page (loads markdown)
├── resume.html             # Resume page (loads markdown)
├── 404.html                # Custom error page
├── CNAME                   # Custom domain config for GitHub Pages
├── css/
│   └── styles.css          # All site styles (Warm Wine theme)
├── content/
│   ├── about.md            # About page content (edit this)
│   ├── resume.md           # Resume content (edit this)
│   ├── resume-header.tex   # LaTeX styling for PDF generation
│   ├── Eric_Askelson_Resume.pdf        # Current PDF for download
│   ├── Eric_Askelson_Resume_YYYY-MM-DD.pdf  # Dated archive copies
│   └── blog/
│       └── *.md            # Blog posts in markdown
├── blog/
│   ├── index.html          # Blog listing page
│   └── posts/
│       ├── _template.html  # Template for generated posts
│       └── *.html          # Generated blog post pages
├── images/
│   └── Profile.jpg         # Profile photo
├── build.py                # Blog post generator script
├── build.bat               # Runs build.py
├── build-pdf.bat           # Generates resume PDF via Pandoc
└── serve.bat               # Starts local dev server
```

## Local Development

Start the local server:
```
serve.bat
```
This opens your browser to http://localhost:8000 automatically.

## Updating Pages

### Home Page (index.html)
Edit `index.html` directly. The hero section and Connect links are plain HTML.

### About Page
Edit `content/about.md` in markdown. Changes appear immediately on refresh (no build step needed).

### Resume Page
Edit `content/resume.md` in markdown. Changes appear immediately on the web page.

**To update the PDF download:**
```
build-pdf.bat
```
This generates a dated PDF and copies it to `Eric_Askelson_Resume.pdf` for the download link.

### Blog Posts

1. Create a new markdown file in `content/blog/` with frontmatter:
   ```markdown
   ---
   title: Your Post Title
   date: 2025-01-15
   excerpt: A brief description for the listing page.
   ---

   Your post content here...
   ```

2. Run the build script:
   ```
   build.bat
   ```
   This generates the HTML file and updates the blog index.

3. To remove a post, delete the `.md` file from `content/blog/` and run `build.bat` again.

## Deploying Changes

All changes deploy automatically when pushed to GitHub:
```
git add -A
git commit -m "Your commit message"
git push
```

GitHub Pages typically updates within 1-2 minutes.

## Dependencies

- **Python** - For local server (`py -m http.server`) and blog build script
- **Pandoc** - For PDF generation (see CLAUDE.md for installation)
- **MiKTeX** - LaTeX engine for Pandoc PDF output (see CLAUDE.md for installation)

## Theme

The site uses a "Warm Wine" color palette defined in CSS variables in `styles.css`:
- Primary: `#5c1a23` (burgundy)
- Accent: `#b8860b` (gold)
- Background: `#faf8f4` (cream)
