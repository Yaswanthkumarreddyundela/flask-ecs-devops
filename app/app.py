from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
import itertools

app = Flask(__name__)

# In-memory todo list and ID generator
todos = []
id_counter = itertools.count(1)

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({'error': 'Task is required'}), 400

    todo = {
        'id': next(id_counter),
        'task': data['task'],
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    data = request.get_json()
    if 'completed' in data:
        todo['completed'] = data['completed']
    if 'task' in data:
        todo['task'] = data['task']

    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({'message': 'Todo deleted'})

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
