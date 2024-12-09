import unittest
from unittest.mock import Mock, patch

from app.models import TodoItem
from app.services import TodoService, TodoItemCreate, TodoItemUpdate, HTTPException


class TestTodoService(unittest.TestCase):

    def setUp(self):
        self.db = Mock()
        self.service = TodoService(self.db)

    @patch.object(TodoService, 'db')
    def test_get_all(self, mock_db):
        mock_db.query.return_value = [Mock(id=1, title="Test"), Mock(id=2, title="Another")]
        result = self.service.get_all()
        mock_db.query.assert_called_once_with(TodoItem)
        self.assertEqual(len(result), 2)

    @patch.object(TodoService, 'db')
    def test_get_by_id(self, mock_db):
        mock_db.query.return_value = Mock(id=1, title="Test")
        result = self.service.get_by_id(1)
        mock_db.query.assert_called_once_with(TodoItem.filter(TodoItem.id == 1))
        self.assertEqual(result.id, 1)

    @patch.object(TodoService, 'db')
    def test_create(self, mock_db):
        todo_data = {"title": "New Todo", "is_completed": False}
        expected_result = {"id": 1, "title": "New Todo", "is_completed": False}
        mock_db.add.return_value = Mock(id=1)
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = Mock(id=1, title="New Todo", is_completed=False)

        result = self.service.create(TodoItemCreate(**todo_data))
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        self.assertEqual(result, expected_result)

    @patch.object(TodoService, 'db')
    def test_update(self, mock_db):
        todo = Mock(id=1, title="Old Title", is_completed=False)
        mock_db.query.return_value = todo
        update_data = {"title": "Updated Title"}

        result = self.service.update(1, TodoItemUpdate(**update_data))
        mock_db.query.assert_called_once_with(TodoItem.filter(TodoItem.id == 1))
        setattr(todo, 'title', "Updated Title")
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        self.assertEqual(result.title, "Updated Title")

    @patch.object(TodoService, 'db')
    def test_delete(self, mock_db):
        todo = Mock(id=1, title="Delete Me")
        mock_db.query.return_value = todo
        self.service.delete(1)
        mock_db.query.assert_called_once_with(TodoItem.filter(TodoItem.id == 1))
        mock_db.delete.assert_called_once_with(todo)
        mock_db.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
