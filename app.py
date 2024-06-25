import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///test.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from models import Todo

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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)