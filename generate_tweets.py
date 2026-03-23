#!/usr/bin/env python3
"""
Tweet Generator for Democracy Tech Articles
Scans the intake/ folder for new content and generates tweet drafts using Claude API.
Saves one markdown file per article into the tweets/ subfolder.
"""

import os
import json
from datetime import date, datetime
from pathlib import Path
from typing import Optional
import anthropic

# ── Configuration ────────────────────────────────────────────────────────────
ROOT_DIR    = Path(__file__).parent
INTAKE_DIR  = ROOT_DIR / "intake"
TWEETS_DIR  = ROOT_DIR / "tweets"
TRACKER_FILE = ROOT_DIR / ".processed_articles.json"
SUPPORTED_EXTENSIONS = [".txt", ".md", ".html", ".pdf"]

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_tracker() -> dict:
    """Load the tracker of already-processed articles."""
    if TRACKER_FILE.exists():
        with open(TRACKER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tracker(tracker: dict):
    with open(TRACKER_FILE, "w") as f:
        json.dump(tracker, f, indent=2)

def read_article(path: Path) -> Optional[str]:
    """Read article content. Handles txt, md, html, and pdf."""
    ext = path.suffix.lower()
    try:
        if ext in [".txt", ".md"]:
            return path.read_text(encoding="utf-8", errors="ignore")
        elif ext == ".html":
            import re
            html = path.read_text(encoding="utf-8", errors="ignore")
            text = re.sub(r"<[^>]+>", " ", html)
            text = re.sub(r"\s+", " ", text).strip()
            return text[:15000]
        elif ext == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(str(path))
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                return text[:15000]
            except ImportError:
                return "[PDF detected but pypdf not installed. Run: pip3 install pypdf --user]"
    except Exception as e:
        return "[Error reading file: {}]".format(e)
    return None

def generate_tweets(client: anthropic.Anthropic, filename: str, content: str) -> str:
    """Call Claude API to generate three tweet drafts from article content."""
    prompt = """You are helping someone who is building tools to improve democratic governance.
They are on a journey — humble but bold, learning in public, with a big vision for using technology
to make democracies more transparent and effective.

Read the following article carefully and generate exactly three tweet drafts:

TWEET 1 — CONVERSATION STARTER
Invite the audience to think about the implications for democracy or governance.
Make it thought-provoking and open-ended. Should spark replies and discussion.

TWEET 2 — TECHNICAL INSIGHT
Explain a specific mechanism or insight from the article showing how technology
can strengthen democratic systems. Be sophisticated but accessible.
Concrete and specific, not vague.

TWEET 3 — PERSONAL INSIGHT / CONTRARIAN TAKE
Pull out a surprising implication or connect this to a broader pattern in how
we design systems. Written as someone learning in public — humble but not afraid
to share bold ideas. First-person voice, like sharing a genuine realisation.

RULES:
- Each tweet must be under 280 characters
- No hashtags
- No emojis unless they genuinely add meaning
- Do not start any tweet with "I think" or "I believe"
- Sound like a thoughtful human, not a press release

---
ARTICLE FILENAME: {filename}

ARTICLE CONTENT:
{content}
---

FORMAT YOUR RESPONSE EXACTLY LIKE THIS (no extra text):
**Key Insight:** [one sentence capturing the article's most important idea]

**Tweet 1 (Conversation Starter):**
[tweet text]

**Tweet 2 (Technical Insight):**
[tweet text]

**Tweet 3 (Personal Insight):**
[tweet text]
""".format(filename=filename, content=content[:12000])

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def tweet_output_path() -> Path:
    """Return the single tweets output file path."""
    return TWEETS_DIR / "tweets.md"

def main():
    # Validate API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set. Add it to your environment variables.")
        return

    client = anthropic.Anthropic(api_key=api_key)
    tracker = load_tracker()

    if not INTAKE_DIR.exists():
        print("📂 intake/ folder not found. Creating it...")
        INTAKE_DIR.mkdir(exist_ok=True)
        print("   Drop your articles (.txt, .md, .html, .pdf) into: {}".format(INTAKE_DIR))
        return

    # Find all supported article files in intake/
    all_files = []
    for ext in SUPPORTED_EXTENSIONS:
        all_files.extend(INTAKE_DIR.glob("*{}".format(ext)))

    articles = [f for f in all_files if not f.name.startswith(".")]

    if not articles:
        print("📂 No articles found in intake/. Drop files there to get started.")
        return

    # Filter to only unprocessed articles
    new_articles = [f for f in articles if f.name not in tracker]

    if not new_articles:
        print("✅ No new articles to process. All caught up!")
        return

    print("📰 Found {} new article(s) to process...\n".format(len(new_articles)))

    TWEETS_DIR.mkdir(exist_ok=True)
    today = date.today().strftime("%Y-%m-%d")
    processed = 0

    for article_path in new_articles:
        print("  📄 Processing: {}".format(article_path.name))
        content = read_article(article_path)

        if not content:
            print("     ⚠️  Could not read {}, skipping.".format(article_path.name))
            continue

        try:
            result = generate_tweets(client, article_path.name, content)

            output_path = tweet_output_path()
            output = [
                "## {}\n".format(article_path.name),
                "_Generated on {}_\n".format(today),
                "---\n",
                result,
                "\n"
            ]
            with open(output_path, "a", encoding="utf-8") as f:
                f.write("\n".join(output))

            tracker[article_path.name] = today
            processed += 1
            print("     ✅ Saved to: {}".format(output_path.name))
        except Exception as e:
            print("     ❌ Error generating tweets for {}: {}".format(article_path.name, e))

    save_tracker(tracker)
    if processed:
        print("\n✨ Done! {} tweet file(s) saved to: {}".format(processed, TWEETS_DIR))

if __name__ == "__main__":
    main()
