class Logon(ctk.CTk):

    def __init__(self):
        super().__init__()

        db = DataBase()
        db.create_tables()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        self.geometry("800x600")
        self.minsize(800, 600)
        self.title('Login')

        self.service = self.authenticate_google_drive()

        if self.check_for_updates():
            self.download_and_apply_update()

        Login_User_Google = Logon_Google_Fuctions(self)

        # Corrigido para usar CTkImage
        img1 = ctk.CTkImage(Image.open("Image/pattern.png"))
        l1 = ctk.CTkLabel(master=self, image=img1)
        l1.pack()

        Frame_Tela_Login = ctk.CTkFrame(master=l1, width=500, height=500, corner_radius=30)
        Frame_Tela_Login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        l2 = ctk.CTkLabel(master=Frame_Tela_Login, text="Logar", font=('Century Gothic', 40))
        l2.place(x=190, y=45)

        self.Entry_Nome_User = ctk.CTkEntry(master=Frame_Tela_Login, width=390, height=50, placeholder_text='Nome')
        self.Entry_Nome_User.place(x=60, y=130)

        self.Entry_Senha_User = ctk.CTkEntry(master=Frame_Tela_Login, width=390, height=50, placeholder_text='Senha', show="*")
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
        email_entry = self.Entry_Nome_User.get().strip()
        password_entry = self.Entry_Senha_User.get().strip()

        # Certifique-se de que os campos estão preenchidos corretamente
        if not email_entry or not password_entry:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        db = DataBase()

        # Verifica se o email e a senha existem no banco de dados
        query = "SELECT * FROM login WHERE email = ? AND senha = ?"
        user_data = db.dql(query, (email_entry, password_entry))

        if user_data:
            # Login bem-sucedido, abre a próxima tela
            messagebox.showinfo("Sucesso", "Login bem-sucedido.")
            self.open_next_screen()  # Aqui você deve chamar a função que abre a próxima tela
        else:
            # Caso as credenciais estejam incorretas ou não existam
            messagebox.showerror("Erro", "Conta não encontrada. Por favor, entre com a conta do Google e crie um usuário local.")

    def open_next_screen(self):
        # Código para abrir a próxima tela do sistema
        new_window = ctk.CTk()
        new_window.geometry("500x500")
        new_window.title("Próxima Tela")
        label = ctk.CTkLabel(new_window, text="Bem-vindo à próxima tela!", font=('Century Gothic', 20, 'bold'))
        label.pack(pady=20)
        new_window.mainloop()
