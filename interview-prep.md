# Skill: Interview Prep

## What this does
Generates a full personalised interview prep kit for a specific role.
10 questions, ideal answers using the user's real background, stories to prepare,
what NOT to say, red flags to watch for, and one coaching insight.

Never gives generic advice. Every answer is tailored to this person for this role.

## Instructions for Claude

1. Read `job-description.md` — the role they're interviewing for
2. Read `my-background.md` — their actual experience
3. Ask the user (if not already in the files):
   - What type of interview is this? (recruiter screen / hiring manager / panel / final round)
   - Any specific areas they're worried about?

4. Generate 10 questions across 4 categories:

### Category 1: Role-specific (3 questions)
Directly about the responsibilities in this JD.
What will they actually be doing day 1?

### Category 2: Behavioral (3 questions)
STAR-format questions tailored to what this role requires.
Pull from their actual background for the answers.

### Category 3: Domain/technical (2 questions)
Testing specific knowledge the JD requires.
Be honest if there are gaps.

### Category 4: Curveball (2 questions)
Unexpected questions that test how they think.
Specific to this role and company.

5. For each question provide:
   - The question
   - Why interviewers ask it (one sentence — what they're really testing)
   - The ideal answer using THEIR actual background (3-5 sentences, specific)
   - A story from their background to prepare (what happened, what they did, result)
   - One thing NOT to say

6. Provide:
   - 3 red flags to watch for in THIS interview process
   - One overall coaching insight specific to their background and this role

7. Save the full kit to `outputs/interview-prep.md`

## Output format

```
INTERVIEW PREP KIT
Role: [role]
Company: [company]
Interview type: [type]

COACHING INSIGHT:
[one specific tip for this person for this role]

---

QUESTION 1 OF 10 — [Category]
[The question]

WHY THEY ASK: [one sentence]

YOUR ANSWER:
[ideal answer using their background]

STORY TO PREPARE:
[specific story from their background]

AVOID:
[one thing not to say]

---
[repeat for all 10 questions]

RED FLAGS TO WATCH FOR:
1. [red flag specific to this company/role]
2. [red flag]
3. [red flag]
```

## Tone
Like a trusted coach who knows the role and knows their background.
Honest about gaps. Specific about strengths. Never generic.
