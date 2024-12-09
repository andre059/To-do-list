import unittest
from unittest.mock import Mock

from fastapi.testclient import TestClient

from main import app
from app.routes import TodoService


class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.service = TodoService(Mock())

    def test_create_todo(self):
        todo_data = {"title": "Test Todo", "is_completed": False}
        response = self.client.post("/api/todo", json=todo_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_read_todo(self):
        todo_id = 1
        response = self.client.get(f"/api/todo/{todo_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_update_todo(self):
        todo_id = 1
        update_data = {"title": "Updated Title"}
        response = self.client.put(f"/api/todo/{todo_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_delete_todo(self):
        todo_id = 1
        response = self.client.delete(f"/api/todo/{todo_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)


if __name__ == '__main__':
    unittest.main()
