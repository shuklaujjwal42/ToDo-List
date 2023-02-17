from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'todo.db'

def get_db():
    if not hasattr(app, 'db'):
        app.db = sqlite3.connect(app.config['DATABASE'])
        app.db.row_factory = sqlite3.Row
    return app.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(app, 'db'):
        app.db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    db = get_db()
    tasks = db.execute('SELECT id, title, description, completed FROM tasks').fetchall()
    return jsonify([dict(task) for task in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    db = get_db()
    db.execute('INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)', 
        (request.json['title'], request.json.get('description', ''), False))
    db.commit()
    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    db = get_db()
    task = db.execute('SELECT id, title, description, completed FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        abort(404)
    if not request.json:
        abort(400)
    data = {}
    if 'title' in request.json:
        data['title'] = request.json['title']
    if 'description' in request.json:
        data['description'] = request.json['description']
    if 'completed' in request.json:
        data['completed'] = request.json['completed']
    db.execute('UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?', 
        (data.get('title', task['title']), data.get('description', task['description']), 
        data.get('completed', task['completed']), task_id))
    db.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    db = get_db()
    task = db.execute('SELECT id, title, description, completed FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        abort(404)
    db.execute('UPDATE tasks SET completed = ? WHERE id = ?', (True, task_id))
    db.commit()
    return jsonify({'message': 'Task marked as completed'})

@app.route('/tasks/<int:task_id>/incomplete', methods=['PUT'])
def incomplete_task(task_id):
    db = get_db()
    task = db.execute('SELECT id, title, description, completed FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        abort(404)
    db.execute('UPDATE tasks SET completed = ? WHERE id = ?', (False, task_id))
    db.commit()
    return jsonify({'message': 'Task marked as incomplete'})

if __name__ == '__main__':
    app.run(debug=True)

