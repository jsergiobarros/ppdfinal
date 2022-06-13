import threading

from client import Client
from server import Server
server = threading.Thread(target=lambda: Server.start_server(host='192.168.0.12'))
server.start()
#CLIENTE = Client(('127.0.0.1', 5050))

#CLIENTE._out(("spy","mensagem publica",'NOME+": "+TOPICO+": "+texto'))
#print(type(CLIENTE._rd(('usuarios', 0, str))))
"""while True:
    print(CLIENTE._in(("spy", "mensagem publica", str)))"""

