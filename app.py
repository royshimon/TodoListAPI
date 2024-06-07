from flask import Flask, request, jsonify, abort

app = Flask(__name__)

todos = []
current_id = 1

def find_todo_or_404(todo_id):
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if todo is None:
        abort(404, description="Todo item not found")
    return todo

def validate_todo_request(data):
    if not data or 'title' not in data or 'description' not in data:
        abort(400, description= "Invalid request: JSON must contain title and description")

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo_by_id(todo_id):
    todo = find_todo_or_404(todo_id)
    return jsonify(todo)

@app.route('/todos', methods=['POST'])
def add_todo():
    if not request.json or 'title' not in request.json or 'description' not in request.json:
        abort(400, description="Invalid request: JSON must contain title and description")
    global current_id
    new_todo = {
        'id': current_id,
        'title': request.json['title'],
        'description': request.json['description']
    }
    todos.append(new_todo)
    current_id += 1
    return jsonify(new_todo), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = find_todo_or_404(todo_id)
    if not request.json or 'title' not in request.json or 'description' not in request.json:
        abort(400, description="Invalid request: JSON must contain title and description")
    todo['title'] = request.json['title']
    todo['description'] = request.json['description']
    return jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todo = find_todo_or_404(todo_id)
    todos = [t for t in todos if t['id'] != todo_id]
    return '', 204

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error)}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True)
