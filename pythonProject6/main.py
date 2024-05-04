import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QDateEdit, QComboBox, QListWidget
import pymysql
import logging

logging.basicConfig(level=logging.INFO)

#  Подключение к бд
def create_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='iceboy',
        db='address_book',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Функция для добавления задачи в бд
def convert_priority_to_number(priority_str):
    priority_mapping = {'Низкий': 1, 'Средний': 2, 'Высокий': 3}
    return priority_mapping.get(priority_str, 1)
def add_task_to_db(task_name, task_description, due_date, status, priority_str):
    priority_num = convert_priority_to_number(priority_str)
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO tasks (title, description, due_date, status, priority) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (task_name, task_description, due_date, status, priority_num))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Ошибка при добавлении задачи: {e}")
    finally:
        connection.close()
class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Task Manager - ЗадачиПроекты')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Добавление проекта
        self.project_input = QLineEdit(self)
        self.project_input.setPlaceholderText('Введите название проекта...')
        layout.addWidget(self.project_input)

        self.add_project_btn = QPushButton('Добавить проект', self)
        self.add_project_btn.clicked.connect(self.add_project)
        layout.addWidget(self.add_project_btn)

        # Список проектов
        self.project_list = QListWidget(self)
        layout.addWidget(self.project_list)

        # Добавление задачи
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText('Введите название задачи...')
        layout.addWidget(self.task_input)

        self.due_date_input = QDateEdit(self)
        layout.addWidget(self.due_date_input)

        self.priority_input = QComboBox(self)
        self.priority_input.addItems(['Низкий', 'Средний', 'Высокий'])
        layout.addWidget(self.priority_input)

        self.add_task_btn = QPushButton('Добавить задачу', self)
        self.add_task_btn.clicked.connect(self.add_task)
        layout.addWidget(self.add_task_btn)

        # Список задач
        self.task_list = QListWidget(self)
        layout.addWidget(self.task_list)

    def add_project(self):
        project_name = self.project_input.text()
        if project_name:
            self.project_list.addItem(project_name)
            self.project_input.clear()

    def add_task(self):
        task_name = self.task_input.text()
        task_description = 'Описание задачи' #  Ввод описания задачи пользователем
        due_date = self.due_date_input.date().toString('yyyy-MM-dd')
        status = 'Не выполнено' # Начальный статус задачи
        priority = self.priority_input.currentText()
        if task_name:
            add_task_to_db(task_name, task_description, due_date, status, priority)
            task_details = f'{task_name} - до {due_date} - Приоритет: {priority}'
            self.task_list.addItem(task_details)
            self.task_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskManager()
    ex.show()
    sys.exit(app.exec_())
