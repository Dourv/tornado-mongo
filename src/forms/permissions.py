#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from pymongo import MongoClient
from validate_email import validate_email
from views.base import base 
import config
import hashlib

class permissions():
	@property
	def db(self):
		if config.debug == True:
			client = MongoClient('localhost', 27017)
		else: 
			client = MongoClient('mongodb://'+config.__user+':'+config.__psw+'@'+config.__host, config.__port)	
		return client[config.database]

	def form(self):
		form = {
			'config' : {
				'method': 'POST',
				'action' : '/admin/permissions',
				'class' : 'form-horizontal',
				'error-class' : ''
			},
			'fields': [
				{
					'required':True,
					'widget':'text',
					'attributes': {
						'data-hint':'Escriba el nombre del permiso',
						'name': 'permission_name',
						'placeholder': 'Nombre del Permiso',
						'class': 'form-control floating-label',
					},	
					'form-group-class': 'col-md-12',
				},
				{
	
					'widget':'submit',
					'attributes':{
						'name': 'submit',
						'class': 'btn btn-primary', 
						'value': 'Crear Permiso'
					},
					'form-group-class': 'col-md-6'

				}
			]
		}
		return form

	def form_edit(self,id):
		data = self.db.permissions.find_one({'_id':ObjectId(id)})
		print str(data['name']).decode('utf-8')
		form = {
			'config' : {
				'method': 'POST',
				'action' : '/admin/permissions/edit/'+id,
				'class' : 'form-horizontal',
				'error-class' : ''
			},
			'fields': [
				{
					'required':True,
					'widget':'text',
					'attributes': {
						'data-hint' :'Escriba el nombre del permiso',
						'class': 'form-control floating-label',
						'name': 'permission_name',
						'placeholder': 'Nombre del Permiso',
						'value': data['name']
					},	
					'form-group-class': 'col-md-12'
				},
				{
	
					'widget':'submit',
					'attributes':{
						'name': 'submit',
						'class': 'btn btn-primary', 
						'value': 'Guardar Permiso'
					},
					'form-group-class': 'col-md-6'

				},
				{
					'widget':'hidden',
					'attributes': {
						'name':'id',
						'value': id
					}
				}

			]
		}
		return form	

	
	def validation(self,data,edit=False):
		validation = {'status':True, 'errors': list() }
		if 'permission_name' in data:		
			if len(data['permission_name']) < 3:
				validation['status'] = False
				validation['errors'].append('El Nombre del permiso debe poseer al menos 3 caracteres')	


			permission = self.db.permissions.find_one({'name': data['permission_name']})
			if permission != None and edit == False:
				validation['status'] = False
				validation['errors'].append('Este permiso ya existe')
			else:
				if edit == True and permission != None:
					if str(data['id']) != str(permission['_id']):
						validation['status'] = False
						validation['errors'].append('Este permiso ya existe')


		else:
			validation['status'] = False
			validation['errors'].append('El campo nombre del permiso es Obligatorio.')

		if edit == True:
			_q = self.db.permissions.find_one({'_id':ObjectId(data['id'])})
			if _q == None:	
				validation['status'] = False
				validation['errors'].append('El id de permiso a editar no existe.')


		if validation['status'] == True:
			if edit == False:
				self.insert(data)
				return 'Nuevo Permiso Creado'	
			else: 
				return self.edit(data)
		else: 
			return validation	

	def insert(self,data):
		_INSERT = {
			'name': data['permission_name'],
		}	
		self.db.permissions.insert(_INSERT)		

	def edit(self,data):
		old_data = self.db.permissions.find_one({'_id':ObjectId(data['id'])})

		if 'block' in old_data and old_data['block'] == True:
			return {'status':False, 'errors':['Este Permiso no puede ser editado.']}
		else:	
			new_data = {
				'name' : data['permission_name'],
				'_id' : ObjectId(data['id'])
			}

			self.db.permissions.update(old_data,new_data)
			return 'Permiso '+old_data['name']+' editado correctamente.'


	def delete(self,id):

		data = self.db.permissions.find_one({'_id':ObjectId(id)})

		if data != None:
			if 'block' in data and data['block'] == True:
				return False
			else:	
				self.db.permissions.remove(data)

				rols = self.db.rols.find()
				for rol in rols:
					tmp = rol
					if data['name'] in rol['permissions']:
						for x in range(0,len(rol['permissions'])):
							if rol['permissions'][x] == data['name']:
								rol['permissions'].pop(x)
								print x
								break
					self.db.rols.update({'_id':rol['_id']},tmp)			

				return 'Eliminado '+data['name']