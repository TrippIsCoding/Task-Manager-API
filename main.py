import sqlite3 as db
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

def get_db():
    conn = db.connect('task_manager.db')
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def create_table():
    with db.connect('task_manager.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     description TEXT,
                     status TEXT,
                     priority INTEGER,
                     deadline TEXT
                     )''')

def row_to_dict(row):
    '''converts a database row (tuple) to a dictionary matching the Task model.'''
    return {
        'id': row[0],
        'title': row[1],
        'description': row[2],
        'status': row[3],
        'priority': row[4],
        'deadline': row[5] 
    } if row else None

app = FastAPI()

create_table()

class Task(BaseModel):
    title: str
    description: str
    status: str
    priority: int
    deadline: str

@app.get('/tasks')
def list_all_tasks(order: str = 'asc', conn: db.Connection = Depends(get_db)):
    '''This probably lists all the tasks in the database who knows really'''

    cursor = conn.cursor()

    if order.lower() == 'asc':
        cursor.execute('SELECT * FROM tasks ORDER BY priority ASC')
    else:
        cursor.execute('SELECT * FROM tasks ORDER BY priority DESC')
    
    tasks = cursor.fetchall()

    if not tasks:
        return {'message': 'could not find any tasks in the database'}

    return {'tasks': [row_to_dict(row) for row in tasks]}

@app.get('/tasks/{id}')
def show_specific_task(id: int, conn: db.Connection = Depends(get_db)):
    '''This is used to find a specific task in the database by its id or is it'''
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,))
        task = cursor.fetchone()
    except (db.IntegrityError, db.OperationalError, db.DatabaseError) as e:
        return {'Error': str(e)}

    if not task:
        raise HTTPException(status_code=404, detail='Task not found')

    return {'task': row_to_dict(task)}

@app.post('/tasks')
def create_task(task: Task, conn: db.Connection = Depends(get_db)):
    '''This is so the user can create tasks cause whats the point of a task manager with no tasks am i right'''
    
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (title, description, status, priority, deadline) VALUES (?, ?, ?, ?, ?)',
                        (task.title, task.description, task.status, task.priority, task.deadline))
            
        return {'message': 'Task created successfully',
                'task_id': cursor.lastrowid
               }

    except (db.IntegrityError, db.OperationalError, db.DatabaseError) as e:
        return {'Error': str(e)}

@app.put('/tasks/{id}')
def update_task(id: int, task: Task, conn: db.Connection = Depends(get_db)):
    '''This is used to update an already created tasks, its some neet stuff'''

    try:
        cursor = conn.cursor()

        if not cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone():
            raise HTTPException(status_code=404, detail='Task not found')

        cursor.execute('UPDATE tasks SET title = ?, description = ?, status = ?, priority = ?, deadline = ? WHERE id = ?',
                        (task.title, task.description, task.status, task.priority, task.deadline, id))
    except (db.IntegrityError, db.OperationalError, db.DatabaseError) as e:
        return {'Error': str(e)}

    return {'message': 'Task updated successfully'}

@app.delete('/tasks/{id}')
def delete_task(id: int, conn: db.Connection = Depends(get_db)):
    '''This is used to delete a specific task literally the name of the function'''

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
        task = cursor.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail='Task not found')

        cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    except (db.IntegrityError, db.OperationalError, db.DatabaseError) as e:
        return {'Error': str(e)}
    
    return {'message': 'Task deleted successfully'}