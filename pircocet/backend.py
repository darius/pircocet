import collections

names = {}
def register(name, client):
    if names.get(name):
        raise Exception("Nick taken")
    else:
        names[name] = client
def send(name, msg):
    recipient = names.get(name)
    if recipient:
        recipient.recv_msg(msg)
    else:
        if msg['cmd'] == "JOIN":
            names[name] = Channel(name)
            names[name].recv_msg(msg)
        else:
            raise Exception("No such nick/channel")

class Channel(object):
    def __init__(self, nick):
        self.nick = nick
        self.clients = []
    def recv_msg(self, msg):
        if msg['cmd'] == "JOIN":
            self.clients.append(msg['frm'])
        elif msg['cmd'] == "PRIVMSG":
            for c in [c for c in self.clients if c != msg['frm']]:
                c.recv_msg(msg)
        else:
            raise Exception("Unknown command", msg['cmd'])

Msg = lambda **kwargs: kwargs
