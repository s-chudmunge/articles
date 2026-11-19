#!/usr/bin/env python3
"""
Static site generator for s-chudmunge/articles GitHub Pages.
Generates an academic-grade, typography-first reading experience inspired by
Zongyi Li's research blog (al-folio academic jekyll style) with LaTeX Booktabs table styling.
"""

import os
import re
import sys
import yaml
import markdown
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://s-chudmunge.github.io/articles"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_meta_title} | Sankalp Chudmunge</title>

<!-- Primary SEO Meta Tags -->
<meta name="title" content="{full_meta_title}">
<meta name="description" content="{excerpt}">
<meta name="author" content="{author}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{canonical_url}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="Sankalp Chudmunge">
<meta property="og:url" content="{canonical_url}">
<meta property="og:title" content="{full_meta_title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="article:published_time" content="{published_iso}">
<meta property="article:author" content="https://github.com/s-chudmunge">
<meta property="article:section" content="{subject}">

<!-- Twitter Cards -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@CompleteSkeptic">
<meta name="twitter:creator" content="@CompleteSkeptic">
<meta name="twitter:url" content="{canonical_url}">
<meta name="twitter:title" content="{full_meta_title}">
<meta name="twitter:description" content="{excerpt}">
<meta name="twitter:image" content="{og_image}">

<!-- Schema.org JSON-LD Structured Data -->
<script type="application/ld+json">
{schema_json}
</script>

<!-- Clean Academic Typography Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&display=swap" rel="stylesheet">

<!-- KaTeX for High-Precision LaTeX Math Rendering -->
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

<!-- Twitter Widget for Embedded Tweets -->
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<style>
  :root {{
    /* Al-Folio Academic Theme Colors (Light Mode) */
    --bg-page: #ffffff;
    --bg-card: #f8f9fa;
    --text-main: #24292f;
    --text-muted: #6e7781;
    --border-color: #e8e8e8;
    --border-subtle: #f0f2f5;
    --link-color: #00369f;
    --link-hover: #002266;
    --code-bg: #f6f8fa;
    --code-border: #e1e4e8;
    --quote-bg: #f8f9fb;
    --quote-border: #00369f;
    --nav-bg: rgba(255, 255, 255, 0.95);
    --btn-bg: #f3f4f6;
    --btn-text: #24292f;
    --btn-border: #d0d7de;
    
    /* Academic Booktabs Table Rules */
    --table-rule-thick: #24292f;
    --table-rule-thin: #d0d7de;
    --table-row-hover: rgba(0, 0, 0, 0.02);
    
    /* Academic Typography */
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    --font-serif: 'Newsreader', Georgia, Cambria, serif;
    --font-mono: 'JetBrains Mono', "Source Code Pro", Consolas, monospace;
    --font-body: var(--font-sans);
  }}

  [data-theme="dark"] {{
    /* High-Contrast Academic Dark Mode */
    --bg-page: #0d1117;
    --bg-card: #161b22;
    --text-main: #c9d1d9;
    --text-muted: #8b949e;
    --border-color: #30363d;
    --border-subtle: #21262d;
    --link-color: #58a6ff;
    --link-hover: #79b8ff;
    --code-bg: #161b22;
    --code-border: #30363d;
    --quote-bg: #131922;
    --quote-border: #388bfd;
    --nav-bg: rgba(13, 17, 23, 0.95);
    --btn-bg: #21262d;
    --btn-text: #c9d1d9;
    --btn-border: #363b42;
    
    --table-rule-thick: #c9d1d9;
    --table-rule-thin: #30363d;
    --table-row-hover: rgba(255, 255, 255, 0.03);
  }}

  /* Font Mode Switcher */
  [data-font="serif"] {{
    --font-body: var(--font-serif);
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  
  html {{
    scroll-behavior: smooth;
    scroll-padding-top: 5rem;
  }}

  body {{
    font-family: var(--font-body);
    background-color: var(--bg-page);
    color: var(--text-main);
    line-height: 1.78;
    padding: 0 0 5rem 0;
    transition: background-color 0.25s ease, color 0.25s ease;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
  }}

  /* Reading Progress Bar */
  #progress-bar {{
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: var(--link-color);
    width: 0%;
    z-index: 100;
    transition: width 0.08s ease-out;
  }}

  /* Fixed Academic Site Header (Al-Folio Style) */
  .site-header {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: var(--nav-bg);
    border-bottom: 1px solid var(--border-color);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    z-index: 50;
    height: 56px;
  }}

  .header-wrapper {{
    max-width: 820px;
    margin: 0 auto;
    padding: 0 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
  }}

  .site-title {{
    font-family: var(--font-sans);
    font-size: 1.15rem;
    font-weight: 400;
    color: var(--text-main);
    text-decoration: none;
    letter-spacing: -0.02em;
  }}
  .site-title strong {{
    font-weight: 700;
    color: var(--text-main);
  }}

  .site-nav {{
    display: flex;
    align-items: center;
    gap: 1.25rem;
  }}

  .site-nav a {{
    font-family: var(--font-sans);
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.15s;
  }}
  .site-nav a:hover {{
    color: var(--link-color);
  }}

  .control-btn {{
    background: var(--btn-bg);
    border: 1px solid var(--btn-border);
    color: var(--btn-text);
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    cursor: pointer;
    font-family: var(--font-sans);
    font-size: 0.8rem;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    transition: all 0.15s;
  }}
  .control-btn:hover {{
    border-color: var(--link-color);
  }}

  /* Content Wrapper: 760px Academic Reading Measure */
  .page-content {{
    padding-top: 5.5rem;
  }}

  .post-wrapper {{
    max-width: 780px;
    margin: 0 auto;
    padding: 0 25px;
  }}

  /* Post Header */
  .post-header {{
    margin-bottom: 2.25rem;
  }}

  .post-category {{
    display: inline-block;
    color: var(--link-color);
    font-family: var(--font-sans);
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.75rem;
  }}

  h1.post-title {{
    font-family: var(--font-sans);
    font-size: clamp(2.35rem, 4.5vw, 3rem);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.03em;
    color: var(--text-main);
    margin-bottom: 0.6rem;
  }}

  .post-subtitle {{
    font-family: var(--font-sans);
    font-size: 1.3rem;
    font-weight: 400;
    line-height: 1.45;
    color: var(--text-muted);
    margin-bottom: 1.15rem;
  }}

  .post-meta {{
    color: var(--text-muted);
    font-family: var(--font-sans);
    font-size: 0.925rem;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-color);
  }}
  .post-meta span.separator {{
    opacity: 0.4;
  }}

  /* Post Content Typography */
  .post-content {{
    font-size: 1.125rem;
    line-height: 1.82;
    color: var(--text-main);
  }}

  .post-content p {{
    margin: 1.55rem 0;
  }}

  .post-content h2 {{
    font-family: var(--font-sans);
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-top: 3.5rem;
    margin-bottom: 1.15rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border-color);
    line-height: 1.3;
    position: relative;
  }}

  .post-content h3 {{
    font-family: var(--font-sans);
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.015em;
    margin-top: 2.5rem;
    margin-bottom: 0.85rem;
    line-height: 1.35;
    position: relative;
  }}

  .heading-anchor {{
    position: absolute;
    left: -1.35rem;
    top: 0;
    color: var(--text-muted);
    text-decoration: none;
    opacity: 0;
    font-weight: 400;
    transition: opacity 0.15s, color 0.15s;
  }}
  h2:hover .heading-anchor, h3:hover .heading-anchor {{
    opacity: 0.65;
  }}
  .heading-anchor:hover {{
    opacity: 1 !important;
    color: var(--link-color);
  }}

  .post-content ul, .post-content ol {{
    margin: 1.35rem 0 1.35rem 1.75rem;
  }}
  .post-content li {{
    margin-bottom: 0.55rem;
  }}

  .post-content a {{
    color: var(--link-color);
    text-decoration: underline;
    text-underline-offset: 3px;
    transition: color 0.15s;
  }}
  .post-content a:hover {{
    color: var(--link-hover);
  }}

  .post-content strong {{
    font-weight: 700;
  }}

  .post-content hr {{
    border: none;
    border-top: 1px solid var(--border-color);
    margin: 3.5rem 0;
  }}

  /* Academic Blockquote Style (Al-Folio) */
  .post-content blockquote {{
    border-left: 3px solid var(--quote-border);
    background-color: var(--quote-bg);
    padding: 1.15rem 1.5rem;
    margin: 2rem 0;
    border-radius: 0 8px 8px 0;
    font-size: 1.05rem;
    line-height: 1.7;
    color: var(--text-main);
  }}
  .post-content blockquote p {{
    margin: 0.5rem 0;
  }}
  .post-content blockquote p:first-child {{ margin-top: 0; }}
  .post-content blockquote p:last-child {{ margin-bottom: 0; }}

  /* Inline Code */
  .post-content :not(pre) > code {{
    font-family: var(--font-mono);
    font-size: 0.88em;
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    color: var(--text-main);
  }}

  /* Code Blocks */
  .code-block-wrapper {{
    position: relative;
    margin: 2rem 0;
  }}
  .code-copy-btn {{
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
    background: rgba(255, 255, 255, 0.12);
    color: #cbd5e1;
    border: 1px solid rgba(255, 255, 255, 0.18);
    padding: 0.25rem 0.65rem;
    border-radius: 5px;
    font-size: 0.75rem;
    font-family: var(--font-sans);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
    z-index: 10;
  }}
  .code-copy-btn:hover {{
    background: rgba(255, 255, 255, 0.22);
    color: #ffffff;
  }}

  .post-content pre {{
    background: #0f141c !important;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1.35rem !important;
    overflow-x: auto;
  }}
  .post-content pre code {{
    font-family: var(--font-mono);
    font-size: 0.925rem;
    line-height: 1.65;
    background: none !important;
    border: none !important;
    padding: 0 !important;
    color: #f1f5f9;
  }}

  /* Academic Figure Layout (.img_row and .caption matching Zongyi Li) */
  .img_row {{
    margin: 2.5rem 0 0.5rem 0;
    text-align: center;
  }}
  .img_row img {{
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    display: inline-block;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.06);
  }}
  .caption {{
    text-align: center;
    color: var(--text-muted);
    font-family: var(--font-sans);
    font-size: 0.885rem;
    line-height: 1.55;
    font-style: italic;
    margin-bottom: 2.25rem;
    padding: 0 1rem;
  }}

  /* ====================================================================
     Academic Booktabs Table Styling (LaTeX / Nature Journal Style)
     Zero ChatGPT boxiness: no outer box, no vertical rules, crisp rules
     ==================================================================== */
  .table-wrapper {{
    width: 100%;
    overflow-x: auto;
    margin: 2.75rem 0 0.65rem 0;
    background: transparent;
    border: none;
    box-shadow: none;
  }}
  table.booktabs {{
    width: 100%;
    border-collapse: collapse;
    font-family: var(--font-sans);
    font-size: 0.935rem;
    line-height: 1.55;
    border-top: 2.2px solid var(--table-rule-thick);
    border-bottom: 2.2px solid var(--table-rule-thick);
    background: transparent;
  }}
  table.booktabs th {{
    font-weight: 700;
    font-size: 0.835rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-main);
    padding: 0.85rem 1.15rem;
    border-top: none;
    border-left: none;
    border-right: none;
    border-bottom: 1.2px solid var(--table-rule-thick);
    background: transparent;
    vertical-align: bottom;
    text-align: left;
  }}
  table.booktabs td {{
    padding: 0.85rem 1.15rem;
    border-top: none;
    border-left: none;
    border-right: none;
    border-bottom: 1px solid var(--table-rule-thin);
    vertical-align: top;
    color: var(--text-main);
    background: transparent;
    text-align: left;
  }}
  table.booktabs tr:last-child td {{
    border-bottom: none;
  }}
  table.booktabs tr:hover td {{
    background-color: var(--table-row-hover);
  }}
  .table-caption {{
    font-family: var(--font-sans);
    font-size: 0.875rem;
    color: var(--text-muted);
    font-style: italic;
    margin-top: 0.65rem;
    margin-bottom: 2.75rem;
    line-height: 1.55;
    text-align: left;
  }}

  /* Embedded Loom Video */
  .loom-container {{
    position: relative;
    padding-bottom: 56.25%;
    height: 0;
    overflow: hidden;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    margin: 2.5rem 0;
    background: var(--bg-card);
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

  /* Post Footer */
  .post-footer {{
    margin-top: 4.5rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 1.25rem;
    font-family: var(--font-sans);
    font-size: 0.9rem;
    color: var(--text-muted);
  }}
  .post-footer a {{
    color: var(--link-color);
    text-decoration: none;
  }}
  .post-footer a:hover {{ text-decoration: underline; }}

  /* Back to Top Floating Button */
  .back-to-top {{
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--btn-bg);
    border: 1px solid var(--btn-border);
    color: var(--btn-text);
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s, transform 0.25s;
    font-size: 1.2rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    z-index: 80;
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
    .header-wrapper {{ padding: 0 15px; }}
    .site-nav {{ gap: 0.75rem; }}
    .post-wrapper {{ padding: 0 16px; }}
    h1.post-title {{ font-size: 2rem; }}
    .post-subtitle {{ font-size: 1.15rem; }}
    .post-content {{ font-size: 1.05rem; }}
    table.booktabs th, table.booktabs td {{ padding: 0.65rem 0.75rem; font-size: 0.85rem; }}
  }}
</style>
</head>
<body>

<div id="progress-bar"></div>

<header class="site-header">
  <div class="header-wrapper">
    <a href="../" class="site-title">
      <strong>Sankalp</strong> Chudmunge
    </a>
    <nav class="site-nav">
      <a href="https://github.com/s-chudmunge" target="_blank" rel="noopener">GitHub</a>
      <button id="fontToggle" class="control-btn" aria-label="Toggle serif / sans font">
        <span id="fontIcon">📖</span>
        <span id="fontText">Serif</span>
      </button>
      <button id="themeToggle" class="control-btn" aria-label="Toggle dark mode">
        <span id="themeIcon">🌙</span>
        <span id="themeText">Dark</span>
      </button>
    </nav>
  </div>
</header>

<div class="page-content">
  <div class="post-wrapper">
    <main class="post">
      <header class="post-header">
        <span class="post-category">{subject}</span>
        <h1 class="post-title">{title}</h1>
        {subtitle_html}
        <p class="post-meta">
          <span>{date}</span>
          <span class="separator">•</span>
          <span>By {author}</span>
          <span class="separator">•</span>
          <span>{read_time} min read</span>
        </p>
      </header>

      {insight_section}

      {hero_section}

      <article class="post-content">
        {body_html}
      </article>

      <footer class="post-footer">
        <div>
          Published by <strong>{author}</strong> • <a href="https://github.com/s-chudmunge/articles" target="_blank" rel="noopener">articles repository</a>
        </div>
        <div>
          <a href="#top" onclick="window.scrollTo({{ top: 0, behavior: 'smooth' }}); return false;">Back to top ↑</a>
        </div>
      </footer>
    </main>
  </div>
</div>

<button id="backToTop" class="back-to-top" aria-label="Back to top">↑</button>

<script>
  // Reading Progress Bar & Back to top
  window.addEventListener('scroll', () => {{
    const winScroll = document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    document.getElementById('progress-bar').style.width = scrolled + '%';

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

  // Theme Toggler
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');
  const themeText = document.getElementById('themeText');

  function initTheme() {{
    const saved = localStorage.getItem('articles_theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (saved === 'dark' || (!saved && prefersDark)) {{
      document.documentElement.setAttribute('data-theme', 'dark');
      themeIcon.textContent = '☀️';
      themeText.textContent = 'Light';
    }} else {{
      document.documentElement.removeAttribute('data-theme');
      themeIcon.textContent = '🌙';
      themeText.textContent = 'Dark';
    }}
  }}
  initTheme();

  themeToggle.addEventListener('click', () => {{
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    if (isDark) {{
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('articles_theme', 'light');
      themeIcon.textContent = '🌙';
      themeText.textContent = 'Dark';
    }} else {{
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('articles_theme', 'dark');
      themeIcon.textContent = '☀️';
      themeText.textContent = 'Light';
    }}
  }});

  // Font Switcher (Serif / Sans)
  const fontToggle = document.getElementById('fontToggle');
  const fontIcon = document.getElementById('fontIcon');
  const fontText = document.getElementById('fontText');

  function initFont() {{
    const savedFont = localStorage.getItem('articles_font');
    if (savedFont === 'serif') {{
      document.documentElement.setAttribute('data-font', 'serif');
      fontIcon.textContent = '🔤';
      fontText.textContent = 'Sans';
    }} else {{
      document.documentElement.removeAttribute('data-font');
      fontIcon.textContent = '📖';
      fontText.textContent = 'Serif';
    }}
  }}
  initFont();

  fontToggle.addEventListener('click', () => {{
    const isSerif = document.documentElement.getAttribute('data-font') === 'serif';
    if (isSerif) {{
      document.documentElement.removeAttribute('data-font');
      localStorage.setItem('articles_font', 'sans');
      fontIcon.textContent = '📖';
      fontText.textContent = 'Serif';
    }} else {{
      document.documentElement.setAttribute('data-font', 'serif');
      localStorage.setItem('articles_font', 'serif');
      fontIcon.textContent = '🔤';
      fontText.textContent = 'Sans';
    }}
  }});

  // Code Block Copy Buttons
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

  // Fix image paths
  (function() {{
    const isGH = window.location.pathname.startsWith('/articles');
    document.querySelectorAll('img').forEach(img => {{
      const src = img.getAttribute('src');
      if (src && src.startsWith('/images/')) {{
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
    def tweet_repl(m):
        tweet_id = m.group(1).strip()
        return f'<div class="tweet-container"><blockquote class="twitter-tweet" data-dnt="true"><a href="https://twitter.com/x/status/{tweet_id}"></a></blockquote></div>'

    md_text = re.sub(r'```tweet\s*\n(.*?)\n```', tweet_repl, md_text, flags=re.DOTALL)

    def loom_repl(m):
        loom_id = m.group(1).strip().replace("https://www.loom.com/share/", "").replace("https://loom.com/share/", "")
        return f'<div class="loom-container"><iframe src="https://www.loom.com/embed/{loom_id}" allowfullscreen></iframe></div>'

    md_text = re.sub(r'```loom\s*\n(.*?)\n```', loom_repl, md_text, flags=re.DOTALL)

    return md_text

def protect_latex(md_text):
    placeholders = []

    def save_math(m):
        idx = len(placeholders)
        placeholders.append(m.group(0))
        return f"KATEXMATHPLACEHOLDER{idx}ENDMATH"

    pattern = re.compile(r'(\$\$.*?\$\$|\$[^\$\n]+?\$)', re.DOTALL)
    protected_text = pattern.sub(save_math, md_text)

    return protected_text, placeholders

def restore_latex(html_text, placeholders):
    for idx, original in enumerate(placeholders):
        html_text = html_text.replace(f"KATEXMATHPLACEHOLDER{idx}ENDMATH", original)
    return html_text

def extract_headings_and_add_ids(html_text):
    used_slugs = set()

    def repl(m):
        level = m.group(1)
        text = m.group(2)
        clean_text = re.sub(r'<.*?>', '', text)
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', clean_text.lower()).strip('-')
        if not slug:
            slug = f"section-{len(used_slugs)}"
        if slug in used_slugs:
            slug = f"{slug}-{len(used_slugs)}"
        used_slugs.add(slug)
        return f'<h{level} id="{slug}"><a href="#{slug}" class="heading-anchor" aria-hidden="true">#</a>{text}</h{level}>'

    return re.sub(r'<h([23])>(.*?)</h\1>', repl, html_text, flags=re.DOTALL)

def build_schema_json(frontmatter, canonical_url, og_image, excerpt, full_meta_title):
    author = frontmatter.get('author', 'Sankalp Chudmunge')
    date_str = frontmatter.get('date', 'September 25, 2026')
    try:
        dt = datetime.strptime(date_str, "%B %d, %Y")
        iso_date = dt.strftime("%Y-%m-%d")
    except Exception:
        iso_date = "2026-09-25"

    synonyms = frontmatter.get('synonyms', [])
    keywords_list = ["Machine Learning", "Artificial Intelligence"] + synonyms

    import json
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "@id": f"{canonical_url}#article",
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": f"{SITE_URL}/#website",
                    "name": "Sankalp Chudmunge Articles",
                    "url": f"{SITE_URL}/"
                },
                "headline": full_meta_title,
                "description": excerpt,
                "image": og_image,
                "datePublished": f"{iso_date}T00:00:00Z",
                "dateModified": f"{iso_date}T00:00:00Z",
                "inLanguage": "en-US",
                "mainEntityOfPage": canonical_url,
                "author": {
                    "@type": "Person",
                    "name": author,
                    "url": "https://github.com/s-chudmunge"
                },
                "publisher": {
                    "@type": "Person",
                    "name": author,
                    "url": "https://github.com/s-chudmunge"
                },
                "keywords": keywords_list,
                "articleSection": frontmatter.get('subject', 'Machine Learning')
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://s-chudmunge.github.io/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Articles",
                        "item": f"{SITE_URL}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": frontmatter.get('title', 'Article')
                    }
                ]
            }
        ]
    }
    return json.dumps(schema, indent=2)

def build_article_html(frontmatter, body_html, raw_body):
    title = frontmatter.get('title', 'What is Jev?')
    subtitle = frontmatter.get('subtitle', '')
    slug = frontmatter.get('slug', 'what-is-jev')
    author = frontmatter.get('author', 'Sankalp Chudmunge')
    date = frontmatter.get('date', '')
    subject = frontmatter.get('subject', 'Machine Learning')
    hero_image = frontmatter.get('heroImage', '')
    excerpt = frontmatter.get('excerpt', '')
    technical_insight = frontmatter.get('technicalInsight', '')
    read_time = estimate_read_time(raw_body)

    canonical_url = f"{SITE_URL}/{slug}/"
    og_image = f"{SITE_URL}{hero_image}" if hero_image.startswith('/') else f"{SITE_URL}/{hero_image}"

    full_meta_title = f"{title}: {subtitle}" if subtitle else title

    synonyms = frontmatter.get('synonyms', [])
    keywords = ", ".join([title, subject, author] + synonyms)

    try:
        dt = datetime.strptime(date, "%B %d, %Y")
        published_iso = dt.strftime("%Y-%m-%dT00:00:00Z")
    except Exception:
        published_iso = "2026-09-25T00:00:00Z"

    # Subtitle HTML
    subtitle_html = f'<p class="post-subtitle">{subtitle}</p>' if subtitle else ''

    # Convert root-relative image paths to relative paths
    rel_hero = hero_image.lstrip('/')
    hero_section = ""
    if hero_image:
        hero_section = f'<div class="img_row"><img src="../{rel_hero}" alt="{title}"></div>'

    # Academic blockquote style for overview/insight
    insight_section = ""
    if technical_insight or excerpt:
        lead_text = technical_insight if technical_insight else excerpt
        insight_section = f'''<blockquote>
          <p><strong>Overview:</strong> {lead_text}</p>
        </blockquote>'''

    # Rewrite /images/ to ../images/ in body_html
    body_html = re.sub(r'src="/images/', r'src="../images/', body_html)

    # Wrap figures in academic .img_row and .caption
    def figure_repl(m):
        img_tag = m.group(1)
        caption_text = m.group(2)
        return f'<div class="img_row">{img_tag}</div>\n<div class="caption">{caption_text}</div>'

    body_html = re.sub(
        r'<p>(<img\s+[^>]+>)</p>\s*<p>(<em>(?:Figure)\s+\d+:.*?</em>)</p>',
        figure_repl,
        body_html
    )

    # Wrap any standalone image paragraph in .img_row
    body_html = re.sub(r'<p>(<img\s+[^>]+>)</p>', r'<div class="img_row">\1</div>', body_html)

    # Add IDs to headings
    body_html = extract_headings_and_add_ids(body_html)

    # Wrap tables in academic Booktabs structure (LaTeX / Nature journal style)
    # Remove all default markdown table styles, strip inline styles, add class="booktabs"
    def table_repl(m):
        tbl = m.group(1)
        # remove inline style="text-align: left;" from th and td
        tbl_clean = re.sub(r'\s*style="text-align:\s*[a-zA-Z]+;?"', '', tbl)
        tbl_booktabs = tbl_clean.replace('<table>', '<table class="booktabs">')
        return f'<div class="table-wrapper">{tbl_booktabs}</div>'

    body_html = re.sub(r'(<table>.*?</table>)', table_repl, body_html, flags=re.DOTALL)

    # Convert Table captions <p><em>Table 1: ...</em></p> into .table-caption
    body_html = re.sub(r'<p>(<em>(?:Table\s+\d+:.*?)</em>)</p>', r'<div class="table-caption">\1</div>', body_html)

    schema_json = build_schema_json(frontmatter, canonical_url, og_image, excerpt, full_meta_title)

    return HTML_TEMPLATE.format(
        title=title,
        full_meta_title=full_meta_title,
        subtitle_html=subtitle_html,
        slug=slug,
        author=author,
        date=date,
        subject=subject,
        hero_image=og_image,
        excerpt=excerpt,
        keywords=keywords,
        canonical_url=canonical_url,
        og_image=og_image,
        published_iso=published_iso,
        schema_json=schema_json,
        read_time=read_time,
        hero_section=hero_section,
        insight_section=insight_section,
        body_html=body_html
    )

def generate_sitemap_and_robots(articles_meta):
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
               '  <url>',
               f'    <loc>{SITE_URL}/</loc>',
               f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>',
               '    <changefreq>weekly</changefreq>',
               '    <priority>1.0</priority>',
               '  </url>']

    for a in articles_meta:
        sitemap.extend([
            '  <url>',
            f'    <loc>{SITE_URL}/{a["slug"]}/</loc>',
            f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>',
            '    <changefreq>monthly</changefreq>',
            '    <priority>0.9</priority>',
            '  </url>'
        ])
    sitemap.append('</urlset>')

    sitemap_path = os.path.join(PROJECT_DIR, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sitemap))
    print("✓ Generated: sitemap.xml")

    robots_path = os.path.join(PROJECT_DIR, 'robots.txt')
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("✓ Generated: robots.txt")

def build_all():
    md_files = [f for f in os.listdir(PROJECT_DIR) if f.endswith('.md') and f.lower() != 'readme.md']
    print(f"Found {len(md_files)} article(s) to compile.")

    articles_meta = []

    for md_file in md_files:
        filepath = os.path.join(PROJECT_DIR, md_file)
        frontmatter, raw_body = parse_markdown_file(filepath)

        title = frontmatter.get('title', md_file.replace('.md', ''))
        slug = frontmatter.get('slug', md_file.replace('.md', ''))

        processed_body = process_custom_blocks(raw_body)
        protected_body, placeholders = protect_latex(processed_body)

        body_html = markdown.markdown(
            protected_body,
            extensions=['fenced_code', 'tables']
        )

        body_html = restore_latex(body_html, placeholders)

        full_html = build_article_html(frontmatter, body_html, raw_body)

        slug_dir = os.path.join(PROJECT_DIR, slug)
        os.makedirs(slug_dir, exist_ok=True)
        slug_out = os.path.join(slug_dir, 'index.html')
        with open(slug_out, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"✓ Generated: {slug}/index.html")

        articles_meta.append({
            'title': title,
            'slug': slug,
            'date': frontmatter.get('date', ''),
            'subject': frontmatter.get('subject', 'Article'),
            'excerpt': frontmatter.get('excerpt', ''),
            'heroImage': frontmatter.get('heroImage', '')
        })

    generate_sitemap_and_robots(articles_meta)

    # Clean minimal redirect at root
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
