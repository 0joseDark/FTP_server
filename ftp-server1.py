import os
import threading
from tkinter import Tk, Label, Button, Entry, filedialog
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class FTPServerApp:
    def __init__(self, master):
        self.master = master
        master.title("Servidor FTP")

        # Label e campo de entrada para o Host
        self.label_host = Label(master, text="Host:")
        self.label_host.pack()
        self.entry_host = Entry(master)
        self.entry_host.insert(0, "0.0.0.0")  # Define o valor padrão para escutar em todas as interfaces
        self.entry_host.pack()

        # Label e campo de entrada para o Nome de Usuário
        self.label_user = Label(master, text="Nome de Usuário:")
        self.label_user.pack()
        self.entry_user = Entry(master)
        self.entry_user.insert(0, "usuario")  # Nome de usuário padrão
        self.entry_user.pack()

        # Label e campo de entrada para a Senha
        self.label_password = Label(master, text="Senha:")
        self.label_password.pack()
        self.entry_password = Entry(master, show="*")  # O caractere '*' oculta a senha digitada
        self.entry_password.insert(0, "senha123")  # Senha padrão
        self.entry_password.pack()

        # Label e campo de entrada para a Porta
        self.label_port = Label(master, text="Porta:")
        self.label_port.pack()
        self.entry_port = Entry(master)
        self.entry_port.insert(0, "21")  # Porta padrão do FTP
        self.entry_port.pack()

        # Label para instrução de seleção de diretório
        self.label = Label(master, text="Escolha o diretório para o servidor FTP:")
        self.label.pack()

        # Botão para selecionar o diretório
        self.select_button = Button(master, text="Selecionar Diretório", command=self.select_directory)
        self.select_button.pack()

        # Botão para iniciar o servidor
        self.start_button = Button(master, text="Ligar Servidor", command=self.start_server, state="disabled")
        self.start_button.pack()

        # Botão para parar o servidor
        self.stop_button = Button(master, text="Desligar Servidor", command=self.stop_server, state="disabled")
        self.stop_button.pack()

        # Botão para sair da aplicação
        self.exit_button = Button(master, text="Sair", command=self.exit_app)
        self.exit_button.pack()

        # Inicialização de variáveis
        self.directory = None
        self.server_thread = None
        self.server = None

    def select_directory(self):
        # Método para selecionar o diretório a ser servido via FTP
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.label.config(text=f"Diretório selecionado: {self.directory}")
            self.start_button.config(state="normal")

    def start_server(self):
        # Método para iniciar o servidor FTP
        if self.directory:
            # Obtenção dos valores de host, porta, nome de usuário e senha
            host = self.entry_host.get()
            port = int(self.entry_port.get())
            username = self.entry_user.get()
            password = self.entry_password.get()

            # Configuração do autorizer para adicionar o usuário com permissões
            authorizer = DummyAuthorizer()
            authorizer.add_user(username, password, self.directory, perm='elradfmwMT')
            
            # Configuração do manipulador e vinculação com o autorizer
            handler = FTPHandler
            handler.authorizer = authorizer

            # Configuração do servidor FTP com o host e porta especificados
            self.server = FTPServer((host, port), handler)

            # Início do servidor em uma nova thread
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True  # Permite que a thread seja fechada corretamente
            self.server_thread.start()

            self.label.config(text=f"Servidor FTP ligado no diretório: {self.directory}")
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")

    def stop_server(self):
        # Método para parar o servidor FTP
        if self.server:
            self.server.close_all()
            self.server_thread.join()
            self.server = None
            self.server_thread = None
            self.label.config(text="Servidor FTP desligado.")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def exit_app(self):
        # Método para sair da aplicação
        if self.server_thread:
            self.stop_server()
        self.master.quit()

# Inicialização da interface gráfica
root = Tk()
ftp_server_app = FTPServerApp(root)
root.mainloop()
