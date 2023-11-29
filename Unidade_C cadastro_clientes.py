import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk

class ClienteApp:
    def __init__(self, root):
        self.root = root
        self.root.title(" Seja bem vindo ao cadastro de Clientes")

 
        self.conn = sqlite3.connect('clientes_database.db')
        self.cursor = self.conn.cursor()

    
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                foto BLOB
            )
        ''')
        self.conn.commit()


        self.create_widgets()

    def create_widgets(self):
   
        self.nome_label = tk.Label(self.root, text='Nome:')
        self.nome_label.grid(row=0, column=0, padx=10, pady=10)
        self.nome_entry = tk.Entry(self.root)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=10)

   
        self.foto_label = tk.Label(self.root, text='Foto:')
        self.foto_label.grid(row=1, column=0, padx=10, pady=10)


        self.adicionar_foto_button = tk.Button(self.root, text='Adicionar Foto', command=self.adicionar_foto)
        self.adicionar_foto_button.grid(row=1, column=1, padx=10, pady=10)

     
        self.cadastrar_cliente_button = tk.Button(self.root, text='Cadastrar Cliente', command=self.cadastrar_cliente)
        self.cadastrar_cliente_button.grid(row=2, columnspan=2, pady=10)

  
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Nome', 'Foto'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Foto', text='Foto')
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


        self.update_clientes_view()

    def adicionar_foto(self):
        filename = filedialog.askopenfilename(initialdir='/', title='Escolha um arquivo',
                                      filetypes=[('Imagens', '*.png;*.gif;*.ppm;*.jpg')])

        if filename:
            self.foto_path = filename
            self.mostrar_foto()

    def mostrar_foto(self):
        try:
            foto = Image.open(self.foto_path)
            foto.thumbnail((50, 50)) 
            foto = ImageTk.PhotoImage(foto)
            self.foto_label.config(image=foto)
            self.foto_label.image = foto 
        except Exception as e:
            messagebox.showerror('Erro', f' Infezlimente de um erro inesperado  ao abrir a foto: {e}')

    def cadastrar_cliente(self):
        nome = self.nome_entry.get()

        if not nome:
            messagebox.showwarning('Aviso', 'Por favor, insira o nome do cliente.')
            return

      
        if hasattr(self, 'foto_path'):
            with open(self.foto_path, 'rb') as file:
                foto_blob = file.read()
        else:
            foto_blob = None

      
        self.cursor.execute('INSERT INTO clientes (nome, foto) VALUES (?, ?)', (nome, foto_blob))
        self.conn.commit()

       
        self.nome_entry.delete(0, tk.END)
        self.foto_label.config(image='')  

   
        self.update_clientes_view()


        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute('SELECT * FROM clientes')
        clientes = self.cursor.fetchall()


        for cliente in clientes:
            self.tree.insert('', 'end', values=cliente)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteApp(root)
    root.mainloop()

app.conn.close()