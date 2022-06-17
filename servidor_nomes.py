import socket
import threading
import time

import Pyro4
import Pyro4.naming
from paho.mqtt import client as mqtt

class mensagem:
    def __init__(self):
        self.client = mqtt.Client("servidor")
        self.client.connect('mqtt.eclipseprojects.io')


    @Pyro4.expose
    def recebe_topico(self,topicos):
        print("tototopic",topicos)
        """self.client = mqtt.Client("servidor")
        self.client.connect('mqtt.eclipseprojects.io')
        self.client.loop_start()
        self.client.publish("topicos", topicos)
        self.client.loop_stop()"""
        print("topico",topicos)
        self.client.publish("topicos", topicos)
        #self.client.publish("mensagem", "topicos")

    @Pyro4.expose
    def recebe_mensagem(self, topico,mensagem):
        """self.client = mqtt.Client("servidor")
        self.client.connect('mqtt.eclipseprojects.io')
        self.client.loop_start()
        self.client.loop_stop()"""
        print("mensagem", mensagem)
        self.client.publish(topico, mensagem)



class servidor:
    def __init__(self):
        ip_local = socket.gethostbyname(socket.gethostname())
        nameserver = Pyro4.naming.startNSloop
        nameServer = threading.Thread(target= lambda: nameserver(ip_local, 50000)) #inica o nameserver em forma de thread para ficar disponivel para visualizacao a porta e o IP
        nameServer.start()

        ns = Pyro4.locateNS(host=ip_local, port=50000)
        daemon = Pyro4.Daemon(host=ip_local)
        uri = daemon.register(mensagem)
        ns.register("Servidor",uri)
        daemon.requestLoop()
        print("saiu do loop")

#servidor()
#mensagem()
