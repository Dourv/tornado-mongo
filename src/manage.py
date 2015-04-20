#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from tornado.options import define, parse_command_line
from urls import urls
import config
import os
import tornado
import tornado.autoreload
import tornado.ioloop
import tornado.web
import views

# define("debug", default =True, help="Corriendo en modo desarrollo", type=bool)
# define("port", default =8000, help="Corriendo el puerto dado", type=int)

application = tornado.web.Application(urls(),debug=config.debug,cookie_secret="0d29a0f932228f674ba3ace8dbec4c2c",default_handler_class=views.base.no_found)

if __name__ == "__main__":
	print("---- SERVIDOR INICIADO ---")
	parse_command_line()



	if config.debug == False:
		application.connect =  MongoClient('mongodb://'+config.user+':'+config.psw+'@'+config.host, config.port)
	else: 
		application.connect =  MongoClient('localhost', config.port)	
	


	application.listen(8888)

	tornado.autoreload.start()
	for dir, _, files in os.walk('templates'):
		[tornado.autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]


	tornado.ioloop.IOLoop.instance().start()