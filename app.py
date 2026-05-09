import streamlit as st
import anthropic
import json

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #F2F3F7; }
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 720px; }

.stTextInput input, .stTextArea textarea {
    border: 1.5px solid #E2E6EF !important; border-radius: 10px !important;
    background: #fff !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 13.5px !important; color: #0F172A !important;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #3B5BDB !important;
    box-shadow: 0 0 0 3px rgba(59,91,219,0.1) !important;
}
.stSelectbox > div > div {
    border: 1.5px solid #E2E6EF !important; border-radius: 10px !important;
    background: #fff !important; font-size: 13.5px !important; color: #0F172A !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    font-size: 10.5px !important; font-weight: 600 !important;
    letter-spacing: .07em !important; text-transform: uppercase !important;
    color: #64748B !important;
}
.stFormSubmitButton button {
    background: #0F172A !important; color: #fff !important;
    border: none !important; border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important; font-size: 13px !important;
    font-weight: 700 !important; letter-spacing: .05em !important;
    box-shadow: 0 2px 10px rgba(15,23,42,0.18) !important;
}
.stFormSubmitButton button:hover { opacity: .88 !important; }
.stProgress > div > div { border-radius: 6px !important; height: 5px !important; }
.stProgress > div { border-radius: 6px !important; background: #EEF1F8 !important; height: 5px !important; }
hr { border-color: #E8EBF4 !important; margin: 1.5rem 0 !important; }

.q-card {
    background: #fff; border: 1.5px solid #E8EBF4; border-radius: 14px;
    padding: 20px 24px; margin-bottom: 16px;
    box-shadow: 0 1px 6px rgba(15,23,42,0.05);
}
.q-num {
    font-family: monospace; font-size: 10px; letter-spacing: .1em;
    text-transform: uppercase; color: #94A3B8; margin-bottom: 6px;
}
.q-text {
    font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 700;
    color: #0F172A; line-height: 1.4; margin-bottom: 12px;
}
.q-type {
    font-size: 10px; font-weight: 600; padding: 2px 9px; border-radius: 20px;
    display: inline-block; margin-bottom: 12px;
}
.answer-box {
    background: #F0F7FF; border: 1.5px solid #BAD5F5; border-radius: 10px;
    padding: 12px 16px; font-size: 13px; color: #0F172A; line-height: 1.7;
    margin-bottom: 10px;
}
.story-box {
    background: #F0FDF4; border: 1.5px solid #86EFAC; border-radius: 10px;
    padding: 12px 16px; font-size: 13px; color: #0F172A; line-height: 1.7;
    margin-bottom: 10px;
}
.avoid-box {
    background: #FFFBF0; border: 1.5px solid #F0D080; border-radius: 10px;
    padding: 10px 14px; font-size: 12.5px; color: #78450A; line-height: 1.6;
    margin-bottom: 10px;
}
.redflag-box {
    background: #FEF2F2; border: 1.5px solid #FECACA; border-radius: 10px;
    padding: 12px 16px; font-size: 13px; color: #7F1D1D; line-height: 1.65;
    margin-bottom: 8px;
}
.section-title {
    font-family: 'Syne', sans-serif; font-size: 11px; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase; color: #0F172A;
    margin-bottom: 10px; margin-top: 4px;
}
.footer {
    text-align: center; color: #94A3B8; font-size: 11px;
    font-family: monospace; letter-spacing: 0.07em;
    margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid #E2E6EF;
}
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """You are an expert interview coach who has helped hundreds of people land jobs at top companies.
You generate highly specific, deeply personalised interview prep kits.

Never give generic advice. Every answer, story, and tip must be tailored to THIS person's background for THIS specific role.

Generate a full interview prep kit with 7 questions across 4 categories:

CATEGORY 1: Role-specific questions (2 questions)
Directly about the responsibilities in this job description.

CATEGORY 2: Behavioral questions (2 questions)
STAR-format questions tailored to what this role requires.

CATEGORY 3: Domain/technical questions (2 questions)
Testing specific knowledge the JD requires.

CATEGORY 4: Curveball questions (1 question)
An unexpected question that tests how they think — specific to this role.

For each question provide:
- The question itself
- Why interviewers ask it (what they're really testing)
- The ideal answer using THIS person's actual background (3-5 sentences, specific)
- A story from their background they should prepare
- One thing NOT to say

Also provide:
- 3 red flags to watch for in THIS interview process
- One overall coaching tip specific to their background and this role

Return ONLY valid JSON:
{
  "roleTitle": "<job title from JD>",
  "company": "<company name if mentioned>",
  "interviewType": "<interview type>",
  "overallTip": "<one specific coaching insight for this person for this role>",
  "questions": [
    {
      "number": 1,
      "category": "<Role-specific|Behavioral|Domain|Curveball>",
      "categoryColor": "<#3B5BDB|#0D9A6A|#E07B2A|#7C3AED>",
      "question": "<the question>",
      "whyTheyAsk": "<what they are really testing — one sentence>",
      "idealAnswer": "<ideal answer using their actual background — 3-5 sentences>",
      "storyToPrep": "<specific story from their background to prepare — what happened, what they did, what the result was>",
      "avoid": "<one thing not to say or do>"
    }
  ],
  "redFlags": [
    "<red flag 1 specific to this company/role>",
    "<red flag 2>",
    "<red flag 3>"
  ]
}"""

# Header
st.markdown("""
<div style="background:linear-gradient(135deg,#0F172A 0%,#1E3A5F 100%);border-radius:14px;
padding:28px 32px 22px;margin-bottom:20px;box-shadow:0 4px 20px rgba(15,23,42,0.18);">
    <div style="font-family:monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;
    color:#4B7BA8;margin-bottom:8px;">🎤 AI Interview Coach</div>
    <div style="font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:#fff;
    line-height:1.2;margin-bottom:8px;">Your personal interview<br>prep kit. In minutes.</div>
    <div style="font-size:13px;color:#7FA3C4;line-height:1.6;">10 tailored questions, ideal answers using your background,
    stories to prepare, and what not to say. For any role.</div>
</div>
""", unsafe_allow_html=True)

with st.form("interview_coach"):
    jd = st.text_area(
        "Paste the job description",
        placeholder="Paste the full job description here — including responsibilities and requirements.",
        height=140
    )
    background = st.text_area(
        "Your background",
        placeholder="Paste your resume or describe your experience — the more specific the better. Include real numbers, outcomes, and achievements.",
        height=140
    )
    c1, c2 = st.columns(2)
    with c1:
        interview_type = st.selectbox(
            "Interview type",
            ["First round / recruiter screen", "Hiring manager interview",
             "Panel interview", "Final round", "Case study / take-home"]
        )
    with c2:
        focus = st.selectbox(
            "What do you want to focus on?",
            ["Balanced — cover everything", "Behavioral questions",
             "Technical / domain questions", "Leadership questions", "Culture fit"]
        )
    submitted = st.form_submit_button("Generate my prep kit →", use_container_width=True)

if submitted:
    if not jd.strip() or not background.strip():
        st.error("Please paste both the job description and your background.")
    else:
        with st.spinner("Building your personalised prep kit..."):
            try:
                client = anthropic.Anthropic()
                message = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=8000,
                    system=SYSTEM_PROMPT,
                    messages=[{
                        "role": "user",
                        "content": f"Job description:\n{jd}\n\nMy background:\n{background}\n\nInterview type: {interview_type}\nFocus: {focus}"
                    }]
                )
                text = message.content[0].text
                r = json.loads(text.replace("```json", "").replace("```", "").strip())

                # Header
                st.markdown(f"""
                <div style="background:#fff;border:1.5px solid #E8EBF4;border-radius:14px;
                padding:20px 24px;margin-bottom:20px;box-shadow:0 1px 6px rgba(15,23,42,0.05);">
                    <div style="font-family:monospace;font-size:9px;letter-spacing:.1em;
                    text-transform:uppercase;color:#94A3B8;margin-bottom:4px;">Prep kit for</div>
                    <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
                    color:#0F172A;">{r.get('roleTitle', 'Your Role')}{' at ' + r['company'] if r.get('company') else ''}</div>
                    <div style="font-size:12px;color:#64748B;margin-top:4px;">{r.get('interviewType', interview_type)}</div>
                </div>""", unsafe_allow_html=True)

                # Overall tip
                st.markdown(f"""
                <div style="background:#0F172A;border-radius:12px;padding:16px 20px;margin-bottom:20px;">
                    <div style="font-family:Syne,sans-serif;font-size:10px;font-weight:700;
                    letter-spacing:.1em;text-transform:uppercase;color:#4B7BA8;margin-bottom:6px;">
                    🎯 Your coaching insight</div>
                    <div style="font-size:14px;color:#F1F5F9;line-height:1.65;">{r['overallTip']}</div>
                </div>""", unsafe_allow_html=True)

                st.divider()

                # Questions
                st.markdown("<div class='section-title'>The 10 questions — with your answers</div>", unsafe_allow_html=True)

                for q in r["questions"]:
                    cat_color = q.get("categoryColor", "#3B5BDB")
                    cat_bg = cat_color + "18"
                    st.markdown(f"""
                    <div class="q-card">
                        <div class="q-num">Question {q['number']} of 10</div>
                        <div style="font-size:10px;font-weight:600;padding:2px 9px;border-radius:20px;
                        background:{cat_bg};color:{cat_color};display:inline-block;margin-bottom:10px;">
                        {q['category']}</div>
                        <div class="q-text">{q['question']}</div>
                        <div style="font-size:11px;color:#94A3B8;margin-bottom:10px;font-style:italic;">
                        What they're testing: {q['whyTheyAsk']}</div>
                    </div>""", unsafe_allow_html=True)

                    st.markdown(f"<div class='answer-box'><strong style='font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:#1A4A7A;'>💬 Your ideal answer</strong><br><br>{q['idealAnswer']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='story-box'><strong style='font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:#166534;'>📖 Story to prepare</strong><br><br>{q['storyToPrep']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='avoid-box'>⚠ <strong>Don't say:</strong> {q['avoid']}</div>", unsafe_allow_html=True)
                    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

                st.divider()

                # Red flags
                st.markdown("<div class='section-title'>🚩 Red flags to watch for in this process</div>", unsafe_allow_html=True)
                for rf in r["redFlags"]:
                    st.markdown(f"<div class='redflag-box'>{rf}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Generation failed — please try again. ({e})")

st.markdown("""
<div class='footer'>
    Built by Lachezar Atanasov · lachezaratanasov.com ·
    <a href='https://github.com/ibmlachezar/ai-interview-coach' style='color:#94A3B8;'>GitHub</a>
</div>
""", unsafe_allow_html=True)
