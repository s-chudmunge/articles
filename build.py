#!/usr/bin/env python3
"""
Static site generator for s-chudmunge/articles GitHub Pages.
Converts markdown articles into standalone, elegant HTML pages matching the
design system of fep-papers-archive and setr-papers-archive.
"""

import os
import re
import sys
import yaml
import markdown

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Sankalp Chudmunge</title>

<!-- Primary SEO Meta Tags -->
<meta name="title" content="{title}">
<meta name="description" content="{excerpt}">
<meta name="author" content="{author}">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="article">
<meta property="og:url" content="https://s-chudmunge.github.io/articles/{slug}/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:image" content="{hero_image}">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://s-chudmunge.github.io/articles/{slug}/">
<meta property="twitter:title" content="{title}">
<meta property="twitter:description" content="{excerpt}">
<meta property="twitter:image" content="{hero_image}">

<!-- KaTeX for Fast & Pristine LaTeX Math Rendering -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{
      delimiters: [
        {{left: '$$', right: '$$', display: true}},
        {{left: '$', right: '$', display: false}}
      ],
      throwOnError: false
    }});"></script>

<!-- Prism.js for Syntax Highlighting -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-typescript.min.js"></script>

<!-- Twitter Widget for Embedded Tweets -->
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<style>
  :root {{
    --bg-page: #f8fafc;
    --bg-card: #ffffff;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --border-color: #e2e8f0;
    --btn-bg: #f1f5f9;
    --btn-text: #334155;
    --btn-border: #cbd5e1;
    --link-color: #2563eb;
    --link-hover: #1d4ed8;
    --code-bg: #f1f5f9;
    --code-border: #e2e8f0;
    --callout-bg: #f0f9ff;
    --callout-border: #0284c7;
    --table-header: #f8fafc;
    --table-row-hover: #f1f5f9;
    --tag-bg: #eff6ff;
    --tag-text: #1d4ed8;
    --tag-border: #bfdbfe;
  }}

  [data-theme="dark"] {{
    --bg-page: #0b0f19;
    --bg-card: #151d30;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --border-color: #263352;
    --btn-bg: #1e293b;
    --btn-text: #cbd5e1;
    --btn-border: #334155;
    --link-color: #60a5fa;
    --link-hover: #93c5fd;
    --code-bg: #0d1424;
    --code-border: #1e293b;
    --callout-bg: rgba(56, 189, 248, 0.08);
    --callout-border: #38bdf8;
    --table-header: #101728;
    --table-row-hover: #192338;
    --tag-bg: rgba(59, 130, 246, 0.12);
    --tag-text: #93c5fd;
    --tag-border: rgba(59, 130, 246, 0.3);
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg-page);
    color: var(--text-main);
    line-height: 1.8;
    padding: 0 1.25rem 5rem 1.25rem;
    transition: background-color 0.25s ease, color 0.25s ease;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
  }}

  /* Top Navigation */
  .top-nav {{
    max-width: 860px;
    margin: 0 auto;
    padding: 1.75rem 0 1.25rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
  }}

  .nav-brand {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-muted);
    text-decoration: none;
    transition: color 0.2s;
  }}
  .nav-brand:hover {{ color: var(--link-color); }}
  .nav-brand span.author-name {{ color: var(--text-main); font-weight: 700; }}

  .theme-toggle {{
    background: var(--btn-bg);
    border: 1px solid var(--btn-border);
    color: var(--btn-text);
    padding: 0.45rem 0.9rem;
    border-radius: 9999px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    transition: all 0.2s;
  }}
  .theme-toggle:hover {{ opacity: 0.85; border-color: var(--link-color); }}

  /* Reading Progress */
  #progress-bar {{
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: var(--link-color);
    width: 0%;
    z-index: 100;
    transition: width 0.1s ease-out;
  }}

  /* Article Wrapper */
  .article-container {{
    max-width: 860px;
    margin: 2.5rem auto 0 auto;
  }}

  /* Article Header */
  .article-header {{
    margin-bottom: 2rem;
  }}

  .badge-subject {{
    display: inline-block;
    background: var(--tag-bg);
    color: var(--tag-text);
    border: 1px solid var(--tag-border);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 1.25rem;
  }}

  h1.article-title {{
    font-size: clamp(2.1rem, 4.2vw, 2.85rem);
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: -0.025em;
    color: var(--text-main);
    margin-bottom: 1.25rem;
  }}

  .article-meta {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 1.25rem;
    color: var(--text-muted);
    font-size: 0.925rem;
    padding-bottom: 1.75rem;
    border-bottom: 1px solid var(--border-color);
  }}
  .article-meta span {{ display: inline-flex; align-items: center; gap: 0.35rem; }}

  /* Hero Image */
  .hero-image-wrapper {{
    margin: 2.5rem 0;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border-color);
    background: var(--bg-card);
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.06);
  }}
  .hero-image-wrapper img {{
    width: 100%;
    height: auto;
    display: block;
  }}

  /* Technical Insight Callout Box */
  .insight-box {{
    background: var(--callout-bg);
    border-left: 4px solid var(--callout-border);
    border-radius: 0 10px 10px 0;
    padding: 1.4rem 1.75rem;
    margin: 2.25rem 0;
  }}
  .insight-title {{
    font-size: 0.825rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--callout-border);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }}
  .insight-text {{
    font-size: 1.025rem;
    line-height: 1.65;
    color: var(--text-main);
  }}

  /* Article Content Typography */
  .article-content {{
    font-size: 1.1rem;
    color: var(--text-main);
  }}

  .article-content p {{
    margin: 1.5rem 0;
  }}

  .article-content h2 {{
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 3.5rem 0 1.25rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border-color);
    line-height: 1.3;
  }}

  .article-content h3 {{
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.015em;
    margin: 2.4rem 0 0.85rem 0;
    line-height: 1.35;
  }}

  .article-content ul, .article-content ol {{
    margin: 1.25rem 0 1.25rem 1.75rem;
  }}
  .article-content li {{
    margin-bottom: 0.55rem;
  }}

  .article-content a {{
    color: var(--link-color);
    text-decoration: underline;
    text-underline-offset: 3px;
    transition: color 0.15s;
  }}
  .article-content a:hover {{
    color: var(--link-hover);
  }}

  .article-content strong {{
    font-weight: 700;
  }}

  .article-content hr {{
    border: none;
    border-top: 1px solid var(--border-color);
    margin: 3.5rem 0;
  }}

  .article-content blockquote {{
    border-left: 3px solid var(--callout-border);
    background: var(--callout-bg);
    padding: 0.85rem 1.25rem;
    margin: 1.85rem 0;
    border-radius: 0 8px 8px 0;
    color: var(--text-main);
  }}

  /* Inline Code */
  .article-content :not(pre) > code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.88em;
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    color: var(--text-main);
  }}

  /* Code Block Container with Copy Button */
  .code-block-wrapper {{
    position: relative;
    margin: 1.75rem 0;
  }}
  .code-copy-btn {{
    position: absolute;
    top: 0.65rem;
    right: 0.65rem;
    background: rgba(255, 255, 255, 0.1);
    color: #cbd5e1;
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 0.25rem 0.6rem;
    border-radius: 5px;
    font-size: 0.75rem;
    font-family: ui-monospace, monospace;
    cursor: pointer;
    transition: all 0.15s;
    z-index: 10;
  }}
  .code-copy-btn:hover {{
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff;
  }}

  .article-content pre {{
    background: #111827 !important;
    border: 1px solid var(--code-border);
    border-radius: 8px;
    padding: 1.25rem !important;
    overflow-x: auto;
    box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.1);
  }}
  .article-content pre code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.9rem;
    line-height: 1.6;
    background: none !important;
    border: none !important;
    padding: 0 !important;
    color: #f8fafc;
  }}

  /* Content Images */
  .article-content img {{
    max-width: 100%;
    height: auto;
    border-radius: 10px;
    border: 1px solid var(--border-color);
    display: block;
    margin: 2.25rem auto 0.75rem auto;
    box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.06);
  }}
  
  .article-content p > em:only-child,
  .figure-caption {{
    display: block;
    text-align: center;
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-top: 0.5rem;
    margin-bottom: 2rem;
    font-style: italic;
    line-height: 1.5;
  }}

  /* Tables */
  .table-wrapper {{
    width: 100%;
    overflow-x: auto;
    margin: 2.25rem 0;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    box-shadow: 0 2px 8px -2px rgba(0, 0, 0, 0.04);
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95rem;
    background: var(--bg-card);
  }}
  th, td {{
    padding: 0.9rem 1.15rem;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
  }}
  th {{
    background: var(--table-header);
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--text-muted);
  }}
  tr:last-child td {{
    border-bottom: none;
  }}
  tr:hover td {{
    background: var(--table-row-hover);
  }}

  /* Embedded Loom Video */
  .loom-container {{
    position: relative;
    padding-bottom: 56.25%; /* 16:9 aspect ratio */
    height: 0;
    overflow: hidden;
    border-radius: 10px;
    border: 1px solid var(--border-color);
    margin: 2.5rem 0;
    background: var(--bg-card);
    box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.06);
  }}
  .loom-container iframe {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
  }}

  /* Embedded Tweet */
  .tweet-container {{
    margin: 2.5rem 0;
    display: flex;
    justify-content: center;
  }}

  /* Article Footer */
  .article-footer {{
    margin-top: 4.5rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 1.5rem;
    font-size: 0.925rem;
    color: var(--text-muted);
  }}
  .article-footer a {{
    color: var(--link-color);
    text-decoration: none;
  }}
  .article-footer a:hover {{ text-decoration: underline; }}

  /* Back to Top */
  .back-to-top {{
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--btn-bg);
    border: 1px solid var(--btn-border);
    color: var(--btn-text);
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s, transform 0.25s;
    font-size: 1.25rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  }}
  .back-to-top.visible {{
    opacity: 1;
    pointer-events: auto;
  }}
  .back-to-top:hover {{
    transform: translateY(-2px);
    border-color: var(--link-color);
  }}

  @media (max-width: 640px) {{
    body {{ padding: 0 1rem 3rem 1rem; }}
    h1.article-title {{ font-size: 1.85rem; }}
    .article-meta {{ gap: 0.75rem; font-size: 0.85rem; }}
    th, td {{ padding: 0.65rem 0.75rem; font-size: 0.85rem; }}
  }}
</style>
</head>
<body>

<div id="progress-bar"></div>

<header class="top-nav">
  <a href="../" class="nav-brand">
    ← <span class="author-name">Sankalp Chudmunge</span> / articles
  </a>
  <button id="themeToggle" class="theme-toggle" aria-label="Toggle dark mode">
    <span id="themeIcon">🌙</span>
    <span id="themeText">Dark Mode</span>
  </button>
</header>

<main class="article-container">
  <article>
    <header class="article-header">
      <span class="badge-subject">{subject}</span>
      <h1 class="article-title">{title}</h1>
      <div class="article-meta">
        <span>✍️ <strong>{author}</strong></span>
        <span>📅 {date}</span>
        <span>⏱️ {read_time} min read</span>
      </div>
    </header>

    {hero_section}

    {insight_section}

    <div class="article-content">
      {body_html}
    </div>

    <footer class="article-footer">
      <div>
        Published by <strong>{author}</strong> • GitHub Pages
      </div>
      <div>
        <a href="https://github.com/s-chudmunge/articles" target="_blank" rel="noopener">GitHub Repository</a>
      </div>
    </footer>
  </article>
</main>

<button id="backToTop" class="back-to-top" aria-label="Back to top">↑</button>

<script>
  // Reading Progress Bar
  window.addEventListener('scroll', () => {{
    const winScroll = document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    document.getElementById('progress-bar').style.width = scrolled + '%';

    // Back to top toggle
    const btt = document.getElementById('backToTop');
    if (winScroll > 400) {{
      btt.classList.add('visible');
    }} else {{
      btt.classList.remove('visible');
    }}
  }});

  document.getElementById('backToTop').addEventListener('click', () => {{
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }});

  // Theme Toggler with LocalStorage & System Preference
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');
  const themeText = document.getElementById('themeText');

  function initTheme() {{
    const saved = localStorage.getItem('articles_theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (saved === 'dark' || (!saved && prefersDark)) {{
      document.documentElement.setAttribute('data-theme', 'dark');
      themeIcon.textContent = '☀️';
      themeText.textContent = 'Light Mode';
    }} else {{
      document.documentElement.removeAttribute('data-theme');
      themeIcon.textContent = '🌙';
      themeText.textContent = 'Dark Mode';
    }}
  }}
  initTheme();

  themeToggle.addEventListener('click', () => {{
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    if (isDark) {{
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('articles_theme', 'light');
      themeIcon.textContent = '🌙';
      themeText.textContent = 'Dark Mode';
    }} else {{
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('articles_theme', 'dark');
      themeIcon.textContent = '☀️';
      themeText.textContent = 'Light Mode';
    }}
  }});

  // Code Copy Buttons
  document.querySelectorAll('pre').forEach(pre => {{
    const wrapper = document.createElement('div');
    wrapper.className = 'code-block-wrapper';
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);

    const btn = document.createElement('button');
    btn.className = 'code-copy-btn';
    btn.textContent = 'Copy';
    btn.addEventListener('click', () => {{
      const code = pre.querySelector('code') ? pre.querySelector('code').innerText : pre.innerText;
      navigator.clipboard.writeText(code).then(() => {{
        btn.textContent = 'Copied!';
        setTimeout(() => {{ btn.textContent = 'Copy'; }}, 2000);
      }});
    }});
    wrapper.appendChild(btn);
  }});

  // Fix image paths for subdirectories & GitHub Pages
  (function() {{
    const isGH = window.location.pathname.startsWith('/articles');
    document.querySelectorAll('img').forEach(img => {{
      const src = img.getAttribute('src');
      if (src && src.startsWith('/images/')) {{
        // Try relative to parent first
        img.src = '../' + src.replace(/^\\//, '');
        img.onerror = function() {{
          this.onerror = null;
          this.src = (isGH ? '/articles' : '') + src;
        }};
      }}
    }});
  }})();
</script>
</body>
</html>
"""

def estimate_read_time(text):
    words = len(text.split())
    return max(1, round(words / 220))

def parse_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    frontmatter = {}
    body = raw

    match = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.DOTALL)
    if match:
        frontmatter = yaml.safe_load(match.group(1)) or {}
        body = match.group(2)

    return frontmatter, body

def process_custom_blocks(md_text):
    # Process ```tweet <tweet_id> ```
    def tweet_repl(m):
        tweet_id = m.group(1).strip()
        return f'<div class="tweet-container"><blockquote class="twitter-tweet" data-dnt="true"><a href="https://twitter.com/x/status/{tweet_id}"></a></blockquote></div>'

    md_text = re.sub(r'```tweet\s*\n(.*?)\n```', tweet_repl, md_text, flags=re.DOTALL)

    # Process ```loom <video_id> ```
    def loom_repl(m):
        loom_id = m.group(1).strip().replace("https://www.loom.com/share/", "").replace("https://loom.com/share/", "")
        return f'<div class="loom-container"><iframe src="https://www.loom.com/embed/{loom_id}" allowfullscreen></iframe></div>'

    md_text = re.sub(r'```loom\s*\n(.*?)\n```', loom_repl, md_text, flags=re.DOTALL)

    return md_text

def protect_latex(md_text):
    """
    Protects display math $$...$$ and inline math $...$ from being mangled
    by python-markdown (e.g. turning underscores _ into <em>).
    """
    placeholders = []

    def save_math(m):
        idx = len(placeholders)
        placeholders.append(m.group(0))
        return f"KATEXMATHPLACEHOLDER{idx}ENDMATH"

    # Match $$...$$ or $...$ (not across empty lines)
    pattern = re.compile(r'(\$\$.*?\$\$|\$[^\$\n]+?\$)', re.DOTALL)
    protected_text = pattern.sub(save_math, md_text)

    return protected_text, placeholders

def restore_latex(html_text, placeholders):
    for idx, original in enumerate(placeholders):
        html_text = html_text.replace(f"KATEXMATHPLACEHOLDER{idx}ENDMATH", original)
    return html_text

def build_article_html(frontmatter, body_html, raw_body):
    title = frontmatter.get('title', 'Untitled Article')
    slug = frontmatter.get('slug', 'article')
    author = frontmatter.get('author', 'Sankalp Chudmunge')
    date = frontmatter.get('date', '')
    subject = frontmatter.get('subject', 'Article')
    hero_image = frontmatter.get('heroImage', '')
    excerpt = frontmatter.get('excerpt', '')
    technical_insight = frontmatter.get('technicalInsight', '')
    read_time = estimate_read_time(raw_body)

    # Convert root-relative image paths to relative paths for depth-1 directories
    rel_hero = hero_image.lstrip('/')
    if hero_image:
        hero_section = f'<div class="hero-image-wrapper"><img src="../{rel_hero}" alt="{title}"></div>'

    insight_section = ""
    if technical_insight:
        insight_section = f'''<div class="insight-box">
          <div class="insight-title">⚡ Technical Insight</div>
          <div class="insight-text">{technical_insight}</div>
        </div>'''

    # Rewrite /images/ to ../images/ in body_html
    body_html = re.sub(r'src="/images/', r'src="../images/', body_html)

    # Wrap tables in responsive wrapper
    body_html = re.sub(r'(<table>.*?</table>)', r'<div class="table-wrapper">\1</div>', body_html, flags=re.DOTALL)

    # Style captions following images: <p><em>Figure ...</em></p>
    body_html = re.sub(r'<p>(<em>(?:Figure|Table)\s+\d+:.*?</em>)</p>', r'<div class="figure-caption">\1</div>', body_html)

    return HTML_TEMPLATE.format(
        title=title,
        slug=slug,
        author=author,
        date=date,
        subject=subject,
        hero_image=hero_image,
        excerpt=excerpt,
        read_time=read_time,
        hero_section=hero_section,
        insight_section=insight_section,
        body_html=body_html
    )

def build_all():
    md_files = [f for f in os.listdir(PROJECT_DIR) if f.endswith('.md') and f.lower() != 'readme.md']
    print(f"Found {len(md_files)} article(s) to compile.")

    articles_meta = []

    for md_file in md_files:
        filepath = os.path.join(PROJECT_DIR, md_file)
        frontmatter, raw_body = parse_markdown_file(filepath)

        title = frontmatter.get('title', md_file.replace('.md', ''))
        slug = frontmatter.get('slug', md_file.replace('.md', ''))
        short_slug = frontmatter.get('shortSlug')

        processed_body = process_custom_blocks(raw_body)
        protected_body, placeholders = protect_latex(processed_body)

        body_html = markdown.markdown(
            protected_body,
            extensions=['fenced_code', 'tables']
        )

        body_html = restore_latex(body_html, placeholders)

        full_html = build_article_html(frontmatter, body_html, raw_body)

        # Output to <slug>/index.html
        slug_dir = os.path.join(PROJECT_DIR, slug)
        os.makedirs(slug_dir, exist_ok=True)
        slug_out = os.path.join(slug_dir, 'index.html')
        with open(slug_out, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"✓ Generated: {slug}/index.html")

        # Output to <shortSlug>/index.html if defined
        if short_slug and short_slug != slug:
            short_slug_dir = os.path.join(PROJECT_DIR, short_slug)
            os.makedirs(short_slug_dir, exist_ok=True)
            short_slug_out = os.path.join(short_slug_dir, 'index.html')
            with open(short_slug_out, 'w', encoding='utf-8') as f:
                f.write(full_html)
            print(f"✓ Generated alias: {short_slug}/index.html")

        articles_meta.append({
            'title': title,
            'slug': slug,
            'shortSlug': short_slug,
            'date': frontmatter.get('date', ''),
            'subject': frontmatter.get('subject', 'Article'),
            'excerpt': frontmatter.get('excerpt', ''),
            'heroImage': frontmatter.get('heroImage', '')
        })

    # Minimal clean index.html at root (in case root is visited)
    if articles_meta:
        first_article = articles_meta[0]
        root_index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url=./{first_article['slug']}/">
<title>Articles | Sankalp Chudmunge</title>
<script>window.location.href = "./{first_article['slug']}/";</script>
</head>
<body style="font-family: system-ui, sans-serif; padding: 2rem; text-align: center;">
<p>Redirecting to <a href="./{first_article['slug']}/">{first_article['title']}</a>...</p>
</body>
</html>"""
        with open(os.path.join(PROJECT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(root_index)
        print("✓ Generated root redirect index.html")

if __name__ == '__main__':
    build_all()
