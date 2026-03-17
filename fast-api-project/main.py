from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from sheets import get_all_students, add_student, delete_student, update_student
from groq_ai import ask_groq

app = FastAPI(
    title="Student Record Manager",
    description="FastAPI + Google Sheets + Groq AI",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Pydantic Models ──────────────────────────────────────────────

class Student(BaseModel):
    name: str
    age: int
    grade: str


class UpdateStudent(BaseModel):
    age: Optional[int] = None
    grade: Optional[str] = None


class Question(BaseModel):
    question: str


# ── Routes ───────────────────────────────────────────────────────

@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/students")
def read_students():
    """Get all students from Google Sheet"""
    students = get_all_students()
    return {"total": len(students), "students": students}


@app.post("/students")
def create_student(student: Student):
    result = add_student(student.name, student.age, student.grade)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.patch("/students/{name}")
def update_student_record(name: str, update: UpdateStudent):
    """Update a student's age or grade by name"""
    result = update_student(name, update.age, update.grade)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.delete("/students/{name}")
def remove_student(name: str):
    """Delete a student by name"""
    result = delete_student(name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/ask")
def ask_question(body: Question):
    """Ask Groq AI a question about the student data"""
    students = get_all_students()
    answer = ask_groq(body.question, students)
    return {"question": body.question, "answer": answer}
