#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from pymongo import MongoClient
from validate_email import validate_email
from views.base import base 
import config
import hashlib

class rols():
	@property
	def db(self):
		if config.debug == True:
			client = MongoClient('localhost', 27017)
		else: 
			client = MongoClient('mongodb://'+config.__user+':'+config.__psw+'@'+config.__host, config.__port)	
		return client[config.database]

	def form(self):
		form = {'config' : {
				'method': 'POST',
				'action' : '/admin/rols',
				'class' : 'form-horizontal',
				'error-class' : ''},
			'fields': [{
					'required':True,
					'widget': 'text',
					'attributes': {
						'data-hint' : 'Escriba el nombre del rol',
						'class': 'form-control floating-label',
						'placeholder': 'Nombre del Rol',
						'name': 'rol_name'
					}, 
					'form-group-class': 'col-md-12'
					
				}]
		}

		permissions = self.db.permissions.find()

		for permission in permissions:
			name = permission['name']
			field = {
				'widget': 'checkbox',
				'attributes' : {
					'name': name,
					'class': 'checkbox'

				},
				'form-group-class': 'col-md-4'
			}

			form['fields'].append(field)

		
		submit = {
					'widget':'submit',
					'attributes':{
						'name': 'submit',
						'class': 'btn btn-primary', 
						'value': 'Crear nuevo rol'
					},
					'form-group-class': 'col-md-6'
				}	

		form['fields'].append(submit)		

		return form

	def form_edit(self, id):
		data = self.db.rols.find_one({'_id': ObjectId(id)})
		print data
		form = {'config' : {
				'method': 'POST',
				'action' : '/admin/rols/edit/'+id,
				'class' : 'form-horizontal',
				'error-class' : ''},
			'fields': [{
					'required':True,
					'widget': 'text',
					'attributes': {
						'data-hint' : 'Escriba el nombre del rol',
						'class': 'form-control floating-label',
						'placeholder': 'Nombre del Rol',
						'name': 'rol_name',
						'value': data['name']
					}, 
					'form-group-class': 'col-md-12'
				},
				{
					'widget':'hidden',
					'attributes':{
						'value': id,
						'name':'id'
					}
				}

			]
		}

		permissions = self.db.permissions.find()

		for permission in permissions:
			name = permission['name']
			field = {
				'widget': 'checkbox',
				'attributes' : {
					'name': name,
					'class': 'checkbox'
				},
				'form-group-class': 'col-md-4'
			}
			if name in data['permissions']:
				field['attributes']['checked'] = 'True'

			form['fields'].append(field)

		
		submit = {
					'widget':'submit',
					'attributes':{
						'name': 'submit',
						'class': 'btn btn-primary', 
						'value': 'Guardar'
					},
					'form-group-class': 'col-md-6'
				}		

		form['fields'].append(submit)		

		return form

	
	def validation(self,data,edit=False):
		validation = {'status':True, 'errors': list() }
		if 'rol_name' in data:		
			if len(data['rol_name']) < 3:
				validation['status'] = False
				validation['errors'].append('El Nombre del rol debe poseer al menos 3 caracteres')		
			else:
				rol = self.db.rols.find_one({'name':data['rol_name']})
				if rol != None and data['id'] != str(rol['_id']) :
					validation['status'] = False
					validation['errors'].append('El nombre de rol ya esta siendo utilizado')

		else:
			validation['status'] = False
			validation['errors'].append('El campo nombre del rol es Obligatorio.')

		if edit == True:
			_q = self.db.rols.find_one({'_id':ObjectId(data['id'])})
			if _q == None:	
				validation['status'] = False
				validation['errors'].append('El id de rol a editar no existe.')


		if validation['status'] == True:
			if edit == False:
				self.insert(data)
				return 'Nuevo rol '+data['rol_name']+' Creado'	
			else: 
				return self.edit(data)
		else: 
			return validation	

	def insert(self,data):
		_INSERT ={
			'name': data['rol_name'],
			'permissions': list()
		}

		for permission in self.db.permissions.find().sort('name',1):
			if data[permission['name']] == 'on':
				_INSERT['permissions'].append(permission['name'])

		return self.db.rols.insert(_INSERT)


	def edit(self,data):
		old_data = self.db.rols.find_one({'_id':ObjectId(data['id'])})

		if 'block' in old_data:
			return {'status':False,'errors':['Este rol esta bloqueado no puede ser editado.']}	
		else:	
			new_data = {
				'name' : data['rol_name'],
				'_id' : ObjectId(data['id']),
				'permissions': list()
			}
			for permission in self.db.permissions.find().sort('name',1):
				if data[permission['name']] == 'on':
					new_data['permissions'].append(permission['name'])


			self.db.rols.update(old_data,new_data)
			return 'Rol '+old_data['name']+' editado correctamente.'

	def delete(self, id):
		data = self.db.rols.find_one({'_id':ObjectId(id)})

		if data != None:
			if 'block' in data and data['block'] == True:
				return False
			else:
				self.db.rols.remove(data)

				users = self.db.users.find()
				for user in users:
					tmp = user
					if data['name'] == user['rol']:
						tmp['rol'] = 'User'

					self.db.users.update({'_id':user['_id']},tmp)	
					return 'Eliminado rol '+ data['name']
						

				