# restful-crud
API для керування списком задач на Flask

Залежності: flask, pymysql, flask-mysql. 

## Встановлення: 

```
pip install flask

pip install pymysql

pip install flask-mysql
```

Для тестування необхідний локальний сервер MySQL (конфігурацію у db_config.py необхідно оновити) зі створеною таблицею:

```
CREATE TABLE crud.tasks (
  idtasks INT NOT NULL AUTO_INCREMENT,

  title VARCHAR(45) NOT NULL,
  
  description VARCHAR(45) NULL,
  
  due_date DATE NULL,
  
  status VARCHAR(45) NULL,
  
  PRIMARY KEY (idtasks));
```

Сервер запускається виконанням файлу main.py. 

## Для тестування API можна використати [Postman](https://www.postman.com). Приклади запитів:

```
GET: http://localhost:5000/tasks?status=completed&dueDate=2025-03-08

POST: http://localhost:5000/tasks?title=test&dueDate=2026-01-01&description=just a test task

PUT: http://localhost:5000/tasks/12?description=updating one field

DELETE: http://localhost:5000/tasks/12
```
