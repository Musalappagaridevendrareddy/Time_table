import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()


def create_table(u_name):
	c.execute(f'CREATE TABLE IF NOT EXISTS {u_name}(task TEXT,task_status TEXT,task_due_date DATE, day TEXT)')


def add_data(u_name, task,task_status,task_due_date,day):
	c.execute(f'INSERT INTO {u_name}(task,task_status,task_due_date, day) VALUES (?,?,?,?)',(task,task_status,task_due_date,day))
	conn.commit()


def view_all_data(u_name):
	c.execute(f'SELECT * FROM {u_name}')
	data = c.fetchall()
	return data

def view_all_task_names(u_name):
	c.execute(f'SELECT DISTINCT task FROM {u_name}')
	data = c.fetchall()
	return data

def get_task(u_name, task):
	c.execute(f'SELECT * FROM {u_name} WHERE task="{task}"')
	data = c.fetchall()
	return data

def edit_task_data(u_name, new_task,new_task_status,new_task_date,new_day,task,task_status,task_due_date,day):
	c.execute(f"UPDATE {u_name} SET task =?,task_status=?,task_due_date=?,day? WHERE task=? and task_status=? and task_due_date=? and day?",(new_task,new_task_status,new_task_date,new_day,task,task_status,task_due_date,day))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(u_name, task):
	c.execute(f'DELETE FROM {u_name} WHERE task="{task}"')
	conn.commit()

def delete_user(u_name):
	c.execute(f'DROP TABLE {u_name}')
	conn.commit()