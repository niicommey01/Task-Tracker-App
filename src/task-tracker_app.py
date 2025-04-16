from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QSize
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QPushButton, QLineEdit,
                             QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QCheckBox)
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5 import QtCore

import json
import os

import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    return os.path.join(base_path, relative_path)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Tracker")
        self.setGeometry(700, 300, 500, 500)
        self.setFixedSize(700, 700)
        self.setWindowIcon(QIcon(resource_path("resources/th-1828655096.ico")))

        self.setStyleSheet(f"""
            QMainWindow {{
                background-image: url({resource_path('resources/crumpled-paper-1-1969922722.jpg')});
                background-repeat: no-repeat;
                background-position: center;
            }}
        """)

        self.label1 = QLabel("What do I have to do?", self)
        self.label1.setFont(QFont("Comic Sans MS", 18))
        self.label1.setStyleSheet("color: black;")

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setPlaceholderText("Enter task here")
        self.lineEdit.setStyleSheet("font-family: comic sans ms; font-size: 20px;")
        self.lineEdit.returnPressed.connect(self.add_task_to_tasks)

        self.add_task = QPushButton("Add Task", self)
        self.add_task.clicked.connect(self.add_task_to_tasks)
        self.add_task.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.task_list_widget = QListWidget(self)
        self.task_list_widget.itemChanged.connect(self.handle_task_change)
        self.task_list_widget.setFocusPolicy(Qt.StrongFocus)

        def clear_selection_on_focus_out(event):
            self.task_list_widget.clearSelection()
            QListWidget.focusOutEvent(self.task_list_widget, event)

        self.task_list_widget.focusOutEvent = clear_selection_on_focus_out

        # self.task_list_widget.focusOutEvent = lambda event: (
        # self.task_list_widget.clearSelection(), QListWidget.focusOutEvent(self.task_list_widget, event))

        self.task_file = "tasks.json"
        self.load_tasks()

        self.toast_queue = []

        self.initUI()

    def initUI(self):
        self.label1.setGeometry(10, 10, 300, 50)

        self.lineEdit.setGeometry(10, 70, 500, 40)
        self.lineEdit.setStyleSheet("""
                    QLineEdit {
                        font-family: 'Comic Sans MS';
                        font-size: 20px;
                        padding: 5px;
                        border: 2px solid #542b00;  /* Brown border */
                        border-radius: 5px;         /* Rounded corners */
                        background-color: #f9f9f9;  /* Light gray background */
                        color: #333;                 /* Dark text color */
                    }
                    QLineEdit:focus {
                        border: 2px solid #3d1f00;  /* Darker brown when focused */
                        background-color: #ffffff;  /* White background when focused */
                    }
                """)

        self.add_task.setStyleSheet("""
                    QPushButton {
                        font-family: 'Comic Sans MS';
                        font-size: 20px;
                        padding: 10px;
                        border-radius: 15px;         /* Rounded corners */
                        background-color: #7c3600;  /* Light gray background */
                        color: #ffffff;                 /* Dark text color */
                    }
                    QPushButton:focus {
                        border: none;
                        background-color: rgba(124, 54, 0, 100);         
                    }
                """)

        self.task_list_widget.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                font-family: 'Comic Sans MS';
                font-size: 20px;
                color: #333; /* Dark text color */
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
            background-color: #bf6a03; /* Darker brown when selected */
            color: white;
            }
        """)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.lineEdit)
        h_layout.addWidget(self.add_task)

        v_layout = QVBoxLayout()
        v_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        v_layout.addWidget(self.label1)
        v_layout.addLayout(h_layout)

        v_layout.addWidget(self.task_list_widget)

        central_widget = QWidget(self)
        central_widget.setLayout(v_layout)
        self.setCentralWidget(central_widget)

    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QCheckBox, QListWidgetItem

    def add_task_to_tasks(self):
        task_name = self.lineEdit.text()
        if not task_name:
            self.show_toast("Please enter a task name", 2000)
            self.lineEdit.setFocus()
            return

        # Create a QListWidgetItem
        item = QListWidgetItem()
        self.task_list_widget.addItem(item)

        # Create a custom widget to hold everything
        task_widget = QWidget()
        layout = QHBoxLayout(task_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Checkbox
        checkbox = self.QCheckBox()
        layout.addWidget(checkbox)

        # Task label
        label = QLabel(task_name)
        label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 20px;")
        layout.addWidget(label)

        # Delete button
        delete_button = QPushButton("🗑")
        delete_button.setStyleSheet("font-size: 16px; padding: 4px; border: none;")
        layout.addWidget(delete_button)

        # Connect signals
        checkbox.stateChanged.connect(lambda state, lbl=label: lbl.setStyleSheet(
            "font-family: 'Comic Sans MS'; font-size: 20px; text-decoration: line-through;" if state else
            "font-family: 'Comic Sans MS'; font-size: 20px;"
        ))
        delete_button.clicked.connect(lambda _, item=item: self.delete_task(item))

        # Set the custom widget
        self.task_list_widget.setItemWidget(item, task_widget)

        self.lineEdit.clear()

        # Save the task to a file
        self.save_tasks()

    def handle_task_change(self, item):
        font = item.font()
        if item.checkState() == Qt.Checked:
            font.setStrikeOut(True)
        else:
            font.setStrikeOut(False)
        item.setFont(font)

        # Save the task state to a file
        self.save_tasks()

    def delete_task(self, item):
        row = self.task_list_widget.row(item)
        self.task_list_widget.takeItem(row)
        self.show_toast("Task deleted", 2000)

        # Save the task list to a file
        self.save_tasks()

    def show_toast(self, message, duration=2000):
        toast_label = QLabel(message, self)
        toast_label.setStyleSheet("""
            QLabel {
                background-color: #7c3600;
                color: white;
                padding: 10px 20px;
                border-radius: 15px;
                font-family: 'Comic Sans MS';
                font-size: 20px;
            }
        """)
        toast_label.setAlignment(Qt.AlignCenter)
        toast_label.setVisible(True)

        # Add the toast to the queue and start the animation
        self.toast_queue.append(toast_label)
        self._animate_toast(toast_label, duration)

    def _animate_toast(self, toast_label, duration):
        width = 300
        height = 50
        x = (self.width() - width) // 2
        y = self.height()

        toast_label.setGeometry(x, y, width, height)
        self.centralWidget().layout().addWidget(toast_label)

        animation = QPropertyAnimation(toast_label, b"geometry")
        animation.setDuration(500)  # Duration of the slide in
        animation.setStartValue(QRect(x, self.height(), width, height))
        animation.setEndValue(QRect(x, self.height() - height - len(self.toast_queue) * 60, width, height))
        animation.start()

        # Hide the toast after the specified duration
        QTimer.singleShot(duration, lambda: self._hide_toast(toast_label))

    def _hide_toast(self, toast_label):
        # Animate the toast sliding out
        x = toast_label.x()
        y = self.height()
        animation = QPropertyAnimation(toast_label, b"geometry")
        animation.setDuration(500)  # Duration of the slide out
        animation.setStartValue(toast_label.geometry())
        animation.setEndValue(QRect(x, y, toast_label.width(), toast_label.height()))
        animation.start()

        # Remove from the queue after the animation is complete
        QTimer.singleShot(500, lambda: self._remove_toast(toast_label))

    def _remove_toast(self, toast_label):
        self.toast_queue.remove(toast_label)
        toast_label.deleteLater()


    # Save to json file
    def save_tasks(self):
        tasks = []
        for i in range(self.task_list_widget.count()):
            item = self.task_list_widget.item(i)
            widget = self.task_list_widget.itemWidget(item)

            if widget:
                label = widget.findChild(QLabel)
                checkbox = widget.findChild(QCheckBox)

                if label and checkbox:
                    tasks.append({
                        "text": label.text(),
                        "completed": checkbox.isChecked()
                    })

        with open(self.task_file, "w") as f:
            json.dump(tasks, f, indent=4)

    # Load from json file
    def load_tasks(self):
        if os.path.exists(self.task_file):
            with open(self.task_file, "r") as f:
                tasks = json.load(f)
                for task in tasks:
                    # Create a QListWidgetItem
                    item = QListWidgetItem()
                    self.task_list_widget.addItem(item)

                    # Create a custom widget to hold everything
                    task_widget = QWidget()
                    layout = QHBoxLayout(task_widget)
                    layout.setContentsMargins(0, 0, 0, 0)

                    # Checkbox
                    checkbox = QCheckBox()
                    checkbox.setChecked(task["completed"])
                    layout.addWidget(checkbox)

                    # Task label
                    label = QLabel(task["text"])
                    label.setStyleSheet(
                        "font-family: 'Comic Sans MS'; font-size: 20px;" +
                        (" text-decoration: line-through;" if task["completed"] else "")
                    )
                    layout.addWidget(label)

                    # Delete button
                    delete_button = QPushButton("🗑")
                    delete_button.setStyleSheet("font-size: 16px; padding: 4px; border: none;")
                    layout.addWidget(delete_button)

                    # Connect signals
                    checkbox.stateChanged.connect(lambda state, lbl=label: self.update_checkbox_state(state, lbl))
                    checkbox.stateChanged.connect(self.save_tasks)  # Directly call save_tasks
                    delete_button.clicked.connect(lambda _, item=item: self.delete_task(item))

                    # Set the custom widget
                    self.task_list_widget.setItemWidget(item, task_widget)

    def update_checkbox_state(self, state, label):
        if state == Qt.Checked:
            label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 20px; text-decoration: line-through;")
        else:
            label.setStyleSheet("font-family: 'Comic Sans MS'; font-size: 20px;")



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
