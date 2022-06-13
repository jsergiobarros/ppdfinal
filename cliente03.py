import threading

from client import Client
from server import Server
#server = threading.Thread(target=lambda: Server.start_server(host='127.0.0.1'))
#server.start()
CLIENTE = Client(('192.168.0.12', 5050))
CLIENTE._out(("spy", "mensagem publica", "nome:xico"))
#CLIENTE._out(('mensagens', 0, 0))
#print(type(CLIENTE._rd(('usuarios', 0, str))))
"""while True:
    mensagem = CLIENTE._in(("spy", "mensagem publica", str))
    print(mensagem)
    indice = CLIENTE._in(("mensagens", 0, int))
    print(indice)
    CLIENTE._out(("mensagens", 0, indice + 1))
    CLIENTE._out(("mensagens", indice + 1, mensagem))"""

