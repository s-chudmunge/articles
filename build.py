#!/usr/bin/env python3
"""
Static site generator for s-chudmunge/articles GitHub Pages.
Generates search-engine optimized, typography-first, magazine-grade HTML articles
matching the design philosophy of fep-papers-archive and setr-papers-archive.
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
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Sankalp Chudmunge</title>

<!-- Primary SEO Meta Tags -->
<meta name="title" content="{title}">
<meta name="description" content="{excerpt}">
<meta name="author" content="{author}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{canonical_url}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="Sankalp Chudmunge — Research & Articles">
<meta property="og:url" content="{canonical_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="article:published_time" content="{published_iso}">
<meta property="article:modified_time" content="{published_iso}">
<meta property="article:author" content="https://github.com/s-chudmunge">
<meta property="article:section" content="{subject}">

<!-- Twitter Cards -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@CompleteSkeptic">
<meta name="twitter:creator" content="@CompleteSkeptic">
<meta name="twitter:url" content="{canonical_url}">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{excerpt}">
<meta name="twitter:image" content="{og_image}">

<!-- Schema.org JSON-LD Structured Data for Search Engine Rich Snippets -->
<script type="application/ld+json">
{schema_json}
</script>

<!-- Google Fonts: Newsreader (Editorial Serif), Plus Jakarta Sans (Modern Geometric Sans), JetBrains Mono (Code) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&family=Plus+Jakarta+Sans:ital,wght@0,400..800;1,400..800&display=swap" rel="stylesheet">

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

<!-- Twitter Widget for Embedded Tweets -->
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<style>
  :root {{
    /* Eye-Comfort Warm Paper Palette (Light Mode) */
    --bg-page: #fdfcfb;
    --bg-card: #ffffff;
    --text-main: #181a1f;
    --text-muted: #57606a;
    --border-color: #e5e7eb;
    --border-subtle: #f0f2f5;
    --btn-bg: #f3f4f6;
    --btn-text: #374151;
    --btn-border: #d1d5db;
    --link-color: #1d4ed8;
    --link-hover: #1e40af;
    --code-bg: #f6f8fa;
    --code-border: #e1e4e8;
    --callout-bg: #f0f7ff;
    --callout-border: #2563eb;
    --callout-text: #1e3a8a;
    --table-header: #f8fafc;
    --table-row-hover: #f8fafc;
    --tag-bg: #eff6ff;
    --tag-text: #1d4ed8;
    --tag-border: #bfdbfe;
    --accent-glow: rgba(37, 99, 235, 0.08);

    /* Typography font variable */
    --font-prose: 'Newsreader', Georgia, Cambria, serif;
    --font-heading: 'Plus Jakarta Sans', system-ui, sans-serif;
    --font-ui: 'Plus Jakarta Sans', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', ui-monospace, Menlo, Monaco, Consolas, monospace;
  }}

  [data-theme="dark"] {{
    /* Deep Slate / Zinc OLED-friendly Dark Palette */
    --bg-page: #0d1117;
    --bg-card: #161b22;
    --text-main: #e6edf3;
    --text-muted: #8b949e;
    --border-color: #30363d;
    --border-subtle: #21262d;
    --btn-bg: #21262d;
    --btn-text: #c9d1d9;
    --btn-border: #363b42;
    --link-color: #58a6ff;
    --link-hover: #79b8ff;
    --code-bg: #161b22;
    --code-border: #30363d;
    --callout-bg: rgba(56, 189, 248, 0.08);
    --callout-border: #38bdf8;
    --callout-text: #bae6fd;
    --table-header: #131820;
    --table-row-hover: #1c2129;
    --tag-bg: rgba(56, 189, 248, 0.12);
    --tag-text: #7dd3fc;
    --tag-border: rgba(56, 189, 248, 0.28);
    --accent-glow: rgba(56, 189, 248, 0.1);
  }}

  /* Font Switcher Preference */
  [data-font="sans"] {{
    --font-prose: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  
  html {{
    scroll-behavior: smooth;
    scroll-padding-top: 5rem;
  }}

  body {{
    font-family: var(--font-prose);
    background-color: var(--bg-page);
    color: var(--text-main);
    line-height: 1.82;
    padding: 0 1.25rem 6rem 1.25rem;
    transition: background-color 0.25s ease, color 0.25s ease;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }}

  /* Top Navigation Bar */
  .top-nav-wrapper {{
    position: sticky;
    top: 0;
    background: var(--bg-page);
    background: color-mix(in srgb, var(--bg-page) 88%, transparent);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    z-index: 90;
    border-bottom: 1px solid var(--border-color);
    margin: 0 -1.25rem 2.5rem -1.25rem;
    padding: 0 1.25rem;
  }}

  .top-nav {{
    max-width: 1080px;
    margin: 0 auto;
    padding: 0.95rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .nav-brand {{
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    font-family: var(--font-ui);
    font-size: 0.925rem;
    font-weight: 600;
    color: var(--text-muted);
    text-decoration: none;
    transition: color 0.15s;
  }}
  .nav-brand:hover {{ color: var(--link-color); }}
  .nav-brand span.author-name {{ color: var(--text-main); font-weight: 700; }}

  .nav-controls {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }}

  .pill-control {{
    background: var(--btn-bg);
    border: 1px solid var(--btn-border);
    color: var(--btn-text);
    padding: 0.35rem 0.75rem;
    border-radius: 9999px;
    cursor: pointer;
    font-family: var(--font-ui);
    font-size: 0.8rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.35rem;
    transition: all 0.15s;
  }}
  .pill-control:hover {{
    opacity: 0.9;
    border-color: var(--link-color);
  }}

  /* Reading Progress Bar */
  #progress-bar {{
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--link-color), #8b5cf6);
    width: 0%;
    z-index: 100;
    transition: width 0.08s ease-out;
  }}

  /* Page Layout Grid with Sticky TOC on Desktop */
  .layout-grid {{
    max-width: 1080px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: minmax(0, 740px) 260px;
    gap: 4.5rem;
    align-items: start;
    justify-content: center;
  }}

  @media (max-width: 1080px) {{
    .layout-grid {{
      grid-template-columns: minmax(0, 740px);
      gap: 0;
    }}
    .toc-sidebar {{
      display: none !important;
    }}
  }}

  /* Main Article Column */
  .article-main {{
    width: 100%;
    max-width: 740px;
  }}

  /* Header Section */
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
    font-family: var(--font-ui);
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 1.25rem;
  }}

  h1.article-title {{
    font-family: var(--font-heading);
    font-size: clamp(2.25rem, 4.4vw, 2.95rem);
    font-weight: 800;
    line-height: 1.18;
    letter-spacing: -0.03em;
    color: var(--text-main);
    margin-bottom: 1.25rem;
  }}

  .article-meta {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 1.25rem;
    color: var(--text-muted);
    font-family: var(--font-ui);
    font-size: 0.9rem;
    padding-bottom: 1.75rem;
    border-bottom: 1px solid var(--border-color);
  }}
  .article-meta span {{ display: inline-flex; align-items: center; gap: 0.35rem; }}

  /* Hero Image */
  .hero-image-wrapper {{
    margin: 2.25rem 0;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border-color);
    background: var(--bg-card);
    box-shadow: 0 8px 30px -4px rgba(0, 0, 0, 0.08);
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
    padding: 1.45rem 1.85rem;
    margin: 2.5rem 0;
    box-shadow: 0 2px 10px -2px var(--accent-glow);
  }}
  .insight-title {{
    font-family: var(--font-ui);
    font-size: 0.825rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--callout-border);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
  }}
  .insight-text {{
    font-size: 1.05rem;
    line-height: 1.7;
    color: var(--text-main);
  }}

  /* Article Content Typography */
  .article-content {{
    font-size: 1.15rem;
    color: var(--text-main);
  }}

  .article-content p {{
    margin: 1.65rem 0;
  }}

  .article-content h2 {{
    font-family: var(--font-heading);
    font-size: 1.95rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    margin: 3.75rem 0 1.25rem 0;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid var(--border-color);
    line-height: 1.28;
    position: relative;
  }}

  .article-content h3 {{
    font-family: var(--font-heading);
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -0.015em;
    margin: 2.75rem 0 0.85rem 0;
    line-height: 1.35;
    position: relative;
  }}

  .heading-anchor {{
    position: absolute;
    left: -1.4rem;
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

  .article-content ul, .article-content ol {{
    margin: 1.4rem 0 1.4rem 1.85rem;
  }}
  .article-content li {{
    margin-bottom: 0.6rem;
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
    margin: 3.75rem 0;
  }}

  .article-content blockquote {{
    border-left: 3px solid var(--callout-border);
    background: var(--callout-bg);
    padding: 0.95rem 1.4rem;
    margin: 2rem 0;
    border-radius: 0 8px 8px 0;
    color: var(--text-main);
    font-style: normal;
  }}

  /* Inline Code */
  .article-content :not(pre) > code {{
    font-family: var(--font-mono);
    font-size: 0.86em;
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    color: var(--text-main);
  }}

  /* Code Block Container with Language Badge & Copy Button */
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
    font-family: var(--font-ui);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
    z-index: 10;
  }}
  .code-copy-btn:hover {{
    background: rgba(255, 255, 255, 0.22);
    color: #ffffff;
  }}

  .article-content pre {{
    background: #0f141c !important;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 1.35rem !important;
    overflow-x: auto;
    box-shadow: 0 4px 20px -3px rgba(0, 0, 0, 0.12);
  }}
  .article-content pre code {{
    font-family: var(--font-mono);
    font-size: 0.925rem;
    line-height: 1.65;
    background: none !important;
    border: none !important;
    padding: 0 !important;
    color: #f1f5f9;
  }}

  /* Content Images */
  .article-content img {{
    max-width: 100%;
    height: auto;
    border-radius: 10px;
    border: 1px solid var(--border-color);
    display: block;
    margin: 2.5rem auto 0.85rem auto;
    box-shadow: 0 6px 25px -4px rgba(0, 0, 0, 0.08);
  }}
  
  .figure-caption {{
    display: block;
    text-align: center;
    color: var(--text-muted);
    font-family: var(--font-ui);
    font-size: 0.875rem;
    margin-top: 0.65rem;
    margin-bottom: 2.25rem;
    font-style: italic;
    line-height: 1.55;
    max-width: 90%;
    margin-left: auto;
    margin-right: auto;
  }}

  /* Tables */
  .table-wrapper {{
    width: 100%;
    overflow-x: auto;
    margin: 2.5rem 0;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    background: var(--bg-card);
    box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.04);
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: var(--font-ui);
    font-size: 0.925rem;
  }}
  th, td {{
    padding: 0.95rem 1.25rem;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
    vertical-align: top;
  }}
  th {{
    background: var(--table-header);
    font-weight: 700;
    font-size: 0.825rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
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
    margin: 2.75rem 0;
    background: var(--bg-card);
    box-shadow: 0 6px 20px -3px rgba(0, 0, 0, 0.08);
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
    margin: 2.75rem 0;
    display: flex;
    justify-content: center;
  }}

  /* Sticky Table of Contents (TOC) Sidebar on Desktop */
  .toc-sidebar {{
    position: sticky;
    top: 5rem;
    max-height: calc(100vh - 6rem);
    overflow-y: auto;
    padding-left: 1.5rem;
    border-left: 1px solid var(--border-color);
    font-family: var(--font-ui);
  }}
  .toc-title {{
    font-size: 0.775rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 0.95rem;
  }}
  .toc-list {{
    list-style: none;
    padding: 0;
    margin: 0;
  }}
  .toc-item {{
    margin-bottom: 0.55rem;
    font-size: 0.85rem;
    line-height: 1.4;
  }}
  .toc-item.h3 {{
    padding-left: 0.85rem;
    font-size: 0.8rem;
  }}
  .toc-link {{
    color: var(--text-muted);
    text-decoration: none;
    display: block;
    transition: color 0.15s, transform 0.15s;
  }}
  .toc-link:hover {{
    color: var(--link-color);
    transform: translateX(2px);
  }}
  .toc-link.active {{
    color: var(--link-color);
    font-weight: 700;
  }}

  /* Article Footer */
  .article-footer {{
    margin-top: 5rem;
    padding-top: 2.25rem;
    border-top: 1px solid var(--border-color);
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 1.5rem;
    font-family: var(--font-ui);
    font-size: 0.925rem;
    color: var(--text-muted);
  }}
  .article-footer a {{
    color: var(--link-color);
    text-decoration: none;
  }}
  .article-footer a:hover {{ text-decoration: underline; }}

  /* Back to Top Floating Button */
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
    transition: opacity 0.25s, transform 0.25s, border-color 0.2s;
    font-size: 1.25rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    z-index: 80;
  }}
  .back-to-top.visible {{
    opacity: 1;
    pointer-events: auto;
  }}
  .back-to-top:hover {{
    transform: translateY(-3px);
    border-color: var(--link-color);
  }}

  @media (max-width: 640px) {{
    body {{ padding: 0 1rem 3.5rem 1rem; }}
    h1.article-title {{ font-size: 1.95rem; }}
    .article-meta {{ gap: 0.75rem; font-size: 0.85rem; }}
    th, td {{ padding: 0.75rem 0.85rem; font-size: 0.85rem; }}
    .insight-box {{ padding: 1.15rem 1.35rem; }}
  }}
</style>
</head>
<body>

<div id="progress-bar"></div>

<div class="top-nav-wrapper">
  <header class="top-nav">
    <a href="../" class="nav-brand">
      ← <span class="author-name">Sankalp Chudmunge</span> / articles
    </a>
    <div class="nav-controls">
      <button id="fontToggle" class="pill-control" aria-label="Toggle serif / sans font">
        <span id="fontIcon">🔤</span>
        <span id="fontText">Sans</span>
      </button>
      <button id="themeToggle" class="pill-control" aria-label="Toggle dark mode">
        <span id="themeIcon">🌙</span>
        <span id="themeText">Dark</span>
      </button>
    </div>
  </header>
</div>

<div class="layout-grid">
  <main class="article-main">
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

  <!-- Sticky Sidebar Table of Contents -->
  <aside class="toc-sidebar">
    <div class="toc-title">On this page</div>
    <ul class="toc-list">
      {toc_html}
    </ul>
  </aside>
</div>

<button id="backToTop" class="back-to-top" aria-label="Back to top">↑</button>

<script>
  // Reading Progress Bar & Back-to-Top
  window.addEventListener('scroll', () => {{
    const winScroll = document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    document.getElementById('progress-bar').style.width = scrolled + '%';

    const btt = document.getElementById('backToTop');
    if (winScroll > 450) {{
      btt.classList.add('visible');
    }} else {{
      btt.classList.remove('visible');
    }}

    // Scroll spy for Table of Contents
    const headings = document.querySelectorAll('.article-content h2, .article-content h3');
    let currentId = '';
    headings.forEach(h => {{
      const rect = h.getBoundingClientRect();
      if (rect.top <= 120) {{
        currentId = h.id;
      }}
    }});
    document.querySelectorAll('.toc-link').forEach(link => {{
      if (link.getAttribute('href') === '#' + currentId) {{
        link.classList.add('active');
      }} else {{
        link.classList.remove('active');
      }}
    }});
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

  // Font Switcher (Serif vs Sans)
  const fontToggle = document.getElementById('fontToggle');
  const fontIcon = document.getElementById('fontIcon');
  const fontText = document.getElementById('fontText');

  function initFont() {{
    const savedFont = localStorage.getItem('articles_font');
    if (savedFont === 'sans') {{
      document.documentElement.setAttribute('data-font', 'sans');
      fontIcon.textContent = '📖';
      fontText.textContent = 'Serif';
    }} else {{
      document.documentElement.removeAttribute('data-font');
      fontIcon.textContent = '🔤';
      fontText.textContent = 'Sans';
    }}
  }}
  initFont();

  fontToggle.addEventListener('click', () => {{
    const isSans = document.documentElement.getAttribute('data-font') === 'sans';
    if (isSans) {{
      document.documentElement.removeAttribute('data-font');
      localStorage.setItem('articles_font', 'serif');
      fontIcon.textContent = '🔤';
      fontText.textContent = 'Sans';
    }} else {{
      document.documentElement.setAttribute('data-font', 'sans');
      localStorage.setItem('articles_font', 'sans');
      fontIcon.textContent = '📖';
      fontText.textContent = 'Serif';
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

  // Fix image paths for subdirectories & GitHub Pages
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
    headings = []
    used_slugs = set()

    def repl(m):
        level = m.group(1)
        text = m.group(2)
        clean_text = re.sub(r'<.*?>', '', text)
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', clean_text.lower()).strip('-')
        if not slug:
            slug = f"section-{len(headings)}"
        if slug in used_slugs:
            slug = f"{slug}-{len(headings)}"
        used_slugs.add(slug)
        headings.append({'level': int(level), 'title': clean_text, 'id': slug})
        return f'<h{level} id="{slug}"><a href="#{slug}" class="heading-anchor" aria-hidden="true">#</a>{text}</h{level}>'

    html_with_ids = re.sub(r'<h([23])>(.*?)</h\1>', repl, html_text, flags=re.DOTALL)
    return html_with_ids, headings

def build_schema_json(frontmatter, canonical_url, og_image, excerpt):
    title = frontmatter.get('title', 'Article')
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
                "headline": title,
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
                        "name": title
                    }
                ]
            }
        ]
    }
    return json.dumps(schema, indent=2)

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

    canonical_url = f"{SITE_URL}/{slug}/"
    og_image = f"{SITE_URL}{hero_image}" if hero_image.startswith('/') else f"{SITE_URL}/{hero_image}"

    synonyms = frontmatter.get('synonyms', [])
    keywords = ", ".join([title, subject, author] + synonyms)

    try:
        dt = datetime.strptime(date, "%B %d, %Y")
        published_iso = dt.strftime("%Y-%m-%dT00:00:00Z")
    except Exception:
        published_iso = "2026-09-25T00:00:00Z"

    # Convert root-relative image paths to relative paths for depth-1 directories
    rel_hero = hero_image.lstrip('/')
    hero_section = ""
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

    # Add IDs to headings and extract TOC
    body_html, headings = extract_headings_and_add_ids(body_html)

    # Wrap tables in responsive wrapper
    body_html = re.sub(r'(<table>.*?</table>)', r'<div class="table-wrapper">\1</div>', body_html, flags=re.DOTALL)

    # Style captions following images: <p><em>Figure ...</em></p>
    body_html = re.sub(r'<p>(<em>(?:Figure|Table)\s+\d+:.*?</em>)</p>', r'<div class="figure-caption">\1</div>', body_html)

    # Build Table of Contents HTML
    toc_items = []
    for h in headings:
        cls = "toc-item h3" if h['level'] == 3 else "toc-item"
        toc_items.append(f'<li class="{cls}"><a href="#{h["id"]}" class="toc-link">{h["title"]}</a></li>')
    toc_html = "\n      ".join(toc_items)

    schema_json = build_schema_json(frontmatter, canonical_url, og_image, excerpt)

    return HTML_TEMPLATE.format(
        title=title,
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
        body_html=body_html,
        toc_html=toc_html
    )

def generate_sitemap_and_robots(articles_meta):
    # sitemap.xml
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

    # robots.txt
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

        # Output to <slug>/index.html
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

    # Generate sitemap and robots
    generate_sitemap_and_robots(articles_meta)

    # Minimal clean index.html at root
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
