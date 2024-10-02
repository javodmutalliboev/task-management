import sys

from PyQt5.QtWidgets import \
    QApplication, QWidget, \
    QVBoxLayout, QLineEdit, \
    QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox, \
    QTextEdit, QDateEdit, QCheckBox, \
    QHBoxLayout, QLabel
from PyQt5.QtCore import QDate

import mysql.connector

# MySQL database-ga ulash
conn = mysql.connector.connect(
    host="localhost",
    user="javod",
    password="hHh(26Y2%C~w",
    database="task_management"
)
cursor = conn.cursor()


# main window class yaratish
class TaskManagementApp(QWidget):
    title: QLineEdit
    description: QTextEdit
    due_date: QDateEdit
    completed: QCheckBox
    table: QTableWidget

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Task Management")

        # VLayout
        vLayout = QVBoxLayout()

        self.title = QLineEdit(self)
        self.title.setPlaceholderText("Enter title")
        vLayout.addWidget(self.title)

        self.description = QTextEdit(self)
        self.description.setPlaceholderText("Enter description...")
        vLayout.addWidget(self.description)

        due_date_h_layout = QHBoxLayout()
        due_date_label = QLabel("Due Date:")
        due_date_h_layout.addWidget(due_date_label)
        self.due_date = QDateEdit()
        self.due_date.setDate(QDate.currentDate())
        due_date_h_layout.addWidget(self.due_date)
        vLayout.addLayout(due_date_h_layout)

        completed_h_layout = QHBoxLayout()
        completed_label = QLabel("Completed:")
        completed_h_layout.addWidget(completed_label)
        self.completed = QCheckBox()
        completed_h_layout.addWidget(self.completed)
        vLayout.addLayout(completed_h_layout)

        add_button = QPushButton("Add task")
        add_button.clicked.connect(self.add_task)
        vLayout.addWidget(add_button)

        update_button = QPushButton("Update selected task")
        update_button.clicked.connect(self.update_task)
        vLayout.addWidget(update_button)

        delete_button = QPushButton("Delete selected task")
        delete_button.clicked.connect(self.delete_task)
        vLayout.addWidget(delete_button)

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        (self.table
         .setHorizontalHeaderLabels(["ID", "Title", "Description",
                                     "Due Date", "Completed"]))
        self.table.cellClicked.connect(self.select_task)
        vLayout.addWidget(self.table)

        self.load_tasks()

        self.setLayout(vLayout)

    def load_tasks(self):
        self.table.setRowCount(0)
        cursor.execute(
            "SELECT id, title, description, due_date, completed FROM tasks"
        )
        for row_idx, (task_id, title, description, due_date, completed) in enumerate(cursor.fetchall()):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(task_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(title))
            self.table.setItem(row_idx, 2, QTableWidgetItem(description))
            self.table.setItem(row_idx, 3, QTableWidgetItem(due_date.strftime("%Y-%m-%d")))
            self.table.setItem(row_idx, 4, QTableWidgetItem("True" if completed else "False"))

    def select_task(self, row, column):
        try:
            # task_id = self.table.item(row, 0).text()
            title = self.table.item(row, 1).text()
            description = self.table.item(row, 2).text()
            due_date = self.table.item(row, 3).text()
            completed = self.table.item(row, 4).text() == "True"

            self.title.setText(title)
            self.description.setText(description)
            due_date = QDate.fromString(due_date, "yyyy-MM-dd")
            self.due_date.setDate(due_date)
            self.completed.setChecked(completed)
        except Exception as exp:
            print(exp)

    def delete_task(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            task_id = int(self.table.item(selected_row, 0).text())
            cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
            conn.commit()
            self.load_tasks()
            self.title.clear()
            self.description.clear()
            self.due_date.setDate(QDate.currentDate())
            self.completed.setChecked(False)

    def update_task(self):
        try:
            selected_row = self.table.currentRow()
            if selected_row != -1:
                task_id = int(self.table.item(selected_row, 0).text())
                title = self.title.text()
                description = self.description.toPlainText()
                due_date = self.due_date.date().toString("yyyy-MM-dd")
                completed = self.completed.isChecked()
                if title and description and due_date:
                    cursor.execute(
                        "UPDATE tasks SET title=%s, \
                        description=%s, due_date=%s, \
                        completed=%s",
                        (title, description, due_date, completed)
                    )
                    conn.commit()
                    self.load_tasks()
                    self.title.clear()
                    self.description.clear()
                    self.due_date.setDate(QDate.currentDate())
                    self.completed.setChecked(False)
                else:
                    QMessageBox.warning(self, "Input Error",
                                        "title, description, due_date majburiy")
        except Exception as exp:
            print(exp)

    def add_task(self):
        try:
            title = self.title.text()
            description = self.description.toPlainText()
            due_date = self.due_date.date().toString("yyyy-MM-dd")
            completed = self.completed.isChecked()

            if title and description and due_date:
                cursor.execute(
                    "INSERT INTO tasks (title, description, \
                    due_date, completed) VALUES (%s, %s, %s, %s)",
                    (title, description, due_date, completed)
                )
                conn.commit()
                self.load_tasks()
                self.title.clear()
                self.description.clear()
                self.due_date.setDate(QDate.currentDate())
                self.completed.setChecked(False)
            else:
                QMessageBox.warning(self, "Input Error",
                                    "title, description, due_date majburiy")
        except Exception as istisno:
            print(istisno)


def main():
    app = QApplication(sys.argv)
    window = TaskManagementApp()
    window.show()
    exit(app.exec_())


if __name__ == '__main__':
    main()
