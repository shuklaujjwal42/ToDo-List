# ToDo-List
This is a simple TODO list application built with Flask.

Requirements
Python 3.9 or later
External modules listed in requirements.txt

Running the Application
1. Install the required external modules by running pip install -r requirements.txt.

2. Set the FLASK_APP environment variable to app.py:
export FLASK_APP=app.py
(On Windows, use set instead of export.)

3. Start the Flask development server:
flask run

4. Open a web browser and go to http://localhost:5000/ to access the application.

API Endpoints
1. Get All Tasks
GET /tasks
This endpoint returns a JSON array of all tasks.

2. Get a Task by ID
GET /tasks/<int:task_id>
This endpoint returns a JSON object for the task with the specified ID.

3. Create a New Task
POST /tasks
This endpoint creates a new task with the specified title and description, and returns a JSON object for the new task.

4. Update a Task
PUT /tasks/<int:task_id>
This endpoint updates the task with the specified ID to have the specified title, description, and completed status. It returns a JSON object for the updated task.

5. Delete a Task
DELETE /tasks/<int:task_id>
This endpoint deletes the task with the specified ID and returns a JSON object for the deleted task. 

