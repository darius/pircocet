import collections

names = {}
def register(name, client):
    if name in names:
        raise Exception("Nick taken")
    else:
        names[name] = client
def send(name, msg):
    recipient = names.get(name)
    if recipient:
        recipient.recv_msg(msg)
    else:
        if msg.cmd == "JOIN":
            names[name] = Channel(name)
            names[name].recv_msg(msg)
        else:
            raise Exception("No such nick/channel")

class Channel(object):
    def __init__(self, nick):
        self.nick = nick
        self.clients = []
    def recv_msg(self, msg):
        if msg.cmd == "JOIN":
            self.clients.append(msg.frm)
            # XXX add: for c in self.clients: c.recv_msg(msg)?
        elif msg.cmd == "PRIVMSG":
            for c in [c for c in self.clients if c != msg.frm]:
                c.recv_msg(msg)
        else:
            raise Exception("Unknown command", msg.cmd)

class Msg:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
