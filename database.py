
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "career_analyzer.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                education TEXT,
                target_role TEXT,
                skills TEXT,
                interests TEXT,
                projects TEXT,
                discoverable INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS milestones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_email TEXT NOT NULL,
                title TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                completed_at TIMESTAMP,
                FOREIGN KEY(student_email) REFERENCES students(email)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_email TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                project_link TEXT,
                verification_status TEXT DEFAULT 'Unverified',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()


def save_student(
    name,
    email,
    education,
    target_role,
    skills,
    interests,
    projects,
    discoverable=False
):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO students (
                name, email, education, target_role,
                skills, interests, projects, discoverable
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                name=excluded.name,
                education=excluded.education,
                target_role=excluded.target_role,
                skills=excluded.skills,
                interests=excluded.interests,
                projects=excluded.projects,
                discoverable=excluded.discoverable
        """, (
            name,
            email,
            education,
            target_role,
            skills,
            interests,
            projects,
            int(discoverable)
        ))

        connection.commit()


def get_student(email):
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(
            "SELECT * FROM students WHERE email = ?",
            (email,)
        ).fetchone()

        return dict(result) if result else None


def get_discoverable_students():
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row

        results = connection.execute("""
            SELECT name, education, target_role, skills, projects
            FROM students
            WHERE discoverable = 1
        """).fetchall()

        return [dict(row) for row in results]


def add_milestone(email, title):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO milestones (student_email, title)
            VALUES (?, ?)
        """, (email, title))

        connection.commit()


def get_milestones(email):
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row

        results = connection.execute("""
            SELECT id, title, status
            FROM milestones
            WHERE student_email = ?
            ORDER BY id
        """, (email,)).fetchall()

        return [dict(row) for row in results]


def complete_milestone(milestone_id):
    with get_connection() as connection:
        connection.execute("""
            UPDATE milestones
            SET status = 'Completed',
                completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (milestone_id,))

        connection.commit()


def add_project(email, title, description, link):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO projects (
                student_email, title, description, project_link
            )
            VALUES (?, ?, ?, ?)
        """, (email, title, description, link))

        connection.commit()


def get_projects(email):
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row

        results = connection.execute("""
            SELECT title, description, project_link,
                   verification_status
            FROM projects
            WHERE student_email = ?
            ORDER BY id DESC
        """, (email,)).fetchall()

        return [dict(row) for row in results]
