import pircocet.backend
import select
import socket
import sys

def serve(address="0.0.0.0", port=6667):
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((address, port))
    lsock.listen(1)
    inputs = [lsock, sys.stdin]
    while True:
        rs, ws, es = select.select(inputs, [], [])
        print rs, ws, es
        for r in rs:
            if r == lsock:
                conn, _ = lsock.accept()
                inputs.append(Client(conn))
            else:
                data = r.recv(1024 * 16)
                ms, rest = parse(r.buf + data)
                for m in ms:
                    r.handle(m)
                r.buf = rest

def parse(lump):
    splits = lump.split("\r\n")
    return [parse_msg(s) for s in splits[:-1] if s], splits[-1]

def parse_msg(s):
    pre = ""
    if s.startswith(":"):
        end_of_pre = s.find(" ")
        if end_of_pre == -1:
            return None
        pre = s[1:end_of_pre]
        s = s[end_of_pre + 1:]

    end_of_cmd = s.find(" ")
    if end_of_cmd == -1:
        return None
    cmd = s[:end_of_cmd]
    s = s[end_of_cmd + 1:]

    argstring, _, trail = s.partition(":")
    return pircocet.backend.Msg(pre=pre, cmd=cmd, args=argstring.split(), trail=trail)

def unparse(msg):
    s = ""
    if msg.frm:
        s += ":" + msg.frm
    s += " " + msg.cmd
    if msg.args:
        s += " " + " ".join(msg.args)
    if msg.trail:
        s += " :" + msg.trail
    return s

class Client(object):
    def __init__(self, conn):
        self.buf = ""
        self.conn = conn
    def handle(self, msg):
        if msg.cmd == "NICK":
            nick = msg.args[0]
            pircocet.backend.register(nick, self)
            self.nick = nick
        elif msg.cmd == "PRIVMSG":
            self.send_msg(msg.args[0], msg)
        else:
            raise Exception("Unknown command", msg.cmd)
    def send_msg(self, name, msg):
        msg.frm = self
        return pircocet.backend.send(name, msg)
    def recv_msg(self, msg):
        print "%s <-- %s" % (self.nick, msg)
    def send(self, data):
        return self.conn.send(data)
    def recv(self, size):
        return self.conn.recv(size)
    def fileno(self):
        return self.conn.fileno()
