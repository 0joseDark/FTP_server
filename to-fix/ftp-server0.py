import os
import threading
from tkinter import Tk, Label, Button, filedialog
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class FTPServerApp:
    def __init__(self, master):
        self.master = master
        master.title("Servidor FTP")

        self.label = Label(master, text="Escolha o diretório para o servidor FTP:")
        self.label.pack()

        self.select_button = Button(master, text="Selecionar Diretório", command=self.select_directory)
        self.select_button.pack()

        self.start_button = Button(master, text="Ligar Servidor", command=self.start_server, state="disabled")
        self.start_button.pack()

        self.stop_button = Button(master, text="Desligar Servidor", command=self.stop_server, state="disabled")
        self.stop_button.pack()

        self.exit_button = Button(master, text="Sair", command=self.exit_app)
        self.exit_button.pack()

        self.directory = None
        self.server_thread = None
        self.server = None

    def select_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.label.config(text=f"Diretório selecionado: {self.directory}")
            self.start_button.config(state="normal")

    def start_server(self):
        if self.directory:
            # Configura o autorizer com permissões
            authorizer = DummyAuthorizer()
            authorizer.add_anonymous(self.directory, perm='elradfmwMT')

            handler = FTPHandler
            handler.authorizer = authorizer

            # Configura o servidor FTP na porta 2121
            self.server = FTPServer(('0.0.0.0', 2121), handler)

            # Inicia o servidor em uma nova thread
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True  # Permite que o thread seja fechado corretamente
            self.server_thread.start()

            self.label.config(text=f"Servidor FTP ligado no diretório: {self.directory}")
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")

    def stop_server(self):
        if self.server:
            # Para o servidor FTP
            self.server.close_all()
            self.server_thread.join()
            self.server = None
            self.server_thread = None
            self.label.config(text="Servidor FTP desligado.")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def exit_app(self):
        if self.server_thread:
            self.stop_server()
        self.master.quit()

root = Tk()
ftp_server_app = FTPServerApp(root)
root.mainloop()
