import streamlit as st

# Customizing Streamlit Style
st.markdown(
    """
    <style>
        body {
            background-color: #FF0000;
        }
        .navbar {
            display: flex;
            background-color: #333;
            padding: 10px;
            justify-content: space-around;
            color: white;
        }
        .navbar a {
            color: white;
            text-decoration: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def home():
    st.title("My Portfolio - Home")
    st.subheader("Welcome to my personal portfolio!")
    st.write(
        "I am a passionate software developer with experience in building web applications and machine learning projects."
    )

def skills():
    st.title("My Portfolio - Skills")
    st.header("Skills")
    skills = ["Python", "JavaScript", "React", "Flask", "Machine Learning"]
    st.write(", ".join(skills))

def projects():
    st.title("My Portfolio - Projects")
    st.header("Projects")
    projects = [
        {"name": "Project 1", "description": "Description of Project 1"},
        {"name": "Project 2", "description": "Description of Project 2"},
    ]

    for project in projects:
        st.write(f"**{project['name']}**: {project['description']}")

def contact():
    st.title("My Portfolio - Contact")
    st.header("Contact")
    st.write("Feel free to reach out to me at: your.email@example.com")

def main():
    st.markdown("<h1 class='navbar'>", unsafe_allow_html=True)
    page = st.radio("Go to", ["Home", "Skills", "Projects", "Contact"])

    if page == "Home":
        home()
    elif page == "Skills":
        skills()
    elif page == "Projects":
        projects()
    elif page == "Contact":
        contact()

if __name__ == "__main__":
    main()
