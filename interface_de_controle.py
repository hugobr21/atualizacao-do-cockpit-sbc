import tkinter as tk
from tkinter import messagebox
import json

def agendarPausa():
    while True:
        try:
            with open("pause.json", "r") as infile:
                parametros = json.load(infile)
            break
        except FileNotFoundError:
            parametros = {
            "statuspausa": False,
        }
            with open("pause.json", "w") as outfile:
                json.dump(parametros, outfile)

    if parametros["statuspausa"] == True:
        parametros["statuspausa"] = False
    else:
        parametros["statuspausa"] = True
    parametros = {
        "statuspausa": parametros["statuspausa"],
    }
    with open("pause.json", "w") as outfile:
        json.dump(parametros, outfile)
    messagebox.showinfo(title="Feito!", message="Pausa agendada com sucesso!")

def gravarParametros():

    try:
        #validação de campos numéricos

        int(delaycarregamentoentry.get())
        int(delayacompanhamentoentry.get())
        int(delaypreclickwebentry.get())

        # validação de campo vazio

        if '' in [
            caminhonavegadorentry.get(),
            iddaplanilhaentry.get(),
            linkdolookerentry.get(),
            delaycarregamentoentry.get(),
            delayacompanhamentoentry.get(),
            delaypreclickwebentry.get()
            ]:
            messagebox.showinfo(title="Cuidado!", message="Há campos vazios!")
        else:
            parametros = {
                "caminhonavegador": caminhonavegadorentry.get(),
                "idplanilha": iddaplanilhaentry.get(),
                "linkdolooker": linkdolookerentry.get(),
                "delayprecarregamento": delaycarregamentoentry.get(),
                "delayacompanhamento": delayacompanhamentoentry.get(),
                "delayclicweb": delaypreclickwebentry.get()
            }

            with open("parametros.json", "w") as outfile:
                json.dump(parametros, outfile)
            messagebox.showinfo(title="Feito!", message="Parâmetros gravados com sucesso!")
    except:
        messagebox.showinfo(title="Cuidado!", message="Valores de Delay inválidos")



def carregarParametros():
    with open("parametros.json", "r") as infile:
        parametros = json.load(infile)
    caminhonavegadorentry.insert(0,parametros["caminhonavegador"])
    iddaplanilhaentry.insert(0,parametros["idplanilha"])
    linkdolookerentry.insert(0,parametros["linkdolooker"])
    delaycarregamentoentry.insert(0,parametros["delayprecarregamento"])
    delayacompanhamentoentry.insert(0,parametros["delayacompanhamento"])
    delaypreclickwebentry.insert(0,parametros["delayclicweb"])
    return parametros

window = tk.Tk()
window.geometry("600x280")
window.title("Parâmetros do robô")
window.resizable(False,False)
window.columnconfigure(1, weight=1)
window.columnconfigure(0, weight=3)

# labels da interface

caminhonavegador = tk.Label(text="Caminho de instalação Firefox/Chrome: ")
caminhonavegador.grid(column=0,row=0,sticky=tk.E)
iddaplanilha = tk.Label(text="ID da planilha do Google Sheets: ")
iddaplanilha.grid(column=0,row=1,sticky=tk.E)
linkdolooker = tk.Label(text="Link do looker com filtros: ")
linkdolooker.grid(column=0,row=2,sticky=tk.E)
delayacompanhamento = tk.Label(text="Tempo(s*) de pausa para atualização de DataStudio (Sugerido: 10 minutos): ")
delayacompanhamento.grid(column=0,row=3,sticky=tk.E)
delaycarregamento = tk.Label(text="Tempo(s*) de pausa para baixar arquivos (Sugerido: 70 segundos): ")
delaycarregamento.grid(column=0,row=4,sticky=tk.E)
delaypreclickweb = tk.Label(text="Tempo(m*) de pausa para clicar no botão no Firefox/Chrome (Sugerido: 10 segundos): ")
delaypreclickweb.grid(column=0,row=5,sticky=tk.E)
observacoes = tk.Label(text="*Onde: s=Segundos, m=Minutos")
observacoes.grid(column=0,row=9,sticky=tk.E)

# campos de entrada

caminhonavegadorentry = tk.Entry(window)
caminhonavegadorentry.grid(column=1,row=0,sticky=tk.E)
iddaplanilhaentry = tk.Entry()
iddaplanilhaentry.grid(column=1,row=1,sticky=tk.E)
linkdolookerentry = tk.Entry()
linkdolookerentry.grid(column=1,row=2,sticky=tk.E)
delayacompanhamentoentry = tk.Entry()
delayacompanhamentoentry.grid(column=1,row=3,sticky=tk.E)
delaycarregamentoentry = tk.Entry()
delaycarregamentoentry.grid(column=1,row=4,sticky=tk.E)
delaypreclickwebentry = tk.Entry()
delaypreclickwebentry.grid(column=1,row=5,sticky=tk.E)


# botões de agendamento

agendamentodepausa = tk.Button(window,text='1 - Agendar Pausa/Retornar de Pausa',command=agendarPausa)
agendamentodepausa.grid(column=0,row=6, columnspan=2,padx=5, pady=5,sticky=tk.E)
atualizarparametros = tk.Button(window,text='2 - Atualizar parâmetros', command=gravarParametros)
atualizarparametros.grid(column=0,row=7, columnspan=2,padx=5, pady=5,sticky=tk.E)
atualizarparametros = tk.Button(window,text='3 - Carregar parâmetros', command=carregarParametros)
atualizarparametros.grid(column=0,row=8, columnspan=2,padx=5, pady=5,sticky=tk.E)


window.mainloop()