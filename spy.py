import threading

from client import Client
from server import Server
#server = threading.Thread(target=lambda: Server.start_server(host='127.0.0.1'))
#server.start()
CLIENTE = Client(('192.168.0.12', 5050))

#CLIENTE._out(('mensagens', 0, 0))

while True:
    mensagem = CLIENTE._in(("spy", "mensagem publica", str))
    indice = CLIENTE._in(("mensagens", 0, int))
    indice+=1
    CLIENTE._out(("mensagens", 0, indice ))
    CLIENTE._out(("mensagens", indice , mensagem))
    ###### Implementar a interface rmi rpc


