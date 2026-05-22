# ============================================================
#  Task Manager API - Now with a real database! (SQLite)
# ============================================================
#  Endpoints:
#    GET    /tasks         -> get all tasks        (READ)
#    GET    /tasks/<id>    -> get one task          (READ)
#    POST   /tasks         -> create a task         (CREATE)
#    PUT    /tasks/<id>    -> update a task         (UPDATE)
#    DELETE /tasks/<id>    -> delete a task         (DELETE)
# ============================================================

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config - creates a file called "database.db" in your project folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ── Database Schema ──────────────────────────────────────────
# This defines the "tasks" table - like designing columns in Excel
class Task(db.Model):
    id          = db.Column(db.Integer, primary_key=True)    # auto-generated ID
    title       = db.Column(db.String(100), nullable=False)  # required field
    description = db.Column(db.String(300), nullable=True)   # optional field
    completed   = db.Column(db.Boolean, default=False)       # true or false

    def to_dict(self):
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "completed":   self.completed,
        }


# ── Helpers ──────────────────────────────────────────────────
def success(data, status=200):
    return jsonify({"success": True, "data": data}), status

def error(message, status=400):
    return jsonify({"success": False, "error": message}), status


# ── CREATE: POST /tasks ──────────────────────────────────────
@app.route("/tasks", methods=["POST"])
def create_task():
    body = request.get_json()
    if not body:
        return error("Request body must be JSON")
    title       = body.get("title", "").strip()
    description = body.get("description", "").strip()
    if not title:
        return error("'title' is required and cannot be empty")
    if len(title) > 100:
        return error("'title' must be 100 characters or less")
    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return success(task.to_dict(), 201)


# ── READ: GET /tasks ─────────────────────────────────────────
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return success([t.to_dict() for t in tasks])


# ── READ: GET /tasks/<id> ────────────────────────────────────
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return error(f"Task with id {task_id} not found", 404)
    return success(task.to_dict())


# ── UPDATE: PUT /tasks/<id> ──────────────────────────────────
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return error(f"Task with id {task_id} not found", 404)
    body = request.get_json()
    if not body:
        return error("Request body must be JSON")
    if "title" in body:
        title = body["title"].strip()
        if not title:
            return error("'title' cannot be empty")
        task.title = title
    if "description" in body:
        task.description = body["description"].strip()
    if "completed" in body:
        if not isinstance(body["completed"], bool):
            return error("'completed' must be true or false")
        task.completed = body["completed"]
    db.session.commit()
    return success(task.to_dict())


# ── DELETE: DELETE /tasks/<id> ───────────────────────────────
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return error(f"Task with id {task_id} not found", 404)
    db.session.delete(task)
    db.session.commit()
    return success(f"Task {task_id} deleted successfully")


# ── Start the server ─────────────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the database file + table if they don't exist
    app.run(debug=True, port=5000)