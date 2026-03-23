# 🍞 Breadcrumb

> *Leaving a trail of thoughts so you don't have to.*

Breadcrumb is your lazy-but-brilliant AI-powered assistant for turning the articles you actually read into tweets people actually want to read. Drop an article in a folder, go touch grass, and come back to polished tweet drafts waiting for you. That's it. That's the app.

Built for builders working at the intersection of democracy and technology — because the world needs more people sharing what they're learning, and fewer people staring at a blinking cursor.

---

## What It Does

You read things. Important things. Things about civic tech, democratic governance, and how we can build better institutions. Breadcrumb takes those things and uses Claude AI to generate **three distinct tweet drafts** per article:

1. **The Conversation Starter** — thought-provoking, invites replies, makes people think
2. **The Technical Insight** — shows you actually understand the mechanism, not just the vibe
3. **The Personal Take** — first-person, learning in public, humble but bold

No hashtag spam. No "Thoughts?" at the end. No marketing-speak. Just tweets that sound like a smart human wrote them — because, well, you reviewed them.

---

## Getting Started

**One-time setup:**
```bash
bash setup.sh
```

This installs dependencies, hooks up your Anthropic API key, and schedules a cron job to run every morning at 8:00 AM. You're welcome.

**Drop an article:**
```
intake/your-article.pdf
intake/your-article.txt
intake/your-article.md
intake/your-article.html
```

**Check your drafts:**
```
tweets/tweets.md
```

**Run it manually whenever:**
```bash
python3 generate_tweets.py
```

---

## Supported Formats

Breadcrumb isn't picky. Drop in:
- `.txt` — plain text, classic
- `.md` — markdown, for the nerds
- `.html` — copy-paste from the web, chaos welcome
- `.pdf` — because PDFs are forever

---

## Requirements

- Python 3.7+
- An [Anthropic API key](https://console.anthropic.com/)
- The willingness to share what you're learning (the hardest dependency)

---

## What's Coming

Breadcrumb is just getting started. The roadmap is ambitious and the vibes are immaculate:

### More Publishing Channels
Right now it's all tweets. Soon it'll be *everywhere*:
- **Bluesky** — for the decentralization maximalists
- **LinkedIn** — for when you need to be professional about it
- **Substack** — long-form drafts from your reading notes
- **Medium** — because some ideas deserve more than 280 characters
- *...and wherever else the internet decides to congregate*

### More Features
- **A real UI** — because markdown files are great until they're not
- **Mobile app** — drop articles on the go, get drafts on the go
- **Scheduling & publishing** — skip the copy-paste, post directly
- **Analytics** — find out which takes land and which ones miss
- **Multi-topic modes** — not just democracy tech, but whatever you're obsessing over

---

## Philosophy

The best public thinkers aren't necessarily the most prolific writers — they're the most consistent ones. Breadcrumb removes the activation energy from sharing. You already did the hard part (reading). This just helps you leave the trail.

---

## License

MIT — do whatever, just build something good with it.

---

*Made with too much coffee and genuine concern for democratic institutions.*
