import pymysql
import pymysql.cursors
import logging
from app import app
from db_config import mysql
from flask import jsonify, request

@app.before_request
def log_request():
    logging.info(
        "%s %s %s %s",
        request.remote_addr,
        request.method,
        request.path,
        request.get_data(as_text=True)
    )

@app.route('/tasks', defaults={'task_id': None}, methods=['GET', 'POST'])
@app.route('/tasks/<task_id>', methods=['PUT', 'DELETE'])
def tasks(task_id):
    if not task_id:
        match request.method:
            case "GET":
                status = request.args.get('status')
                dueDate = request.args.get('dueDate')
                query = "SELECT * FROM tasks ORDER BY status, due_date DESC"

                try:
                    connection = mysql.connect()
                    cursor = connection.cursor(pymysql.cursors.DictCursor)
                    if status and dueDate:
                        query = "SELECT * FROM tasks WHERE status = %s AND due_date = %s"
                        cursor.execute(query, (status, dueDate))
                    elif status:
                        query = "SELECT * FROM tasks WHERE status = %s ORDER BY due_date DESC"
                        cursor.execute(query, (status))
                    elif dueDate:
                        query = "SELECT * FROM tasks WHERE due_date = %s ORDER BY due_date DESC"
                        cursor.execute(query, (dueDate))
                    else:
                        cursor.execute(query)

                    raw_data = cursor.fetchall()
                    response = jsonify(raw_data)
                    response.status_code = 200
                    return response
        
                except Exception as e:
                    print(e)
        
                finally: 
                    cursor.close
                    connection.close
            
            case "POST":
                title = request.args.get('title')

                if not title:
                    return jsonify({"error": "Title is mandatory"}), 400

                desc = request.args.get('description')
                dueDate = request.args.get('dueDate')
                status = request.args.get('status', 'pending')
                query = "INSERT INTO tasks (title, description, due_date, status) VALUES (%s, %s, %s, %s)"
                
                try:
                    connection = mysql.connect()
                    cursor = connection.cursor(pymysql.cursors.DictCursor)
                    cursor.execute(query, (title, desc, dueDate, status))
                    connection.commit()
                    return jsonify({"message": "Task created"}), 201
                
                except Exception as e:
                    print(e)
        
                finally: 
                    cursor.close
                    connection.close
            case _:
                return jsonify({"error": "This method is not supported"}), 405

    else:
        match request.method:
            case "PUT":
                title = request.args.get('title')
                desc = request.args.get('description')
                dueDate = request.args.get('dueDate')
                status = request.args.get('status')

                try:
                    connection = mysql.connect()
                    cursor = connection.cursor(pymysql.cursors.DictCursor)
                    if title:
                        cursor.execute("UPDATE tasks SET title = %s WHERE idtasks = %s", (title, task_id))
                        connection.commit()
                    elif desc:
                        cursor.execute("UPDATE tasks SET description = %s WHERE idtasks = %s", (desc, task_id))
                        connection.commit()
                    elif dueDate:
                        cursor.execute("UPDATE tasks SET due_date = %s WHERE idtasks = %s", (dueDate, task_id))
                        connection.commit()
                    elif status:
                        cursor.execute("UPDATE tasks SET status = %s WHERE idtasks = %s", (status, task_id))
                        connection.commit()
                        return jsonify({"message": "Task updated"}), 200
                    else:
                        return jsonify({"error": "No values were provided"})
                
                except Exception as e:
                    print(e)
        
                finally: 
                    cursor.close
                    connection.close
            
            case "DELETE":
                query = "DELETE FROM tasks WHERE idtasks = %s"

                try:
                    connection = mysql.connect()
                    cursor = connection.cursor(pymysql.cursors.DictCursor)
                    cursor.execute(query, (task_id))
                    connection.commit()
                    return jsonify({"message": "Task deleted"}), 200
                
                except Exception as e:
                    print(e)
        
                finally: 
                    cursor.close
                    connection.close
            
            case _:
                return jsonify({"error": "This method is not supported"}), 405


if __name__ == "__main__":
    app.run()