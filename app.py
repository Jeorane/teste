# Importando as bibliotecas necessárias
import streamlit as st
import sqlite3

# Função para inicializar o banco de dados SQLite
def init_db():
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    # Criando a tabela se não existir
    c.execute('''CREATE TABLE IF NOT EXISTS tarefas (
                 id INTEGER PRIMARY KEY,
                 tarefa TEXT NOT NULL,
                 feita BOOLEAN NOT NULL DEFAULT 0)''')
    conn.commit()
    conn.close()

# Função para adicionar uma nova tarefa
def add_tarefa(tarefa):
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("INSERT INTO tarefas (tarefa, feita) VALUES (?, ?)", (tarefa, False))
    conn.commit()
    conn.close()

# Função para obter todas as tarefas
def get_tarefas():
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tarefas")
    tarefas = c.fetchall()
    conn.close()
    return tarefas

# Função para marcar uma tarefa como concluída
def marcar_como_feita(id):
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("UPDATE tarefas SET feita = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# Função para excluir uma tarefa
def excluir_tarefa(id):
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    c.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# Inicializando o banco de dados
init_db()

# Configurando a interface do Streamlit
st.title("Lista de Tarefas")

# Campo de input para adicionar uma nova tarefa
nova_tarefa = st.text_input("Adicione uma nova tarefa:")

# Botão para adicionar a tarefa
if st.button("Adicionar Tarefa"):
    if nova_tarefa:
        add_tarefa(nova_tarefa)
        st.success("Tarefa adicionada com sucesso!")
    else:
        st.warning("Por favor, insira uma tarefa.")

# Exibindo as tarefas
tarefas = get_tarefas()
if tarefas:
    for tarefa in tarefas:
        id, descricao, feita = tarefa
        # Caixa de seleção para marcar a tarefa como feita
        checkbox = st.checkbox(descricao, value=feita, key=id)
        if checkbox and not feita:
            marcar_como_feita(id)
            st.success(f"Tarefa '{descricao}' marcada como feita.")
        
        # Botão para excluir a tarefa
        if st.button("Excluir", key=f"del_{id}"):
            excluir_tarefa(id)
            st.warning(f"Tarefa '{descricao}' excluída.")
else:
    st.info("Nenhuma tarefa adicionada ainda.")
