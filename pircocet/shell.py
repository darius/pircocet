import pircocet.backend

class Client(object):
    def __init__(self, nick):
        self.nick = nick
    def send_msg(self, name, msg):
        return pircocet.backend.send(name, msg)
    def recv_msg(self, msg):
        print "%s <-- %s: %s" % (self.nick, msg['frm'].nick, msg['trail'])
