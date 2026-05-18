import customtkinter as ctk
from tkinter import messagebox
from supabase import create_client

# ATENÇÃO: Para testes locais. Em produção, use um arquivo .env para esconder essas credenciais.
URL = "https://chcudyivoxfynokdqkcv.supabase.co"
KEY = "sb_publishable_45_ggMieNcAEniVOZ5EtQg_WnZUq8DP"
supabase = create_client(URL, KEY)

app = ctk.CTk()
app.title("Sistema de Mercado Pro")
app.geometry("600x700")

# --- FUNÇÕES ---
def carregar_estoque():
    # Limpa a lista visual antes de carregar
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    try:
        # OTIMIZAÇÃO: Busca apenas os campos necessários, melhorando a performance
        res = supabase.table("produtos").select("id, nome, preco, quantidade").order("nome").execute()
        produtos = res.data
        
        header = ctk.CTkLabel(frame_lista, text="PRODUTO | PREÇO | QTD", font=("Arial", 12, "bold"))
        header.pack(pady=5)

        for p in produtos:
            texto = f"{p['nome']}  |  R$ {p['preco']:.2f}  |  Un: {p['quantidade']}"
            item = ctk.CTkLabel(frame_lista, text=texto, anchor="w")
            item.pack(pady=2, fill="x", padx=10)
            
    except Exception as e:
        print(f"Erro ao carregar: {e}")

def cadastrar():
    nome = entry_nome.get()
    preco = entry_preco.get().replace(',', '.')
    qtd = entry_qtd.get()
    
    if nome and preco and qtd:
        # UX: Caixa de confirmação antes de salvar no banco
        resposta = messagebox.askyesno("Confirmação", f"Deseja cadastrar o produto '{nome}'?")
        
        if resposta:
            try:
                data = {"nome": nome, "preco": float(preco), "quantidade": int(qtd)}
                supabase.table("produtos").insert(data).execute()
                label_status.configure(text=f"{nome} salvo com sucesso!", text_color="green")
                
                # Limpa os campos após o cadastro
                entry_nome.delete(0, 'end')
                entry_preco.delete(0, 'end')
                entry_qtd.delete(0, 'end')
                carregar_estoque() 
            except Exception as e:
                label_status.configure(text="Erro ao salvar no banco!", text_color="red")
    else:
        label_status.configure(text="Preencha todos os campos!", text_color="yellow")

# --- INTERFACE ---
ctk.CTkLabel(app, text="GERENCIADOR DE ESTOQUE", font=("Arial", 22, "bold")).pack(pady=20)

# Frame de Cadastro
frame_cad = ctk.CTkFrame(app)
frame_cad.pack(pady=10, padx=20, fill="x")

entry_nome = ctk.CTkEntry(frame_cad, placeholder_text="Nome do Produto")
entry_nome.pack(pady=5, padx=10, fill="x")

entry_preco = ctk.CTkEntry(frame_cad, placeholder_text="Preço")
entry_preco.pack(pady=5, padx=10, fill="x")

entry_qtd = ctk.CTkEntry(frame_cad, placeholder_text="Quantidade")
entry_qtd.pack(pady=5, padx=10, fill="x")

btn_salvar = ctk.CTkButton(frame_cad, text="CADASTRAR", command=cadastrar, fg_color="green")
btn_salvar.pack(pady=10)

label_status = ctk.CTkLabel(frame_cad, text="")
label_status.pack()

# --- ÁREA DE VISUALIZAÇÃO ---
ctk.CTkLabel(app, text="ITENS EM ESTOQUE", font=("Arial", 16, "bold")).pack(pady=10)

# Lista com barra de rolagem
frame_lista = ctk.CTkScrollableFrame(app, width=550, height=300)
frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

# Botão de atualização manual
btn_refresh = ctk.CTkButton(app, text="ATUALIZAR LISTA", command=carregar_estoque, fg_color="blue")
btn_refresh.pack(pady=10)

# Carrega os dados assim que o programa é aberto
carregar_estoque()

app.mainloop()