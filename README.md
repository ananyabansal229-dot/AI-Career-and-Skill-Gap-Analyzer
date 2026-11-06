# AI Career & Skill Gap Analyzer

### An AI-powered career co-pilot for Students, Founders and Recruiters.

## About the Project

AI Career & Skill Gap Analyzer is a platform designed to help students understand the skills required for their desired careers and create personalized learning roadmaps.

The platform analyzes existing skills, projects, interests and job descriptions to identify skill gaps and recommend practical next steps.

It also supports founders looking for startup opportunities and recruiters searching for candidates with relevant skills.

## Problem Statement

Students often lack clarity about the skills, programming languages, projects and experiences required for their desired careers.

Beginners especially struggle to identify where to start.

Traditional career guidance is often generic and disconnected from real-world opportunities.

Recruiters also need better ways to discover candidates based on relevant skills and demonstrable work.

## Our Solution

We are building an intelligent career development platform that connects:

- Career exploration
- Skill gap analysis
- Personalized learning roadmaps
- Project recommendations
- Hackathon and event discovery
- Internship and placement opportunities
- Founder and startup guidance
- Proof-of-work resume building
- Consent-based recruiter matching

## Key Features

### 1. Student Journey

- Create a career profile.
- Upload an existing PDF resume.
- Identify existing skills.
- Select a target career.
- Analyze skill gaps.
- Generate a personalized roadmap.
- Discover relevant opportunities.
- Track completed milestones.

### 2. Career Intelligence

- Extract skills from text.
- Analyze job descriptions.
- Compare skills with career requirements.
- Prioritize missing skills.
- Recommend projects and learning activities.

### 3. Opportunity Discovery

- Hackathons
- Ideathons
- Workshops
- Competitions
- Internships
- Startup programs
- Networking events

### 4. Founder Journey

- Product problem discovery.
- Market research.
- MVP planning.
- Product development.
- User validation.
- Pitch preparation.
- Startup ecosystem discovery.

### 5. Proof-of-Work Resume

- Save projects.
- Record completed milestones.
- Build a resume from achievements.
- Download resume content.

### 6. Recruiter Journey

- Search opted-in student profiles.
- Match skills with hiring requirements.
- Compare relevant candidate skills.
- Respect user consent and privacy.

## Technology Stack

| Component | Technology |
|---|---|
| Programming | Python |
| Frontend | Streamlit |
| Database | SQLite |
| Data Processing | Pandas |
| Resume Reading | PyPDF |
| NLP | Rule-based skill extraction |
| Recommendation | Skill matching engine |
| Version Control | GitHub |

## Project Architecture

Student Profile / Resume / Job Description
                  |
                  v
          NLP Skill Extraction
                  |
                  v
         Career Analytics Engine
                  |
                  v
          Skill Gap Detection
                  |
                  v
        Recommendation Engine
                  |
          ----------------
          |              |
          v              v
    Learning Roadmap   Opportunities
          |
          v
     Evidence Layer
          |
          v
    Resume Builder
          |
          v
      Feedback Loop

## Repository Structure

AI-Career-and-Skill-Gap-Analyzer/
|
|-- app.py
|-- career_engine.py
|-- database.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|
|-- data/
    |-- career_roles.json
    |-- opportunities.json

## Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/AI-Career-and-Skill-Gap-Analyzer.git

Move into the project folder:

cd AI-Career-and-Skill-Gap-Analyzer

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

## Future Enhancements

- Transformer-based NLP.
- Semantic skill matching.
- AI-powered resume analysis.
- Real-time opportunity APIs.
- React frontend.
- Django REST backend.
- PostgreSQL database.
- Secure authentication.
- Verified project credentials.
- Personalized event recommendations.
- Advanced career analytics.
- Consent-based professional profile integrations.

## Privacy and Responsible AI

The prototype uses locally stored profiles and a consent-based recruiter discovery option.

It does not scrape LinkedIn, Instagram or other external platforms.

Skill match scores are indicative and must not be treated as hiring decisions or guaranteed employment outcomes.

## Team

**Team Name:** Apex Devs

**Team Members:** Ananya Bansal, Anchal, Jayant Sindhav, Sparsh Dheer

## Project Vision

Not just a career suggestion.

A measurable journey from ambition to evidence.
