# 🎤 AI Interview Coach

**Your personal interview prep kit. For any role. In minutes.**

10 tailored questions, ideal answers using your actual background, stories to prepare,
what not to say, and red flags to watch for — generated in minutes.

Two ways to use it: **web app** (no setup) or **Claude Code CLI** (runs locally).

---

## Option 1 — Web app ((fastest))

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

1. Go to the live app: [link once deployed]
2. Paste the job description
3. Paste your background
4. Pick your interview type
5. Get your full prep kit

No setup. No install. Just results.

---

## Option 2 — Claude Code CLI (runs locally, private)

**Requirements:** [Claude Code](https://claude.ai/code)

```bash
# 1. Install Claude Code
npm install -g @anthropic-ai/claude-code

# 2. Clone this repo
git clone https://github.com/ibmlachezar/ai-interview-coach
cd ai-interview-coach

# 3. Add your job description
# Open job-description.md and paste the full JD

# 4. Add your background
# Open my-background.md and paste your resume or experience

# 5. Run Claude Code
claude

# 6. Run the prep
read the file .claude/commands/interview-prep.md and follow the instructions
```

Your prep kit saves to `outputs/interview-prep.md`

---

## What you get

For each of the 10 questions:

- **The question** — tailored to this specific role
- **Why they ask it** — what the interviewer is really testing
- **Your ideal answer** — using your actual background, not generic advice
- **Story to prepare** — the specific experience to draw from
- **What not to say** — the common mistake for this question

Plus:
- **3 red flags** to watch for in this specific interview process
- **One coaching insight** specific to your background and this role

---

## Works for any role

Tech, product, business, sales, operations, design — any industry, any seniority level.
The more specific your background and job description, the better the output.

---

## Privacy

Your background and job description are **gitignored** — they never get committed or shared.
The CLI version runs entirely on your machine.

---

## Built by

**Lachezar Atanasov** — Head of AI Product, AI startup founder, advisor to multiple AI companies.

→ [lachezaratanasov.com](https://lachezaratanasov.com)
→ [LinkedIn](https://www.linkedin.com/in/lachezar-atanasov198/)
→ [career-ops](https://github.com/ibmlachezar/career-ops) ← AI job search system
→ [ai-product-toolkit](https://github.com/ibmlachezar/ai-product-toolkit) ← AI PM tools

---

## Contributing

Found a question type that's missing? Have an improvement?
Open an issue or submit a PR.

## License

MIT
