import streamlit as st
import pandas as pd 
from db_file import * 
import streamlit.components.v1 as stc
 


HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">TIME TABLE</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
    """


def main():
	con = st.container()
	stc.html(HTML_BANNER)
	menu = ["Create","Read","Update","Delete","About", "Table"]
	choice = st.sidebar.selectbox("Menu",menu)
	create_table()

	if choice == "Create":
		st.subheader("Add Course")
		col1,col2 = st.columns(2)
		
		with col1:
			task = st.text_input("CourseID")
			task_due_date = st.text_input("Time")

		with col2:
			task_status = st.text_input("Link")
			day = st.selectbox("Day",["Monday","Tuesday","Wednesday","Thursday","Friday"])

		if st.button("Add Course"):
			add_data(task,task_status,str(task_due_date),day)
			con.success("Added {} to Database".format(task))


	elif choice == "Read":
		# st.subheader("View Items")
		with st.expander("View All"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["CourseID","Link","Time","Day"])
			st.dataframe(clean_df)

	elif choice == "Update":
		st.subheader("Edit Courses")
		with st.expander("Current Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["CourseID","Link","Time","Day"])
			st.dataframe(clean_df)

		list_of_tasks = [i[0] for i in view_all_task_names()]
		selected_task = st.selectbox("Courses",list_of_tasks)
		task_result = get_task(selected_task)
		# st.write(task_result)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]
			day = task_result[0][3]

			col1,col2 = st.columns(2)
			
			with col1:
				new_task = st.text_input("CourseID",task)
				new_day = st.selectbox("Day",["Monday","Tuesday","Wednesday","Thursday","Friday"])

			with col2:
				new_task_status = st.text_input("Link", task_status)
				new_task_due_date = st.text_input("Time", (task_due_date))

			if st.button("Update Task"):
				edit_task_data(new_task,new_task_status,str(new_task_due_date),new_day,task,task_status,task_due_date,day)
				con.success("Updated -- {} ---> {}".format(task,new_task))

			with st.expander("View Updated Data"):
				result = view_all_data()
				# st.write(result)
				clean_df = pd.DataFrame(result,columns=["CourseID","Link","Time","Day"])
				st.dataframe(clean_df)


	elif choice == "Delete":
		st.subheader("Delete")
		with st.expander("View Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["CourseID","Link","Time","Day"])
			st.dataframe(clean_df)

		unique_list = [i[0] for i in view_all_task_names()]
		delete_by_task_name =  st.selectbox("Select CourseID",unique_list)
		if st.button("Delete"):
			delete_data(delete_by_task_name)
			st.warning("Deleted: '{}'".format(delete_by_task_name))

		with st.expander("Updated Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["CourseID","Link","Time","Day"])
			st.dataframe(clean_df)

	elif choice == "Table":
		result = view_all_data()
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


if __name__ == '__main__':
	main()