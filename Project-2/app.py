# ============================================================
#  Simple Task Manager API - Built with Flask (Python)
# ============================================================
#  Endpoints:
#    GET  /tasks         → get all tasks
#    GET  /tasks/<id>    → get one task by ID
#    POST /tasks         → create a new task
#    POST /tasks/<id>/complete → mark a task as complete
# ============================================================

from flask import Flask, request, jsonify

# Create the Flask app
app = Flask(__name__)


# ── In-memory "database" (just a list for now) ──────────────
# In a real project, this would be a real database like PostgreSQL
tasks = []
next_id = 1  # keeps track of the next task ID


# ── Helper: build a success response ────────────────────────
def success(data, status=200):
    return jsonify({"success": True, "data": data}), status


# ── Helper: build an error response ─────────────────────────
def error(message, status=400):
    return jsonify({"success": False, "error": message}), status


# ── Route 1: GET /tasks ─────────────────────────────────────
# Returns all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return success(tasks)


# ── Route 2: GET /tasks/<id> ────────────────────────────────
# Returns a single task by its ID
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    # Search for the task in our list
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return error(f"Task with id {task_id} not found", 404)

    return success(task)


# ── Route 3: POST /tasks ────────────────────────────────────
# Creates a new task
@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id

    # Get the JSON body sent by the client
    body = request.get_json()

    # ── Validation ──────────────────────────────────────────
    if not body:
        return error("Request body must be JSON")

    title = body.get("title", "").strip()
    description = body.get("description", "").strip()

    if not title:
        return error("'title' is required and cannot be empty")

    if len(title) > 100:
        return error("'title' must be 100 characters or less")

    # ── Create the task object ───────────────────────────────
    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "completed": False,
    }

    tasks.append(task)
    next_id += 1

    # Return 201 Created with the new task
    return success(task, 201)


# ── Route 4: POST /tasks/<id>/complete ──────────────────────
# Marks a task as completed
@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
def complete_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return error(f"Task with id {task_id} not found", 404)

    if task["completed"]:
        return error("Task is already completed")

    task["completed"] = True
    return success(task)


# ── Start the server ─────────────────────────────────────────
if __name__ == "__main__":
    # debug=True → auto-restarts when you change the code (dev only!)
    app.run(debug=True, port=5000)