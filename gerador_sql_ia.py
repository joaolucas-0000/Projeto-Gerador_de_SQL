import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk  # Importante: Importando o módulo ttk para o Combobox
import google.generativeai as genai

CHAVE_API = "SUA_API_KEY_AQUI" 
genai.configure(api_key=CHAVE_API)

def gerar_sql():
    """Função para capturar a demanda, o tipo de banco, enviar para a IA e exibir o SQL."""
    demanda = text_entrada.get("1.0", tk.END).strip()
    banco_escolhido = combo_banco.get() # Captura o banco selecionado
    
    if not demanda:
        messagebox.showwarning("Aviso", "Por favor, descreva a demanda do sistema.")
        return

    # Desabilitar o botão enquanto a IA processa
    btn_gerar.config(text="Gerando...", state=tk.DISABLED)
    root.update()

    try:
        model = genai.GenerativeModel('gemini-2.5-flash') 
        
        # Prompt atualizado para exigir o dialeto correto do banco de dados
        prompt = f"""
        Você é um Arquiteto de Banco de Dados Sênior especializado em {banco_escolhido}. 
        Analise a seguinte demanda de sistema e crie um script SQL completo com as instruções CREATE TABLE adaptadas EXCLUSIVAMENTE para o banco de dados {banco_escolhido}.
        
        Demanda do usuário: "{demanda}"
        
        Regras estritas:
        1. Retorne APENAS o código SQL puro. Nada de explicações.
        2. Não use formatação markdown (como ```sql). O retorno deve ser texto limpo.
        3. Use os tipos de dados estritamente compatíveis e otimizados para {banco_escolhido}.
        4. Use as melhores práticas (Chaves Primárias, Chaves Estrangeiras e nomenclatura clara).
        5. Garanta que as tabelas sejam criadas na ordem correta para respeitar as restrições de chave estrangeira.
        """
        
        response = model.generate_content(prompt)
        
        # Limpar o campo de saída e inserir o novo SQL
        text_saida.delete("1.0", tk.END)
        text_saida.insert(tk.END, response.text.strip())
        
    except Exception as e:
        messagebox.showerror("Erro de Integração", f"Ocorreu um erro ao conectar com a IA:\n{e}")
    finally:
        # Reabilitar o botão
        btn_gerar.config(text="Gerar Tabelas SQL", state=tk.NORMAL)


# ==========================================
# CONFIGURAÇÃO DA INTERFACE GRÁFICA (GUI)
# ==========================================
root = tk.Tk()
root.title("Gerador Dinâmico de Banco de Dados com IA")
root.geometry("850x750") # Aumentei um pouco a altura da janela
root.configure(padx=20, pady=20)

# Título Principal
lbl_titulo = tk.Label(root, text="Gerador de Esquemas SQL", font=("Arial", 16, "bold"))
lbl_titulo.pack(pady=(0, 10))

# Seção: Escolha do Banco de Dados
lbl_banco = tk.Label(root, text="Selecione o Sistema de Banco de Dados alvo:", font=("Arial", 10, "bold"))
lbl_banco.pack(anchor="w")

# Lista de opções de Bancos de Dados
opcoes_bancos = ["PostgreSQL", "MySQL", "SQL Server", "Oracle", "SQLite"]
combo_banco = ttk.Combobox(root, values=opcoes_bancos, state="readonly", font=("Arial", 10), width=30)
combo_banco.current(0) # Define PostgreSQL como o padrão (índice 0)
combo_banco.pack(anchor="w", pady=(0, 15))

# Seção de Entrada (Demanda do Usuário)
lbl_entrada = tk.Label(root, text="Descreva o que o seu sistema precisa gerenciar (Ex: 'Um sistema escolar com alunos e notas'):", font=("Arial", 10))
lbl_entrada.pack(anchor="w")

text_entrada = scrolledtext.ScrolledText(root, height=5, width=100, font=("Consolas", 10))
text_entrada.pack(pady=5)

# Botão de Ação
btn_gerar = tk.Button(root, text="Gerar Tabelas SQL", command=gerar_sql, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
btn_gerar.pack(pady=15)

# Seção de Saída (SQL Gerado)
lbl_saida = tk.Label(root, text="Script SQL Gerado:", font=("Arial", 10))
lbl_saida.pack(anchor="w")

text_saida = scrolledtext.ScrolledText(root, height=20, width=100, font=("Consolas", 10, "normal"), bg="#1e1e1e", fg="#d4d4d4")
text_saida.pack(pady=5)

# Iniciar o loop da interface gráfica
if __name__ == "__main__":
    root.mainloop()