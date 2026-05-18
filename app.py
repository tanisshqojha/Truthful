import streamlit as st
from openai import OpenAI


# OpenRouter API setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

# Page config
st.set_page_config(
    page_title="TRUTHFUL",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# CSS
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background-color: #000000;
    color: white;
}

/* TITLE */
.truthful-title {
    text-align: center;
    color: white;
    font-family: 'Inter', sans-serif;
    font-size: 72px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 5px;
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    font-size: 16px;
    color: #d1d1d1;
    margin-bottom: 40px;
    font-weight: 500;
}

/* TEXT AREA CONTAINER */
div[data-testid="stTextArea"] {
    width: 60%;
    margin: auto;
}

/* TEXT AREA */
textarea {
    background-color: #050505 !important;
    color: white !important;

    border: 1px solid #333333 !important;
    border-radius: 10px !important;

    font-size: 16px !important;
    font-weight: 500 !important;

    padding: 18px !important;

    min-height: 110px !important;
    max-height: 110px !important;
    height: 110px !important;

    resize: none !important;

    box-shadow: none !important;
    outline: none !important;
}

/* CENTER TEXT AREA */
[data-testid="stTextArea"] {
    display: flex;
    justify-content: center;
}

/* ANALYZE BUTTON */
div.stButton > button {

    background-color: white;
    color: black;

    font-family: 'Inter', sans-serif;
    font-weight: 700;

    height: 42px;
    width: 140px;

    border-radius: 10px;

    border: none;

    font-size: 15px;

    transition: 0.2s ease;
}

/* BUTTON HOVER */
div.stButton > button:hover {
    background-color: #d9d9d9;
}

/* RESULT CARD */
.result-card {

    background-color: #0d0d0d;

    border: 1px solid #2a2a2a;

    border-radius: 14px;

    padding: 28px;

    margin-top: 30px;

    color: white;

    font-size: 17px;

    line-height: 1.8;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #050505;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #8a8a8a;
    font-size: 12px;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<h1 class="truthful-title">TRUTHFUL</h1>
<p class="subtitle">
AI-Based Claim Verification & Perspective Analysis System
</p>
""", unsafe_allow_html=True)

# Input
user_input = st.text_area(
    "Enter a claim, statement, or news headline:",
    height=200
)

# Button
col1, col2, col3 = st.columns([2,1,2])

with col2:
    analyze_clicked = st.button(
        "Analyze",
        use_container_width=True
    )

# Analysis
if analyze_clicked:

    if user_input.strip() == "":
        st.warning("Please enter some text.")

    else:

        with st.spinner("Truthful is analyzing credibility and perspectives..."):

            prompt = f"""
You are an AI fact-checking and perspective-analysis assistant.

Analyze the following claim carefully.

Claim:
{user_input}

Your task:
1. Determine whether the claim appears factual, misleading, false, opinion-based, or unverifiable.
2. Explain the reasoning clearly.
3. If the topic is opinion-heavy, provide multiple perspectives.
4. If the claim is false or misleading, provide corrected information.
5. Suggest trusted sources where users can verify information.
6. Keep the tone professional and educational.
"""

            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = response.choices[0].message.content
            # Color and label based on verdict
            if "false" in result.lower() or "misleading" in result.lower():
                accent = "#FF4C4C"
                verdict = "⚠ POTENTIALLY MISLEADING"
                verdict_bg = "#2a0a0a"

            elif "factual" in result.lower() or "real" in result.lower():
                accent = "#4CAF82"
                verdict = "✓ APPEARS FACTUAL"
                verdict_bg = "#0a1f14"

            else:
                accent = "#4C9FFF"
                verdict = "◈ UNVERIFIABLE / OPINION"
                verdict_bg = "#0a1220"

            # Display
            st.markdown(f"""
                <div style="
                    background-color: #0d0d0d;
                    border: 1px solid #1f1f1f;
                    border-left: 4px solid {accent};
                    border-radius: 12px;
                    padding: 28px 32px;
                    margin-top: 24px;
                    font-size: 16px;
                    line-height: 1.9;
                    color: #e0e0e0;
                ">
                    <div style="
                        display: inline-block;
                        background-color: {verdict_bg};
                        color: {accent};
                        font-size: 11px;
                        font-weight: 700;
                        letter-spacing: 2px;
                        padding: 5px 12px;
                        border-radius: 6px;
                        margin-bottom: 18px;
                    ">{verdict}</div>
                    <div>{result}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Disclaimer
        st.markdown("""
        <div class="footer">
        TRUTHFUL assists users in evaluating credibility and perspective-bias using AI-driven contextual reasoning.<br>
        The system does not claim absolute truth determination.
        </div>
        """, unsafe_allow_html=True)
