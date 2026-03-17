import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_groq(question: str, students: list) -> str:
    """Send student data + question to Groq and get an answer"""

    if not students:
        return "No student data available in the sheet."

    # Format student data as readable text for Groq
    student_text = "\n".join(
        [f"- Name: {s.get('Name')}, Age: {s.get('Age')}, Grade: {s.get('Grade')}"
         for s in students]
    )

    prompt = f"""You are a helpful assistant. Here is a list of students from a database:

{student_text}

Answer the following question based only on this data:
{question}

Be concise and helpful."""

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content
