from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from config import get_db_connection

tasks_blueprint = Blueprint('tasks', __name__)

@tasks_blueprint.route('/tasks')
@login_required
def task_list():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks WHERE user_id = %s ORDER BY status, status_date', (current_user.id,))
    tasks = cursor.fetchall()
    connection.close()
    return render_template('tasks.html', tasks=tasks)


@tasks_blueprint.route('/tasks/add', methods=['POST'])
@login_required
def add_task():
    task_title = request.form.get('task')
    if not task_title:
        flash('Task cannot be empty.')
        return redirect(url_for('tasks.task_list'))

    status = request.form.get('status', 'To Do')  # Default status to 'To Do'
    deadline = request.form.get('deadline')  # Deadline may be empty if not set

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO tasks (user_id, task, status, deadline) VALUES (%s, %s, %s, %s)',
        (current_user.id, task_title, status, deadline)
    )
    connection.commit()
    connection.close()
    flash('Task added successfully!')
    return redirect(url_for('tasks.task_list'))


@tasks_blueprint.route('/tasks/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s AND user_id = %s', (task_id, current_user.id))
    connection.commit()
    connection.close()
    flash('Task deleted successfully!')
    return redirect(url_for('tasks.task_list'))


@tasks_blueprint.route('/tasks/update_status/<int:task_id>', methods=['POST'])
@login_required
def update_task_status(task_id):
    new_status = request.form.get('status')
    new_deadline = request.form.get('deadline')  # New deadline value from form
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE tasks SET status = %s, deadline = %s WHERE id = %s AND user_id = %s',
        (new_status, new_deadline, task_id, current_user.id)
    )
    connection.commit()
    connection.close()
    flash('Task updated successfully!')
    return redirect(url_for('tasks.task_list'))
