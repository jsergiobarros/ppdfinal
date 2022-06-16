import random
from tkinter.scrolledtext import ScrolledText
from tkinter import *
import paho.mqtt.client as paho

class Cliente:

    def onMessage(self,client,userdata,message):
        self.insertTxt(str(message.payload.decode('utf-8')))

    def __init__(self):
        self.broker = 'mqtt.eclipseprojects.io'
        aux = str(random.randint(-10000, 100000))
        self.client = paho.Client(aux)
        self.client.on_message = self.onMessage
        self.client.connect(self.broker)
        self.client.loop_start()
        self.janela()

    def subscribe(self,temp,umi,velo):
        self.client.loop_stop()
        if temp!="0":
            print(temp)
            self.client.subscribe("Temperatura",2)
        else:
            self.client.unsubscribe("Temperatura")
        if umi!="0":
            print(umi)
            self.client.subscribe("Umidade",2)
        else:
            self.client.unsubscribe("Umidade")
        if velo!="0":
            print(velo)
            self.client.subscribe("Velocidade",2)
        else:
            self.client.unsubscribe("Velocidade")
        self.client.loop_start()

    def insertTxt(self,txt):  ###metodo de INSERIR MENSAGEM
        self.chat.configure(state='normal')
        self.chat.insert(END, txt)
        self.chat.insert(END, "\n")
        self.chat.see('end')
        self.chat.configure(state='disabled')

    def cls(self):  ###metodo de INSERIR MENSAGEM
        self.chat.configure(state='normal')
        self.chat.delete('1.0', END)
        self.chat.see('end')
        self.chat.configure(state='disabled')

    def janela(self):
        janela=Tk()
        janela.geometry("800x400")
        janela.resizable(False, False)
        janela.title("Cliente")
        var1 = StringVar()
        var2 = StringVar()
        var3 = StringVar()
        label=Label(janela,text="Canais")
        label2 = Label(janela, text="Leituras")
        c0 = Checkbutton(janela, text="Temperatura",onvalue="Temperatura", variable=var1,command=lambda: self.subscribe(var1.get(),var2.get(),var3.get()))
        c1 = Checkbutton(janela, text="Umidade", variable=var2, onvalue="Umidade", command=lambda: self.subscribe(var1.get(),var2.get(),var3.get()))
        c2 = Checkbutton(janela, text="Velocidade", onvalue="Velocidade", variable=var3, command=lambda: self.subscribe(var1.get(),var2.get(),var3.get()))
        button = Button(text="Limpar Tela",borderwidth=2,command=self.cls)
        self.chat = ScrolledText(janela, width=85, height=20, state='disabled')
        self.chat.place(x=100,y=40)
        label.place(x=35,y=10)
        label2.place(x=400,y=10)
        c0.place(x=5,y=40)
        c1.place(x=5,y=70)
        c2.place(x=5,y=100)
        button.place(x=10,y=330)
        c0.deselect()
        c1.deselect()
        c2.deselect()
        janela.mainloop()


def main():
    cliente = Cliente()
main()