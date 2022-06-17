import random
import threading
from functools import partial

from client import Client
from server import Server
from paho.mqtt import client as mqtt
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import *

class servidor_mensagem:
    TOPICOS=0
    var=[0,0]

    def subunsub(self,topico,variavel):
        if(variavel.get()):
            self.client.subscribe(topico,2)
        else:
            self.client.unsubscribe(topico, 2)

    def __init__(self):
        def onMessage( client, userdata, message):
            aux = message.payload.decode('utf-8').split(":")
            print(aux)
            if (aux[0] == "topico" and int(aux[1]) > self.TOPICOS):
                for i in range(self.TOPICOS+2,int(aux[1])+2):
                    self.var.append(IntVar())
                    button = Checkbutton(self.canvas, text=aux[i],variable=self.var[i])
                    button.grid(row=i,sticky = W)
                    button["command"] = partial(self.subunsub, aux[i],self.var[i])
                self.TOPICOS = int(aux[1])
            elif(aux[0]!="topico"):
                self.chat_public.configure(state='normal')
                self.chat_public.insert(END, message.payload.decode('utf-8'))
                self.chat_public.insert(END, "\n")
                self.chat_public.see('end')
                self.chat_public.configure(state='disabled')
        broker = 'mqtt.eclipseprojects.io'
        aux = str(random.randint(-10000, 100000))
        self.client = mqtt.Client(aux)
        self.client.on_message = onMessage
        self.client.connect(broker)
        self.client.subscribe("topicos",2)
        server = threading.Thread(target=self.janela)
        server.start()
        print("start")
        self.client.loop_forever()

        print("close")


    def janela(self):
        janela = Tk()
        janela.geometry("800x500")
        janela.resizable(False, False)
        janela.title("Cliente")
        self.chat_public = ScrolledText(janela, width=75, height=29, state='disabled')
        self.chat_public.place(x=10, y=10)
        self.canvas=Canvas(janela,width=100,height=600)
        self.canvas.place(x=670,y=10)

        janela.mainloop()

servidor_mensagem()

