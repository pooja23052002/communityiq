"""
CommunityIQ v2
Global UI Theme

Google Cloud inspired styling
"""

import streamlit as st


def load_css():
    st.markdown(
        """
<style>

/* ===============================
   IMPORT FONT
================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family: 'Inter', sans-serif;
}

/* ===============================
   HIDE DEFAULT STREAMLIT
================================ */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* ===============================
   PAGE
================================ */

.stApp{
    background:#F5F7FB;
}

/* ===============================
   HERO
================================ */

.hero{

background:linear-gradient(135deg,#1A73E8,#4285F4);

padding:32px;

border-radius:24px;

color:white;

margin-bottom:25px;

box-shadow:0 8px 25px rgba(26,115,232,.20);

}

.hero h1{

margin:0;

font-size:38px;

font-weight:700;

}

.hero h3{

margin-top:10px;

font-weight:400;

opacity:.95;

}

.hero p{

margin-top:18px;

font-size:16px;

opacity:.90;

}

/* ===============================
   SECTION TITLE
================================ */

.section-title{

font-size:24px;

font-weight:700;

margin-top:15px;

margin-bottom:20px;

color:#1F2937;

}

/* ===============================
   KPI CARD
================================ */

.kpi-card{

background:white;

border-radius:18px;

padding:22px;

box-shadow:0 4px 18px rgba(0,0,0,.08);

transition:.3s;

border-top:4px solid #4285F4;

}

.kpi-card:hover{

transform:translateY(-4px);

box-shadow:0 12px 28px rgba(0,0,0,.12);

}

.kpi-title{

font-size:14px;

color:#6B7280;

margin-bottom:8px;

}

.kpi-value{

font-size:36px;

font-weight:700;

color:#111827;

}

.kpi-change{

font-size:14px;

font-weight:600;

color:#34A853;

}

/* ===============================
   DASHBOARD CARD
================================ */

.dashboard-card{

background:white;

padding:24px;

border-radius:20px;

box-shadow:0 4px 15px rgba(0,0,0,.07);

margin-bottom:20px;

}

/* ===============================
   AI CARD
================================ */

.ai-card{

background:#F8FBFF;

border:1px solid #D2E3FC;

border-left:6px solid #4285F4;

padding:22px;

border-radius:18px;

margin-bottom:15px;

}

/* ===============================
   RECOMMENDATION
================================ */

.recommend-card{

background:#F1F8F4;

border-left:6px solid #34A853;

padding:18px;

border-radius:16px;

margin-top:10px;

}

/* ===============================
   WARNING
================================ */

.warning-card{

background:#FFF8E1;

border-left:6px solid #FBBC05;

padding:18px;

border-radius:16px;

}

/* ===============================
   CRITICAL
================================ */

.critical-card{

background:#FDECEC;

border-left:6px solid #EA4335;

padding:18px;

border-radius:16px;

}

/* ===============================
   AGENT CARD
================================ */

.agent-card{

background:white;

padding:20px;

border-radius:18px;

box-shadow:0 4px 14px rgba(0,0,0,.08);

border-top:5px solid #1A73E8;

margin-bottom:18px;

}

/* ===============================
   BADGES
================================ */

.badge{

display:inline-block;

padding:6px 12px;

border-radius:999px;

font-size:13px;

font-weight:600;

margin-right:8px;

}

.badge-blue{

background:#D2E3FC;

color:#174EA6;

}

.badge-green{

background:#E6F4EA;

color:#137333;

}

.badge-yellow{

background:#FEF7E0;

color:#B06000;

}

.badge-red{

background:#FCE8E6;

color:#C5221F;

}

/* ===============================
   SIDEBAR
================================ */

section[data-testid="stSidebar"]{

background:white;

border-right:1px solid #E5E7EB;

}

/* ===============================
   BUTTON
================================ */

.stButton>button{

background:#1A73E8;

color:white;

border-radius:12px;

border:none;

padding:.6rem 1.3rem;

font-weight:600;

}

.stButton>button:hover{

background:#1557B0;

}

/* ===============================
   METRIC
================================ */

div[data-testid="metric-container"]{

background:white;

padding:18px;

border-radius:18px;

box-shadow:0 3px 12px rgba(0,0,0,.06);

}

/* ===============================
   CHAT
================================ */

.stChatMessage{

border-radius:16px;

padding:12px;

}

/* ===============================
   DATAFRAME
================================ */

[data-testid="stDataFrame"]{

border-radius:18px;

overflow:hidden;

}

/* ===============================
   SCROLLBAR
================================ */

::-webkit-scrollbar{

width:8px;

}

::-webkit-scrollbar-thumb{

background:#C9D2E3;

border-radius:10px;

}

</style>
""",
        unsafe_allow_html=True,
    )


def hero_section():

    st.markdown(
        """
<div class="hero">

<h1>🏙️ CommunityIQ</h1>

<h3>AI-Powered Decision Intelligence Platform</h3>

<p>
Built with <b>Google Gemini</b>,
<b>Vertex AI</b>,
<b>Google Cloud</b>,
and Explainable AI to help cities make
smarter and faster community decisions.
</p>

</div>
""",
        unsafe_allow_html=True,
    )


def section(title):

    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True,
    )