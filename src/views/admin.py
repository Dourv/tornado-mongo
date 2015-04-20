#!/usr/bin/env python
# -*- coding: utf-8 -*-
import calendar
import config
import hashlib
import json
import os
import pymongo
import tornado
import base # Heredando de base para todas las vistas. 
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from models import get_form 

""" You can delete install class, if you comment or delete URL /Install """
class install(base.base):
	def get(self):
		data = {
			'form' : get_form().render('admin.admin()')
		}
		self._render('admin/install.html',data)

	def post(self):
		form = {
			'username':self.get_argument('username' ,None),
			'first_name': self.get_argument('first_name' ,None),		
			'last_name': self.get_argument('last_name' ,None),
			'email': self.get_argument('email' ,None),
			'password': self.get_argument('password' ,None),
			'password_confirm': self.get_argument('password_confirm' ,None),
			'rol': self.get_argument('rol', None)
		}
		_valid = get_form().validation('users.users()',form)
		if 'status' in _valid:
			if _valid['status'] == False:
				for message in _valid['errors']:
					self.set_message_error(message)
		else:
			self.set_message(_valid)
			rol_admin ={
				'name': 'admin',
				'block': True,
				'permissions' : list()
			}
			rol_user = {
				'name': 'user',
				'block': True,
				'permissions' : list()
			}


			for permission in config.permissions:
				self.db.permissions.insert(permission)
				rol_admin['permissions'].append(permission['name'])

			self.db.rols.insert(rol_admin)	
			self.db.rols.insert(rol_user)	


		self.redirect('/install')
			

class login(base.base):
	def get(self):
		if self.is_login() == False:
			datos = {
				'form': get_form().render('login.login()')
			}			

			self._render('admin/login.html',datos)
		else:
			self.set_message_error('Ya se encuentra logeado')
			return self.redirect('/')
				
	def post(self):
		form = {
			'username':self.get_argument('username' ,None),
			'password': self.get_argument('password' ,None),
		}	

		valid = get_form().validation('login.validation()',form)
		if 'status' in valid:
			if valid['status'] == False:
				for message in valid['errors']:
					self.set_message_error(message)
			else:
				self.set_loged_user(form['username'])
				self.set_message('Bienvenido(a) ' + form ['username'])
		

		self.redirect('/admin')


					

class home(base.base):	
	def get(self):
		if self.is_login():
			datos = {
				'active': 'home'
			}

			self._render('admin/index.html',datos)
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')	

class users(base.base):
	def get(self):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::view_users'):
				_get_form = get_form()
				#self.set_message('test get')	
				datos = {
					'form': _get_form.render('users.users()'),
					'users': self.db.users.find({})
				}
				self._render('admin/users.html',datos)
			else:
				self._render('admin/status/403.html')	
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')		

	def post(self):
		if self.is_admin():	
			if self.is_admin() or self.has_permission('admin::add_users'):
				_get_form = get_form()
				form = {
					'username':self.get_argument('username' ,None),
					'first_name': self.get_argument('first_name' ,None),		
					'last_name': self.get_argument('last_name' ,None),
					'email': self.get_argument('email' ,None),
					'password': self.get_argument('password' ,None),
					'password_confirm': self.get_argument('password_confirm' ,None),
					'rol': self.get_argument('rol', None)
				}
				_valid = _get_form.validation('users.users()',form)
				if 'status' in _valid:
					if _valid['status'] == False:
						for message in _valid['errors']:
							self.set_message_error(message)
				else:
					self.set_message(_valid)
				
			else:
				self.set_message_error('No puedes añadir usuarios usuarios.')
			
			self.redirect('/admin/users')		
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')	

class users_edit(base.base):
	def get(self,id):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::edit_users'):
				_get_form = get_form()
				datos = {
					'form': _get_form.render('users.users()',id),
					'users': self.db.users.find({})
				}

				self._render('admin/users.html',datos)
			else: 
				self._rebder('admin/status/403.html')	
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')		

	def post(self,id):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::edit_users'):
				_get_form = get_form()
				form = {
					'username':self.get_argument('username' ,None),
					'first_name': self.get_argument('first_name' ,None),		
					'last_name': self.get_argument('last_name' ,None),
					'email': self.get_argument('email' ,None),
					'password': self.get_argument('password' ,None),
					'password_confirm': self.get_argument('password_confirm' ,None),
					'rol': self.get_argument('rol', None),
					'id':self.get_argument('id' ,None)
				}
				_valid = _get_form.validation('users.users()',form,edit=True)
				if 'status' in _valid:
					if _valid['status'] == False:
						for message in _valid['errors']:
							self.set_message_error(message)
				else:
					self.set_message(_valid)
				self.redirect('/admin/users/edit/'+id)
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')			



class rols(base.base):
	def get(self):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::view_rols'):
				datos = {
					'form': get_form().render('rols.rols()'),
					'rols': self.db.rols.find()

				}
				self._render('admin/rols.html',datos)
			else:
				self._render('admin/status/403.html')	
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')	
					
	def post(self):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::add_rols'):
				form = {
					'rol_name': self.get_argument('rol_name',None)
				}

				for permission in self.db.permissions.find():
					form[permission['name']] = self.get_argument(permission['name'],None)

				_valid = get_form().validation('rols.rols()',form)

				if 'status' in _valid:
					if _valid['status'] == False:
						for message in _valid['errors']:
							self.set_message_error(message)
				else:
					self.set_message(_valid)
				
			else:
				self.set_message_error('No puedes añadir Roles.')

			self.redirect('/admin/rols')		
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')		


class rols_edit(base.base):
	def get(self,id):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::edit_rols'):
				_get_form = get_form()
				datos = {
					'form': _get_form.render('rols.rols()',id),
					'rols': self.db.rols.find()
				}

				self._render('admin/rols.html',datos)
			else:
				self._render('admin/status/403.html')	
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')			

	def post(self,id):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::edit_rols'):
				_get_form = get_form()
				form = {
					'rol_name':self.get_argument('rol_name' ,None),
					'id':self.get_argument('id' ,None)
				}	
				for permission in self.db.permissions.find():
					form[permission['name']] = self.get_argument(permission['name'],None)

				_valid = _get_form.validation('rols.rols()',form,edit=True)

				if 'status' in _valid:
					if _valid['status'] == False:
						for message in _valid['errors']:
							self.set_message_error(message)
					self.redirect('/admin/rols/edit/'+id)			
				else:
					self.set_message(_valid)
					self.redirect('/admin/rols')
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')				
			

class rols_delete(base.base):
	def get(self,id):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::delete_rols'):
				_get_form = get_form()
				data = self.db.rols.find_one({'_id':ObjectId(id)})
				
				deleted = _get_form.delete('rols.rols()',id)

				if deleted != False:
					self.set_message(deleted)
				else:
					self.set_message_error('No se puede eliminar un rol del core.')
			else:
				self.set_message_error('No puedes eliminar Rols')	
			self.redirect('/admin/rols')
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')		

class permissions(base.base):
	def get(self):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::view_permissions'):
				datos = {
					'form': get_form().render('permissions.permissions()'),
					'permissions': self.db.permissions.find().sort('name',1)
				}

				self._render('admin/permissions.html',datos)
			else:
				self._render('admin/status/403.html')	
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')			

	def post(self):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::add_permissions'):

				form = {
					'permission_name':self.get_argument('permission_name' ,None)
				}


				_valid = get_form().validation('permissions.permissions()',form)

				if 'status' in _valid:
					if _valid['status'] == False:
						for message in _valid['errors']:
							self.set_message_error(message)
				else:
					self.set_message(_valid)
			else:
				self.set_message_error('No puedes agregar nuevos permisos')		
			self.redirect('/admin/permissions')			
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')	
				
class permissions_edit(base.base):
	def get(self,id):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::edit_permissions'):
				_get_form = get_form()

				datos = {
					'form': _get_form.render('permissions.permissions()',id),
					'permissions': self.db.permissions.find().sort('name',1)
				}

				self._render('admin/permissions.html',datos)
			else:
				self._render('admin/status/403.html')	
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')	
					
	def post(self,id):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::edit_permissions'):
				form = {
					'permission_name':self.get_argument('permission_name' ,None),
					'id':self.get_argument('id' ,None)
				}	
				
				_valid = get_form().validation('permissions.permissions()',form,edit=True)

				if 'status' in _valid:
					if _valid['status'] == False:
						for message in _valid['errors']:
							self.set_message_error(message)
					self.redirect('/admin/permissions/edit/'+id)			
				else:
					self.set_message(_valid)
			else:
				self.set_message_error('No puedes editar permissions')
			self.redirect('/admin/permissions')		
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')	
				
class permissions_delete(base.base):
	def get(self,id):
		if self.is_login():
			if self.is_admin() or self.has_permission('admin::delete_permissions'):
				data = self.db.permissions.find_one({'_id':ObjectId(id)})
				
				deleted = get_form().delete('permissions.permissions()',id)

				if deleted != False:
					self.set_message(deleted)
				else:
					self.set_message_error('No puedes eliminar permisos del core')	
				
			else:
				self.set_message_error('No tienes permisos para eliminar permisos.')
			self.redirect('/admin/permissions')
		else:
			self.set_message_error('Debes estar logeado para acceder a este lugar')
			self.redirect('/login')		