#!/usr/bin/python
# _*_ coding:utf-8 _*_

from os import getcwd,getuid,_exit
from os.path import exists
from sys import path,argv,exit,version,version_info
path.insert(0,getcwd() + '/src/')
path.insert(0,getcwd() + '/src/core/')
path.insert(0,getcwd() + '/src/modules/')
path.insert(0,getcwd() + '/src/lib/')
from commands import getoutput
# module loading
from src.modules import ddos,scanner,sniffer,services
import config
import database
from core import colors
import platform
import util
import stream
import parse_cmd
import importlib
import session_manager
try:
	# load py2.7 stuff here so we can get to the depends check
	import parse_cmd
	import importlib
	import session_manager
	import stream
except:
	pass

class LoadeModules:
	"""
	load modules
	"""
	def __init__(self):
		self.total = 0
		self.ddos = []
		self.sniffer = []
		self.scanner = []
		self.services = []

	def load(self):
		"""
		load modules.verify the module loads successfully before
		loading it up into the module list;this prevents
		crashes related to unment dependencies.
		"""
		for module in ddos.__all__:
			if util.check_dependency('src.modules.ddos.%s' % module):
				mod = getattr(importlib.import_module(
					'src.modules.ddos.%s' % module,'ddos'),
					module)
				self.ddos.append(mod)
				self.total += 1
		
		for module in sniffer.__all__:
			if util.check_dependency('src.modules.sniffer.%s' % module):
				mod = getattr(importlib.import_module(
					'src.modules.sniffer.%s' % module,'sniffer'),
					module)
				self.sniffer.append(mod)
				self.total += 1
		
		for module in scanner.__all__:
			if util.check_dependency('src.modules.scanner.%s' % module):
				mod = getattr(importlib.import_module(
					'src.modules.scanner.%s' % module,'scanner'),
					module)
				self.scanner.append(mod)
				self.total += 1
		
		for module in services.__all__:
			if util.check_dependency('src.modules.services.%s' % module):
				mod = getattr(importlib.import_module(
					'src.modules.services.%s' % module,'services'),
					module)
				self.services.append(mod)
				self.total += 1

def main():
	"""
	donghuangzhong entry point
	"""

	#set up configuration
	config.initialize()

	#set up database
	database.initialize()

	#load modules
	loader = LoadeModules()
	loader.load()
	util.Msg('Loaded %d modules.' % loader.total)

	#handle command line option first
	if len(argv) > 1:
		parse_cmd.parse(argv,loader)
	#menus
	main_menu = ['DDos Attacks','Sniffers','Scanners','Services']

	running = True
	choice = -1
	while running:
		util.header()
		choice = util.print_menu(main_menu)
		if choice == 0:
			#check if they've got running sessions!
			cnt = stream.get_session_count()
			if cnt >0 :
				dispaly = color.B_YELLOW +'You hanve %d sessions running.' +\
					'Are you sure?' +color.B_GREEN +'['+color.B_YELLOW +\
					'Y' + color.B_GREEN + '/' +color.B_YELLOW +'n' +\
					color.B_GREEN +']' +color.END
				choice = raw_input(dispaly % cnt)
				if 'y' in choice.lower() or choice == '':
					util.Msg('Shutting all sessions down ...')
					stream.stop_session('all',-1)
					running = False
			else:
				util.debug("Exiting with session count:%s" % (cnt))
				util.Msg("Exiting...")
				running = False
			#remove donghuangzhong temporary directory
			util.init_app('rm -fr /tem/.donghuangzhong/')
			#recheck that all sessions are down
			cnt = stream.get_session_count()
			if cnt <= 0:
				#some libs dont clean up their own threads,so
				#we need to hard quit thoes to avoid hanging;FIXME
				_exit(1)
		
		elif choice == 1:
			while True:
				choice = util.print_menu([x().which for x in loader.ddos])
				if choice == 0:
					break;
				elif choice == -1:
					pass
				elif choice > len(loader.ddos):
					continue
				else:
					stream.initialize(loader.ddos[choice - 1])		
		
		elif choice == 2:
			while True:
				choice = util.print_menu([x().which for x in loader.sniffer])
				if choice == 0:
					break;
				elif choice == -1:
					pass
				elif choice > len(loader.sniffer):
					continue
				else:
					stream.initialize(loader.sniffer[choice - 1])
				
		elif choice == 3:
			while True:
				choice = util.print_menu([x().which for x in loader.scanner])
				if choice == 0:
					break;
				elif choice == -1:
					pass
				elif choice > len(loader.scanner):
					continue
				else:
					stream.initialize(loader.scanner[choice - 1])
		elif choice == 4:
			while True:
				choice = util.print_menu([x().which for x in loader.services])
				if choice == 0:
					break;
				elif choice == -1:
					pass
				elif choice > len(loader.services):
					continue
				else:
					stream.initialize(loader.services[choice - 1])		
		elif choice == -1:
			pass

#Application entry;dependency checks,etc.
if __name__ == "__main__":
	#perm check
	if int(getuid()) > 0:
		util.Error('please run as root.')
		_exit(1)

	#check python version
	if version_info[1] < 7:
		util.Error('donghuangzhong must be run with Pyton 2.7.x. You are currently using %s' % version)
		_exit(1)

	#check for forwarding
	system = platform.system().lower()
	if system == 'darwin':
		if not getoutput('sysctl -n net.inet.ip.forwarding') == '1':
			util.Msg('IPv4 forwarding disabled. Enabling..')
			tmp = getoutput(
				'sudo sh -c \'sysctl -w net.inet.ip.forwarding=1\'')
			if 'not permitted' in tmp:
				util.Error('Error enabling IPv4 forwarding.')
				exit(1)
	elif system == 'linux':
		if not getoutput('cat /proc/sys/net/ipv4/ip_forward') == '1':
			util.Msg('IPv4 forwarding disabled.Enabling..')
			tmp = getoutput(
				'sudo sh -c \'echo "1" >/proc/sys/net/ipv4/ip_forward\'')
			if len(tmp) > 0:
				util.Error('Error enabling IPv4 forwarding.')
				exit(1)
	else:
		util.Error('Unknow operating system.Cannot IPv4 forwarding.')
		exit(1)
	# create tmpporary directory for donghuangzhong to stash stuff
	if exists("/tem/.donghuangzhong"):
		util.init_app("rm -fr /tem/.donghaungzhong")
	util.init_app("mkdir /tem/.donghuangzhong")

	main()	
