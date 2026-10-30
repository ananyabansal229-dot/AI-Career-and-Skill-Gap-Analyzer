
import streamlit as st
import pandas as pd
from pypdf import PdfReader
from io import BytesIO

from career_engine import (
    load_roles,
    extract_skills,
    analyze_career,
    recommend_opportunities,
    build_founder_roadmap
)

from database import (
    initialize_database,
    save_student,
    get_student,
    get_discoverable_students,
    add_milestone,
    get_milestones,
    complete_milestone,
    add_project,
    get_projects
)


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Career & Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)

initialize_database()

roles = load_roles()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "student_email" not in st.session_state:
    st.session_state.student_email = ""

if "uploaded_skills" not in st.session_state:
    st.session_state.uploaded_skills = []


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_student_data():
    email = st.session_state.student_email

    if not email:
        return None

    return get_student(email)


def parse_resume(uploaded_file):
    try:
        reader = PdfReader(BytesIO(uploaded_file.getvalue()))

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    except Exception as error:
        st.error(f"Could not read the resume: {error}")
        return ""


def show_header(title, subtitle):
    st.title(title)
    st.caption(subtitle)
    st.divider()


def get_progress():
    student = get_student_data()

    if not student:
        return 0

    milestones = get_milestones(student["email"])

    if not milestones:
        return 0

    completed = sum(
        1 for item in milestones
        if item["status"] == "Completed"
    )

    return round(completed / len(milestones) * 100)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎯 CareerPilot AI")
st.sidebar.caption("Your journey from skills to opportunities")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Home Dashboard",
        "Student Profile",
        "Career Explorer",
        "Skill Gap Analyzer",
        "Personalized Roadmap",
        "Opportunities",
        "Founder Journey",
        "Resume Builder",
        "Recruiter Dashboard"
    ]
)

st.sidebar.divider()

if st.session_state.student_email:
    st.sidebar.success(
        "Logged-in profile: " +
        st.session_state.student_email
    )
else:
    st.sidebar.info(
        "Create your profile to access saved progress."
    )


# --------------------------------------------------
# HOME DASHBOARD
# --------------------------------------------------

if page == "Home Dashboard":

    show_header(
        "AI Career & Skill Gap Analyzer",
        "An intelligent career co-pilot for students, founders and recruiters."
    )

    st.markdown(
        """
        ### Turn your career ambitions into an actionable plan.

        Discover what to learn, what to build, where to participate,
        and which opportunities match your career goals.
        """
    )

    student = get_student_data()

    if student:

        progress = get_progress()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Target Career",
                student["target_role"] or "Not selected"
            )

        with col2:
            st.metric(
                "Learning Progress",
                f"{progress}%"
            )

        with col3:
            st.metric(
                "Projects Added",
                len(get_projects(student["email"]))
            )

        st.subheader("Your Career Journey")

        st.progress(progress / 100)

        st.write(
            f"Welcome, {student['name']}!"
        )

        st.info(
            "Continue your roadmap and record your achievements."
        )

    else:

        st.info(
            "You haven't created your student profile yet. "
            "Visit Student Profile to get started."
        )

    st.subheader("Explore Platform Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🎓 Student Journey")
        st.write(
            "Personalized learning paths, projects, "
            "hackathons and internship discovery."
        )

    with col2:
        st.markdown("### 🚀 Founder Journey")
        st.write(
            "Product development, ideathons, "
            "pitch events and startup opportunities."
        )

    with col3:
        st.markdown("### 💼 Recruiter Journey")
        st.write(
            "Discover candidates who have opted in "
            "to skills-based profile discovery."
        )

    st.divider()

    st.markdown(
        "**Our USP:** Not just a career suggestion. "
        "A measurable journey from ambition to evidence."
    )


# --------------------------------------------------
# STUDENT PROFILE
# --------------------------------------------------

elif page == "Student Profile":

    show_header(
        "Create Your Student Profile",
        "Tell us about your background, interests and career goals."
    )

    with st.form("student_profile_form"):

        name = st.text_input("Full Name")

        email = st.text_input("Email Address")

        education = st.text_input(
            "Education",
            placeholder="B.Tech CSE, 2nd Year"
        )

        career_options = list(roles.keys())

        target_role = st.selectbox(
            "Your Target Career",
            career_options
        )

        interests = st.text_area(
            "Your Interests",
            placeholder="Artificial Intelligence, Web Development, Data Science..."
        )

        skill_text = st.text_area(
            "Your Existing Skills",
            placeholder="Python, HTML, CSS, SQL..."
        )

        project_text = st.text_area(
            "Projects You Have Built",
            placeholder="Personal portfolio, chatbot, data analysis..."
        )

        discoverable = st.checkbox(
            "I consent to making my profile discoverable "
            "to recruiters using this prototype."
        )

        submitted = st.form_submit_button(
            "Save My Profile"
        )

        if submitted:

            if not name.strip() or not email.strip():
                st.error(
                    "Please enter your name and email."
                )

            elif "@" not in email or "." not in email:
                st.error(
                    "Please enter a valid email address."
                )

            else:

                save_student(
                    name=name.strip(),
                    email=email.strip().lower(),
                    education=education,
                    target_role=target_role,
                    skills=skill_text,
                    interests=interests,
                    projects=project_text,
                    discoverable=discoverable
                )

                st.session_state.student_email = (
                    email.strip().lower()
                )

                st.success(
                    "Your profile has been saved successfully!"
                )


    st.divider()

    st.subheader("Upload Your Existing Resume")

    uploaded_file = st.file_uploader(
        "Upload a PDF resume to extract your skills",
        type=["pdf"]
    )

    if uploaded_file:

        resume_text = parse_resume(uploaded_file)

        if resume_text:

            found_skills = extract_skills(resume_text)

            st.session_state.uploaded_skills = found_skills

            st.success("Resume processed successfully.")

            st.write("Recognized skills:")

            if found_skills:
                st.write(", ".join(found_skills))
            else:
                st.info(
                    "No supported skills were recognized. "
                    "You can enter your skills manually."
                )


# --------------------------------------------------
# CAREER EXPLORER
# --------------------------------------------------

elif page == "Career Explorer":

    show_header(
        "Explore Career Paths",
        "Discover skills, programming languages and projects required by different industries."
    )

    selected_role = st.selectbox(
        "Select a career",
        list(roles.keys())
    )

    role = roles[selected_role]

    st.subheader(selected_role)

    st.write(
        f"Industry: {role['industry']}"
    )

    st.subheader("Required Skills")

    skill_df = pd.DataFrame([
        {
            "Skill": skill,
            "Importance": importance.title()
        }
        for skill, importance in role["skills"].items()
    ])

    st.dataframe(
        skill_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Programming Languages")

    st.write(", ".join(role["languages"]))

    st.subheader("Suggested Projects")

    for project in role["projects"]:
        st.write(f"• {project}")

    st.subheader("Recommended Learning Sequence")

    for index, lesson in enumerate(
        role["learning"], start=1
    ):
        st.write(f"{index}. {lesson}")


# --------------------------------------------------
# SKILL GAP ANALYZER
# --------------------------------------------------

elif page == "Skill Gap Analyzer":

    show_header(
        "AI Skill Gap Analyzer",
        "Compare your current capabilities with your desired career or a specific job description."
    )

    student = get_student_data()

    default_skills = ""

    if student:
        default_skills = student["skills"] or ""

    if st.session_state.uploaded_skills:
        uploaded_text = ", ".join(
            st.session_state.uploaded_skills
        )
        default_skills = (
            default_skills + ", " + uploaded_text
        ).strip(", ")

    with st.form("skill_analysis_form"):

        target_role = st.selectbox(
            "Select Your Target Role",
            list(roles.keys())
        )

        current_skills = st.text_area(
            "Enter your current skills",
            value=default_skills,
            placeholder="Python, SQL, HTML, CSS..."
        )

        interests = st.text_area(
            "Your career interests",
            placeholder="AI, software development, analytics..."
        )

        job_description = st.text_area(
            "Paste a target job description (optional)",
            placeholder="Paste the required skills and responsibilities from a job listing..."
        )

        analyze = st.form_submit_button(
            "Analyze My Skill Gap"
        )

        if analyze:

            skill_list = [
                item.strip()
                for item in current_skills.split(",")
                if item.strip()
            ]

            result = analyze_career(
                target_role=target_role,
                current_skills=skill_list,
                interests=interests,
                job_description=job_description
            )

            st.session_state.analysis = result

            st.success(
                "Your career skill analysis is ready!"
            )

    result = st.session_state.analysis

    if result:

        st.divider()

        st.subheader("Your Skill Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Skill Match",
                f"{result['match_percentage']}%"
            )

        with col2:
            st.metric(
                "Skills Matched",
                len(result["matched_skills"])
            )

        with col3:
            st.metric(
                "Skills To Develop",
                len(result["missing_skills"])
            )

        st.progress(
            result["match_percentage"] / 100
        )

        st.subheader("Skills You Already Have")

        if result["matched_skills"]:
            st.success(
                ", ".join(result["matched_skills"])
            )
        else:
            st.info("No matching skills detected yet.")

        st.subheader("Your Skill Gaps")

        if result["missing_skills"]:

            gap_df = pd.DataFrame([
                {
                    "Missing Skill": item["skill"],
                    "Priority": item["priority"].title(),
                    "Recommended Action": item["action"]
                }
                for item in result["roadmap"]
            ])

            st.dataframe(
                gap_df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.success(
                "All skills in this selected target "
                "have been recognized in your profile."
            )

        st.caption(
            "The match percentage measures recognized skill overlap, "
            "not employability or guaranteed job readiness."
        )


# --------------------------------------------------
# PERSONALIZED ROADMAP
# --------------------------------------------------

elif page == "Personalized Roadmap":

    show_header(
        "Your Personalized Learning Roadmap",
        "Follow your learning journey from beginner level to your target career."
    )

    student = get_student_data()

    if not student:

        st.warning(
            "Create your profile first to access your saved roadmap."
        )

    else:

        st.write(
            f"Target career: **{student['target_role']}**"
        )

        if st.session_state.analysis:

            result = st.session_state.analysis

            st.subheader("Recommended Learning Path")

            for item in result["roadmap"]:

                with st.expander(
                    f"Step {item['step']}: {item['skill']}"
                ):

                    st.write(
                        f"Priority: {item['priority'].title()}"
                    )

                    st.write(item["action"])

            st.subheader("Recommended Projects")

            for project in result["projects"]:
                st.write(f"• {project}")

            st.subheader("Learning Sequence")

            for lesson in result["learning"]:
                st.write(f"• {lesson}")

            if st.button("Save Roadmap Milestones"):

                for item in result["roadmap"]:
                    add_milestone(
                        student["email"],
                        f"Learn {item['skill']}"
                    )

                for project in result["projects"]:
                    add_milestone(
                        student["email"],
                        f"Build: {project}"
                    )

                st.success(
                    "Roadmap milestones saved to your profile."
                )

        else:

            st.info(
                "Run Skill Gap Analyzer first to generate "
                "your personalized roadmap."
            )

        st.divider()

        st.subheader("Track Your Progress")

        milestones = get_milestones(student["email"])

        if milestones:

            for item in milestones:

                if item["status"] == "Completed":
                    st.write(
                        f"✅ {item['title']} — Completed"
                    )
                else:

                    if st.button(
                        f"Mark completed: {item['title']}",
                        key=f"milestone_{item['id']}"
                    ):

                        complete_milestone(item["id"])

                        st.rerun()

        else:

            st.info(
                "Generate and save your roadmap to start tracking progress."
            )


# --------------------------------------------------
# OPPORTUNITY FINDER
# --------------------------------------------------

elif page == "Opportunities":

    show_header(
        "Opportunity Discovery",
        "Discover hackathons, competitions, workshops and internships."
    )

    student = get_student_data()

    audience = st.selectbox(
        "Opportunity category",
        [
            "Student",
            "Developer",
            "AI Engineer",
            "Data Scientist",
            "Data Analyst",
            "Founder",
            "Entrepreneur"
        ]
    )

    if student and audience == "Student":
        skills = [
            item.strip()
            for item in (student["skills"] or "").split(",")
            if item.strip()
        ]

    elif student:
        skills = [
            item.strip()
            for item in (student["skills"] or "").split(",")
            if item.strip()
        ]

    else:
        skills = []

    extra_skills = st.text_input(
        "Add skills to improve opportunity matching",
        placeholder="Python, AI, Git..."
    )

    skills.extend(
        item.strip()
        for item in extra_skills.split(",")
        if item.strip()
    )

    if st.button("Find Opportunities"):

        recommendations = recommend_opportunities(
            skills,
            audience
        )

        if not recommendations:

            st.info("No matching opportunities found.")

        else:

            for item in recommendations:

                with st.container(border=True):

                    st.subheader(item["title"])

                    st.caption(
                        f"{item['type']} | {item['location']}"
                    )

                    st.write(item["description"])

                    st.write(
                        f"Skill match score: {item['match_score']}"
                    )

                    st.write(
                        "Relevant skills: " +
                        (
                            ", ".join(item["matched_skills"])
                            if item["matched_skills"]
                            else "General opportunity"
                        )
                    )

                    st.caption(item["status"])

                    st.link_button(
                        "Visit Official Website",
                        item["url"]
                    )


# --------------------------------------------------
# FOUNDER JOURNEY
# --------------------------------------------------

elif page == "Founder Journey":

    show_header(
        "Founder & Startup Journey",
        "Turn your product idea into a validated startup concept."
    )

    product_idea = st.text_area(
        "Describe your product or startup idea",
        placeholder="What problem are you solving? Who are your target users?"
    )

    if st.button("Generate Founder Roadmap"):

        if product_idea.strip():

            roadmap = build_founder_roadmap(
                product_idea
            )

            st.subheader("Your Startup Development Roadmap")

            for item in roadmap:

                with st.expander(item["phase"]):

                    st.write(item["task"])

                    st.success(
                        "Expected output: " + item["output"]
                    )

            st.info(
                "Explore the Opportunities section for "
                "startup programs, networking and pitch resources."
            )

        else:

            st.warning(
                "Please describe your product idea first."
            )


# --------------------------------------------------
# PROJECTS AND RESUME BUILDER
# --------------------------------------------------

elif page == "Resume Builder":

    show_header(
        "Proof-of-Work Resume Builder",
        "Build a resume from your saved skills, projects and achievements."
    )

    student = get_student_data()

    if not student:

        st.warning(
            "Please create a student profile first."
        )

    else:

        st.subheader("Add a Project")

        with st.form("project_form"):

            project_title = st.text_input(
                "Project Title"
            )

            description = st.text_area(
                "Project Description"
            )

            project_link = st.text_input(
                "GitHub / Portfolio Link"
            )

            add_project_button = st.form_submit_button(
                "Add Project"
            )

            if add_project_button:

                if project_title.strip():

                    add_project(
                        student["email"],
                        project_title,
                        description,
                        project_link
                    )

                    st.success(
                        "Project added successfully."
                    )

                else:

                    st.warning(
                        "Please enter a project title."
                    )

        st.divider()

        projects = get_projects(student["email"])

        st.subheader("Your Saved Projects")

        for project in projects:

            st.markdown(
                f"**{project['title']}**"
            )

            st.write(project["description"])

            if project["project_link"]:
                st.write(project["project_link"])

            st.caption(
                "Evidence status: " +
                project["verification_status"]
            )

        st.divider()

        st.subheader("Your Resume Preview")

        resume = f"""
{student['name']}
{student['email']}

EDUCATION
{student['education']}

CAREER OBJECTIVE
Aspiring professional targeting the role of
{student['target_role']}.

SKILLS
{student['skills']}

INTERESTS
{student['interests']}

PROJECTS
{student['projects']}
"""

        for project in projects:

            resume += f"""

{project['title']}
{project['description']}
Project Link: {project['project_link']}
Evidence Status: {project['verification_status']}
"""

        milestones = get_milestones(student["email"])

        resume += "\nACHIEVEMENTS AND MILESTONES\n"

        for item in milestones:

            if item["status"] == "Completed":

                resume += (
                    f"\n- {item['title']}"
                )

        st.text_area(
            "Resume Content",
            resume,
            height=350
        )

        st.download_button(
            "Download My Resume",
            data=resume,
            file_name="my_career_resume.txt",
            mime="text/plain"
        )

        st.caption(
            "This is an initial editable text resume. "
            "Review all information before using it professionally."
        )


# --------------------------------------------------
# RECRUITER DASHBOARD
# --------------------------------------------------

elif page == "Recruiter Dashboard":

    show_header(
        "Recruiter Candidate Discovery",
        "Find candidates based on their skills and career profiles."
    )

    st.warning(
        "Prototype demonstration: This dashboard uses only "
        "profiles explicitly opted into discovery within this "
        "application. It does not scrape LinkedIn, Instagram "
        "or other external platforms."
    )

    required_role = st.selectbox(
        "Hiring for",
        list(roles.keys())
    )

    required_skills = st.text_input(
        "Required skills",
        placeholder="Python, SQL, Machine Learning..."
    )

    if st.button("Search Candidates"):

        candidates = get_discoverable_students()

        requested_skills = extract_skills(
            required_skills
        )

        results = []

        for candidate in candidates:

            candidate_skills = extract_skills(
                candidate["skills"]
            )

            matched = set(candidate_skills).intersection(
                requested_skills
            )

            score = (
                round(
                    len(matched) / len(requested_skills) * 100
                )
                if requested_skills else 0
            )

            if (
                candidate["target_role"] == required_role
                or matched
            ):

                results.append({
                    "Name": candidate["name"],
                    "Education": candidate["education"],
                    "Target Role": candidate["target_role"],
                    "Matched Skills": ", ".join(matched),
                    "Skill Match": f"{score}%"
                })

        if results:

            results.sort(
                key=lambda item: int(
                    item["Skill Match"].replace("%", "")
                ),
                reverse=True
            )

            st.subheader("Matching Candidates")

            st.dataframe(
                pd.DataFrame(results),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No matching opted-in profiles found."
            )

        st.caption(
            "Skill similarity is not a hiring decision. "
            "Recruiters must independently assess candidates "
            "and obtain permission before contacting them."
        )
