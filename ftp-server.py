import os
import threading
from tkinter import Tk, Label, Button, filedialog
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Classe do Servidor FTP
class FTPServerApp:
    def __init__(self, master):
        self.master = master
        master.title("Servidor FTP")

        # Label informativa
        self.label = Label(master, text="Escolha o diretório para o servidor FTP:")
        self.label.pack()

        # Botão para selecionar o diretório
        self.select_button = Button(master, text="Selecionar Diretório", command=self.select_directory)
        self.select_button.pack()

        # Botão para iniciar o servidor FTP
        self.start_button = Button(master, text="Ligar Servidor", command=self.start_server, state="disabled")
        self.start_button.pack()

        # Botão para desligar o servidor FTP
        self.stop_button = Button(master, text="Desligar Servidor", command=self.stop_server, state="disabled")
        self.stop_button.pack()

        # Botão para sair da aplicação
        self.exit_button = Button(master, text="Sair", command=self.exit_app)
        self.exit_button.pack()

        # Diretório que será servido
        self.directory = None
        # Thread do servidor
        self.server_thread = None

    def select_directory(self):
        # Abre um diálogo para selecionar o diretório
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.label.config(text=f"Diretório selecionado: {self.directory}")
            self.start_button.config(state="normal")

    def start_server(self):
        if self.directory:
            # Configura o servidor FTP
            authorizer = DummyAuthorizer()
            authorizer.add_anonymous(self.directory, perm='elradfmw')  # Permissões totais ao usuário anônimo

            handler = FTPHandler
            handler.authorizer = authorizer

            self.server = FTPServer(('0.0.0.0', 2121), handler)

            # Inicia o servidor em uma nova thread para não bloquear a interface gráfica
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.start()

            self.label.config(text=f"Servidor FTP ligado no diretório: {self.directory}")
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")

    def stop_server(self):
        if self.server_thread:
            # Para o servidor FTP
            self.server.close_all()
            self.server_thread.join()
            self.server_thread = None
            self.label.config(text="Servidor FTP desligado.")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def exit_app(self):
        # Se o servidor estiver rodando, desliga antes de sair
        if self.server_thread:
            self.stop_server()
        self.master.quit()

# Criação da interface gráfica e execução da aplicação
root = Tk()
ftp_server_app = FTPServerApp(root)
root.mainloop()
