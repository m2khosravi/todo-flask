import os
from flask import Flask, jsonify, request
from models import db, Todo
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return jsonify(todo.to_dict()), 200

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = Todo(name=data['name'], description=data['description'], task=data['task'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)