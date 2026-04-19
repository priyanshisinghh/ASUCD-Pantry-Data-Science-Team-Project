import streamlit as st
import base64

st.set_page_config(page_title="ASUCD Pantry Data Science Team")

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64("pages/images/home-bg.png")

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    </style>
""", unsafe_allow_html=True)

st.title("ASUCD Pantry")
st.subheader("Data Science Team — Satisfaction Survey Analysis")

st.markdown("---")

# Key findings upfront
st.header("What We Found")
st.write("We surveyed UC Davis students who use the Pantry. Here are the top takeaways:")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    🛒 **Item satisfaction drives experience**
    
    How happy patrons are with the item selection is the best predictor of their overall shopping experience.
    """)

with col2:
    st.info("""
    📣 **Outreach works differently for volunteers versus patrons**
    
    Volunteers and patrons discover the Pantry through very different channels. Targeted outreach will be more effective than broad campaigns.
    """)

with col3:
    st.info("""
    🥦 **Demographics don't predict produce access**
    
    No significant difference was found between racial or ethnic groups in how often they find the produce they need.
    """)

st.markdown("---")

st.header("About ASUCD Pantry")
st.write("""
The ASUCD Pantry is a free, student-run food resource at UC Davis dedicated to fighting food insecurity 
on campus. We believe that no student should have to choose between buying groceries and paying for 
tuition, housing, or other essentials. The Pantry is open to all UC Davis students, faculty, and UC Davis affiliated members.
""")

st.markdown("---")

st.header("About This Project")
st.write("""
This site was created by the ASUCD Pantry Data Science Team. We designed and distributed a satisfaction 
survey to better understand the experiences of students who use the Pantry. Through this project we explored:
""")

col_a, col_b = st.columns(2)
with col_a:
    st.write("""
    - How satisfied students are with the Pantry's services and offerings
    - What types of items students want more of
    """)
with col_b:
    st.write("""
    - Whether demographics affect access to produce
    - What drives a good overall shopping experience
    """)

st.markdown("---")

st.header("How to Use This Site")
st.write("""
Use the **sidebar on the left** to explore each team member's analysis. You don't need any stats 
background — each page explains its findings in plain English with interactive tools you can play with.
""")

col1, col2, col3, col4 = st.columns(4)
col1.success("🛍️ **Shopping Experience**\nAndrew's analysis")
col2.success("📣 **Outreach & Inventory**\nJaxon's analysis")
col3.success("🥗 **Item Requests**\nPri's analysis")
col4.success("👥 **Demographics**\nRisitha's analysis")

st.markdown("---")
st.caption("ASUCD Pantry Data Science Team · UC Davis · 2025-2026")
