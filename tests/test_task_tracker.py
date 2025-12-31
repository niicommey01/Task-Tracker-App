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
        cls.app = QApplication([]) 
        cls.window = MainWindow(load_tasks_on_init=True)  
    def setUp(self):
        self.window.task_list_widget.clear()

    def test_add_task(self):
        self.window.lineEdit.setText("Test Task")
        self.window.add_task_to_tasks()

        self.assertEqual(self.window.task_list_widget.count(), 1)

        with open(self.window.task_file, "r") as f:
            tasks = json.load(f)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["text"], "Test Task")
        self.assertFalse(tasks[0]["completed"])

    def test_delete_task(self):
        self.window.lineEdit.setText("Task to Delete")
        self.window.add_task_to_tasks()

        item = self.window.task_list_widget.item(0)
        self.window.delete_task(item)

        self.assertEqual(self.window.task_list_widget.count(), 0)

        with open(self.window.task_file, "r") as f:
            tasks = json.load(f)
        self.assertEqual(len(tasks), 0)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

if __name__ == "__main__":
    unittest.main()