import streamlit as st
import sqlite3
from datetime import datetime, date

# Função para criar a tabela no banco de dados
def create_table():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  description TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  finished_at TIMESTAMP NOT NULL,
                  status TEXT CHECK(status IN ('Finalizada', 'Adiada', 'Em Andamento')) NOT NULL)''')
    conn.commit()
    conn.close()

# Função para adicionar uma nova tarefa
def add_task(description, finished_at, status):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (description, finished_at, status) VALUES (?, ?, ?)',
              (description, finished_at, status))
    conn.commit()
    conn.close()

# Função para visualizar todas as tarefas
def view_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return tasks

# Função para atualizar uma tarefa
def update_task(task_id, description, finished_at, status):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET description = ?, finished_at = ?, status = ? WHERE id = ?',
              (description, finished_at, status, task_id))
    conn.commit()
    conn.close()

# Função para deletar uma tarefa
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# Inicializar o banco de dados
create_table()

# Interface do Streamlit
st.title("Aplicativo de Lista de Tarefas")

# Adicionar uma nova tarefa
st.header("Adicionar Nova Tarefa")
description = st.text_input("Descrição da Tarefa (Obrigatório)")
finished_at = st.date_input("Data de Finalização (Não pode ser anterior a hoje)", min_value=date.today())
status = st.selectbox("Status da Tarefa", ["Finalizada", "Adiada", "Em Andamento"])

if st.button("Adicionar Tarefa"):
    if description:
        add_task(description, finished_at, status)
        st.success("Tarefa adicionada com sucesso!")
    else:
        st.error("Descrição da Tarefa é obrigatória.")

# Visualizar e atualizar tarefas
st.header("Tarefas Existentes")
tasks = view_tasks()

for task in tasks:
    st.subheader(f"Tarefa ID: {task[0]}")
    st.write("Descrição:", task[1])
    st.write("Data de Inclusão:", task[2])
    st.write("Data de Finalização:", task[3])
    st.write("Status:", task[4])

    # Campos para atualização
    new_description = st.text_input(f"Atualizar Descrição para Tarefa ID {task[0]}", value=task[1])
    new_finished_at = st.date_input(f"Atualizar Data de Finalização para Tarefa ID {task[0]}", min_value=date.today(), value=datetime.strptime(task[3], "%Y-%m-%d"))
    new_status = st.selectbox(f"Atualizar Status para Tarefa ID {task[0]}", ["Finalizada", "Adiada", "Em Andamento"], index=["Finalizada", "Adiada", "Em Andamento"].index(task[4]))

    # Botões para atualizar e deletar
    if st.button(f"Atualizar Tarefa ID {task[0]}"):
        update_task(task[0], new_description, new_finished_at, new_status)
        st.success(f"Tarefa ID {task[0]} atualizada com sucesso!")

    if st.button(f"Deletar Tarefa ID {task[0]}"):
        delete_task(task[0])
        st.warning(f"Tarefa ID {task[0]} deletada!")

# Para rodar o aplicativo, execute o seguinte comando no terminal:
# streamlit run app.py
