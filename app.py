from dotenv import load_dotenv
load_dotenv()  # loads all environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and give us SQL query as output
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

# Function to generate answer from database using SQL query generated above
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Function to execute SQL commands (for add, update, delete operations)
def execute_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

# Define your prompt
prompt = [
    """
    You are an expert in converting English language to SQL query! The SQL database has the name STUDENT and 
    has the following columns - NAME, CLASS, SECTION, and MARKS.\n\n For example,\nExample 1 - How many 
    entries of records are present? The SQL command will be something like this: SELECT * FROM STUDENT;
    \nExample 2 - Tell me all the students studying in math class? The SQL command will be something like
    this: SELECT * FROM STUDENT WHERE CLASS="math";\nExample 3 - Give all the names of students in ascending order,
    the SQL command will be something like: SELECT * FROM STUDENT ORDER BY NAME ASC;
    \nExample 4 - Give me the name of the student whose class is biology and marks have value greater than
    55, the SQL command will be something like: SELECT * FROM STUDENT WHERE MARKS > 55 AND CLASS = 'Biology';
    \nExample 5 - Give me the average of all the marks, the SQL command will something be like: SELECT AVG(MARKS) AS Average_Marks FROM STUDENT;
    \nExample 6 - Kitne students ke marks 30 se zyada hai, the SQL command will something be like: SELECT * FROM STUDENT WHERE MARKS > 30;
    also the SQL code should not have ``` in beginning or end and SQL word in the output.
    """
]

# Streamlit app
st.set_page_config(page_title="CRUD Application for STUDENT Database")
st.header("CRUD Application to Manage STUDENT Data")

# --- Create Operation ---
st.subheader("Add a New Student")
with st.form(key='add_student_form'):
    name = st.text_input("Name")
    student_class = st.text_input("Class")
    section = st.text_input("Section")
    marks = st.number_input("Marks", min_value=0, max_value=100)
    submit_add = st.form_submit_button("Add Student")
    
    if submit_add:
        add_sql = f"INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('{name}', '{student_class}', '{section}', {marks});"
        execute_sql_query(add_sql, "student.db")
        st.success(f"Student {name} added successfully!")

# --- Read Operation ---
st.subheader("View All Students")
if st.button("Refresh Data"):
    students = read_sql_query("SELECT * FROM STUDENT;", "student.db")
    st.write(students)

# --- Update Operation ---
st.subheader("Update Student Marks")
update_name = st.selectbox("Select Student to Update", [row[0] for row in read_sql_query("SELECT NAME FROM STUDENT;", "student.db")])
new_marks = st.number_input("New Marks", min_value=0, max_value=100)
submit_update = st.button("Update Marks")

if submit_update:
    update_sql = f"UPDATE STUDENT SET MARKS = {new_marks} WHERE NAME = '{update_name}';"
    execute_sql_query(update_sql, "student.db")
    st.success(f"Marks for {update_name} updated to {new_marks}!")

# --- Delete Operation ---
st.subheader("Delete a Student")
delete_name = st.selectbox("Select Student to Delete", [row[0] for row in read_sql_query("SELECT NAME FROM STUDENT;", "student.db")])
submit_delete = st.button("Delete Student")

if submit_delete:
    delete_sql = f"DELETE FROM STUDENT WHERE NAME = '{delete_name}';"
    execute_sql_query(delete_sql, "student.db")
    st.success(f"Student {delete_name} deleted successfully!")

# --- Query Input Operation ---
st.subheader("Ask a Question")
question = st.text_input("Type your question in English or Hindi:")
if st.button("Get Answer"):
    if question:
        response = get_gemini_response(question, prompt)
        st.write("SQL Query Generated (for internal use):")
        st.code(response)

        # Execute the generated SQL query
        try:
            query_result = read_sql_query(response, "student.db")
            if query_result:
                # If the query result has only one row and one column, show that value
                if len(query_result) == 1 and len(query_result[0]) == 1:
                    st.subheader("Answer:")
                    st.write(query_result[0][0])  # Show the single value
                else:
                    st.subheader("Query Result:")
                    st.write(query_result)  # Show the full result for other cases
            else:
                st.write("No results found.")
        except Exception as e:
            st.error(f"Error executing the SQL query: {e}")
