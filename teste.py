import customtkinter as ctk
from bokeh.plotting import figure, output_file, save
from bokeh.embed import server_document
import pandas as pd
import os

class Dashboard:
    def __init__(self, master):
        self.w = master
        self.Show_Dashboard()

    def Show_Dashboard(self):
        for widget in self.w.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        Frame_Dashboard = ctk.CTkFrame(self.w, corner_radius=30)
        Frame_Dashboard.pack(fill="both", expand=True, padx=10, pady=10)

        # Cria um exemplo de DataFrame
        data = {'faixa_etaria': ['18-25', '26-35', '36-45', '46-55', '56+'],
                'contagem': [10, 20, 15, 30, 25]}
        df = pd.DataFrame(data)

        # Criação do gráfico
        self.create_graph(df)

    def create_graph(self, df):
        # Criando um gráfico de barras
        p = figure(x_range=df['faixa_etaria'], height=250, title="Quantidade de Pessoas por Faixa Etária",
                   toolbar_location=None, tools="")

        p.vbar(x=df['faixa_etaria'], top=df['contagem'], width=0.9)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0

        # Saída do arquivo HTML
        output_file("grafico.html")
        save(p)

        # Carregar o HTML do gráfico
        os.system("xdg-open grafico.html")

if __name__ == "__main__":
    root = ctk.CTk()
    app = Dashboard(root)
    root.mainloop()
