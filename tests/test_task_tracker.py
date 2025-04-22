import unittest
import os
import sys
import json
from PyQt5.QtWidgets import QApplication

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.task_tracker_app import MainWindow

class TestTaskTrackerApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])  # Create a QApplication instance
        cls.window = MainWindow(load_tasks_on_init=False)  # Skip loading tasks

    def setUp(self):
        # Clear tasks.json before each test
        if os.path.exists(self.window.task_file):
            os.remove(self.window.task_file)

        # Clear the task list widget
        self.window.task_list_widget.clear()

    def test_add_task(self):
        # Simulate adding a task
        self.window.lineEdit.setText("Test Task")
        self.window.add_task_to_tasks()

        # Verify the task was added to the list
        self.assertEqual(self.window.task_list_widget.count(), 1)

        # Verify the task was saved to the file
        with open(self.window.task_file, "r") as f:
            tasks = json.load(f)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["text"], "Test Task")
        self.assertFalse(tasks[0]["completed"])

    def test_delete_task(self):
        # Add a task
        self.window.lineEdit.setText("Task to Delete")
        self.window.add_task_to_tasks()

        # Delete the task
        item = self.window.task_list_widget.item(0)
        self.window.delete_task(item)

        # Verify the task list is empty
        self.assertEqual(self.window.task_list_widget.count(), 0)

        # Verify the task file is empty
        with open(self.window.task_file, "r") as f:
            tasks = json.load(f)
        self.assertEqual(len(tasks), 0)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

if __name__ == "__main__":
    unittest.main()