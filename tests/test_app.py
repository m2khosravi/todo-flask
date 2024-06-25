import unittest
from app import app, db
from models import Todo

class TestTodoApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "healthy"})

    def test_create_todo(self):
        todo_data = {
            "name": "Test Todo",
            "description": "This is a test",
            "task": "Complete the test"
        }
        response = self.client.post('/todos', json=todo_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["name"], todo_data["name"])
        self.assertEqual(response.json["description"], todo_data["description"])
        self.assertEqual(response.json["task"], todo_data["task"])

    def test_get_todo(self):
        # First, create a todo
        todo_data = {
            "name": "Test Todo",
            "description": "This is a test",
            "task": "Complete the test"
        }
        create_response = self.client.post('/todos', json=todo_data)
        todo_id = create_response.json["id"]

        # Now, try to get the todo
        get_response = self.client.get(f'/todos/{todo_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json["id"], todo_id)
        self.assertEqual(get_response.json["name"], todo_data["name"])
        self.assertEqual(get_response.json["description"], todo_data["description"])
        self.assertEqual(get_response.json["task"], todo_data["task"])

if __name__ == '__main__':
    unittest.main()