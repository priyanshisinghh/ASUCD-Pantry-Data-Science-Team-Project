import streamlit as st

st.set_page_config(page_title="ASUCD Pantry - Data Science Team", layout="wide")

st.title("🛒 ASUCD Pantry")
st.subheader("Data Science Team — Satisfaction & Impact Analysis")

st.markdown("---")

st.header("About the ASUCD Pantry")
st.write("""
The ASUCD Pantry is a free, student-run food resource at UC Davis dedicated to fighting food insecurity 
on campus. We believe that no student should have to choose between buying groceries and paying for 
tuition, housing, or other essentials. The Pantry is open to all UC Davis students, no questions asked.
""")

st.markdown("---")

st.header("Our Mission")
st.write("""
Our mission is to provide accessible, dignified food support to the UC Davis community. We are committed 
to reducing the stigma around food insecurity and ensuring every student has the nutrition they need to 
thrive academically and personally.
""")

st.markdown("---")

st.header("What We Offer")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🥫 Free Groceries")
    st.write("Students can shop for free groceries including fresh produce, pantry staples, snacks, and hygiene products.")

with col2:
    st.subheader("📦 No Eligibility Requirements")
    st.write("Any UC Davis student can visit the Pantry — no proof of need, no forms, no barriers.")

with col3:
    st.subheader("🤝 Community Support")
    st.write("Beyond food, we connect students with campus resources, emergency funds, and other support services.")

st.markdown("---")

st.header("About This Project")
st.write("""
This site was created by the ASUCD Pantry Data Science Team. Our goal was to better understand 
the experiences of students who use the Pantry by designing and distributing a satisfaction survey. 
Through this project we explored:
""")

st.write("""
- How satisfied students are with the Pantry's services, hours, and offerings
- What barriers students face when accessing the Pantry
- How the Pantry can better serve the UC Davis community
- Trends in usage and student feedback over time
""")

st.info("👈 Use the sidebar to explore each team member's individual findings and analysis.")

st.markdown("---")
st.caption("ASUCD Pantry Data Science Team · UC Davis · 2025")