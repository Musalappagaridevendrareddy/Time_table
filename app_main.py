import streamlit as st
import pandas as pd 
from db_file import * 
import streamlit.components.v1 as stc


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data_main.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def del_user(username):
	c.execute('DELETE FROM userstable WHERE username = ?',(username,))
	conn.commit()


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">TIME TABLE</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
    """
con = st.container()

def app(u_name):
	stc.html(HTML_BANNER)
	menu = ["Create","Read","Update","Delete","About", "Table"]
	choice = st.selectbox("Menu",menu,key='choice')
	create_table(u_name)

	if choice == "Create":
		st.subheader("Add Course")
		col1,col2 = st.columns(2)
		
		with col1:
			task = st.text_input("CourseID")
			task_due_date = st.text_input("Time")

		with col2:
			task_status = st.text_input("Link")
			day = st.selectbox("Day",["Monday","Tuesday","Wednesday","Thursday","Friday"],key='day')

		if st.button("Add Course"):
			add_data(u_name, task,task_status,str(task_due_date),day)
			con.success("Added {} to Database".format(task))


	elif choice == "Read":
		# st.subheader("View Items")
		with st.expander("View All"):
			result = view_all_data(u_name)
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["CourseID","Link","Time","Day"])
			st.dataframe(clean_df)

	elif choice == "Update":
		st.subheader("Edit Courses")
		with st.expander("Current Data"):
			result = view_all_data(u_name)
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["CourseID","Link","Time","Day"])
			st.dataframe(clean_df)

		list_of_tasks = [i[0] for i in view_all_task_names(u_name)]
		selected_task = st.selectbox("Courses",list_of_tasks,key='selected_task')
		task_result = get_task(u_name, selected_task)
		# st.write(task_result)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]
			day = task_result[0][3]

			col1,col2 = st.columns(2)
			
			with col1:
				new_task = st.text_input("CourseID",task)
				new_day = st.selectbox("Day",["Monday","Tuesday","Wednesday","Thursday","Friday"],key='new_day')

			with col2:
				new_task_status = st.text_input("Link", task_status)
				new_task_due_date = st.text_input("Time", (task_due_date))

			if st.button("Update Task"):
				edit_task_data(u_name, new_task,new_task_status,str(new_task_due_date),new_day,task,task_status,task_due_date,day)
				con.success("Updated -- {} ---> {}".format(task,new_task))

			with st.expander("View Updated Data"):
				result = view_all_data(u_name)
				# st.write(result)
				clean_df = pd.DataFrame(result,columns=["CourseID","Link","Time","Day"])
				st.dataframe(clean_df)


	elif choice == "Delete":
		st.subheader("Delete")
		with st.expander("View Data"):
			result = view_all_data(u_name)
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["CourseID","Link","Time","Day"])
			st.dataframe(clean_df)

		unique_list = [i[0] for i in view_all_task_names(u_name)]
		delete_by_task_name =  st.selectbox("Select CourseID",unique_list,key='delete_by_task_name')
		if st.button("Delete"):
			delete_data(u_name, delete_by_task_name)
			st.warning("Deleted: '{}'".format(delete_by_task_name))

		with st.expander("Updated Data"):
			result = view_all_data(u_name)
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["CourseID","Link","Time","Day"])
			st.dataframe(clean_df)

	elif choice == "Table":
		result = view_all_data(u_name)
		if result:
			df = pd.DataFrame(result,columns=["CourseID","Link", "Time","Day"])
			gp = df.groupby(['Day'])
			h1, h2, h3, h4, h5, h6, h7 = st.columns(7)
			h = [h2, h3, h4, h5, h6, h7]
			with h1:
				st.write('Day')
			for ind, t in enumerate(df['Time'].unique()):
				if len(result) >= ind:
					with h[ind]:
						st.write(t)
		# st.write(gp['Day'].head(7))
			c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
			DN = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
			ID = []
			LK = []
			try:
				for ind1, i in enumerate(DN):
					if len(result) >= ind1:
						t = gp.get_group(i)['CourseID']
						l = gp.get_group(i)['Link']
						LK.append(l.tolist())
						ID.append(t.tolist())
				c = [c2, c3, c4, c5, c6, c7]
				for i in range(len(DN)):
					with c1:
						st.write(DN[i])
					for j in range(len(ID[i])):
						with c[i]:
							st.write(f'[{ID[i][j]}]({LK[i][j]})')
			except:
				con.warning('Insert Data Completely')
			
		else:
			st.write('Insert Data to view time table')

	else:
		st.subheader("Time Table App")
		st.info("Built with Streamlit")


def main():
	"""Simple Login App"""

	st.title("Simple Login App")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu,key='main_choice')

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.sidebar.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		Login = st.sidebar.checkbox("Login")
		if Login:
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				# st.balloons()
				con.success("Logged In as {}".format(username))
				app(username)

				delete = st.sidebar.button("Delete User")
				if delete:
					delete_user(username)
					del_user(username)
					con.success("Deleted User! Sorry to see you go")

				
			else:
				con.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.sidebar.subheader("Create New Account")
		new_user = st.sidebar.text_input("Username")
		new_password = st.sidebar.text_input("Password",type='password')

		if st.sidebar.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			con.success("You have successfully created a valid Account")
			con.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()