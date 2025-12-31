"""
Build script for Eric Askelson's personal website.

This script handles all build tasks:
1. Generates blog post HTML files from markdown files in content/blog/
2. Updates the blog index with all posts
3. Generates static HTML for about and resume pages from markdown
4. Generates resume PDF using Pandoc (if available)

Usage:
    py build.py           # Build everything
    py build.py blog      # Build blog only
    py build.py pages     # Build about/resume HTML only
    py build.py pdf       # Build resume PDF only
    py build.py all       # Build everything (explicit)
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime

# Paths
ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
CONTENT_BLOG = CONTENT / "blog"
BLOG_POSTS = ROOT / "blog" / "posts"
BLOG_INDEX = ROOT / "blog" / "index.html"
BLOG_TEMPLATE = BLOG_POSTS / "_template.html"
TEMPLATES = ROOT / "templates"

# Try to import markdown library, fall back to basic conversion
try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False


def md_to_html(md_content):
    """
    Convert markdown to HTML.
    Uses the markdown library if available, otherwise uses basic regex conversion.
    """
    if HAS_MARKDOWN:
        return markdown.markdown(md_content, extensions=['extra', 'smarty'])

    # Basic fallback converter
    html = md_content

    # Headers
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Horizontal rule
    html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)

    # Bold and italic
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

    # Lists (simple)
    lines = html.split('\n')
    in_list = False
    result = []
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    if in_list:
        result.append('</ul>')
    html = '\n'.join(result)

    # Paragraphs (wrap non-tagged text)
    lines = html.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('<'):
            result.append(f'<p>{stripped}</p>')
        else:
            result.append(line)

    return '\n'.join(result)


def extract_frontmatter(markdown_content):
    """
    Extract YAML-like frontmatter from markdown.

    Expected format at top of .md file:
    ---
    title: My Post Title
    date: 2025-01-15
    excerpt: A brief description...
    ---
    """
    frontmatter = {}

    if markdown_content.startswith('---'):
        parts = markdown_content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            for line in fm_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()

    return frontmatter


def get_title_from_markdown(markdown_content):
    """Extract title from first H1 heading if no frontmatter."""
    for line in markdown_content.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    return None


def count_blog_posts():
    """Count the number of publishable blog posts."""
    if not CONTENT_BLOG.exists():
        return 0
    md_files = [f for f in CONTENT_BLOG.glob("*.md") if not f.name.startswith('_')]
    return len(md_files)


def update_blog_links(has_posts):
    """Show or hide blog links in navigation based on whether posts exist."""
    print("\n=== Updating Blog Links ===")

    # Files to update (with their blog link patterns)
    files_to_update = [
        (ROOT / "index.html", 'href="blog/index.html"'),
        (ROOT / "about.html", 'href="blog/index.html"'),
        (ROOT / "resume.html", 'href="blog/index.html"'),
        (TEMPLATES / "about.html", 'href="blog/index.html"'),
        (TEMPLATES / "resume.html", 'href="blog/index.html"'),
        (BLOG_TEMPLATE, 'href="../index.html"'),  # Blog template uses relative path
    ]

    # Pattern to match the blog nav link (both visible and hidden versions)
    # Matches: <a href="..." class="nav-link">Blog</a>
    # Or: <!-- BLOG_LINK <a href="..." class="nav-link">Blog</a> -->

    for file_path, href_pattern in files_to_update:
        if not file_path.exists():
            continue

        content = file_path.read_text(encoding='utf-8')
        original = content

        if has_posts:
            # Uncomment the blog link if it's hidden
            # Pattern: <!-- BLOG_LINK <a ...>Blog</a> -->
            pattern = r'<!-- BLOG_LINK (<a[^>]*class="nav-link"[^>]*>Blog</a>) -->'
            content = re.sub(pattern, r'\1', content)
        else:
            # Comment out the blog link if it exists and isn't already hidden
            # Find: <a href="..." class="nav-link">Blog</a> (not already in comment)
            # But don't match if it's already wrapped in <!-- BLOG_LINK ... -->

            # First check if there's an uncommented blog link
            pattern = r'(<a[^>]*href="[^"]*blog[^"]*"[^>]*class="nav-link"[^>]*>Blog</a>)'
            if re.search(pattern, content, re.IGNORECASE):
                # Only wrap if not already wrapped
                if '<!-- BLOG_LINK' not in content:
                    content = re.sub(pattern, r'<!-- BLOG_LINK \1 -->', content, flags=re.IGNORECASE)

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            status = "shown" if has_posts else "hidden"
            print(f"  {file_path.name}: Blog link {status}")

    print(f"Blog links {'visible' if has_posts else 'hidden'} (posts: {count_blog_posts()})")


def build_blog():
    """Generate HTML files for all blog posts and update the index."""
    print("\n=== Building Blog ===")

    if not BLOG_TEMPLATE.exists():
        print(f"Error: Template not found at {BLOG_TEMPLATE}")
        return False

    template_content = BLOG_TEMPLATE.read_text(encoding='utf-8')
    posts = []

    # Find all markdown files (excluding those starting with _)
    md_files = [f for f in CONTENT_BLOG.glob("*.md") if not f.name.startswith('_')]

    print(f"Found {len(md_files)} blog post(s) to process...")

    for md_file in md_files:
        slug = md_file.stem
        content = md_file.read_text(encoding='utf-8')

        # Try to get metadata from frontmatter
        frontmatter = extract_frontmatter(content)

        title = frontmatter.get('title') or get_title_from_markdown(content) or slug.replace('-', ' ').title()
        date = frontmatter.get('date') or datetime.fromtimestamp(md_file.stat().st_mtime).strftime('%Y-%m-%d')
        excerpt = frontmatter.get('excerpt') or ''

        # Format date for display
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_display = date_obj.strftime('%B %d, %Y')
        except:
            date_display = date

        # Generate HTML file
        html_content = template_content
        html_content = html_content.replace('POST_TITLE', title)
        html_content = html_content.replace('POST_DATE', date_display)
        html_content = html_content.replace('POST_EXCERPT', excerpt)
        html_content = html_content.replace('POST_SLUG', slug)

        output_path = BLOG_POSTS / f"{slug}.html"
        output_path.write_text(html_content, encoding='utf-8')
        print(f"  Generated: {output_path.name}")

        posts.append({
            'slug': slug,
            'title': title,
            'date': date,
            'excerpt': excerpt
        })

    # Sort posts by date (newest first)
    posts.sort(key=lambda p: p['date'], reverse=True)

    # Update blog index
    update_blog_index(posts)

    print(f"Blog build complete! {len(posts)} post(s) processed.")
    return True


def update_blog_index(posts):
    """Update the posts array in blog/index.html."""

    if not BLOG_INDEX.exists():
        print(f"Error: Blog index not found at {BLOG_INDEX}")
        return

    content = BLOG_INDEX.read_text(encoding='utf-8')

    # Generate the new posts array
    posts_json = json.dumps(posts, indent=12)
    # Fix indentation for embedding in JS
    posts_js = posts_json.replace('\n', '\n        ')

    # Replace the posts array using regex
    pattern = r'const posts = \[[\s\S]*?\];'
    replacement = f'const posts = {posts_js};'

    new_content = re.sub(pattern, replacement, content)

    BLOG_INDEX.write_text(new_content, encoding='utf-8')
    print(f"  Updated: blog/index.html")


def build_pages():
    """Generate static HTML for about and resume pages from markdown."""
    print("\n=== Building Static Pages ===")

    pages = [
        ('about.md', 'about.html'),
        ('resume.md', 'resume.html'),
    ]

    for md_file, html_file in pages:
        md_path = CONTENT / md_file
        template_path = TEMPLATES / html_file
        output_path = ROOT / html_file

        if not md_path.exists():
            print(f"  Skipping {html_file}: {md_file} not found")
            continue

        if not template_path.exists():
            print(f"  Skipping {html_file}: template not found")
            continue

        # Read markdown and convert to HTML
        md_content = md_path.read_text(encoding='utf-8')
        html_content = md_to_html(md_content)

        # Read template and inject content
        template = template_path.read_text(encoding='utf-8')
        final_html = template.replace('{{CONTENT}}', html_content)

        # Write output
        output_path.write_text(final_html, encoding='utf-8')
        print(f"  Generated: {html_file}")

    if not HAS_MARKDOWN:
        print("  Note: Install 'markdown' package for better rendering: pip install markdown")

    print("Static pages build complete!")
    return True


def build_pdf():
    """Generate resume PDF using Pandoc."""
    print("\n=== Building Resume PDF ===")

    resume_md = CONTENT / "resume.md"
    resume_header = CONTENT / "resume-header.tex"

    if not resume_md.exists():
        print(f"Error: Resume not found at {resume_md}")
        return False

    # Find Pandoc
    pandoc_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Pandoc\pandoc.exe"),
        "pandoc",  # Try system PATH
    ]

    pandoc = None
    for p in pandoc_paths:
        try:
            result = subprocess.run([p, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                pandoc = p
                break
        except FileNotFoundError:
            continue

    if not pandoc:
        print("Error: Pandoc not found. Install with: winget install JohnMacFarlane.Pandoc")
        return False

    # Find pdflatex
    pdflatex_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"),
        "pdflatex",  # Try system PATH
    ]

    pdflatex = None
    for p in pdflatex_paths:
        try:
            result = subprocess.run([p, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                pdflatex = p
                break
        except FileNotFoundError:
            continue

    if not pdflatex:
        print("Error: pdflatex not found. Install MiKTeX with: winget install MiKTeX.MiKTeX")
        return False

    # Generate date stamp
    datestamp = datetime.now().strftime('%Y-%m-%d')
    dated_output = CONTENT / f"Eric_Askelson_Resume_{datestamp}.pdf"
    main_output = CONTENT / "Eric_Askelson_Resume.pdf"

    # Build Pandoc command
    cmd = [
        pandoc,
        str(resume_md),
        "-o", str(dated_output),
        f"--pdf-engine={pdflatex}",
        "-V", "geometry:margin=0.75in",
        "-V", "fontsize=11pt",
        "-V", "colorlinks=true",
        "-V", "linkcolor=blue",
        "-V", "parskip=0.5em",
        "--metadata", "title=",
    ]

    # Add header file if it exists
    if resume_header.exists():
        cmd.extend(["-H", str(resume_header)])

    print(f"  Running Pandoc...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error generating PDF:")
        print(result.stderr)
        return False

    print(f"  Generated: {dated_output.name}")

    # Copy to main output file
    import shutil
    shutil.copy(dated_output, main_output)
    print(f"  Copied to: {main_output.name}")

    print("PDF build complete!")
    return True


def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else ['all']

    # Normalize arguments
    args = [a.lower() for a in args]

    success = True
    is_full_build = 'all' in args

    if is_full_build:
        args = ['blog', 'pages', 'pdf']

    if 'blog' in args:
        success = build_blog() and success

    if 'pages' in args:
        success = build_pages() and success

    if 'pdf' in args:
        success = build_pdf() and success

    # Legacy support: 'resume' now means both pages and pdf
    if 'resume' in args:
        success = build_pages() and success
        success = build_pdf() and success

    # Update blog link visibility based on post count (always run on full build)
    if is_full_build or 'blog' in args or 'pages' in args:
        has_posts = count_blog_posts() > 0
        update_blog_links(has_posts)

    print("\n" + "=" * 40)
    if success:
        print("All builds completed successfully!")
    else:
        print("Some builds had errors.")

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
