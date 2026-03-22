from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import Optional, List
from sqlalchemy.orm import Session
from database import JobApplication, create_tables, get_db

app = FastAPI(title="Job Tracker API", version="1.0.0")

# Allow Flask frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
create_tables()


# ── Pydantic Models ──────────────────────────────────────────────

VALID_STATUSES = ["Applied", "Interview", "Offer", "Rejected", "Withdrawn"]

class JobCreate(BaseModel):
    company: str
    role: str
    status: str = "Applied"
    date: str
    location: Optional[str] = ""
    notes: Optional[str] = ""

    @validator("company", "role")
    def must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    @validator("status")
    def valid_status(cls, v):
        if v not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {VALID_STATUSES}")
        return v


class JobUpdate(BaseModel):
    company:  Optional[str] = None
    role:     Optional[str] = None
    status:   Optional[str] = None
    location: Optional[str] = None
    notes:    Optional[str] = None

    @validator("status")
    def valid_status(cls, v):
        if v and v not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {VALID_STATUSES}")
        return v


# ── Routes ───────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Job Tracker API is running 🚀"}


@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobApplication).order_by(JobApplication.id.desc()).all()
    jobs_list = [
        {"id": j.id, "company": j.company, "role": j.role,
         "status": j.status, "date": j.date,
         "location": j.location, "notes": j.notes}
        for j in jobs
    ]
    # Stats summary
    total = len(jobs_list)
    stats = {s: sum(1 for j in jobs_list if j["status"] == s) for s in VALID_STATUSES}
    return {"total": total, "jobs": jobs_list, "stats": stats}


@app.post("/jobs")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = JobApplication(**job.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"message": f"Application to {job.company} added!", "id": new_job.id}


@app.patch("/jobs/{job_id}")
def update_job(job_id: int, update: JobUpdate, db: Session = Depends(get_db)):
    job = db.query(JobApplication).filter(JobApplication.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    for field, value in update.dict(exclude_none=True).items():
        setattr(job, field, value)
    db.commit()
    return {"message": "Application updated!"}


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobApplication).filter(JobApplication.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Application deleted!"}
