import random
import socket
import threading
import time
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from client import Client
from server import Server
from functools import partial
NOME = ""
INDICE=0
MENSAGEM=0
id_mensagem=0
id_usuario=0
DIRETO=""
TOPICO = ""
USERS=[]
USR=[]
CANAIS=[]
CLIENTE=0
topicovigente=0
ip_local = socket.gethostbyname(socket.gethostname())
control=0
BOOL=TRUE

def main_chat():
    global CANAIS,CLIENTE,USERS,TOPICO,NOME


    janela = Tk()
    janela.geometry(("800x600"))
    janela.resizable(False, False)

    endereco = Entry(janela,width=75)
    endereco.insert(0,"Chat no endereço: "+ip_local+" - Nome: "+NOME)
    endereco["state"]='disabled'
    endereco.place(x=10,y=10)
    #botoes para os topicos


    def atualizanome():  #codigo de atualizar a lista de usuarios do canal
        global USR,USERS,id_usuario
        CLIENTE2 = Client((ip_local, 5050))
        usuario = CLIENTE._rd(('usuarios', 0, int))
        usuarios["text"]="Lista de Usuarios\n"
        for i in range(usuario):
            if (CLIENTE._rd(('usuarios', i+1, str))=="VAZIO"):
                pass
            else:
                usuarios["text"]+=str(CLIENTE._rd(('usuarios', i+1, str)))+"\n"
        id_usuario = usuario
        CLIENTE2.close()


    #topicos.place(x=10,y=40)
    users = Canvas(janela, width=100, height=500)
    usuarios=Label(users)
    usuarios.grid()
    users.place(x=650,y=70)
    #botoes para os topicos

    def insert_public():  ###metodo de INSERIR MENSAGEM
        texto=entry_group.get()
        CLIENTE._out(("spy","mensagem publica",NOME+": "+texto))
        entry_group.delete(0,END)


    def espiao():
        mensagem=CLIENTE._in(("spy","mensagem publica",str))
        indice=CLIENTE._in(("mensagens",0,int))
        CLIENTE._out(("mensagens",0,indice+1))
        CLIENTE._out(("mensagens", indice+1, mensagem))



    chat_public = ScrolledText(janela, width=75, height=29, state='disabled')
    chat_public.place(x=10, y=70)
    entry_group = Entry(janela, width=75)
    entry_group.place(x=10,y=545)
    send_group = Button(janela, text="Enviar Grupo", command=insert_public)
    send_group.place(x=475, y=545)


    def mensagem_recebida():  # thread que recebe mensagens enviadas para o usuario diretamente
        global BOOL,id_mensagem
        CLIENTE2 = Client((ip_local, 5050))
        while BOOL:
            aux=CLIENTE._rd(('mensagens', 0, int))
            atualizanome()
            if(aux==id_mensagem or aux==0):
                time.sleep(1)
            else:
                chat_public.configure(state='normal')
                for i in range(id_mensagem,aux):
                    mensagem= CLIENTE._rd(('mensagens', i+1, str))
                    chat_public.insert(END, mensagem)
                    chat_public.insert(END, "\n")
                    chat_public.see('end')
                chat_public.configure(state='disabled')
                id_mensagem=aux
        CLIENTE2.close()

    privado = threading.Thread(target=mensagem_recebida)
    privado.start()

    def desliga():
        global BOOL,CLIENTE,INDICE
        BOOL=False
        CLIENTE._in(('usuarios', INDICE, str))
        CLIENTE._out(('usuarios', INDICE, "VAZIO"))
        CLIENTE.close()
        janela.destroy()
    janela.protocol("WM_DELETE_WINDOW", desliga)
    janela.mainloop()



def define_nome():

    def iniciar():
        global NOME, CLIENTE,USERS,CANAIS,TOPICO,ip_local,INDICE,MENSAGEM
        NOME=nome.get()
        try:
            CLIENTE=Client((endereco.get(), 5050))
            ip_local=endereco.get()
            indice=CLIENTE._in(('usuarios', 0, int))
            INDICE=indice+1
            MENSAGEM=CLIENTE._rd(('mensagens', 0, int))
            CLIENTE._out(('usuarios', 0, INDICE))
            CLIENTE._out(('usuarios', INDICE, NOME))

        except:
            if(messagebox.askyesno(title="Servidor não existe", message=f"Servidor não existe, deseja iniciar um no ip{ip_local}?")):
                server = threading.Thread(target=lambda: Server.start_server(host=ip_local))
                server.start()
                CLIENTE = Client((endereco.get(), 5050))
                INDICE=1
                CLIENTE._out(('mensagens', 0, 0))
                CLIENTE._out(('usuarios', 0, 1))
                CLIENTE._out(('usuarios', 1, NOME))


            else:
                return

        janela.destroy()
        main_chat()

    janela = Tk()
    janela.geometry(("150x150"))
    endereco=Entry(janela,width=20)
    nome=Entry(janela,width=20)
    iniciar = Button(janela,text="Inicar Chat",command=iniciar)



    endereco.insert(0,ip_local)
    aux = "Usuário" + str(random.randint(10000, 100000))
    nome.insert(0,aux)
    nome.grid(pady=10,padx=10,row=0)
    endereco.grid(pady=10,padx=10,row=1)
    iniciar.grid(pady=10,padx=10,row=2)
    janela.mainloop()


define_nome()
