#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from pymongo import MongoClient
from validate_email import validate_email
from views.base import base 
import config
import hashlib


class login():
	@property
	def db(self):
		if config.debug == True:
			client = MongoClient('localhost', 27017)
		else: 
			client = MongoClient('mongodb://'+config.__user+':'+config.__psw+'@'+config.__host, config.__port)	
		return client[config.database]

	def form(self):
		_form = {
			'config' : {
				'method': 'POST',
				'action' : '/login',
				'class' : 'form-horizontal',
				'error-class' : ''
			},
			'fields': [
				{
					'required':True,
					'widget':'text',
					'attributes': {
						'class': 'form-control floating-label',
						'data-hint': 'Por favor escriba el usuario para ingresar',
						'id' : 'username',
						'name': 'username',
						'placeholder': 'Username'
					},
					'form-group-class': 'col-md-12'
				},
				{
					'required':True,
					'widget':'password',
					'attributes':  {
						'class': 'form-control floating-label',
						'data-hint': 'Escriba su contraseña de usuario',
						'form-group-class': 'col-md-12',
						'id': 'contraseña',
						'name': 'password',
						'placeholder': 'Contraseña'
					},
					'form-group-class': 'col-md-12'	
				},
				{
					'widget':'submit',
					'attributes':{
						'name': 'submit',
						'class': 'btn btn-primary', 
						'value': 'Ingresar'
					},
					'form-group-class': 'col-md-6'					
				},	

				{
					'widget':'reset',
					'attributes':{
						'name': 'submit',
						'class': 'btn btn-default', 
						'value': 'Limpiar formulario'
					},
					'form-group-class': 'col-md-6'					
				}	
			]	
		}
		return _form

	def validation(self,data,edit):
		_validation = { 'status': True,'errors': list()}

		user = self.db.users.find_one({'username': data['username'].lower()})

		if user == None:
			_validation['status'] = False
			_validation['errors'].append('El nombre de usuario no existe')
		else:
			password = hashlib.md5(data['password']).hexdigest()
			if password != user['password']:
				_validation['status'] = False
				_validation['errors'].append('La contraseña es invalida')
					
		if user['status'] == False:
			_validation['status'] = False
			_validation['errors'].append('Usuario Inactivo por favor contacte con el administrador')	

		print _validation
		return _validation	
				



