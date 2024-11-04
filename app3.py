import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

def create_connection(db_file):
    """ Cria uma conexão com o banco de dados SQLite """
    # ... (código da função create_connection)

def create_table(conn, create_table_sql):
    """ Cria uma tabela no banco de dados """
    # ... (código da função create_table)

def add_task(conn, description, due_date, status):
    """ Adiciona uma nova tarefa ao banco de dados """
    sql = ''' INSERT INTO tasks(description,due_date,status)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (description, due_date, status))
    conn.commit()
    return cur.lastrowid

def list_tasks(conn, status=None):
    """ Lista todas as tarefas ou as tarefas com um status específico """
    cur = conn.cursor()
    if status:
        cur.execute("SELECT * FROM tasks WHERE status=?", (status,))
    else:
        cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=['ID', 'Descrição', 'Criado em', 'Data de Finalização', 'Status'])
    return df

def edit_task(conn, task_id, description, due_date, status):
    """ Edita uma tarefa existente """
    sql = ''' UPDATE tasks
              SET description = ?,
                  due_date = ?,
                  status = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (description, due_date, status, task_id))
    conn.commit()

def delete_task(conn, task_id):
    """ Exclui uma tarefa """
    sql = 'DELETE from tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

# Cria a conexão e a tabela (executado apenas uma vez)
conn = create_connection("tasks.db")
if conn is not None:
    create_table(conn, sql_create_tasks_table)

# Interface do usuário
st.title("Lista de Tarefas")

# Formulário para adicionar tarefas
with st.form("add_task"):
    description = st.text_input("Descrição")
    due_date = st.date_input("Data de Finalização")
    status = st.selectbox("Status", ["Finalizada", "Adiada", "Em Andamento"])
    if st.form_submit_button("Adicionar"):
        add_task(conn, description, due_date, status)
        st.success("Tarefa adicionada com sucesso!")

# Filtro por status
status_filter = st.selectbox("Filtrar por status", ["Todos"] + ["Finalizada", "Adiada", "Em Andamento"])

# Lista de tarefas
tasks_df = list_tasks(conn, status_filter if status_filter != "Todos" else None)
st.dataframe(tasks_df)

# Formulário para editar tarefas
task_id = st.number_input("ID da tarefa para editar", min_value=1)
if task_id:
    task = tasks_df[tasks_df['ID'] == task_id]
    if not task.empty:
        with st.form("edit_task"):
            description = st.text_input("Descrição", value=task['Descrição'].values[0])
            due_date = st.date_input("Data de Finalização", value=pd.to_datetime(task['Data de Finalização'].values[0]))
            status = st.selectbox("Status", ["Finalizada", "Adiada", "Em Andamento"], index=["Finalizada", "Adiada", "Em Andamento"].index(task['Status'].values[0]))
            if st.form_submit_button("Editar"):
                edit_task(conn, task_id, description, due_date, status)
                st.success("Tarefa editada com sucesso!")

# Botão para excluir tarefas
if st.button("Excluir Tarefa Selecionada"):
    delete_task(conn, task_id)
    st.success("Tarefa excluída com sucesso!")

conn.close()