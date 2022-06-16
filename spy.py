import socket
import time
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import *
import threading

import Pyro4

import servidor_nomes
from client import Client
from server import Server
#server = threading.Thread(target=lambda: Server.start_server(host='127.0.0.1'))
#server.start()


#CLIENTE._out(('mensagens', 0, 0))
class spy:
    def __init__(self):

        ip_local = socket.gethostbyname(socket.gethostname())
        server = threading.Thread(target=lambda: Server.start_server(host=ip_local))
        server.start()


        #self.janela()
        win = threading.Thread(target=self.janela)
        win.start()
        self.CLIENTE = Client((ip_local, 5050))
        self.CLIENTE._out(('mensagens', 0, 0))
        self.CLIENTE._out(('usuarios', 0, 0))
        while True:
            print("entrou")
            mensagem = self.CLIENTE._in(("spy", "mensagem publica", str))
            print(mensagem)
            indice = self.CLIENTE._in(("mensagens", 0, int))
            indice+=1
            self.CLIENTE._out(("mensagens", 0, indice ))
            self.CLIENTE._out(("mensagens", indice , mensagem))
            ###### Implementar a interface rmi rpc
        self.CLIENTE.close()



    @classmethod
    def janela(self):
        self.topicos=[]
        self.lable=""
        def topico():
            nome=entrada.get()
            if nome=="":
                return
            try:
                print(self.topicos.index(nome))
                entrada.delete(0, END)
                return
            except:
                pass
            self.topicos.append(nome)
            texto2["text"]+=(nome+"\n")
            entrada.delete(0, END)


        ip_local = socket.gethostbyname(socket.gethostname())
        janela = Tk()
        janela.geometry("400x400")
        janela.resizable(False, False)
        janela.title("Cliente")
        entrada=Entry(janela,width=20)
        texto=Label(janela,text=f"Monitorando servidor: {ip_local}\nDigite o tópico suspeito")
        texto2 = Label(janela,text="Tópicos:\n")
        botao=Button(janela,text="incluir",command=topico)

        texto1=Label(janela,text="Indique o ip do servidor RMI:")
        entrada1 = Entry(janela, width=20)
        entrada1.insert(0,ip_local)
        self.proxy=0
        def enviaTopico():
            while True:
                ":".join(self.topicos)
                #print(":".join(self.topicos))
                self.proxy.recebe_topico(":".join(self.topicos))
                time.sleep(3)

        def cria_proxy():
            aux=entrada1.get()
            try:
                ns = Pyro4.locateNS(aux, 50000)
                self.proxy = Pyro4.Proxy(ns.lookup("Servidor"))

            except:
                if(messagebox.askyesno(title="Servidor não existe",message=f"Servidor não existe no endereco{aux}, deseja iniciar um no ip {ip_local}?")):
                    servidor=threading.Thread(target= servidor_nomes.servidor)
                    servidor.start()
                    time.sleep(1)
                    ns = Pyro4.locateNS(aux, 50000)
                    self.proxy = Pyro4.Proxy(ns.lookup("Servidor"))
                else:
                    return
            botao1.destroy()
            entrada1.destroy()
            texto1.destroy()
            enviar = threading.Thread(target=enviaTopico)
            enviar.start()

        botao1 = Button(janela, text="Procurar", command=cria_proxy)
        texto1.place(x=10,y=80)
        entrada1.place(x=10,y=100)
        botao1.place(x=140,y=100)
        texto.place(x=10,y=10)
        entrada.place(x=10,y=50)
        botao.place(x=140,y=45)
        texto2.place(x=270,y=10)


        janela.mainloop()

#aux = spy()