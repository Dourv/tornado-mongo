#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import tornado
import tornado.autoreload
import tornado.ioloop
import tornado.web
from views import admin, web


def urls():
	_url = [
		#Comentar la siguiente linea, si no quieres disponible la vista de configuración 
		(r"/install/?", admin.install ),


		(r"/login/?", admin.login ),
		(r'/admin/static/(.*)', tornado.web.StaticFileHandler, {'path': config.root+'/templates/admin/static'}),
		(r"/admin/?", admin.home),
		(r"/admin/users/?", admin.users),
		(r"/admin/users/edit/(\w+?)/?", admin.users_edit),
		(r"/admin/rols/?", admin.rols),
		(r"/admin/rols/edit/(\w+?)/?",admin.rols_edit),
		(r"/admin/rols/delete/(\w+?)/?",admin.rols_delete),
		(r"/admin/permissions/?", admin.permissions),
		(r"/admin/permissions/edit/(\w+?)/?",admin.permissions_edit),
		(r"/admin/permissions/delete/(\w+?)/?",admin.permissions_delete),

		(r'/theme/static/(.*)', tornado.web.StaticFileHandler, {'path': config.root+'/templates/theme/static'}),
		(r"/", web.home)
	]

	return _url