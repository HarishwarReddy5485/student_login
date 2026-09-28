from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


fake_database = {}

app = FastAPI()

class Student(BaseModel):
    id: str
    name: str
    email: str
    age: int
    course: str

class updateuser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None

@app.get("/student")
def home():
    return "this is student login"

@app.post("/student/login")
def std_login(student: Student):
    id = student.id
    name = student.name
    email = student.email
    age = student.age
    course = student.course
    if id in fake_database:
        return f"the {id} is already there please try again"
    fake_database[id] = student
    return id, f"the value inserted in the database is : {fake_database}"

@app.get("/students")
def student_display():
    return fake_database

@app.put("/update/{id}")
def update_students(id: str, updateuser: updateuser):
    if id not in fake_database:
        return f"The {id} is not there please register first"
    
    student = fake_database[id]
    if updateuser.name is not None:
        student.name = updateuser.name
    if updateuser.email is not None:
        student.email = updateuser.email
    if updateuser.age is not None:
        student.age = updateuser.age
    if updateuser.course is not None:
        student.course = updateuser.course
    
    return fake_database[id]

@app.delete("/delete/{id}")
def delete_students(id: str):
    if id not in fake_database:
        return "the id is not there please register first"
    del fake_database[id]  
    return f"the student with {id} has been deleted"

@app.get("/course/{course_name}")
def course_name(course_name: str):
    matching_students = [
        student for student in fake_database.values()
        if student.course.lower() == course_name.lower()
    ]
    if not matching_students:
        return f"No students found enrolled in course: {course_name}"
    return matching_students