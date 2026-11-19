# Sankalp Chudmunge: Technical Articles

Personal research essays and engineering breakdowns published directly to GitHub Pages.

🔗 **Live Portal:** [https://s-chudmunge.github.io/articles/](https://s-chudmunge.github.io/articles/)

---

## 📚 Published Articles

| Article | Category | Slug | Status |
| :--- | :--- | :--- | :--- |
| **What are Decision Models? The System One Architecture Blueprint** | Machine Learning | [`/decision-models`](https://s-chudmunge.github.io/articles/decision-models/) | ✅ Published |

---

## 🛠️ Publishing New Articles

To add a new article in the future:

1. Create a markdown file `[your-article-slug].md` in this repo root with YAML frontmatter:
   ```yaml
   ---
   title: "Your Article Title"
   slug: "your-article-slug"
   shortSlug: "short-slug"
   author: "Sankalp Chudmunge"
   date: "Month Day, Year"
   subject: "Machine Learning"
   heroImage: "/images/articles/your-hero.png"
   excerpt: "One-sentence summary."
   technicalInsight: "Key technical takeaway."
   ---
   ```
2. Place any diagram or screenshot images into `images/articles/`.
3. Compile all articles:
   ```bash
   python3 build.py
   ```
4. Commit and push:
   ```bash
   git add .
   git commit -m "Publish: your article title"
   git push origin main
   ```
The article will immediately be live at `https://s-chudmunge.github.io/articles/[your-article-slug]/`!

---

## 🎨 Features & Architecture

- **Zero Heavy Frameworks:** Pure static HTML + CSS + JS matching the design language of [`fep-papers-archive`](https://s-chudmunge.github.io/fep-papers-archive/) and [`setr-papers-archive`](https://s-chudmunge.github.io/setr-papers-archive/).
- **LaTeX Math Rendering:** Pristine inline (`$...$`) and display (`$$...$$`) math rendering via KaTeX.
- **Dark Mode Support:** Auto-synced with system color preference with manual toggle and local storage persistence.
- **Embedded Media:** Native support for X/Twitter tweets and responsive Loom video walkthroughs.
- **Code Highlighting:** Syntax highlighted code blocks with one-click copy buttons.
- **SEO & Social Cards:** Complete OpenGraph and Twitter card metadata for rich previews.
