#!/usr/bin/env python
# -*- encoding: utf8 -*-
import sys
sys.dont_write_bytecode = True

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

import storage
import modules

class TechBot(irc.bot.SingleServerIRCBot):
	# cheat sheet
	# self.disconnect -> disconnects
	# self.die() -> dies
	# e -> event??
	# self.connection -> c
	# c.notice(nick, msg)
	# self.channels -> list of channel objects

	def __init__(self, channel, nickname, server, port=6667):
		irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
		self.channel = channel

	def on_nicknameinuse(self, c, e):
		c.nick('_' + c.get_nickname() + '_')

	def on_welcome(self, c, e):
		c.join(self.channel)

	def on_privmsg(self, c, e):
		self.do_command(e, e.arguments[0])

	def on_pubmsg(self, c, e):
		message = e.arguments[0]
		#a = e.arguments[0].split(":", 1)
		#if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
		#	self.do_command(e, a[1].strip())
		#return

	def on_dccmsg(self, c, e):
		# non-chat DCC messages are raw bytes; decode as text
		text = e.arguments[0].decode('utf-8')
		c.privmsg("You said: " + text)

	def on_dccchat(self, c, e):
		if len(e.arguments) != 2:
			return
		args = e.arguments[1].split()
		if len(args) == 4:
			try:
				address = ip_numstr_to_quad(args[2])
				port = int(args[3])
			except ValueError:
				return
			self.dcc_connect(address, port)

	#def do_command(self, e, cmd):
	#nick = e.source.nick
	#c = self.connection

	#if cmd == "disconnect":
	#	self.disconnect()
	#elif cmd == "die":
	#	self.die()
	#elif cmd == "stats":
	#	for chname, chobj in self.channels.items():
	#		c.notice(nick, "--- Channel statistics ---")
	#		c.notice(nick, "Channel: " + chname)
	#		users = sorted(chobj.users())
	#		c.notice(nick, "Users: " + ", ".join(users))
	#		opers = sorted(chobj.opers())
	#		c.notice(nick, "Opers: " + ", ".join(opers))
	#		voiced = sorted(chobj.voiced())
	#		c.notice(nick, "Voiced: " + ", ".join(voiced))
	#elif cmd == "dcc":
	#	dcc = self.dcc_listen()
	#	c.ctcp("DCC", nick, "CHAT chat %s %d" % (
	#		ip_quad_to_numstr(dcc.localaddress),
	#		dcc.localport))
	#else:
	#	c.notice(nick, "Not understood: " + cmd)

def main():
	channel = '#Technocrat'
	nickname = 'TechBot_'
	server = 'irc.broke-it.com'
	port = 6667

	bot = TechBot(channel, nickname, server, port)
	bot.start()

if __name__ == "__main__":
	main()