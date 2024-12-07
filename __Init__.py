import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import time
import sqlite3
from tkinter import filedialog, messagebox
import io
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import threading
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import shutil
import requests
import zipfile
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import webbrowser
from sqlite3 import Error
import base64
from PIL import Image, ImageDraw, ImageFont
from tkcalendar import DateEntry
from datetime import datetime
from io import BytesIO
import re
from packaging import version
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tkinterhtml import HtmlFrame  


class DataBase:

    def __init__(self):

        # Caminho do banco de dados
        PathApp = os.path.dirname(__file__)
        self.DataBaseDir = os.path.join(PathApp, "DataBase")

        # Verifica se o diretório do banco de dados existe; se não, cria
        if not os.path.exists(self.DataBaseDir):
            os.makedirs(self.DataBaseDir)

        self.DataName = os.path.join(self.DataBaseDir, "DataBase.db")

    def connect(self):

        try:
            # Certifique-se de que o caminho para o banco de dados esteja correto
            PathApp = os.path.dirname(__file__)
            DataName = os.path.join(PathApp, 'DataBase', 'DataBase.db')
            
            # Tente abrir a conexão com o banco de dados
            con = sqlite3.connect(DataName)
            return con
        except sqlite3.Error as ex:
            print(f"Erro ao conectar com o banco de dados: {ex}")
            return None

    # def create_tables(self):
        # Criação da tabela Informacoes_Usuario_Fibromialgia
        query_fibromialgia = '''
        CREATE TABLE IF NOT EXISTS Cadastro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nascimento DATE,
            tipo_sanguineo TEXT,
            numero_cadastro TEXT,
            data_emissao DATE,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE,
            cns TEXT UNIQUE,
            filiacao TEXT,
            imagem BLOB,
            name_image TEXT,
            faixa_etaria TEXT,
            mes TEXT,
            pdf BLOB,
            name_pdf TEXT,
            name_carteira TEXT,
            carteirinha BLOB,
            telefone TEXT,
            estado_carteira TEXT


        )
        '''
        
        # Criação da tabela login
        query_login = '''
        CREATE TABLE IF NOT EXISTS login (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT ,
            senha TEXT ,
            email TEXT ,
            nome_email TEXT,
            imagem_url BLOD
        )
        '''
        
        # Criação da tabela backup_agendado
        query_backup = '''
        CREATE TABLE IF NOT EXISTS backup_agendado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caminho_computador TEXT NOT NULL,
            horario TEXT NOT NULL,
            dia_semana TEXT NOT NULL,
            dia_mes TEXT NOT NULL
        )
        '''
        
        try:
            con = self.connect()
            if con:
                c = con.cursor()
                
                # Executa as queries para criar as tabelas
                c.execute(query_fibromialgia)
                c.execute(query_login)
                c.execute(query_backup)
                
                con.commit()
                con.close()
                print("Tabelas criadas com sucesso!")
                
        except sqlite3.Error as ex:
            print(f"Erro ao criar as tabelas: {ex}")

    def dml(self, query, params=()):  # DELETE, UPDATE, INSERT
        try:
            vcon = self.connect()
            if vcon:
                c = vcon.cursor()
                c.execute(query, params)
                vcon.commit()
                vcon.close()
        except sqlite3.Error as ex:
            print(f"Erro ao executar DML: {ex}")

    def dql(self, query, parametros=None):  # SELECT

        vcon = None
        try:
            vcon = self.connect()
            if vcon is None:
                raise sqlite3.Error("Conexão com o banco de dados falhou.")
            
            c = vcon.cursor()
            c.execute(query, parametros or ())
            res = c.fetchall()
            return res
        except sqlite3.Error as ex:
            print(f"Erro ao executar DQL: {ex}")
            return []
        finally:
            if vcon:
                vcon.close()

    def dql_Image(self, query, parametros=None):  # SELECT
        try:
            vcon = self.connect()
            c = vcon.cursor()
            c.execute(query, parametros or ())
            res = c.fetchone()
            vcon.close()
            return res
        except sqlite3.Error as ex:
            print(f"Erro ao executar DQL_Image: {ex}")
            return []

    def dmlWithParament(self, query, Parament=None):  # dml with all arguments
        try:
            conn = self.connect() 
            cursor = conn.cursor()
            if Parament is not None:
                cursor.execute(query, Parament)
            else:
                cursor.execute(query)
            conn.commit()
            conn.close()
        except sqlite3.Error as ex:
            print(f"Erro ao executar DML com parâmetros: {ex}")

class Logon(ctk.CTk): 

    def __init__(self):
        super().__init__()

        db = DataBase()
        # db.create_tables()
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        self.geometry("800x600")
        self.minsize(800, 600)
        self.title('Login')
        
        self.service = self.authenticate_google_drive()

        if self.check_for_updates():
            self.download_and_apply_update()

        Login_User_Google = Logon_Google_Fuctions(self)
        
                
        # Imagem pattern imagem inical da tela de login
        img1 = ImageTk.PhotoImage(Image.open("Image/pattern.png"))
        l1 = ctk.CTkLabel(master=self, image=img1)
        l1.pack()

        Frame_Tela_Login = ctk.CTkFrame(master=l1, width=500, height=500, corner_radius=30)
        Frame_Tela_Login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        l2 = ctk.CTkLabel(master=Frame_Tela_Login, text="Logar", font=('Century Gothic', 40))
        l2.place(x=190, y=45)

        self.Entry_Nome_User = ctk.CTkEntry(master=Frame_Tela_Login, width=390, height=50, placeholder_text='Nome', font=('Century Gothic', 20))
        self.Entry_Nome_User.place(x=60, y=130)

        self.Entry_Senha_User = ctk.CTkEntry(master=Frame_Tela_Login, width=390, height=50, placeholder_text='Senha', show="*", font=('Century Gothic', 20))
        self.Entry_Senha_User.place(x=60, y=200)

        l3 = ctk.CTkLabel(master=Frame_Tela_Login, text="Esqueceu senha?", font=('Century Gothic', 16))
        l3.place(x=310, y=255)

        Button_Logar = ctk.CTkButton(master=Frame_Tela_Login, width=390, height=50, text="Entrar", command=self.login_user, corner_radius=6)
        Button_Logar.place(x=60, y=300)

        img2 = ctk.CTkImage(Image.open("Image/Google.webp").resize((20, 20), Image.LANCZOS))
       
        button2 = ctk.CTkButton(master=Frame_Tela_Login, image=img2, text="Google", width=390, height=50, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF', command=Login_User_Google.login_with_google)
        button2.place(x=60, y=370)
    
    def login_user(self):
        
        # Obtém os valores dos campos de entrada para email e senha
        nome_entry = self.Entry_Nome_User.get().strip()
        password_entry = self.Entry_Senha_User.get().strip()

        # Certifique-se de que os campos estão preenchidos corretamente
        if not nome_entry or not password_entry:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        db = DataBase()

        # Verifica se o email e a senha existem no banco de dados
        query = "SELECT * FROM login WHERE nome = ? AND senha = ?"
        user_data = db.dql(query, (nome_entry, password_entry))

        if user_data:
            self.Show_Window_Home()  # Aqui você deve chamar a função que abre a próxima tela
        else:
            # Caso as credenciais estejam incorretas ou não existam
            messagebox.showerror("Erro", "Conta não encontrada. Por favor, entre com a conta do Google e crie um usuário local.")

    def authenticate_google_drive(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        CLIENT_SECRET_FILE = 'fibromialgia.json'
        TOKEN_DIR = 'FIBROMIALGIA'
        TOKEN_PICKLE_FILE = os.path.join(TOKEN_DIR, 'token.pickle')

        if not os.path.exists(TOKEN_DIR):
            os.makedirs(TOKEN_DIR)

        creds = None
        if os.path.exists(TOKEN_PICKLE_FILE):
            with open(TOKEN_PICKLE_FILE, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(TOKEN_PICKLE_FILE, 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        return service

    @staticmethod
    def find_file_by_name(service, folder_id, file_name):

        try:
            query = f"'{folder_id}' in parents and name='{file_name}'"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            items = results.get('files', [])
            
            if not items:
                print(f"No file found with the name {file_name}.")
                return None
            return items[0]['id']
        except Exception as e:
            print(f"Error searching for file: {e}")
            return None

    def check_for_updates(self):

        try:
            folder_id = '1B9NpUSk3xtBFiCvauWoHzAGDo3sXQoR5'
            version_file_id = self.find_file_by_name(self.service, folder_id, 'version.txt')

            if not version_file_id:
                raise FileNotFoundError("Erro ao localizar 'version.txt'.")

            request = self.service.files().get_media(fileId=version_file_id)
            latest_version = request.execute().decode('utf-8').strip()

            try:
                with open("version.txt", "r") as file:
                    current_version = file.read().strip()
            except FileNotFoundError:
                current_version = "0.0.0"

            print(f"Versão atual: {current_version}")
            print(f"Versão no Drive: {latest_version}")

            if version.parse(latest_version) > version.parse(current_version):
                messagebox.showinfo("Nova versão disponível!")
                self.download_and_apply_update(folder_id, version_file_id)
                return True
            else:
                print("Seu sistema está atualizado.")
                return False
        except Exception as e:
            print(f"Erro ao verificar atualizações na função 'check_for_updates': {e}")
            return False

    def download_and_apply_update(self, *args, **kwargs):
        try:
            # Obtém o caminho da pasta de Downloads e o diretório de instalação do sistema
            downloads_folder = str(Path.home() / "Downloads")
            system_folder = os.path.dirname(os.path.abspath(__file__))

            # ID da pasta no Google Drive
            folder_id = '1B9NpUSk3xtBFiCvauWoHzAGDo3sXQoR5'

            # Baixar o executável FIBROMIALGIA.exe
            exe_file_id = self.find_file_by_name(self.service, folder_id, 'FIBROMIALGIA.exe')
            if exe_file_id:
                exe_save_path = os.path.join(downloads_folder, "FIBROMIALGIA.exe")
                with open(exe_save_path, "wb") as exe_file:
                    request = self.service.files().get_media(fileId=exe_file_id)
                    exe_file.write(request.execute())
                messagebox.showinfo(f"Atualização baixada para: {exe_save_path}")
            else:
                print("Erro ao localizar 'FIBROMIALGIA.exe'.")

            # Baixar e substituir o arquivo version.txt na pasta do sistema
            version_file_id = self.find_file_by_name(self.service, folder_id, 'version.txt')
            if version_file_id:
                version_save_path = os.path.join(system_folder, "version.txt")
                with open(version_save_path, "wb") as version_file:
                    request = self.service.files().get_media(fileId=version_file_id)
                    version_file.write(request.execute())
                print(f"'version.txt' atualizado em: {version_save_path}")
            else:
                print("Erro ao localizar 'version.txt'.")

            # Mensagem de sucesso ao usuário
            print("Sucesso", f"Atualização baixada!\n- 'FIBROMIALGIA.exe' em: {exe_save_path}\n- 'version.txt' atualizado no sistema.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

    def apply_update(self):
        try:
            # Verifica se o arquivo FIBROMIALGIA.exe foi baixado corretamente
            if os.path.exists("FIBROMIALGIA.exe"):
                # Simplesmente informa ao usuário que o arquivo foi baixado
                messagebox.showinfo("Atualização", "Atualização baixada com sucesso! Por favor, execute o arquivo 'FIBROMIALGIA.exe' manualmente para aplicar a atualização.")
                print("Arquivo 'FIBROMIALGIA.exe' baixado. Solicite ao usuário para executá-lo.")
            else:
                raise FileNotFoundError("Erro: Arquivo 'FIBROMIALGIA.exe' não encontrado.")
        except Exception as e:
            print(f"Erro ao aplicar a atualização na função 'apply_update': {e}")

    def Show_Window_Home(self):
        
        self.destroy()
        self.w = ctk.CTk()  
        self.w.minsize(800, 600)
        self.w.geometry("1280x720")
        self.w.title('Bem-vindo ao sistema!')

        # self.service = self.authenticate_google_drive()

        self.Frame_Widgets = ctk.CTkFrame(self.w, width=200, corner_radius=40)
        self.Frame_Widgets.pack(side="left", fill="both", padx=10, pady=10)

        user_fibro = Window_User_Fibro(self.w, self.Frame_Widgets)  # Passa Frame_Widgets
        window_Home = Window_Home(self.w, self.Frame_Widgets)
        window_user_fibro_infor = Window_User_Fibro_Infor(self.w, self.Frame_Widgets)
        window_register_user_fibro = Window_register_User_Fibro(self.w, self.Frame_Widgets)
        window_config = Window_config(self.w, self.Frame_Widgets, "Semus Saude")
        windows_Dashbord = Window_Dashboard(self.w, self.Frame_Widgets)

        icon_size = (60, 60)

        Image_Inicio = Image.open("Image/Inicio.png").resize(icon_size, Image.LANCZOS)
        Image_Adicionar = Image.open("Image/adicionar.png").resize(icon_size, Image.LANCZOS)
        Image_Registro = Image.open("Image/registro.png").resize(icon_size, Image.LANCZOS)
        Image_Imagem = Image.open("Image/carregar.png").resize(icon_size, Image.LANCZOS)
        Image_Criar = Image.open("Image/estatisticas.png").resize(icon_size, Image.LANCZOS)
        Image_Configuracao = Image.open("Image/configuracao.png").resize(icon_size, Image.LANCZOS)
        # image7 = Image.open("sair.png").resize(icon_size, Image.LANCZOS)

        Inicio = ctk.CTkImage(light_image=Image_Inicio, size=icon_size)
        Adicionar = ctk.CTkImage(light_image=Image_Adicionar, size=icon_size)
        Registro = ctk.CTkImage(light_image=Image_Registro, size=icon_size)
        Imagem = ctk.CTkImage(light_image=Image_Imagem, size=icon_size)
        Criar = ctk.CTkImage(light_image=Image_Criar, size=icon_size)
        Configuracao = ctk.CTkImage(light_image=Image_Configuracao, size=icon_size)
        # img7 = ctk.CTkImage(light_image=image7, size=icon_size)

        self.Frame_Widgets.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.Frame_Widgets.grid_columnconfigure(0, weight=1)

        icon_Home = ctk.CTkLabel(master=self.Frame_Widgets, image=Inicio, text="")
        icon_Home.grid(row=1, column=0, pady=10, padx=40, sticky="n")

        icon_Mais = ctk.CTkLabel(master=self.Frame_Widgets, image=Adicionar, text="")
        icon_Mais.grid(row=2, column=0, pady=10, padx=40, sticky="n")

        icon_Registro = ctk.CTkLabel(master=self.Frame_Widgets, image=Registro, text="")
        icon_Registro.grid(row=3, column=0, pady=10, padx=40, sticky="n")

        Icon_Imagem = ctk.CTkLabel(master=self.Frame_Widgets, image=Imagem, text="")
        Icon_Imagem.grid(row=4, column=0, pady=10, padx=40, sticky="n")

        icon_Sicro = ctk.CTkLabel(master=self.Frame_Widgets, image=Criar, text="")
        icon_Sicro.grid(row=5, column=0, pady=10, padx=40, sticky="n")

        icon_Config = ctk.CTkLabel(master=self.Frame_Widgets, image=Configuracao, text="")
        icon_Config.grid(row=6, column=0, pady=10, padx=40, sticky="n")

        # icon_Sair = ctk.CTkLabel(master=self.Frame1, image=img7, text="")
        # icon_Sair.grid(row=7, column=0, pady=10, padx=40, sticky="n")

        self.icon_Mais_clicked = False
        self.icon_Home_Clicked = False

        icon_Mais.bind("<Button-1>", lambda e: window_user_fibro_infor.Show_User_Fibro())
        icon_Home.bind("<Button-1>", lambda e: window_Home.Show_Home())
        icon_Registro.bind("<Button-1>", lambda e: window_register_user_fibro.Show_Register_User_Fibro())
        Icon_Imagem.bind("<Button-1>", lambda e: user_fibro.Show_Image_User_Fibro())
        icon_Config.bind("<Button-1>", lambda e: window_config.Show_Config())
        icon_Sicro.bind("<Button-1>", lambda e: windows_Dashbord.Show_Dashboard())

        window_Home.Show_Home()
        self.w.mainloop()
    
class Window_Home():

    def __init__(self, master, frame_widgets):
        self.w = master
        self.Frame_Widgets = frame_widgets  # Armazena o Frame_Widgets

    def Show_Home(self):

        # Destroi o frame atual, se houver
        for widget in self.w.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.Frame_Widgets:
                widget.destroy()
        
        # Recria o Frame9 (o frame principal)
        self.Frame9 = ctk.CTkFrame(self.w, corner_radius=30)
        self.Frame9.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Aqui você pode adicionar de volta os widgets que estavam no Frame9
        largura_desejada = 1000  # Exemplo de largura
        altura_desejada = 1000   # Exemplo de altura

        img_original = Image.open("Image/fibromialgia.png")
        img_resized = img_original.resize((largura_desejada, altura_desejada))  # Defina o tamanho desejado
        img1 = ImageTk.PhotoImage(img_resized)

        # Criar o label sem texto e com a imagem centralizada
        l1 = ctk.CTkLabel(master=self.Frame9, image=img1, text="")  # Define text="" para remover o nome
        l1.pack(anchor="center")  # Centraliza a imagem

class Window_User_Fibro_Infor():

    def __init__(self, master, frame_widgets):
        self.w = master
        self.Frame_Widgets = frame_widgets  # Armazena o Frame_Widgets
        self.pdf_path = None
        self.pdf_bytes = None
        self.image_bytes = None
        self.nome_pdf = None
        self.nome_imagem = None
        self.nome_carteira = None
        self.nome_carteira = None
        self.font_path = 'Roboto/Roboto-Regular.ttf'  # Certifique-se de que este caminho está correto
        self.font_size = 20
        self.background_base64 = """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oUasa9NVIPRrJ66E1Uipx4M3Er5qiblbvvst73gBdXXVHKD18itN4Qk8I+G41ewPUqKXCqL38o3cSegA3XYXWs7+q0xa3Gtqzcqhu8UB2jB/ZP8AP+D/ADrmzzVnuR7TUlmct1Ejx21i028Rv/s0vjynzHyD8H/iu0Dt/KuLmWod510YxUFuo2klFYRzcy15lxb9fMteZXLHMHetah3nXCHLUO3QZOYO9a15tlxB2yBw86A5g5bg4rhDvwrUO/AhJzB3rW7m/CuEO8o6rUO8iAkGEYxWZtl9nxC38wnu9bFSNc1vNyB7gHP28zRu4+oFet1ltdFYbPQ2K2x9nSW6mipKdm+/LHG0NaN/mAWC3AZgfttnF11Cq4yYMfp/BaUlvQ1M4IJB87Yw4Ef/AFjVnex5J714bpLddbcKguEV83/bB57atbfqKmuz6s+ph3WLPso/6xPU395f6YollLGsWvZR/wBYnqb+8v8ATFEvNnLHsXH6xPTL9+v6YrVlUsVfYuP1iemX79f0xWrKpAFTfFT+oLF/8JOD/wCkVArkVN8VP6gsX/wk4P8A6RUCAuRERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAdRkrSKWnmH+1VDCT6u5VxxM0jKjh91JkPiyQ4ld3scO8f6kk6fMVZuQs57PUf2oDv4CCq24iniTh11KkH7PDruf5nItC8zGcJIy09U0yybXcfbCF9NVNDKmIcsrPP6x6iuqrLDUU0Mr2zMMLGkg/stvNt3L6Kykke9lZRu5KqL4p8jh+1K+kV8d0tNRyjklbG5skZ72O2WehWjXjntMVWnjidJR2yqrZHdlJHvG3fxtxvv/wDkXf2i2y0LXvne0ySbbhvcAP8A8q+LHztVSDzx/wDf/wCa75Zo8MmGlFOKl2kO0p/UxXf3y5D/AEvVqYqHaU/qYrv75ch/perUxVjMEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREBFcx/VFg3935v6Lr1KlFcx/VFg3935v6Lr1KkAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREARY+8U/FXPw8XjAsNsOD0uS5LqHW1VLbYrjfYrNQQtp2xukdNVytc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6KfbpJGf87e5w6FdnZW1ZWEtyesH8u9G7aXbt3uy/KeJh79071YuuOhebaC5hLi2W0nPBLzSW64xMPg9bDv0cwnucOnMw9Wk+Ygmul7ynUhWgpweUzvxkprejwCIiuSAiIgLlREX6FOaEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBZH8PXFtetPZKbEtQJ57rjXSKKoJL6i3joBt5ZIgP2HeB8Xu5Tjgi5e19jWW3LZ2t7Dei/FPmn2P8Aj0KThGaxI9gLTd7XfrbTXmy18FbQ1kYlgqIHh8cjD3EEd6+tebXDxxG33Rm7MtlwdLcMUrJQayi33fTk980G52DvKW9zgNuh2cPRTHshs2V2SiyPHrhFXW64RNnp5499ntPqPUEdxB2IIIIBBX5j6WdEbrotc7s/SpS/LPn3PlJcu3iu7mVaTpPuOxREXkjEEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBY08YujT8msbNS8fpC+5WaLkuEUbCXT0gO4f08se5J6fFJ6+KFkstskbJWOilY17Hgtc1w3BB7wQtuxvKlhcRr0+K+a7UZretK3qKpHsPJE96fOr14ndBZ9M7+/KMdpScXuspMYYN/Apj1MTvMw97D5vF8m5opfXLO7pXtGNek8p/zB66lVjXgpw4MfOiItkyGuyAAjdaIhIREQgLRzGyMdG4bteC0/MVqgQFEXKjdQXCpond8Er49/Psdl8ymGpVrdS3plybHtHWxjcj9u3of5OVQ9cqcdyTia0lh4NVq3zLatQeqoVOZpXKw+fuXAwjuXKwqwPoafWuVpXAw9FytKkk52n+VcrT3LgaVytKIsc7VytK+dq5mlWBztK5mnZfO0/wAq5mlAczT0XK0rgaeuy5WlSWRzt9a5WnyLgaVytI8qgsjnaVytK4GlcrSpJPoaVytK4Gu2XK0+ZWBztO65WnyrgaVytKFkc7SuVhK4GnyrlYdu9SSfQ07rmaV87Dv1XK0qQc7Tt+BcrT0XC0rkaVIOdpXKw7rgaTvsFysOyFkc7SuVpXZYth+U5pXstuL2GsuU7iARBGS1nrc74rR6yQFkZp5wXXCo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"""

    def Show_User_Fibro(self):

        # Destroi o frame atual, se houver
        for widget in self.w.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.Frame_Widgets:
                widget.destroy()      
        
        # Frame Principal onde estão os outros frames
        Frame1 = ctk.CTkFrame(self.w, corner_radius=30)
        Frame1.pack(side="left", fill="both", expand=True, padx=5, pady=5)

         # Frame onde os quatros label e entrys estão principal
        Frame0 = ctk.CTkFrame(Frame1, corner_radius=30, height=50)
        Frame0.pack(side="top", fill="both", padx=10, pady=5)
        
        # Frame onde os quatros label e entrys estão principal
        Frame2 = ctk.CTkFrame(Frame1, corner_radius=30)
        Frame2.pack(expand=True, fill="both", padx=10, pady=5)

        Frame3 = ctk.CTkFrame(Frame2, corner_radius=30)
        Frame3.pack(fill="y", padx=5, pady=5)

        Frame4 = ctk.CTkFrame(Frame2, corner_radius=30)
        Frame4.pack(fill="y", padx=5, pady=5)

        Frame5 = ctk.CTkFrame(Frame3, corner_radius=40, fg_color="transparent") 
        Frame5.pack(side="left", expand=True, padx=10, pady=5)

        Frame6 = ctk.CTkFrame(Frame3, corner_radius=40, fg_color="transparent") 
        Frame6.pack(side="left", expand=True, padx=10, pady=5)

        Buttons_Frame = ctk.CTkFrame(Frame1, corner_radius=20, height=70) #fg_color="transparent"
        Buttons_Frame.pack(side="left", expand=True, fill="x", padx=10, pady=5)  

        # Campos inserir imagem
        self.progress_label = ctk.CTkLabel(Frame4, text="carregamento...", font=('Century Gothic', 20,'bold'))
        self.progress_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(Frame4)
        self.progress_bar.pack(pady=5, padx=40)
        self.progress_bar.set(0)

        self.image_name_label = ctk.CTkLabel(Frame4, text="", font=('Century Gothic', 15,'bold'))
        self.image_name_label.pack(pady=5)
        
        self.pdf = ctk.CTkLabel(Frame4, text="PDF AQUI!", font=('Century Gothic', 15,'bold'))
        self.pdf.pack(pady=5)

        self.Cateirinha_label = ctk.CTkLabel(Frame4, text="CARTEIRINHA AQUI!", font=('Century Gothic', 15,'bold'))
        self.Cateirinha_label.pack(pady=5)

        # Campos de entrada
        self.nome_label = ctk.CTkLabel(Frame6, text="NOME:", font=('Century Gothic', 20,'bold'))
        self.nome_label.pack(pady=5, padx=10)
        self.nome_entry = ctk.CTkEntry(Frame6, width=480, height=50, font=('Century Gothic', 20,'bold'))
        self.nome_entry.pack(pady=5, padx=10)

        cpf_label = ctk.CTkLabel(Frame6, text="CPF:", font=('Century Gothic', 20,'bold'))
        cpf_label.pack(pady=5, padx=10)
        self.cpf_entry = ctk.CTkEntry(Frame6, width=480, height=50, font=('Century Gothic', 20,'bold'))
        self.cpf_entry.pack(pady=5, padx=10)
        self.cpf_entry.bind("<FocusOut>", lambda event: self.format_cpf(event, self.cpf_entry))

        cns_label = ctk.CTkLabel(Frame6, text="CNS:", font=('Century Gothic', 20,'bold'))
        cns_label.pack(pady=5, padx=10)
        self.cns_entry = ctk.CTkEntry(Frame6, width=480, height=50, font=('Century Gothic', 20,'bold'))
        self.cns_entry.pack(pady=5, padx=10)
        self.cns_entry.bind("<FocusOut>", lambda event: self.format_cns(event, self.cns_entry))

        filiacao_label = ctk.CTkLabel(Frame6, text="FILIAÇÃO:", font=('Century Gothic', 20,'bold'))
        filiacao_label.pack(pady=5, padx=10)

        self.filiacao_entry = ctk.CTkTextbox(Frame6, width=480, height=50, font=('Century Gothic', 20,'bold'))  # Usar CTkTextbox
        self.filiacao_entry.pack(pady=5, padx=10)

        # Limitar a duas quebras de linha
        def limit_lines(event):
            lines = self.filiacao_entry.get("1.0", "end-1c").splitlines()
            if len(lines) > 2:
                # Exibir um aviso
                messagebox.showwarning("Limite de Linhas", "Você pode inserir no máximo 2 linhas.")
                # Remover a última linha se o limite for ultrapassado
                self.filiacao_entry.delete("end-1c linestart", "end")  # Remove a última linha

        self.filiacao_entry.bind("<KeyRelease>", limit_lines)  # Vincular a função ao evento de tecla

        faixa_etaria_label = ctk.CTkLabel(Frame6, text="FAIXA ETÁRIA:", font=('Century Gothic', 20,'bold'))
        faixa_etaria_label.pack(pady=5, padx=10)
        # Opções de faixa etária
        faixa_etaria_opcoes = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
        # ComboBox para selecionar a faixa etária
        self.faixa_etaria_combobox = ctk.CTkComboBox(Frame6, values=faixa_etaria_opcoes, width=480, height=50, state="readonly", font=('Century Gothic', 20,'bold'))
        self.faixa_etaria_combobox.pack(pady=5, padx=10)

        self.Estado_Carteira_label = ctk.CTkLabel(Frame6, text="ESTADO DA CARTEIRA:", font=('Century Gothic', 20, 'bold'))
        self.Estado_Carteira_label.pack(pady=5, padx=10)

        # Cria uma ComboBox com as opções
        self.Estado_Carteira_combobox = ctk.CTkComboBox(Frame6, values=["--","ESTÁ PRONTA", "NÃO ESTÁ PRONTA", "ESTÁ ASSINADA", "FOI ENTREGUE"], width=480, height=50, state="readonly", font=('Century Gothic', 20, 'bold'))
        self.Estado_Carteira_combobox.pack(pady=5, padx=10)

        #
        local_data_nascimento_label = ctk.CTkLabel(Frame5, text="LOCAL DE DATA DE NASCIMENTO:", font=('Century Gothic', 20,'bold'))
        local_data_nascimento_label.pack(pady=5, padx=10)
        self.local_data_nascimento_entry = ctk.CTkEntry(Frame5, width=480, height=50, font=('Century Gothic', 20,'bold'))
        self.local_data_nascimento_entry.pack(pady=5, padx=10)
        self.local_data_nascimento_entry.bind("<FocusOut>", lambda event: self.format_location_and_birthdate(event, self.local_data_nascimento_entry))

        tipo_sanguineo_label = ctk.CTkLabel(Frame5, text="TIPO SANGUÍNEO:", font=('Century Gothic', 20,'bold'))
        tipo_sanguineo_label.pack(pady=5, padx=10)
        
        Tipos_Sanguineo = [
            "A", "B", "AB", "O", "--"
        ]
        
         # ComboBox para selecionar o mês, sem poder editar o campo
        self.tipo_sanguineo_entry = ctk.CTkComboBox(Frame5, values=Tipos_Sanguineo, width=480, height=50, state="readonly", font=('Century Gothic', 20,'bold'))
        self.tipo_sanguineo_entry.pack(pady=5, padx=10)
        
        NumeroCadastro_label = ctk.CTkLabel(Frame5, text="NÚMERO DE CADASTRO:", font=('Century Gothic', 20,'bold'))
        NumeroCadastro_label.pack(pady=5, padx=10)
        self.NumeroCadastro_entry = ctk.CTkEntry(Frame5, width=480, height=50, font=('Century Gothic', 20,'bold'))
        self.NumeroCadastro_entry.pack(pady=5, padx=10)
        self.NumeroCadastro_entry.bind("<FocusOut>", lambda event: self.validate_numeric_input(event, self.NumeroCadastro_entry))

        DataEmissão_label = ctk.CTkLabel(Frame5, text="DATA DE EMISSÃO:", font=('Century Gothic', 20,'bold'))
        DataEmissão_label.pack(pady=5, padx=10)
        self.DataEmissão_entry = ctk.CTkEntry(Frame5, width=480, height=50, font=('Century Gothic', 20,'bold'))
        self.DataEmissão_entry.pack(pady=5, padx=10)
        self.DataEmissão_entry.bind("<FocusOut>", lambda event: self.format_date_validade(event, self.DataEmissão_entry))
        
        # ComboBox mes do ano 
        mes_label = ctk.CTkLabel(Frame5, text="MÊS:", font=('Century Gothic', 20,'bold'))
        mes_label.pack(pady=5, padx=10)
        # Lista de meses do ano
        meses_opcoes = [
            "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", 
            "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", 
            "NOVEMBRO", "DEZEMBRO"
        ]
        # ComboBox para selecionar o mês, sem poder editar o campo
        self.mes_combobox = ctk.CTkComboBox(Frame5, values=meses_opcoes, width=480, height=50, state="readonly", font=('Century Gothic', 20,'bold'))
        self.mes_combobox.pack(pady=5, padx=10)
        # Se quiser obter o valor selecionado, use o método get()

        Telefone_label = ctk.CTkLabel(Frame5, text="TELEFONE:", font=('Century Gothic', 20,'bold'))
        Telefone_label.pack(pady=5, padx=10)
        self.Telefone_entry = ctk.CTkEntry(Frame5, width=480, height=50, font=('Century Gothic', 20,'bold'))
        self.Telefone_entry.pack(pady=5, padx=10)
        self.Telefone_entry.bind("<FocusOut>", lambda event: self.validate_phone(event, self.Telefone_entry))


        img2_Cadastrar = ctk.CTkImage(Image.open("Image/cadastrar.png").resize((80, 80), Image.LANCZOS))
        img2_Atualizar = ctk.CTkImage(Image.open("Image/atualizar.png").resize((80, 80), Image.LANCZOS))
        img2_Pessoa = ctk.CTkImage(Image.open("Image/imagem.png").resize((80, 80), Image.LANCZOS))
        img2_pdf = ctk.CTkImage(Image.open("Image/documentacao.png").resize((80, 80), Image.LANCZOS))

        icon_size = (50, 50)
        image2 = Image.open("Image/pesquisar.png").resize(icon_size, Image.LANCZOS)
        img2 = ctk.CTkImage(light_image=image2, size=icon_size)

        Frame0.grid_columnconfigure(0, weight=1)  # Coluna esquerda "espacadora"
        Frame0.grid_columnconfigure(8, weight=1)  # Coluna direita "espacadora"

        btn_cadastrar = ctk.CTkButton(Buttons_Frame,
                                        text="CADASTRAR",
                                        image= img2_Cadastrar,
                                        fg_color="DarkViolet",
                                        corner_radius=10,
                                        hover_color="DarkOrchid",
                                        height=60,
                                        width=150,
                                        font=('Century Gothic', 20,'bold'),
                                        command=self.Insert_User_Fibro)
        btn_cadastrar.grid(row=0, column=1, padx=5, pady=10) 

        btn_Atualizar = ctk.CTkButton(Buttons_Frame,
                                        text="ATUALIZAR",
                                        image= img2_Atualizar,
                                        corner_radius=10,
                                        fg_color="DarkViolet",
                                        hover_color="DarkOrchid",
                                        height=60,
                                        width=150,
                                        font=('Century Gothic', 20,'bold'),
                                        command=self.UpdateInfoFibromialgia)
        btn_Atualizar.grid(row=0, column=2,  padx=5, pady=10)  

        btn_Atualizar = ctk.CTkButton(Buttons_Frame,
                                        text="IMAGEM",
                                        image= img2_Pessoa,
                                        corner_radius=10,
                                        fg_color="DarkViolet",
                                        hover_color="DarkOrchid",
                                        height=60,
                                        width=150,
                                        font=('Century Gothic', 20,'bold'),
                                        command=self.load_image)
        btn_Atualizar.grid(row=0, column=3,  padx=5, pady=10)  

        btn_pdf = ctk.CTkButton(Buttons_Frame,
                                        text="PDF",
                                        image= img2_pdf,
                                        corner_radius=10,
                                        fg_color="DarkViolet",
                                        hover_color="DarkOrchid",
                                        height=60,
                                        width=150,
                                        font=('Century Gothic', 20,'bold'),
                                        command=self.upload_pdf)
        btn_pdf.grid(row=0, column=4,  padx=5, pady=10)
        
        img2_Criar = ctk.CTkImage(Image.open("Image/criarcarteira.png").resize((80, 80), Image.LANCZOS))
        btn_cadastrar = ctk.CTkButton(Buttons_Frame,
                                      text="CRIAR",
                                      fg_color="DarkViolet",
                                      image=img2_Criar,
                                      corner_radius=10,
                                      hover_color="DarkOrchid",
                                      height=60,
                                      width=150,
                                      font=('Century Gothic', 20,'bold'),
                                      command=self.save_image)
        btn_cadastrar.grid(row=0, column=5, padx=5, pady=10)

        icon_Home = ctk.CTkLabel(Frame0, text="", image=img2)
        icon_Home.grid(row=0, column=5, padx=5, pady=10, sticky="n")

        img3_Carteirinha = ctk.CTkImage(Image.open("Image/carteirinha.png").resize((80, 80), Image.LANCZOS))
        btn_carteirinha = ctk.CTkButton(Buttons_Frame,
                                      text="INSERIR CARTEIRA",
                                      fg_color="DarkViolet",
                                      image=img3_Carteirinha,
                                      corner_radius=10,
                                      hover_color="DarkOrchid",
                                      height=60,
                                      width=150,
                                      font=('Century Gothic', 20,'bold'),
                                      command=self.load_image_carteira)
        btn_carteirinha.grid(row=0, column=6, padx=5, pady=10)

        self.Seachpeople=ctk.CTkEntry(Frame0,
                                        width=700,
                                        height=50,
                                        text_color="WHITE",
                                        corner_radius=50,
                                        font=('Century Gothic', 20,'bold')
                                        )
        self.Seachpeople.grid(row=0, column=6, padx=5, pady=5) 
        self.Seachpeople.bind("<KeyRelease>", self.SeachInforFibromailgia)

    def validate_numeric_input(self, event, entry):
        
        # Obtém o texto atual e remove todos os caracteres que não são dígitos
        text = entry.get()
        numeric_text = ''.join(filter(str.isdigit, text))

        # Limita a entrada a dois dígitos
        if len(numeric_text) > 3:
            numeric_text = numeric_text[:3]

        # Formata a entrada para ter dois dígitos
        if numeric_text:
            formatted_text = f"{int(numeric_text):03}"  # Adiciona um zero à esquerda se necessário
        else:
            formatted_text = ""

        # Atualiza o campo de entrada com o texto formatado
        entry.delete(0, tk.END)
        entry.insert(0, formatted_text)

    def format_location_and_birthdate(self, event, entry):
        text = entry.get().strip()

        # Verificar se a vírgula está presente
        if "," not in text:
            messagebox.showerror("Erro de entrada", "Por favor, insira a cidade seguida de uma vírgula e a data de nascimento no formato 'Cidade, DD/MM/AAAA'.")
            entry.delete(0, tk.END)
            return

        # Dividir a entrada em cidade e data
        parts = text.split(',')
        city = parts[0].strip()
        date_text = parts[1].strip() if len(parts) > 1 else ""

        if not date_text:
            messagebox.showerror("Erro de entrada", "Por favor, insira a data de nascimento no formato 'DD/MM/AAAA'.")
            entry.delete(0, tk.END)
            entry.insert(0, city + ", ")
            return

        # Remover barras para simplificar a verificação
        date_text = date_text.replace('/', '')

        if not date_text.isdigit():
            messagebox.showerror("Erro de entrada", "Por favor, insira apenas números na data de nascimento.")
            entry.delete(0, tk.END)
            entry.insert(0, city + ", ")
            return

        # Limitar a entrada a 8 caracteres para DDMMYYYY
        if len(date_text) > 8:
            date_text = date_text[:8]

        day, month, year = date_text[:2], date_text[2:4], date_text[4:8]

        # Ajustar os valores máximos de dia e mês
        if day and int(day) > 31:
            day = '31'
        if month and int(month) > 12:
            month = '12'

        formatted_date = day
        if len(date_text) >= 3:
            formatted_date += '/' + month
        if len(date_text) >= 5:
            formatted_date += '/' + year

        # Construir o novo texto formatado
        new_text = f"{city}, {formatted_date}"

        # Atualizar o campo de entrada
        entry.delete(0, tk.END)
        entry.insert(0, new_text)
    
    def format_cns(self, event, entry):
        
        text = entry.get().replace(' ', '')  # Remover espaços para simplificar a verificação

        if not text.isdigit():
            messagebox.showerror("Erro de entrada", "Por favor, insira apenas números.")
            entry.delete(0, tk.END)
            return

        if len(text) > 15:  # Limitar a entrada a 15 caracteres para o CNS
            text = text[:15]

        part1, part2, part3, part4 = text[:3], text[3:7], text[7:11], text[11:15]
        
        new_text = part1
        if len(text) > 3:
            new_text += ' ' + part2
        if len(text) > 7:
            new_text += ' ' + part3
        if len(text) > 11:
            new_text += ' ' + part4

        entry.delete(0, tk.END)
        entry.insert(0, new_text)

    def format_cpf(self, event, entry):
        
        text = entry.get().replace('.', '').replace('-', '')  # Remover pontos e hífen para simplificar a verificação

        if not text.isdigit():
            messagebox.showerror("Erro de entrada", "Por favor, insira apenas números.")
            entry.delete(0, tk.END)
            return

        if len(text) > 11:  # Limitar a entrada a 11 caracteres para o CPF
            text = text[:11]

        # Formatando o CPF no formato XXX.XXX.XXX-XX
        formatted_text = ""
        if len(text) >= 1:
            formatted_text = text[:3]
        if len(text) >= 4:
            formatted_text += '.' + text[3:6]
        if len(text) >= 7:
            formatted_text += '.' + text[6:9]
        if len(text) >= 10:
            formatted_text += '-' + text[9:11]

        entry.delete(0, tk.END)
        entry.insert(0, formatted_text)

    def format_date_validade(self, event, entry):
        
        text = entry.get().replace('/', '')  # Remover barras para simplificar a verificação

        if not text.isdigit():
            messagebox.showerror("Erro de entrada", "Por favor, insira apenas números.")
            entry.delete(0, tk.END)
            return

        if len(text) > 8:  # Limitar a entrada a 8 caracteres para DDMMYYYY
            text = text[:8]

        day, month, year = text[:2], text[2:4], text[4:8]
        if day:
            if int(day) > 31:
                day = '31'
        if month:
            if int(month) > 12:
                month = '12'

        new_text = day
        if len(text) >= 3:
            new_text += '/' + month
        if len(text) >= 5:
            new_text += '/' + year

        entry.delete(0, tk.END)
        entry.insert(0, new_text)  

    def validate_phone(self, event, Entry):
        phone = Entry.get()
        if not self.is_valid_phone(phone):
            messagebox.showerror("Erro de entrada", "Por favor, insira um número de celular válido.")
            Entry.delete(0, tk.END)
            return
        formatted_phone = self.format_phone(phone)
        Entry.delete(0, tk.END)
        Entry.insert(0, formatted_phone)

    def is_valid_phone(self, phone):
        # Permite dígitos, parênteses, espaço e hífen
        phone_digits = re.sub(r'\D', '', phone)  # Remove caracteres não numéricos
        return len(phone_digits) == 11

    def format_phone(self, phone):
        phone_digits = re.sub(r'\D', '', phone)  # Remove caracteres não numéricos
        if len(phone_digits) != 11:
            return phone  # Retorna o original se não houver 11 dígitos
        return f"({phone_digits[:2]}) {phone_digits[2:7]}-{phone_digits[7:]}"
            
    def upload_pdf(self):

        # Abrir a janela para selecionar o arquivo PDF
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        
        if self.pdf_path:
            with open(self.pdf_path, 'rb') as file:  # Abre o PDF em modo binário
                self.pdf_bytes = file.read()  # Lê todo o conteúdo do PDF
            
            # Atualiza o rótulo com o nome do PDF carregado
            self.pdf.configure(text=f"PDF Carregado: {self.pdf_path.split('/')[-1]}")

    def Insert_User_Fibro(self):
        try:
            # Verifique se todos os campos estão preenchidos
            if not self.nome_entry.get() or not self.cns_entry.get() or not self.filiacao_entry.get("1.0", "end-1c").strip() or \
                not self.faixa_etaria_combobox.get() or not self.Estado_Carteira_combobox.get() or not self.local_data_nascimento_entry.get() or \
                not self.tipo_sanguineo_entry.get() or not self.NumeroCadastro_entry.get() or not self.DataEmissão_entry.get() or not self.mes_combobox.get() or \
                not self.Telefone_entry.get() or not self.pdf_bytes or not hasattr(self, 'image_bytes') or not hasattr(self, 'image_bytes_carteira'):
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
                return

            db = DataBase()
            
            # Verifica se o CPF já existe
            query_check_cpf = "SELECT COUNT(*) FROM Cadastro WHERE cpf = ?"
            cpf = self.cpf_entry.get().strip()
            if db.dql(query_check_cpf, (cpf,))[0][0] > 0:
                messagebox.showerror("Erro", "Já existe um usuário cadastrado com esse CPF.")
                return

            # Verifica se o CNS já existe
            query_check_cns = "SELECT COUNT(*) FROM Cadastro WHERE cns = ?"
            cns = self.cns_entry.get().strip()
            if db.dql(query_check_cns, (cns,))[0][0] > 0:
                messagebox.showerror("Erro", "Já existe um usuário cadastrado com esse CNS.")
                return

            # Verifica se o número de cadastro já existe
            query_check_numero_cadastro = "SELECT COUNT(*) FROM Cadastro WHERE numero_cadastro = ?"
            numero_cadastro = self.NumeroCadastro_entry.get().strip()
            if db.dql(query_check_numero_cadastro, (numero_cadastro,))[0][0] > 0:
                messagebox.showerror("Erro", "Já existe um usuário cadastrado com esse número de cadastro.")
                return

            # Verifica se o nome já existe
            query_check_nome = "SELECT COUNT(*) FROM Cadastro WHERE nome = ?"
            nome = self.nome_entry.get().strip()
            if db.dql(query_check_nome, (nome,))[0][0] > 0:
                messagebox.showerror("Erro", "Já existe um usuário cadastrado com esse nome.")
                return

            # Adiciona os nomes dos arquivos PDF e imagem
            self.nome_pdf = self.pdf_path.split('/')[-1] if hasattr(self, 'pdf_path') else None
            self.nome_imagem = self.image_name_label.cget("text").split(':')[-1].strip() if self.image_name_label else None
            text = self.Cateirinha_label.cget("text") if self.Cateirinha_label else ""
            if ":" in text:
                self.nome_carteira = text.split(":")[1].strip()
            else:
                self.nome_carteira = None

            # Query para inserção dos dados, incluindo as imagens em bytes e os PDFs
            query = '''
            INSERT INTO Cadastro 
            (nascimento, tipo_sanguineo, numero_cadastro, data_emissao, nome, cpf, cns, filiacao, imagem, name_image, faixa_etaria, mes, pdf, name_pdf, name_carteira, carteirinha, telefone, estado_carteira) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''

            # Parâmetros que serão inseridos no banco de dados
            parametros = (
                self.local_data_nascimento_entry.get(),
                self.tipo_sanguineo_entry.get(),
                numero_cadastro,
                self.DataEmissão_entry.get(),
                nome,  # Usando a variável nome
                cpf,   # Usando a variável cpf
                cns,   # Usando a variável cns
                self.filiacao_entry.get("1.0", "end-1c"),
                self.image_bytes,  # Imagem redimensionada em formato de bytes
                self.nome_imagem,  # Nome da imagem
                self.faixa_etaria_combobox.get(),
                self.mes_combobox.get(),
                self.pdf_bytes,  # PDF selecionado em bytes
                self.nome_pdf, 
                self.nome_carteira,
                self.image_bytes_carteira,  # Imagem da carteirinha em bytes
                self.Telefone_entry.get(),
                self.Estado_Carteira_combobox.get()
            )

            # Executar a inserção no banco de dados
            db.dmlWithParament(query, parametros)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto: {e}")
  
    def load_image(self):
        
        file_path = filedialog.askopenfilename(
            filetypes=[("Todos os arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp"), 
                    ("PNG", "*.png"),
                    ("JPEG", "*.jpg;*.jpeg"),
                    ("Todos os arquivos", "*.*")]
        )

        if file_path:
            try:
                # Carregar e abrir a imagem
                image = Image.open(file_path)

                # Redimensionar a imagem
                resized_image = image.resize((235, 315))  # Novo tamanho para a imagem

                # Converter a imagem para bytes para armazenar no banco de dados
                import io
                image_byte_arr = io.BytesIO()
                resized_image.save(image_byte_arr, format='PNG')
                self.image_bytes = image_byte_arr.getvalue()  # Armazena os bytes da imagem na instância

                # Atualizar o rótulo de status com o nome da imagem carregada
                self.image_name_label.configure(text="Imagem carregada: " + file_path.split('/')[-1])

                # Atualizar a barra de progresso (simulado)
                def update_progress(progress):
                    self.progress_bar.set(progress / 100.0)
                    self.w.update_idletasks()
                    if progress < 100:
                        self.w.after(20, update_progress, progress + 1)

                update_progress(0)  # Iniciar a simulação de progresso

            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {e}")
    
    def load_image_carteira(self):
        
        file_path = filedialog.askopenfilename(
            filetypes=[("Todos os arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp"), 
                    ("PNG", "*.png"),
                    ("JPEG", "*.jpg;*.jpeg"),
                    ("Todos os arquivos", "*.*")]
        )

        if file_path:
            try:
                # Carregar e abrir a imagem
                image = Image.open(file_path)

                # Converter a imagem para bytes para armazenar no banco de dados
                import io
                image_byte_arr = io.BytesIO()
                image.save(image_byte_arr, format='PNG')
                self.image_bytes_carteira = image_byte_arr.getvalue()  # Armazena os bytes da imagem na instância

                # Atualizar o rótulo de status com o nome da imagem carregada
                self.Cateirinha_label.configure(text="Imagem carregada: " + file_path.split('/')[-1])

            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {e}")

    def SeachInforFibromailgia(self, event=None):

        try:
            SeachInforFibromialgia = self.Seachpeople.get()

            if not SeachInforFibromialgia:
                # Limpa os campos de entrada se a busca estiver vazia
                self.local_data_nascimento_entry.delete(0, tk.END)
                self.tipo_sanguineo_entry.set("")
                self.NumeroCadastro_entry.delete(0, tk.END)
                self.DataEmissão_entry.delete(0, tk.END)
                self.nome_entry.delete(0, tk.END)
                self.cpf_entry.delete(0, tk.END)
                self.cns_entry.delete(0, tk.END)
                self.filiacao_entry.delete("1.0", "end")
                self.image_name_label.configure(text="IMAGEM:")  # Limpa o nome da imagem
                self.faixa_etaria_combobox.set("")
                self.mes_combobox.set("")  # Para comboboxes
                self.pdf.configure(text="PDF:")  # Limpa o nome do PDF
                self.Cateirinha_label.configure(text="IMAGEM CARTEIRA:")
                self.image_bytes_carteira = None
                self.image_bytes = None  # Limpa a imagem armazenada
                self.Telefone_entry.delete(0, tk.END)
                self.Estado_Carteira_combobox.set("")
                return

            # Consulta SQL para buscar os dados no banco
            query = "SELECT * FROM Cadastro WHERE nome LIKE '"+SeachInforFibromialgia+"%' ORDER BY ID"
            linhas = DataBase().dql(query)

            if not linhas:
                # Caso não haja resultados na consulta
                messagebox.showinfo(title="ERRO", message="Nenhum resultado encontrado para a pesquisa.")
                self.Seachpeople.delete(0, tk.END)  # Limpa o campo de pesquisa
                return

            # Preencha os widgets de entrada com os resultados
            for linha in linhas:
                self.local_data_nascimento_entry.delete(0, tk.END)
                self.local_data_nascimento_entry.insert(0, linha[1])

                self.tipo_sanguineo_entry.set(linha[2])

                self.NumeroCadastro_entry.delete(0, tk.END)
                self.NumeroCadastro_entry.insert(0, linha[3])

                self.DataEmissão_entry.delete(0, tk.END)
                self.DataEmissão_entry.insert(0, linha[4])

                self.nome_entry.delete(0, tk.END)
                self.nome_entry.insert(0, linha[5])

                self.cpf_entry.delete(0, tk.END)
                self.cpf_entry.insert(0, linha[6])

                self.cns_entry.delete(0, tk.END)
                self.cns_entry.insert(0, linha[7])

                self.filiacao_entry.delete("1.0", "end")
                self.filiacao_entry.insert("1.0", linha[8])

                # Exibir o nome da imagem
                self.image_name_label.configure(text=f"Imagem: {linha[10]}")

                self.faixa_etaria_combobox.set(linha[11])

                self.mes_combobox.set(linha[12])

                # Exibir o nome do PDF
                self.pdf.configure(text=f"PDF: {linha[14]}")

                self.Cateirinha_label.configure(text=f"CARTEIRINHA: {linha[15]}")
                self.image_bytes_carteira = linha[16] # Armazena a imagem (em bytes) sem exibir

                # Armazenar a imagem em bytes sem exibir
                self.image_bytes = linha[9]  # Armazena a imagem (em bytes) sem exibir

                self.Telefone_entry.delete(0, tk.END)
                self.Telefone_entry.insert(0, linha[17])

                self.Estado_Carteira_combobox.set(linha[18])

        except Error as e:
            messagebox.showinfo(title="ERRO", message=f"Erro ao buscar informações: {e}")
    
    def UpdateInfoFibromialgia(self):
        try:
            # Verifica se o campo de pesquisa está vazio
            Seach = self.Seachpeople.get()
            if not Seach.strip():
                messagebox.showerror("Erro", "Por favor, pesquise pelo nome antes de atualizar.")
                return  # Cancela a atualização se o campo de pesquisa estiver vazio

            # Consulta os dados atuais do banco de dados
            existing_query = "SELECT * FROM Cadastro WHERE nome LIKE ?"
            existing_data = DataBase().dql(existing_query, ('%' + Seach + '%',))

            if not existing_data:
                messagebox.showerror("Erro", "Usuário não encontrado.")
                return

            # Pega os dados existentes
            existing_row = existing_data[0]
            record_id = existing_row[0]  # ID do registro atual

            # Verifica se algum dos campos restritos (CPF, CNS, número de cadastro, nome) já existe em outro registro
            query_check_conflict = """
                SELECT id FROM Cadastro
                WHERE (cpf = ? OR cns = ? OR numero_cadastro = ? OR nome = ?)
                AND id != ?
            """
            conflict_data = DataBase().dql(query_check_conflict, (
                self.cpf_entry.get().strip(),
                self.cns_entry.get().strip(),
                self.NumeroCadastro_entry.get().strip(),
                self.nome_entry.get().strip(),
                record_id
            ))

            # Se houver conflito com outro registro, exibe a mensagem de erro
            if conflict_data:
                messagebox.showerror("Erro", "CPF, CNS, número de cadastro ou nome já existem em outro registro.")
                return

            # Atualiza os dados no banco
            vquery = """
                UPDATE Cadastro
                SET nascimento=?, tipo_sanguineo=?, numero_cadastro=?, data_emissao=?, nome=?, 
                    cpf=?, cns=?, filiacao=?, imagem=?, name_image=?, faixa_etaria=?, mes=?, pdf=?, 
                    name_pdf=?, name_carteira=?, carteirinha=?, telefone=?, estado_carteira=?
                WHERE id=?  
            """
            parament = (
                self.local_data_nascimento_entry.get().strip(),
                self.tipo_sanguineo_entry.get().strip(),
                self.NumeroCadastro_entry.get().strip(),
                self.DataEmissão_entry.get().strip(),
                self.nome_entry.get().strip(),
                self.cpf_entry.get().strip(),
                self.cns_entry.get().strip(),
                self.filiacao_entry.get("1.0", "end-1c").strip(),
                self.image_bytes if hasattr(self, 'image_bytes') and self.image_bytes else existing_row[9],
                self.nome_imagem if self.nome_imagem else existing_row[10],
                self.faixa_etaria_combobox.get().strip(),
                self.mes_combobox.get().strip(),
                self.pdf_bytes if hasattr(self, 'pdf_bytes') and self.pdf_bytes else existing_row[13],
                self.nome_pdf if self.nome_pdf else existing_row[14],
                self.nome_carteira,
                self.image_bytes_carteira if hasattr(self, 'image_bytes_carteira') and self.image_bytes_carteira else existing_row[15],
                self.Telefone_entry.get().strip(),
                self.Estado_Carteira_combobox.get().strip(),
                record_id
            )

            DataBase().dmlWithParament(vquery, parament)
            messagebox.showinfo("Sucesso", "Informações atualizadas com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar informações: {e}")
    
    def base64_to_image(self, base64_string):
        image_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(image_data))

    def add_text_to_image(self, background_base64, output_path, text_dict, font_path, font_size):
        # Converte a imagem de fundo base64 para imagem PIL
        background_image = self.base64_to_image(background_base64)
        image = background_image.copy()
        draw = ImageDraw.Draw(image)

        # Configura a fonte
        font = ImageFont.truetype(font_path, font_size)

        # Define as posições para cada campo
        positions = {
            "nome": (292, 170),
            "cpf": (292, 230),
            "cns": (568, 230),
            "filiacao": (292, 300),
            "local_data_nascimento": (292, 385),
            "tipo_sanguineo": (628, 435),
            "NumeroCadastro": (628, 110),
            "DataEmissão": (1228, 45)
        }

        # Adiciona o texto à imagem
        for key, text in text_dict.items():
            position = positions[key]
            draw.text(position, text, font=font, fill="black")

        # Adiciona a imagem da pessoa se estiver armazenada em self.image_bytes
        if self.image_bytes:
            person_image = Image.open(io.BytesIO(self.image_bytes))  # Carrega a imagem de bytes
            person_image = person_image.resize((235, 315))  # Tamanho da foto 3x4 em pixels
            image.paste(person_image, (25, 130))

        # Salva a imagem modificada
        image.save(output_path)

    def save_image(self):
        # Cria o dicionário com os valores dos campos
        text_dict = {
            "nome": self.nome_entry.get(),
            "cpf": self.cpf_entry.get(),
            "cns": self.cns_entry.get(),
            "filiacao": self.filiacao_entry.get("1.0", "end").strip(),  # remove espaços em branco extras
            "local_data_nascimento": self.local_data_nascimento_entry.get(),
            "tipo_sanguineo": self.tipo_sanguineo_entry.get(),
            "NumeroCadastro": self.NumeroCadastro_entry.get(),
            "DataEmissão": self.DataEmissão_entry.get()
        }

        # Validação: Verificar se algum campo obrigatório está vazio
        missing_fields = [key for key, value in text_dict.items() if not value.strip()]  # Lista os campos vazios

        if missing_fields:
            messagebox.showerror("Erro", f"Os seguintes campos estão vazios: {', '.join(missing_fields)}")
            return  # Sai da função sem gerar a imagem

        # Confirmação de que as informações estão corretas
        confirmar = messagebox.askyesno("Confirmação", "Tem certeza de que todas as informações estão corretas?")
        
        if confirmar:
            # Mensagem de responsabilidade
            responsabilidade = messagebox.askyesno("Responsabilidade", 
                "As informações preenchidas são de total responsabilidade sua. Deseja continuar?")
            
            if responsabilidade:
                # Se todos os campos estiverem preenchidos e as confirmações forem feitas, procede com a geração da carteirinha
                output_path = filedialog.asksaveasfilename(defaultextension=".jpeg", 
                    filetypes=[("Todos os arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), 
                            ("PNG", "*.png"),
                            ("JPEG", "*.jpg;*.jpeg")])

                if output_path:
                    try:
                        # Chamar a função para adicionar texto à imagem
                        self.add_text_to_image(self.background_base64, output_path, text_dict, self.font_path, self.font_size)
                        messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")
                        
                        # Após salvar a imagem, pode chamar a função de cadastro de usuário
                        
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao salvar a imagem: {e}")
            else:
                messagebox.showinfo("Cancelado", "A criação da carteirinha foi cancelada.")
        else:
            messagebox.showinfo("Cancelado", "A criação da carteirinha foi cancelada.")

class Window_register_User_Fibro():

    def __init__(self, master, frame_widgets):
        self.w = master
        self.Frame_Widgets = frame_widgets

    def Show_Register_User_Fibro(self):
        # Destrói o frame atual, se houver
        for widget in self.w.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.Frame_Widgets:
                widget.destroy()

        # Frame principal onde estão os outros frames
        Frame1 = ctk.CTkFrame(self.w, corner_radius=30)
        Frame1.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        Frame2 = ctk.CTkFrame(Frame1, corner_radius=20, height=50)
        Frame2.pack(side="top", fill="both", padx=15, pady=15)

        # Configuração do Treeview sem colunas de imagens
        self.tv = ttk.Treeview(Frame1, columns=(
            'ID', 'NASCIMENTO', 'TIPO SANGUÍNEO', 'NÚMERO DE CADASTRO',
            'DATA DE EMISSÃO', 'NOME', 'CPF', 'CNS', 'FILIAÇÃO', 'IMAGEM',
            'FAIXA ETÁRIA', 'MÊS', 'PDF', 'CARTEIRA', 'TELEFONE', 'ESTADO CARTEIRA'),
            show='headings'
        )

        # Configuração das colunas
        self.tv.column('ID', minwidth=0, width=5)
        self.tv.column('NASCIMENTO', minwidth=0, width=25)
        self.tv.column('TIPO SANGUÍNEO', minwidth=0, width=30)
        self.tv.column('NÚMERO DE CADASTRO', minwidth=0, width=20)
        self.tv.column('DATA DE EMISSÃO', minwidth=0, width=20)
        self.tv.column('NOME', minwidth=0, width=10)
        self.tv.column('CPF', minwidth=0, width=10)
        self.tv.column('CNS', minwidth=0, width=10)
        self.tv.column('FILIAÇÃO', minwidth=0, width=15)
        self.tv.column('IMAGEM', minwidth=0, width=15)
        self.tv.column('FAIXA ETÁRIA', minwidth=0, width=5)
        self.tv.column('MÊS', minwidth=0, width=15)
        self.tv.column('PDF', minwidth=0, width=20)
        self.tv.column('CARTEIRA', minwidth=0, width=10)
        self.tv.column('TELEFONE', minwidth=0, width=10)
        self.tv.column('ESTADO CARTEIRA', minwidth=0, width=15)

        # Cabeçalhos do Treeview
        self.tv.heading('ID', text='ID')
        self.tv.heading('NASCIMENTO', text='NASCIMENTO')
        self.tv.heading('TIPO SANGUÍNEO', text='TIPO SANGUÍNEO')
        self.tv.heading('NÚMERO DE CADASTRO', text='NÚMERO DE CADASTRO')
        self.tv.heading('DATA DE EMISSÃO', text='DATA DE EMISSÃO')
        self.tv.heading('NOME', text='NOME')
        self.tv.heading('CPF', text='CPF')
        self.tv.heading('CNS', text='CNS')
        self.tv.heading('FILIAÇÃO', text='FILIAÇÃO')
        self.tv.heading('IMAGEM', text='IMAGEM')
        self.tv.heading('FAIXA ETÁRIA', text='FAIXA ETÁRIA')
        self.tv.heading('MÊS', text='MÊS')
        self.tv.heading('PDF', text='PDF')
        self.tv.heading('CARTEIRA', text='CARTEIRA')
        self.tv.heading('TELEFONE', text='TELEFONE')
        self.tv.heading('ESTADO CARTEIRA', text='ESTADO CARTEIRA')

        self.LoadFibromialgia()

        self.tv.pack(side="top", fill="both", expand=True, pady=10, padx=20)

        Frame3 = ctk.CTkFrame(Frame1, corner_radius=20, height=70)
        Frame3.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        icon_size = (50, 50)
        image2 = Image.open("Image/pesquisar.png").resize(icon_size, Image.LANCZOS)
        img2 = ctk.CTkImage(light_image=image2, size=icon_size)

        img2_Delete = ctk.CTkImage(Image.open("Image/deletar.png").resize((80, 80), Image.LANCZOS))
        im3_Download_pdf = ctk.CTkImage(Image.open("Image/downloadpdf.png").resize((80,80), Image.LANCZOS))
        im4_Download_image = ctk.CTkImage(Image.open("Image/baixarimagem.png").resize((80,80), Image.LANCZOS))

        Frame2.grid_columnconfigure(0, weight=1)  # Coluna esquerda "espacadora"
        Frame2.grid_columnconfigure(8, weight=1)  # Coluna direita "espacadora"

        btn_cadastrar = ctk.CTkButton(Frame3,
                                    text="DELETAR",
                                    fg_color="DarkViolet",
                                    image=img2_Delete,
                                    corner_radius=10,
                                    hover_color="DarkOrchid",
                                    height=60,
                                    width=150,
                                    font=('Century Gothic', 20, 'bold'),
                                    command=self.deletInfoDFibromialgia)
        btn_cadastrar.grid(row=0, column=1, padx=5, pady=10)

        btn_Dowload_pdf = ctk.CTkButton(Frame3,
                                    text="DOWNLOAD PDF",
                                    fg_color="DarkViolet",
                                    image=im3_Download_pdf,
                                    corner_radius=10,
                                    hover_color="DarkOrchid",
                                    height=60,
                                    width=150,
                                    font=('Century Gothic', 20, 'bold'),
                                    command=self.Dowloadpdf)
        btn_Dowload_pdf.grid(row=0, column=2, padx=5, pady=10)

        btn_Dowload_image = ctk.CTkButton(Frame3,
                                    text="DOWNLOAD IMAGE",
                                    fg_color="DarkViolet",
                                    image=im4_Download_image,
                                    corner_radius=10,
                                    hover_color="DarkOrchid",
                                    height=60,
                                    width=150,
                                    font=('Century Gothic', 20, 'bold'),
                                    command=self.DownloadImage)
        btn_Dowload_image.grid(row=0, column=3, padx=5, pady=10)

        btn_Dowload_image = ctk.CTkButton(Frame3,
                                    text="DOWNLOAD CARTEIRA",
                                    fg_color="DarkViolet",
                                    image=im4_Download_image,
                                    corner_radius=10,
                                    hover_color="DarkOrchid",
                                    height=60,
                                    width=150,
                                    font=('Century Gothic', 20, 'bold'),
                                    command=self.DownloadWallet)
        btn_Dowload_image.grid(row=0, column=4, padx=5, pady=10)

        icon_Search = ctk.CTkLabel(Frame2, text="", image=img2)
        icon_Search.grid(row=0, column=5, pady=10, padx=5, sticky="n")

        self.Seachpeople = ctk.CTkEntry(Frame2,
                                        width=700,
                                        height=50,
                                        text_color="WHITE",
                                        corner_radius=50,
                                        font=('Century Gothic', 20, 'bold'))
        self.Seachpeople.grid(row=0, column=6, padx=5, pady=10)
        self.Seachpeople.bind("<KeyRelease>", self.SeachInforUserFibro)

    # def criar_imagem(self):

    #     selected_item = self.tv.selection()
    #     if selected_item:
    #         values = self.tv.item(selected_item)['values']
    #         text_dict = {
    #             "nome": values[5],
    #             "cpf": values[6],
    #             "cns": values[7],
    #             "filiacao": values[8],
    #             "local_data_nascimento": values[1],
    #             "tipo_sanguineo": values[2],
    #             "NumeroCadastro": values[3],
    #             "DataEmissão": values[4]
    #         }

    #         # Supondo que o caminho da imagem esteja na coluna 9 (ou altere conforme necessário)
    #         image_path = values[9]  

    #         output_path = filedialog.asksaveasfilename(defaultextension=".jpeg", 
    #                                        filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")],
    #                                        initialfile="imagem_salva.jpeg")
    #         if output_path:
    #             try:
    #                 self.add_text_to_image(self.background_base64, output_path, text_dict, self.font_path, self.font_size, image_path)
    #                 messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")
    #             except Exception as e:
    #                 messagebox.showerror("Erro", f"Erro ao salvar a imagem: {e}")
    #     else:
    #         messagebox.showwarning("Atenção", "Selecione um usuário no no campo acima.")

    def base64_to_image(self, base64_string):
        image_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(image_data))

    def add_text_to_image(self, background_base64, output_path, text_dict, font_path, font_size, image_path):
        background_image = self.base64_to_image(background_base64)
        image = background_image.copy()
        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype(font_path, font_size)

        positions = {
            "nome": (292, 170),
            "cpf": (292, 230),
            "cns": (568, 230),
            "filiacao": (292, 300),
            "local_data_nascimento": (292, 385),
            "tipo_sanguineo": (628, 435),
            "NumeroCadastro": (628, 110),
            "DataEmissão": (1228, 45)
        }

        for key, text in text_dict.items():
            position = positions.get(key)
            if position and isinstance(position, tuple):  # Garante que position seja uma tupla
                draw.text(position, str(text), font=font, fill="black")  # Converte texto para string
        
        if image_path:
            overlay_image = Image.open(image_path)
            image.paste(overlay_image, (25, 130), overlay_image)

        image.save(output_path)

    def LoadFibromialgia(self):

        self.tv.delete(*self.tv.get_children())  # Limpa o Treeview
        
        # Seleciona apenas as colunas que correspondem ao Treeview atualizado
        vquery = """
            SELECT id, nascimento, tipo_sanguineo, numero_cadastro, data_emissao, nome, cpf, cns, filiacao, 
                name_image, faixa_etaria, mes, name_pdf, name_carteira, telefone, estado_carteira
            FROM Cadastro ORDER BY id
        """
        
        linhas = DataBase().dql(vquery)
        for i in linhas:
            self.tv.insert("", "end", values=i)

    def deletInfoDFibromialgia(self):
         
        try:
            # Verifica se há um item selecionado no Treeview
            itemSelecionado = self.tv.selection()[0]
            valores = self.tv.item(itemSelecionado, "values")
            vid = valores[0]

            # Exibe uma mensagem de confirmação
            confirmacao = messagebox.askyesno("Confirmação", f"Você realmente deseja deletar o usuário {vid}?")

            # Se o usuário confirmar (clicar em Sim), executa a exclusão
            if confirmacao:
                vquery = "DELETE FROM Cadastro WHERE ID=" + vid
                DataBase().dml(vquery)
                self.tv.delete(itemSelecionado)  # Remove o item da interface
                messagebox.showinfo(title="Sucesso", message="Usuário deletado com sucesso")
            
            else:
                # Se o usuário clicar em Não, cancela a exclusão
                messagebox.showinfo(title="Cancelado", message="A exclusão foi cancelada")

        except IndexError:
            messagebox.showinfo(title="Erro", message="Nenhum item selecionado para deletar")
        except Exception as e:
            messagebox.showinfo(title="Erro", message=f"Erro ao deletar: {e}")

        # Atualiza a lista de usuários
        self.LoadFibromialgia()
    
    def SeachInforUserFibro(self, event=None):
        try:
            # Limpa a Treeview
            self.tv.delete(*self.tv.get_children())

            # Consulta SQL (escolha as colunas explicitamente)
            vquery = """
                SELECT id, nascimento, tipo_sanguineo, numero_cadastro, data_emissao, nome, cpf, cns, filiacao, 
                    name_image, faixa_etaria, mes, name_pdf, name_carteira, telefone, estado_carteira
                FROM Cadastro WHERE nome LIKE ? ORDER BY id
            """
            
            # Faz a consulta usando um parâmetro para evitar injeção SQL
            nome_pesquisa = self.Seachpeople.get().strip() + '%'
            linhas = DataBase().dql(vquery, (nome_pesquisa,))

            # Verifica se o resultado está vazio
            if not linhas:
                messagebox.showinfo(title="ERRO", message="Nenhum resultado encontrado para a pesquisa.")
                self.Seachpeople.delete(0, tk.END)  # Limpa o campo de pesquisa
                self.LoadFibromialgia()
                return

            # Preenche a Treeview com os resultados
            for i in linhas:
                self.tv.insert("", "end", values=i)
        
        except Exception as e:
            messagebox.showinfo(title="ERRO", message=f"Ocorreu um erro: {e}")
    
    def DownloadImage(self):

        try:
            # Verifica se há um item selecionado no Treeview
            itens_selecionados = self.tv.selection()
            if not itens_selecionados:
                messagebox.showinfo(title="Erro", message="Nenhum item selecionado para baixar a imagem.")
                return

            itemSelecionado = itens_selecionados[0]
            valores = self.tv.item(itemSelecionado, "values")
            nome_pessoa = valores[5]  # Ajuste de acordo com a coluna correta do nome da pessoa
            id_pessoa = valores[0]    # Ajuste de acordo com a coluna correta do ID da pessoa

            # Buscar imagem binária do banco de dados usando o ID da pessoa
            query = f"SELECT imagem FROM Cadastro WHERE id={id_pessoa}"
            resultado = DataBase().dql(query)

            if not resultado or not resultado[0][0]:
                messagebox.showerror(title="Erro", message=f"Imagem não encontrada para o usuário {nome_pessoa}")
                return

            imagem_binaria = resultado[0][0]  # Primeiro resultado, primeira coluna (a imagem em binário)

            # Exibe uma mensagem de confirmação
            confirmacao = messagebox.askyesno("Confirmação", f"Deseja baixar a imagem da pessoa: {nome_pessoa}?")

            if confirmacao:
                # Abrir uma janela para escolher o diretório onde salvar a imagem
                diretorio = filedialog.askdirectory()

                if diretorio:
                    # Define o caminho de destino
                    caminho_destino = os.path.join(diretorio, f"{nome_pessoa}_imagem.png")

                    # Salva a imagem binária como um arquivo de imagem
                    with open(caminho_destino, 'wb') as file:
                        file.write(imagem_binaria)

                    messagebox.showinfo(title="Sucesso", message="Imagem baixada com sucesso")
                else:
                    messagebox.showinfo(title="Cancelado", message="Nenhum diretório foi selecionado. Baixamento cancelado.")

            else:
                messagebox.showinfo(title="Cancelado", message=f"Imagem do usuário {nome_pessoa} não baixada.")

        except IndexError:
            messagebox.showinfo(title="Erro", message="Erro ao acessar os valores do item selecionado.")
        except Exception as e:
            messagebox.showinfo(title="Erro", message=f"Erro ao baixar a imagem: {e}")
    
    def Dowloadpdf(self):
        
        try:
            # Verifica se há um item selecionado no Treeview
            itens_selecionados = self.tv.selection()
            if not itens_selecionados:
                messagebox.showinfo(title="Erro", message="Nenhum item selecionado para baixar o PDF.")
                return

            itemSelecionado = itens_selecionados[0]
            valores = self.tv.item(itemSelecionado, "values")
            nome_pessoa = valores[5]  # Ajuste de acordo com a coluna correta do nome da pessoa
            id_pessoa = valores[0]    # Ajuste de acordo com a coluna correta do ID da pessoa

            # Buscar PDF binário do banco de dados usando o ID da pessoa
            query = f"SELECT pdf FROM Cadastro WHERE id={id_pessoa}"
            resultado = DataBase().dql(query)

            if not resultado or not resultado[0][0]:
                messagebox.showerror(title="Erro", message=f"PDF não encontrado para o usuário {nome_pessoa}")
                return

            pdf_binario = resultado[0][0]  # Primeiro resultado, primeira coluna (o PDF em binário)

            # Exibe uma mensagem de confirmação
            confirmacao = messagebox.askyesno("Confirmação", f"Deseja baixar o PDF da pessoa: {nome_pessoa}?")

            if confirmacao:
                # Abrir uma janela para escolher o diretório onde salvar o PDF
                diretorio = filedialog.askdirectory()

                if diretorio:
                    # Define o caminho de destino
                    caminho_destino = os.path.join(diretorio, f"{nome_pessoa}_documento.pdf")

                    # Salva o PDF binário como um arquivo PDF
                    with open(caminho_destino, 'wb') as file:
                        file.write(pdf_binario)

                    messagebox.showinfo(title="Sucesso", message="PDF baixado com sucesso")
                else:
                    messagebox.showinfo(title="Cancelado", message="Nenhum diretório foi selecionado. Baixamento cancelado.")

            else:
                messagebox.showinfo(title="Cancelado", message=f"PDF do usuário {nome_pessoa} não baixado.")

        except IndexError:
            messagebox.showinfo(title="Erro", message="Erro ao acessar os valores do item selecionado.")
        except Exception as e:
            messagebox.showinfo(title="Erro", message=f"Erro ao baixar o PDF: {e}")
    
    def DownloadWallet(self):

        try:
            # Verifica se há um item selecionado no Treeview
            itens_selecionados = self.tv.selection()
            if not itens_selecionados:
                messagebox.showinfo(title="Erro", message="Nenhum item selecionado para baixar a carteira.")
                return

            itemSelecionado = itens_selecionados[0]
            valores = self.tv.item(itemSelecionado, "values")
            nome_pessoa = valores[5]  # Ajuste de acordo com a coluna correta do nome da pessoa
            id_pessoa = valores[0]    # Ajuste de acordo com a coluna correta do ID da pessoa

            # Buscar imagem binária do banco de dados usando o ID da pessoa
            query = f"SELECT carteirinha FROM Cadastro WHERE id={id_pessoa}"
            resultado = DataBase().dql(query)

            if not resultado or not resultado[0][0]:
                messagebox.showerror(title="Erro", message=f"Carteira não encontrada para o usuário {nome_pessoa}")
                return

            imagem_binaria = resultado[0][0]  # Primeiro resultado, primeira coluna (a imagem em binário)

            # Exibe uma mensagem de confirmação
            confirmacao = messagebox.askyesno("Confirmação", f"Deseja baixar a carteira da pessoa: {nome_pessoa}?")

            if confirmacao:
                # Abrir uma janela para escolher o diretório onde salvar a imagem
                diretorio = filedialog.askdirectory()

                if diretorio:
                    # Define o caminho de destino
                    caminho_destino = os.path.join(diretorio, f"{nome_pessoa}_imagem.png")

                    # Salva a imagem binária como um arquivo de imagem
                    with open(caminho_destino, 'wb') as file:
                        file.write(imagem_binaria)

                    messagebox.showinfo(title="Sucesso", message="Carteira baixada com sucesso")
                else:
                    messagebox.showinfo(title="Cancelado", message="Nenhum diretório foi selecionado. Baixamento cancelado.")

            else:
                messagebox.showinfo(title="Cancelado", message=f"Carteira do usuário {nome_pessoa} não baixada.")

        except IndexError:
            messagebox.showinfo(title="Erro", message="Erro ao acessar os valores do item selecionado.")
        except Exception as e:
            messagebox.showinfo(title="Erro", message=f"Erro ao baixar a carteira: {e}")
        
class Window_Dashboard():

    def __init__(self, master, frame_widgets):
        self.w = master
        self.Frame_Widgets = frame_widgets  # Armazena o Frame_Widgets

    def Show_Dashboard(self):

        try:
            # Limpa os widgets antigos
            for widget in self.w.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget != self.Frame_Widgets:
                    widget.destroy()

            Frame_Dashboard = ctk.CTkFrame(self.w, corner_radius=30)
            Frame_Dashboard.pack(fill="both", expand=True, padx=10, pady=10)

            # Obter os dados do banco de dados para faixa etária
            query_age_groups = "SELECT faixa_etaria, COUNT(*) FROM Cadastro GROUP BY faixa_etaria"
            resultados_age_groups = DataBase().dql(query_age_groups)

            age_groups = [resultado[0] for resultado in resultados_age_groups]
            counts_age = [resultado[1] for resultado in resultados_age_groups]

            # Criar o DataFrame para faixa etária
            df_age = pd.DataFrame({'Faixa Etária': age_groups, 'Quantidade': counts_age})

            # Obter os dados do banco de dados para carteirinhas feitas por mês
            query_months = "SELECT mes, COUNT(*) FROM Cadastro GROUP BY mes"
            resultados_months = DataBase().dql(query_months)

            months = [resultado[0] for resultado in resultados_months]
            counts_month = [resultado[1] for resultado in resultados_months]

            # Criar o DataFrame para carteirinhas feitas por mês
            df_month = pd.DataFrame({'Mês': months, 'Quantidade': counts_month})

            # Definir o tema escuro do seaborn
            sns.set_theme(style="darkgrid")

            # Criação do gráfico com tamanho ajustado
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

            # Gráfico de barras: quantidade de pessoas por faixa etária
            sns.barplot(x='Faixa Etária', y='Quantidade', data=df_age, ax=ax1, palette='viridis')
            ax1.set_title('Quantidade de Pessoas com Fibromialgia por Faixa Etária', color='white')
            ax1.set_xlabel('Faixa Etária', color='white')
            ax1.set_ylabel('Quantidade de Pessoas', color='white')
            ax1.tick_params(axis='x', colors='white')
            ax1.tick_params(axis='y', colors='white')
            ax1.set_facecolor('#2e2e2e')

            # Gráfico de linha: quantidade de carteirinhas feitas por mês
            sns.lineplot(x='Mês', y='Quantidade', data=df_month, marker='o', color='cyan', ax=ax2)
            ax2.set_title('Quantidade de Carteirinhas Feitas por Mês', color='white')
            ax2.set_xlabel('Mês', color='white')
            ax2.set_ylabel('Quantidade de Carteirinhas', color='white')
            ax2.tick_params(axis='x', colors='white')
            ax2.tick_params(axis='y', colors='white')
            ax2.set_facecolor('#2e2e2e')

            # Configurar o fundo da figura
            fig.patch.set_facecolor('#1e1e1e')

            # Criação do canvas do Tkinter para colocar o gráfico
            canvas = FigureCanvasTkAgg(fig, master=Frame_Dashboard)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

            # Adicionar a barra de ferramentas
            toolbar = NavigationToolbar2Tk(canvas, Frame_Dashboard)
            toolbar.update()
            toolbar.pack(side='bottom', fill='x')

            # Ajustar layout
            plt.tight_layout()

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

class Window_config():

    def __init__(self, master, frame_widgets, user_name):
        self.w = master
        self.Frame_Widgets = frame_widgets  # Armazena o Frame_Widgets
        self.user_name = user_name
        
    # def retrieve_user_info(self, user_name):
        
    #     """Recupera o nome e e-mail do usuário do banco de dados pelo nome."""
    #     try:
    #         query = "SELECT nome_email, email FROM login WHERE nome_email = ?"
    #         db = DataBase()
    #         # Busca o usuário com o nome fornecido
    #         user_data = db.dql(query, (user_name,))
    #         print(f"Dados do usuário retornados do banco de dados: {user_data}")  # Adicionado para verificar o que está sendo retornado

    #         if user_data:
    #             # Seleciona o primeiro resultado retornado
    #             name, email = user_data[0]
    #             return name, email
    #         else:
    #             print("Nenhum dado encontrado para o nome fornecido.")
    #             return None, None
    #     except Exception as e:
    #         print(f"Erro ao recuperar informações do banco de dados: {e}")
    #         return None, None

    def Show_Config(self):
        
        # Destroi o frame atual, se houver
        for widget in self.w.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.Frame_Widgets:
                widget.destroy()  

        # Frame principal
        Frame_Config1 = ctk.CTkFrame(self.w, corner_radius=30)
        Frame_Config1.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas dentro do Frame_Config1
        canvas = ctk.CTkCanvas(Frame_Config1, bg="#2B2B2B", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

        # Scrollbar dentro do Frame_Config1, alinhada à direita do canvas
        scrollbar = ctk.CTkScrollbar(Frame_Config1, orientation="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        # Configura o canvas para usar a scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        # Frame que será rolado, dentro do canvas
        Frame_Content = ctk.CTkFrame(canvas, corner_radius=30)
        window_id = canvas.create_window((0, 0), window=Frame_Content, anchor="nw")

        # Ajusta a largura do Frame_Content ao Canvas
        Frame_Content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))

        # Função para rolar o conteúdo com o botão de rolagem do mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Vincula o evento de rolagem do mouse ao canvas
        canvas.bind_all("<MouseWheel>", on_mousewheel)  # Para Windows
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Para Linux
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Para Linux

        # Adiciona os frames de configurações dentro do Frame_Content
        Frame_Config2 = ctk.CTkFrame(Frame_Content, corner_radius=30, height=400)
        Frame_Config2.pack(fill="both", expand=True, padx=10, pady=10)

        Frame_Config3 = ctk.CTkFrame(Frame_Content, corner_radius=30, height=400)
        Frame_Config3.pack(fill="both", expand=True, padx=10, pady=10)

        Frame_Config4 = ctk.CTkFrame(Frame_Content, corner_radius=30, height=400)
        Frame_Config4.pack(fill="both", expand=True, padx=10, pady=10)

        Frame_Config5 = ctk.CTkFrame(Frame_Content, corner_radius=30, height=400)
        Frame_Config5.pack(fill="both", expand=True, padx=10, pady=10)

        # Aqui onde ficará a parte da conta do usuário_______________________________________________________________________________________

        # Frame onde está o bottão de logout
        Frame_Config_Name2 = ctk.CTkFrame(Frame_Config2, corner_radius=20, fg_color="RED")  
        Frame_Config_Name2.pack(side="top", fill="x", padx=10, pady=10) 
        
        # Frame onde está o botão de criar usuário local
        Frame_Config_Name3 = ctk.CTkFrame(Frame_Config2, corner_radius=20)  
        Frame_Config_Name3.pack(side="top", fill="x", padx=10, pady=10) 

       
        
        # user_name, user_email = self.retrieve_user_info(self.user_name)

        # # Atualiza os labels com as informações do usuário
        # if user_name and user_email:
        #     # Label para o nome da pessoa
        #     Name_Conta_Google = ctk.CTkLabel(Frame_Config_Name1_texts, text=user_name, font=("Arial", 25, "bold"))
        #     Name_Conta_Google.pack(padx=50, pady=5)  # Adiciona um pequeno espaçamento inferior

        #     # Label para a descrição da conta do Google
        #     Name_conta_da_Google = ctk.CTkLabel(Frame_Config_Name1_texts, text=user_email, font=("Arial", 10, "bold"))
        #     Name_conta_da_Google.pack(padx=50)
        # else:
        #     print("Não foi possível exibir as informações do usuário.")

        # img1_Logout = ctk.CTkImage(Image.open("Image/Google.webp").resize((20, 20), Image.LANCZOS))

        Icon_Logout = Image.open("Image/Google.webp").resize((80, 80), Image.LANCZOS)  # Carrega e redimensiona a imagem
        icon_size = (50, 50)
        # Cria o CTkImage com a imagem PIL diretamente
        icon_Logout = ctk.CTkImage(light_image=Icon_Logout, size=icon_size)
        # Exibe a imagem no Label
        icon_Logout_label = ctk.CTkLabel(Frame_Config_Name2, image=icon_Logout, text="")
        icon_Logout_label.pack(side="left", padx=10, pady=10)

        User_local = Change_Password_Window(self, self.Frame_Widgets)
        
        # Bottão de logout
        btn_Logout = ctk.CTkButton(Frame_Config_Name2,
                                    image=icon_Logout,
                                    text="LOGOUT",
                                    corner_radius=10,
                                    width=150, height=60,
                                    fg_color='darkred',
                                    text_color='white',
                                    hover_color='red',
                                    command=self.delete_token)
        btn_Logout.pack(side="right", padx=10, pady=10) 

        Icon_User_local = Image.open("Image/usuariolocal.png").resize((80, 80), Image.LANCZOS)  # Carrega e redimensiona a imagem
        icon_size = (50, 50)
        # Cria o CTkImage com a imagem PIL diretamente
        icon_User_local = ctk.CTkImage(light_image=Icon_User_local, size=icon_size)
        # Exibe a imagem no Label
        icon_User_local_label = ctk.CTkLabel(Frame_Config_Name3, image=icon_User_local, text="")
        icon_User_local_label.pack(side="left", padx=10, pady=10)

        btn_User_Local = ctk.CTkButton(Frame_Config_Name3,
                                    image=icon_User_local,
                                    text="CRIAR USUÁRIO LOCAL",
                                    corner_radius=10,
                                    width=150, height=60,
                                    fg_color='green',
                                    text_color='white',
                                    hover_color='darkgreen',
                                    command=User_local.Window_Change_Password)
        btn_User_Local.pack(side="right", padx=10, pady=10) 

        # Aqui onde ficará a parte de atualiazacao do sistema __________________________________________________________________________

        # Textbox onde ficará a informacoes da conta da pessoa que irá utilizar o sistema da CODAR 
        Frame_textbox = ctk.CTkFrame(Frame_Config3, corner_radius=30, fg_color="transparent")
        Frame_textbox.pack(side="left", padx=10, pady=10)

        text_box = ctk.CTkTextbox(Frame_textbox, wrap='word', width=500, height=200, fg_color="transparent")
        text_box.pack(side="left",padx=10, pady=10)

        explanation_text = """
        Realizar o backup do banco de dados é crucial para proteger
        as informações contra perdas inesperadas, como falhas no si-
        stema, ataques cibernéticos ou erros humanos. Manter cópias 
        de segurança garante que os dados possam ser restaurados 
        rapidamente, minimizando prejuízos e mantendo a continu-
        idade das operações. Na CODAR, valorizamos a integridade
        dos seus dados e recomendamos backups regulares para gar-
        antir a segurança e a confiabilidade do sistema.
        """
        text_box.configure(font=("Arial", 15, "bold"))
        text_box.insert("1.0", explanation_text)

        # Desabilita a edição do texto para que seja apenas leitura
        text_box.configure(state="disabled")
        
        frame_Update1 = ctk.CTkFrame(Frame_Config3, corner_radius=30, fg_color="transparent")
        frame_Update1.pack(fill="both", side="left", expand=True, padx=10, pady=10)
                

        # Frame Backup In Cloud
        Frame_Buttons_Backup_cloud = ctk.CTkFrame(frame_Update1, corner_radius=20)
        Frame_Buttons_Backup_cloud.pack(side="bottom", fill="x", padx=10, pady=10)
        Icon_Backup_Cloud = Image.open("Image/backupnuvem.png").resize((80, 80), Image.LANCZOS)  # Carrega e redimensiona a imagem
        icon_size = (50, 50)
        # Cria o CTkImage com a imagem PIL diretamente
        icon_Backup_Cloud = ctk.CTkImage(light_image=Icon_Backup_Cloud, size=icon_size)
        # Exibe a imagem no Label
        icon_Backup_Cloud_label = ctk.CTkLabel(Frame_Buttons_Backup_cloud, image=icon_Backup_Cloud, text="")
        icon_Backup_Cloud_label.pack(side="left", padx=10, pady=10)
        Label_Backup_Cloud = ctk.CTkLabel(Frame_Buttons_Backup_cloud, text="Não arrisque perder seus dados. Faça backup regularmente", font=("Arial", 20, "bold"))
        Label_Backup_Cloud.pack(side="left", padx=80, pady=10)
        
        # Frame Backup In Computer
        Frame_Buttons_Backup_Computer = ctk.CTkFrame(frame_Update1, corner_radius=20)
        Frame_Buttons_Backup_Computer.pack(side="bottom", fill="x", padx=10, pady=10)
        Icon_Backup_Computer = Image.open("Image/backupcomputador.png").resize((80, 80), Image.LANCZOS)  # Carrega e redimensiona a imagem
        icon_size = (50, 50)
        # Cria o CTkImage com a imagem PIL diretamente
        icon_Backup_Computer = ctk.CTkImage(light_image=Icon_Backup_Computer, size=icon_size)
        # Exibe a imagem no Label
        icon_Backup_Computer_label = ctk.CTkLabel(Frame_Buttons_Backup_Computer, image=icon_Backup_Computer, text="")
        icon_Backup_Computer_label.pack(side="left", padx=10, pady=10)
        Label_Backup_Computer = ctk.CTkLabel(Frame_Buttons_Backup_Computer, text="Faça backup também em seu computador", font=("Arial", 20, "bold"))
        Label_Backup_Computer.pack(side="left", padx=80, pady=10)
               
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Junta o diretório atual com o nome do banco de dados
        backup_file_dados = os.path.join(diretorio_atual, 'imagens.db')

        btn_Backup_Cloud = ctk.CTkButton(Frame_Buttons_Backup_cloud,
                                      text="BACKUP NA NUVEM",
                                      image=icon_Backup_Cloud,
                                      fg_color="blue",
                                      corner_radius=10,
                                      hover_color="Darkblue",
                                      height=60,
                                      width=150,
                                      command= lambda: self.upload_backup_to_google_drive(backup_file_dados))
        btn_Backup_Cloud.pack(side="right", padx=10, pady=10)

        btn_Backup_Computer = ctk.CTkButton(Frame_Buttons_Backup_Computer,
                                      text="BACKUP NO COMPUTADOR",
                                      image=icon_Backup_Computer,
                                      fg_color="green",
                                      corner_radius=10,
                                      hover_color="Darkgreen",
                                      height=60,
                                      width=150,
                                      command= lambda: self.upload_backup_computer(backup_file_dados))
        btn_Backup_Computer.pack(side="right", padx=10, pady=10)

        # Aqui onde ficará a parte de atualizacao do sistema__________________________________________________________________________
        
        Frame_Updates = ctk.CTkFrame(Frame_Config4, corner_radius=30, fg_color="transparent")
        Frame_Updates.pack(fill="both", expand=True, padx=10, pady=10)

        Frame_Updates1 = ctk.CTkFrame(Frame_Config4, corner_radius=30, fg_color="transparent")
        Frame_Updates1.pack(fill="both", expand=True, padx=10, pady=10)

        Frame_Updates_Filho = ctk.CTkFrame(Frame_Updates, corner_radius=30, fg_color="transparent")
        Frame_Updates_Filho.pack(side="left", padx=10, pady=10)

        Frame_Texts = ctk.CTkFrame(Frame_Updates, corner_radius=30, fg_color="transparent")
        Frame_Texts.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Imagem da agenda backup computador
        Icon_Updates_Filho = Image.open("Image/atualizacao.png").resize((80, 80), Image.LANCZOS)  # Carrega e redimensiona a imagem
        icon_size = (150, 150)
        # Cria o CTkImage com a imagem PIL diretamente
        icon_update = ctk.CTkImage(light_image=Icon_Updates_Filho, size=icon_size)
        # Exibe a imagem no Label
        icon_update_label = ctk.CTkLabel(Frame_Updates_Filho, image=icon_update, text="")
        icon_update_label.pack(side="left", padx=10, pady=10)

        # Label para o nome da pessoa
        Name_Conta_Google = ctk.CTkLabel(Frame_Texts, text="SUAS ATUALIZAÇÕES", font=("Arial", 25, "bold"))
        Name_Conta_Google.pack(side="left", padx=10, pady=5)

        # Botões referente a atualizações 
            
        # Frame Update
        self.Frame_Get_Update = ctk.CTkFrame(Frame_Updates1, corner_radius=20, height=70)
        self.Frame_Get_Update.pack(fill="both", expand=True, padx=10, pady=10)

        # Imagem da agenda backup computador
        Icon_Updates_Filho = Image.open("Image/atualizacao.png").resize((80, 80), Image.LANCZOS)  # Carrega e redimensiona a imagem
        icon_size = (50, 50)
        # Cria o CTkImage com a imagem PIL diretamente
        icon_update = ctk.CTkImage(light_image=Icon_Updates_Filho, size=icon_size)
        # Exibe a imagem no Label
        icon_update_label = ctk.CTkLabel(self.Frame_Get_Update, image=icon_update, text="")
        icon_update_label.pack(side="left", padx=10, pady=10)

        Label_description_Update = ctk.CTkLabel(self.Frame_Get_Update, text="Busque atualizações para garantir a melhor experiência e segurança no sistema", font=("Arial", 20, "bold"))
        Label_description_Update.pack(side="left", padx=80, pady=10)
                

        def open_instagram_edge_or_chrome():

            url = 'https://www.instagram.com/codar_software?igsh=d2Z4aGoyNTZ1aHpl'
            
            # Tentar abrir no Microsoft Edge
            try:
                webbrowser.get('microsoft-edge').open(url)
                print("A URL foi aberta no Microsoft Edge com sucesso.")
            except webbrowser.Error:
                # Se não conseguir, tentar abrir no Google Chrome
                try:
                    webbrowser.get('google-chrome').open(url)
                    print("A URL foi aberta no Google Chrome com sucesso.")
                except webbrowser.Error as e:
                    print(f"Erro ao abrir a URL: {e}")

        def open_instagram():

            webbrowser.open("https://www.instagram.com/seu_perfil")

        def open_whatsapp_edge_or_chrome(number):

            url = f'https://wa.me/{number}'
            
            # Tentar abrir no Microsoft Edge
            try:
                webbrowser.get('microsoft-edge').open(url)
                print("A URL foi aberta no Microsoft Edge com sucesso.")
            except webbrowser.Error:
                # Se não conseguir, tentar abrir no Google Chrome
                try:
                    webbrowser.get('google-chrome').open(url)
                    print("A URL foi aberta no Google Chrome com sucesso.")
                except webbrowser.Error as e:
                    print(f"Erro ao abrir a URL: {e}")

        # Número no formato internacional
        whatsapp_number = '5527997169322'
        
        
        Icon_CODAR = Image.open("Image/CODAR.png").resize((80, 80), Image.LANCZOS)  # Carrega e redimensiona a imagem
        icon_size = (65, 65)
        # Cria o CTkImage com a imagem PIL diretamente
        icon_codar = ctk.CTkImage(light_image=Icon_CODAR, size=icon_size)
        # Exibe a imagem no Label
        icon_codar_label = ctk.CTkLabel(Frame_Config5, image=icon_codar, text="")
        icon_codar_label.pack(side="left", padx=10, pady=10)
      

        Icon_INSTAGRAM = Image.open("Image/instagram.png").resize((80, 80), Image.LANCZOS)  # Carrega e redimensiona a imagem
        icon_size = (50, 50)
        # Cria o CTkImage com a imagem PIL diretamente
        icon_instagram = ctk.CTkImage(light_image=Icon_INSTAGRAM, size=icon_size)
        # Exibe a imagem no Label
        icon_instagram_label = ctk.CTkLabel(Frame_Config5, image=icon_instagram, text="")
        icon_instagram_label.pack(side="right", padx=10, pady=10)
        icon_instagram_label.bind("<Button-1>", lambda e: open_instagram_edge_or_chrome())

        Icon_WHATSSAP = Image.open("Image/whatsapp.png").resize((80, 80), Image.LANCZOS)  # Carrega e redimensiona a imagem
        icon_size = (55, 55)
        # Cria o CTkImage com a imagem PIL diretamente
        icon_whatssap = ctk.CTkImage(light_image=Icon_WHATSSAP, size=icon_size)
        # Exibe a imagem no Label
        icon_whatssap_label = ctk.CTkLabel(Frame_Config5, image=icon_whatssap, text="")
        icon_whatssap_label.pack(side="right", padx=10, pady=10)
        icon_whatssap_label.bind("<Button-1>", lambda e: open_whatsapp_edge_or_chrome(whatsapp_number)) 

    def delete_token(self):

        token_path = 'FIBROMIALGIA/token.json'

        # Verifica se o token existe
        if os.path.exists(token_path):
            os.remove(token_path)
            print("Arquivo token.json excluído.")
            
            # Opcional: Exibir uma mensagem ao usuário
            messagebox.showinfo(title="Logout", message="Você foi deslogado da conta Google.")
            
            # Fecha a janela atual
            self.w.destroy()
        else:
            # Opcional: Exibir uma mensagem de erro ao usuário
            messagebox.showinfo(title="Erro", message="Você não está logado na conta do Google.")
            print("Arquivo token.json não encontrado.")

    def upload_backup_computer(self, backup_file):
        
        def backup():
            try:
                # Abre uma janela para o usuário selecionar o diretório onde o backup será salvo
                selected_directory = filedialog.askdirectory(title="Selecione o diretório de destino para o backup")
                if selected_directory:  # Verifica se o usuário selecionou um diretório
                    # Cria o caminho completo para o backup
                    destination_path = os.path.join(selected_directory, os.path.basename(backup_file))
                    
                    # Copia o arquivo de backup para o diretório escolhido
                    shutil.copy(backup_file, destination_path)
                    
                    print(f"Backup {backup_file} salvo em {selected_directory}.")
                else:
                    print("Nenhum diretório selecionado. Backup cancelado.")
            except Exception as e:
                print(f"Erro ao fazer backup: {e}")

        # Iniciar o processo de backup em uma nova thread
        threading.Thread(target=backup).start()

    def upload_backup_to_google_drive(self, backup_file):
            
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            caminho_json = os.path.join(diretorio_atual, 'fibromialgia.json')
            
            def upload():
                try:
                    gauth = GoogleAuth()
                    gauth.LoadClientConfigFile(caminho_json)
                    gauth.LocalWebserverAuth()  # Autenticação no Google Drive
                    drive = GoogleDrive(gauth)
                    
                    # Upload do arquivo de backup
                    file_drive = drive.CreateFile({'title': os.path.basename(backup_file)})
                    file_drive.SetContentFile(backup_file)
                    file_drive.Upload()
                    print(f"Backup {backup_file} enviado para o Google Drive.")
                except Exception as e:
                    print(f"Erro ao fazer upload: {e}")

            # Iniciar o upload em uma nova thread
            threading.Thread(target=upload).start()
    
    def salvar_backup(self, caminho, horario, dia_semana, dia_mes):

        query = f'''
        INSERT INTO backup_agendado (caminho_computador, horario, dia_semana, dia_mes)
        VALUES ('{caminho}', '{horario}', '{dia_semana}', '{dia_mes}')
        '''
        DataBase().dml(query)
        messagebox.showinfo(title="Sucesso", message="Configuração de backup salva com sucesso.")
    
    def display_user_image(self, picture_url):

        try:
            response = requests.get(picture_url)
            image_data = BytesIO(response.content)
            image = Image.open(image_data)
            image = image.resize((100, 100))  # Redimensione conforme necessário
            photo = ImageTk.PhotoImage(image)

            user_image_label = ctk.CTkLabel(self.Frame_Widgets, image=photo)
            user_image_label.image = photo  # Necessário para manter uma referência e evitar que a imagem seja coletada pelo GC
        except Exception as e:
            print(f"Erro ao carregar a imagem do usuário: {e}")
            
class Change_Password_Window:

    def __init__(self, master, frame_widgets):
        self.w = master
        self.Frame_Widgets = frame_widgets  # Armazena o Frame_Widgets
        
    def Window_Change_Password(self):
        
        self.w = ctk.CTk()
        self.w.geometry("500x530")
        self.w.resizable(False, False)
        self.w.title('CRIAR USUÁRIO LOCAL')

        frame1 = ctk.CTkFrame(self.w, corner_radius=40)  # Corrigido para self.w
        frame1.pack(expand=True, fill="both", padx=10, pady=10)

        label = ctk.CTkLabel(frame1, text="CRIAR USUÁRIO", width=390, height=50, font=('Century Gothic', 30, "bold"))
        label.pack(pady=20)

        email = ctk.CTkEntry(frame1, placeholder_text="SEU EMAIL", width=390, height=50, font=('Century Gothic', 15, "bold"))
        email.pack(pady=10)
        email.bind("<FocusOut>", lambda event: self.validate_email(event, email))

        username = ctk.CTkEntry(frame1, placeholder_text="NOME USUÁRIO", width=390, height=50, font=('Century Gothic', 15, "bold"))
        username.pack(pady=10)

        password = ctk.CTkEntry(frame1, placeholder_text="SENHA", width=390, height=50, font=('Century Gothic', 15, "bold"), show="*")
        password.pack(pady=10)

        repeat_password = ctk.CTkEntry(frame1, placeholder_text="CONFIRME SUA SENHA", width=390, height=50, font=('Century Gothic', 15, "bold"), show="*")
        repeat_password.pack(pady=10)

        def create_user_account():

            # Obtém os valores dos campos (é necessário chamar a função get() corretamente)
            email_entry = email.get().strip()
            username_entry = username.get().strip()
            password_entry = password.get().strip()
            repeat_password_entry = repeat_password.get().strip()

            # Certifique-se de que os campos estão preenchidos corretamente
            if not email_entry or not username_entry or not password_entry or not repeat_password_entry:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
                return

            db = DataBase()

            # Verifica se o email já existe no banco de dados
            query = "SELECT nome, senha FROM login WHERE email = ?"
            user_data = db.dql(query, (email_entry,))

            if user_data:
                # Se um email foi encontrado, verificar se já há um nome de usuário vinculado
                if user_data[0][0] and user_data[0][1]:
                    # Nome de usuário e senha já existem
                    messagebox.showerror("Erro", "Já existe um usuário vinculado a essa conta do Google.")
                    return

            # Verifica se as senhas coincidem
            if password_entry != repeat_password_entry:
                messagebox.showerror("Erro", "As senhas não coincidem.")
                return

            # Caso o email esteja registrado mas ainda não tenha nome e senha, cria um usuário
            if user_data:
                query_update = "UPDATE login SET nome = ?, senha = ? WHERE email = ?"
                db.dml(query_update, (username_entry, password_entry, email_entry))
            else:
                # Caso não exista nenhum registro, cria um novo
                query_insert = "INSERT INTO login (email, nome, senha) VALUES (?, ?, ?)"
                db.dml(query_insert, (email_entry, username_entry, password_entry))

            messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")

        btn_Alterar_Senha = ctk.CTkButton(frame1,
                                          text="CADASTRAR USUÁRIO",
                                          fg_color="Orange",
                                          corner_radius=10,
                                          hover_color="DarkOrange",
                                          height=50,
                                          width=390,
                                          command=create_user_account)
        btn_Alterar_Senha.pack(pady=10)

        btn_Cancelar = ctk.CTkButton(frame1,
                                     text="CANCELAR",
                                     fg_color="red",
                                     corner_radius=10,
                                     hover_color="DarkRed",
                                     height=50,
                                     width=390,
                                     command=self.w.destroy)  # Corrigido para fechar a janela
        btn_Cancelar.pack(pady=10)

        self.w.mainloop()

    def validate_email(self, event, entry):
        email = entry.get()
        if not self.is_valid_email(email):
            messagebox.showerror("Erro de entrada", "Por favor, insira um email válido.")
            entry.delete(0, tk.END)
            return

    def is_valid_email(self, email):
        # Verifica se o email tem pelo menos um caractere antes de @, um @, pelo menos um caractere depois de @,
        # um ponto após @, e pelo menos dois caracteres após o ponto
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
        
class Window_User_Fibro():

    def __init__(self, master, frame_widgets):
        self.w = master
        self.Frame_Widgets = frame_widgets  # Armazena o Frame_Widgets
     
    def Show_Image_User_Fibro(self):
        
        # Destroi o frame atual, se houver
        for widget in self.w.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.Frame_Widgets:
                widget.destroy()      

        # Recria o Frame9 (o frame principal)
        self.Frame1 = ctk.CTkFrame(self.w, corner_radius=30)
        self.Frame1.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.Frame2 = ctk.CTkFrame(self.Frame1, corner_radius=30)
        self.Frame2.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.Frame3 = ctk.CTkFrame(self.Frame1, corner_radius=20, height=50)
        self.Frame3.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        img1_Inserir = ctk.CTkImage(Image.open("Image/InseirImagem.png").resize((80, 80), Image.LANCZOS))
        img2_Baixar = ctk.CTkImage(Image.open("Image/baixarimagem.png").resize((80, 80), Image.LANCZOS))
        img2_Anterior = ctk.CTkImage(Image.open("Image/anterior.png").resize((80, 80), Image.LANCZOS))
        img2_Proximo = ctk.CTkImage(Image.open("Image/proximo.png").resize((80, 80), Image.LANCZOS))

        # Funcoes da tela InsertImageUserFibro
        
        def buscar_imagens():
            
            query="SELECT carteirinha FROM Cadastro"
            imagens = DataBase().dql(query)
            return imagens

        self.imagens = buscar_imagens()
        self.indice = 0

        self.lbl_imagem = ctk.CTkLabel(self.Frame2, text="")
        self.lbl_imagem.pack(pady=200)
        
        btn_Anterior = ctk.CTkButton(self.Frame3,
                                      text="ANTERIOR",
                                      fg_color="DarkViolet",
                                      image=img2_Anterior,
                                      corner_radius=10,
                                      hover_color="DarkOrchid",
                                      height=60,
                                      width=150,
                                      font=('Century Gothic', 20,'bold'),
                                      command=self.imagem_proxima)
        btn_Anterior.grid(row=0, column=3, padx=5, pady=10)

        btn_Proximo = ctk.CTkButton(self.Frame3,
                                      text="PRÓXIMO",
                                      fg_color="DarkViolet",
                                      image=img2_Proximo,
                                      corner_radius=10,
                                      hover_color="DarkOrchid",
                                      height=60,
                                      width=150,
                                      font=('Century Gothic', 20,'bold'),
                                      command=self.imagem_anterior)
        btn_Proximo.grid(row=0, column=4, padx=5, pady=10)

        self.exibir_imagem()

    def exibir_imagem(self):
        
        if self.imagens:
            imagem_blob = self.imagens[self.indice][0]
            imagem = Image.open(io.BytesIO(imagem_blob))
            imagem.thumbnail((1400, 1400))
            imagem_tk = ImageTk.PhotoImage(imagem)

            self.lbl_imagem.configure(image=imagem_tk)
            self.lbl_imagem.image = imagem_tk
        else:
            self.lbl_imagem.configure(text="Nenhuma imagem no banco de dados.", font=('Century Gothic', 20,'bold'))

    def imagem_anterior(self):

        if self.indice > 0:
            self.indice -= 1
            self.exibir_imagem()

    def imagem_proxima(self):
        if self.indice < len(self.imagens) - 1:
            self.indice += 1
            self.exibir_imagem()

class Logon_Google_Fuctions:

    def __init__(self, logon_instance):
        self.Logon_user = logon_instance
    
    def login_with_google(self):

        def login_process():

            SCOPES = [
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email',
                'openid'
            ]
            creds = None

            try:
                # Defina o caminho da pasta "FIBROMIALGIA"
                token_dir = os.path.join(os.getcwd(), 'FIBROMIALGIA')
                token_path = os.path.join(token_dir, 'token.json')

                # Verifique se a pasta "FIBROMIALGIA" existe, se não, crie-a
                if not os.path.exists(token_dir):
                    os.makedirs(token_dir)

                # Verifique se o arquivo "token.json" existe nessa pasta
                if os.path.exists(token_path):
                    creds = Credentials.from_authorized_user_file(token_path, SCOPES)

                # Caso não tenha credenciais válidas, solicite novo login
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file('fibromialgia.json', SCOPES)
                        creds = flow.run_local_server(port=0)

                    # Salve o arquivo "token.json" na pasta "FIBROMIALGIA"
                    with open(token_path, 'w') as token:
                        token.write(creds.to_json())

                # Função para obter informações do usuário
                def get_user_info():

                    try:
                        user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
                        headers = {'Authorization': f'Bearer {creds.token}'}
                        response = requests.get(user_info_url, headers=headers)
                        user_info = response.json()

                        if 'name' in user_info and 'email' in user_info and 'picture' in user_info:
                            self.user_name = user_info['name']  # Armazena o nome do usuário
                            self.user_email = user_info['email']  # Armazena o email do usuário
                            self.user_picture_url = user_info['picture']  # URL da imagem de perfil do usuário

                            print(f"Usuário logado: {self.user_name}")
                            print(f"E-mail: {self.user_email}")
                            print(f"URL da imagem de perfil: {self.user_picture_url}")

                            # Salva o nome, e-mail e URL da imagem no banco de dados
                            self.save_user_info(self.user_name, self.user_email, self.user_picture_url)
                            # Chama display_user_image da instância de Window_config

                            self.Logon_user.after(0, self.Logon_user.Show_Window_Home)
                        else:
                            print("Erro: Login falhou.")
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao obter informações do usuário: {e}")

                # Executa a requisição de informações do usuário em uma thread separada
                threading.Thread(target=get_user_info).start()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao fazer login, verifique sua conexão com a internet! Detalhes: {e}")
                print(f"Erro ao fazer login: {e}")

        # Inicia o processo de login em uma nova thread para não bloquear a interface
        threading.Thread(target=login_process).start()

    def save_user_info(self, name, email, picture_url):

        """Salva o nome, e-mail e a URL da imagem do usuário no banco de dados, se ainda não existir."""
        try:
            # Verifica se o usuário já está no banco de dados
            query = "SELECT * FROM login WHERE nome_email = ? AND email = ?"
            db = DataBase()
            existing_user = db.dql(query, (name, email))

            if not existing_user:
                # Se o usuário não existir, insere o novo registro
                query_insert = '''
                    INSERT INTO login (nome_email, email, imagem_url)
                    VALUES (?, ?, ?)
                '''
                db.dmlWithParament(query_insert, (name, email, picture_url))
                print("Informações do usuário salvas no banco de dados.")
            else:
                print("Usuário já está salvo no banco de dados.")

        except Exception as e:
            print(f"Erro ao salvar informações no banco de dados: {e}")
    
if __name__ == "__main__":
    logon = Logon()
    logon.mainloop()



