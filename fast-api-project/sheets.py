import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHEETBEST_URL = os.getenv("SHEETBEST_URL")


def get_all_students():
    """Read all students from Google Sheet"""
    response = requests.get(SHEETBEST_URL)
    if response.status_code == 200:
        return response.json()
    return []


def add_student(name: str, age: int, grade: str):
    data = {"Name": name, "Age": age, "Grade": grade}
    print(f"[DEBUG] Sending: {data}")
    response = requests.post(SHEETBEST_URL, json=data)
    print(f"[DEBUG] Response: {response.status_code} | {response.text}")
    if response.status_code in (200, 201):
        return {"message": f"Student '{name}' added successfully!"}
    return {"error": f"Sheet.best error ({response.status_code}): {response.text}"}


def delete_student(name: str):
    """Delete a student by name from Google Sheet"""
    url = f"{SHEETBEST_URL}/Name/{name}"
    response = requests.delete(url)
    if response.status_code == 200:
        return {"message": f"Student '{name}' deleted successfully!"}
    return {"error": f"Failed to delete student '{name}'"}


def update_student(name: str, age: int = None, grade: str = None):
    """Update a student's details by name"""
    url = f"{SHEETBEST_URL}/Name/{name}"
    data = {}
    if age is not None:
        data["Age"] = age
    if grade is not None:
        data["Grade"] = grade
    response = requests.patch(url, json=data)
    if response.status_code == 200:
        return {"message": f"Student '{name}' updated successfully!"}
    return {"error": f"Failed to update student '{name}'"}
