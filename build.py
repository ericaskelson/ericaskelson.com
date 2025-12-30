"""
Build script for Eric Askelson's personal website.

This script:
1. Generates blog post HTML files from markdown files in content/blog/
2. Updates the blog index with all posts
3. (Future) Generates PDF from resume markdown

Usage:
    py build.py           # Build everything
    py build.py blog      # Build blog only
    py build.py resume    # Build resume PDF only
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Paths
ROOT = Path(__file__).parent
CONTENT_BLOG = ROOT / "content" / "blog"
BLOG_POSTS = ROOT / "blog" / "posts"
BLOG_INDEX = ROOT / "blog" / "index.html"
TEMPLATE = BLOG_POSTS / "_template.html"

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

def build_blog():
    """Generate HTML files for all blog posts and update the index."""

    if not TEMPLATE.exists():
        print(f"Error: Template not found at {TEMPLATE}")
        return False

    template_content = TEMPLATE.read_text(encoding='utf-8')
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

def build_resume_pdf():
    """
    Generate PDF from resume markdown.
    Requires: pip install markdown weasyprint
    """
    try:
        import markdown
        from weasyprint import HTML, CSS
    except ImportError:
        print("PDF generation requires additional packages.")
        print("Run: pip install markdown weasyprint")
        print("Note: weasyprint also requires GTK libraries on Windows.")
        print("See: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html")
        return False

    resume_md = ROOT / "content" / "resume.md"
    resume_pdf = ROOT / "content" / "resume.pdf"
    css_file = ROOT / "css" / "styles.css"

    if not resume_md.exists():
        print(f"Error: Resume not found at {resume_md}")
        return False

    md_content = resume_md.read_text(encoding='utf-8')
    html_content = markdown.markdown(md_content)

    # Wrap in basic HTML structure
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                color: #2c2c2c;
                max-width: 800px;
                margin: 0 auto;
                padding: 40px;
            }}
            h1 {{ font-size: 24pt; margin-bottom: 5px; }}
            h2 {{ font-size: 14pt; border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-top: 20px; }}
            h3 {{ font-size: 12pt; margin-bottom: 5px; }}
            ul {{ padding-left: 20px; }}
            hr {{ border: none; border-top: 1px solid #ccc; margin: 15px 0; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    HTML(string=full_html).write_pdf(str(resume_pdf))
    print(f"Generated: {resume_pdf}")
    return True

def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else ['all']

    if 'all' in args or 'blog' in args:
        build_blog()

    if 'all' in args or 'resume' in args:
        build_resume_pdf()

if __name__ == '__main__':
    main()
