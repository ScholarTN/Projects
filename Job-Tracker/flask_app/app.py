from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "jobtracker_secret_key"

API_URL = "http://127.0.0.1:8000"


@app.route("/")
def index():
    try:
        res = requests.get(f"{API_URL}/jobs")
        data = res.json()
        jobs  = data.get("jobs", [])
        stats = data.get("stats", {})
        total = data.get("total", 0)
    except Exception as e:
        jobs, stats, total = [], {}, 0
        flash(f"Could not connect to API: {e}", "error")
    return render_template("index.html", jobs=jobs, stats=stats, total=total)


@app.route("/add", methods=["POST"])
def add_job():
    payload = {
        "company":  request.form.get("company", "").strip(),
        "role":     request.form.get("role", "").strip(),
        "status":   request.form.get("status", "Applied"),
        "date":     request.form.get("date", ""),
        "location": request.form.get("location", "").strip(),
        "notes":    request.form.get("notes", "").strip(),
    }
    if not payload["company"] or not payload["role"] or not payload["date"]:
        flash("Company, role and date are required!", "error")
        return redirect(url_for("index"))
    try:
        res = requests.post(f"{API_URL}/jobs", json=payload)
        if res.ok:
            flash(f"✅ Application to {payload['company']} added!", "success")
        else:
            flash(res.json().get("detail", "Failed to add"), "error")
    except Exception as e:
        flash(f"API error: {e}", "error")
    return redirect(url_for("index"))


@app.route("/update/<int:job_id>", methods=["POST"])
def update_job(job_id):
    payload = {
        "status":   request.form.get("status"),
        "notes":    request.form.get("notes", "").strip(),
        "location": request.form.get("location", "").strip(),
    }
    payload = {k: v for k, v in payload.items() if v}
    try:
        res = requests.patch(f"{API_URL}/jobs/{job_id}", json=payload)
        if res.ok:
            flash("✅ Application updated!", "success")
        else:
            flash(res.json().get("detail", "Failed to update"), "error")
    except Exception as e:
        flash(f"API error: {e}", "error")
    return redirect(url_for("index"))


@app.route("/delete/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    try:
        res = requests.delete(f"{API_URL}/jobs/{job_id}")
        if res.ok:
            flash("🗑️ Application deleted!", "success")
        else:
            flash("Failed to delete", "error")
    except Exception as e:
        flash(f"API error: {e}", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
