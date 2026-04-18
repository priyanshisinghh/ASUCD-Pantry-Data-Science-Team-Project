import streamlit as st
import base64

st.set_page_config(page_title="ASUCD Pantry Data Science Team")

#background stuff
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
#end background stuff

st.title("ASUCD Pantry")
st.subheader("Data Science Team - Satisfaction Survey Analysis")

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

st.info("Click on the sidebar to see each member's findings and analysis")

st.markdown("---")
