from pircocet.backend import register, Msg
import pircocet.shell
import pircocet.irc

alan = pircocet.shell.Client("alan")
register("alan", alan)
matt = pircocet.shell.Client("matt")
register("matt", matt)
margo = pircocet.shell.Client("margo")
register("margo", margo)

try: register("alan", margo)   # same nick twice should fail
except Exception: pass
else: assert False

alan.send_msg("#hs", Msg(frm=alan, cmd="JOIN", args=["#hs"], trail=""))
matt.send_msg("#hs", Msg(frm=matt, cmd="JOIN", args=["#hs"], trail=""))
margo.send_msg("#hs", Msg(frm=margo, cmd="JOIN", args=["#hs"], trail=""))

alan.send_msg("#hs", Msg(frm=alan, cmd="PRIVMSG", args=["#hs"], trail="sup hackerschool channel"))

matt.send_msg("alan", Msg(frm=matt, cmd="PRIVMSG", args=["alan"], trail="this is topsecret alan"))
margo.send_msg("matt", Msg(frm=margo, cmd="PRIVMSG", args=["matt"], trail="this is also topsecret"))
