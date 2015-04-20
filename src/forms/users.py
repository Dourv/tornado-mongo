#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from pymongo import MongoClient
from validate_email import validate_email
from views.base import base 
import config
import hashlib

''' 
forms constructor.

* Es necesario crear una variable tipo dict() que debe llevar la siguiente estructura.
	{
		'config(requerido)':{
			'method(requerido)': 'valores POST o GET',
			'action(requerido)': 'url para enviar la data',
			'class' : 'Clases de css',
			'error-class': 'Clase para el error'
		},
		fields(requerido): [
			{
				'name(requerido)': 'nombre del campo',
				'widget(requerido)': 'Tipo de input',
				'class': 'Clases de css',
				'id': 'Valor del ID',
				'label'(*Requiere que el ID del campo este seteado.): {
					'attributes': 'Cualquier otro valor que no este disponible. ejemplo: data-*= "" ',
					'class': 'Clases de css'
				}
				'placeholder': 'Valor del placeholder',
				'required': 'Valores True o False',
				'value': 'valor default del campo.'
			}
		]

	}
'''

class users(): 
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
				'action' : '/admin/users',
				'class' : 'form-horizontal',
				'error-class' : ''
			},
			'fields': [
				{
					'name': 'username',
					'placeholder': 'Username',
					'required':True,
					'widget':'text',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Por favor escriba el usuario que usara para ingresar"'
				},
				{
					'name': 'first_name',
					'placeholder': 'Nombre',
					'required':True,
					'widget':'text',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Escriba el nombre del usuario"'
				},
				{
					'name': 'last_name',
					'placeholder': 'Last Name',
					'required':True,
					'widget':'text',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Escriba el apellido del usuario"'
				},
				{
					'name': 'email',
					'placeholder': 'Email',
					'required':True,
					'widget':'email',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Escriba el correo electronico del Usuario"'
				},
				{
					'name': 'rol',
					'required':True,
					'widget':'select',
					'class': 'form-control',
					'label_class':'col-lg-1 control-label',
					'form-group-class': 'col-md-12',
					'placeholder' : 'Seleccione un Rol de Usuario',
					'options': list()
				},
				{
					'name': 'password',
					'placeholder': 'Password',
					'required':True,
					'widget':'password',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Escriba la contraseña para el usuario"',
				},
				{
					'name': 'password_confirm',
					'placeholder': 'Confirm Password',
					'required':True,
					'widget':'password',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Confirme la contraseña del usuario"'
				},
				{
					'name': 'submit', 
					'class': 'btn btn-primary',
					'widget':'submit',
					'value': 'Añadir usuario',
					'form-group-class': 'col-md-12',
					'reset': {
						'value':'Limpiar Formulario',
						'class':'btn btn-default'
					}
				}
			]
		}

		rols = self.db.rols.find()

		for rol in rols:
			data ={
				'name':rol['name']
			}
			_form['fields'][4]['options'].append(data)

		return _form	

		
	def form_edit(self,id):
		user = self.db.users.find_one({'_id':ObjectId(id)})
		_form = {
			'config' : {
				'method': 'POST',
				'action' : '/admin/users/edit/'+id,
				'class' : 'form-horizontal',
				'error-class' : ''
			},
			'fields': [
				{
					'name': 'username',
					'placeholder': 'Username',
					'value': user['username'],
					'required':True,
					'widget':'text',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Por favor escriba el usuario que usara para ingresar"'
				},
				{
					'name': 'first_name',
					'placeholder': 'Nombre',
					'value': user['first_name'],
					'required':True,
					'widget':'text',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Escriba el nombre del usuario"'
				},
				{
					'name': 'last_name',
					'placeholder': 'Last Name',
					'value': user['last_name'],
					'required':True,
					'widget':'text',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Escriba el apellido del usuario"'
				},
				{
					'name': 'email',
					'placeholder': 'Email',
					'value': user['email'],
					'required':True,
					'widget':'email',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Escriba el correo electronico del Usuario"'
				},
				{
					'name': 'rol',
					'required':True,
					'widget':'select',
					'class': 'form-control',
					'label_class':'col-lg-1 control-label',
					'form-group-class': 'col-md-12',
					'placeholder' : 'Seleccione un Rol de Usuario',
					'options': list()
				},
				{
					'name': 'password',
					'placeholder': 'Password',
					'widget':'password',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Escriba la contraseña para el usuario"',
				},
				{
					'name': 'password_confirm',
					'placeholder': 'Confirm Password',
					'widget':'password',
					'class': 'form-control floating-label',
					'form-group-class': 'col-md-12',
					'attributes': 'data-hint="Confirme la contraseña del usuario"'
				},
				{
					'name':'id',
					'widget':'hidden',
					'value': id
				},
				{
					'name': 'submit', 
					'class': 'btn btn-primary',
					'widget':'submit',
					'value': 'Añadir usuario',
					'form-group-class': 'col-md-12',
					'reset': {
						'value':'Limpiar Formulario',
						'class':'btn btn-default'
					}
				}
			]
		}

		rols = self.db.rols.find()

		for rol in rols:
			data ={
				'name':rol['name'],
				'selected': False
			}

			if user['rol'] == rol['name']:
				print user['rol']
				print rol['name']
				data['selected'] = True
			_form['fields'][4]['options'].append(data)

		return _form	

	def validation(self,data,edit=False):
		form = self.form()
		validation = {'status':True, 'errors': list() }
		
		if 'username' in data:		
			user = self.db.users.find_one({'username': data['username']})
			if len(data['username']) < 3:
				validation['status'] = False
				validation['errors'].append('El campo nombre debe poseer al menos 3 caracteres.')		

			if user != None:
				if edit == False:
					validation['status'] = False
					validation['errors'].append('El nombre de usuario ya existe.')
				else:
					if data['id'] != str(user['_id']):
						validation['status'] = False
						validation['errors'].append('El nombre de usuario ya existe.')					
		else:
			validation['status'] = False
			validation['errors'].append('El campo nombre es Obligatorio.')

		if 'first_name' in data:		
			if len(data['first_name']) < 3:
				validation['status'] = False
				validation['errors'].append({'field':'first_name','value':'El campo nombre debe poseer al menos 3 caracteres.'})		
		else:
			validation['status'] = False
			validation['errors'].append('El campo nombre es Obligatorio.')		

		if 'last_name' in data:		
			if len(data['last_name']) < 3:
				validation['status'] = False
				validation['errors'].append('El campo Apellido debe poseer al menos 3 caracteres.')		
		else:
			validation['status'] = False
			validation['errors'].append('El campo Apellido es Obligatorio.')		
		
		if 'email' in data:	
			if validate_email(data['email']) == False:
				validation['status'] = False
				validation['errors'].append('Inserte un email valido.')		
			else:
				if edit == False:
					if self.db.users.find_one({'email':data['email']}) != None:
						validation['status'] = False
						validation['errors'].append('Ya existe un usuario con este email.')		
				else:
					email = self.db.users.find_one({'email':data['email']})
					print data['id']
					print str(email['_id'])
					if email != None and data['id'] != str(email['_id']):
						validation['status'] = False
						validation['errors'].append('Otro usuario ya tiene este email.')	



					
		else:
			validation['status'] = False
			validation['errors'].append('El campo Email es Obligatorio.')

		if 'rol' in data:
			rols = self.db.rols.find_one({'name':data['rol']})
			if rols == None:
				if self.db.users.find().count() <= 0:
					if data['rol'] != 'admin':
						validation['status'] = False
						validation['errors'].append('El Primer usuario debe ser Admin')
						
				else:	
					validation['status'] = False
					validation['errors'].append('Seleccione un rol valido')

		password = False
		if len(data['password']) > 0:
			password = True
			if len(data['password']) < 4:
				validation['status'] = False		
				validation['errors'].append('La Contraseña debe tener al menos 4 Caracteres')
				password = False

		if password == True:
			if data['password_confirm'] != data['password']:
				validation['status'] = False		
				validation['errors'].append('Las Contraseñas no coinciden')	  		


		if validation['status'] == True:
			if edit == False:
				if self.db.users.find().count() <= 0:
					self.insert(data,admin=True)
				else: 	
					self.insert(data)
				return 'Nuevo usuario '+data['username']+' Creado'	
			else: 
				return self.edit(data)
		else: 
			return validation			

	def insert(self,data,admin=False):
		_INSERT = {
			'username': data['username'].lower(),
			'first_name': data['first_name'],
			'last_name': data['last_name'],
			'email': data['email'],
			'password': hashlib.md5(data['password']).hexdigest(),
			'rol' : data['rol'],
			'status' : True
		}	

		if admin == True:
			_INSERT['block'] = True

		self.db.users.insert(_INSERT)

	def edit(self, data):
		old_data = self.db.users.find_one({'_id':ObjectId(data['id'])})

		new_data = {
			'username': data['username'].lower(),
			'first_name': data['first_name'],
			'last_name': data['last_name'],
			'email': data['email'],
			'password': hashlib.md5(data['password']).hexdigest(),
			'rol' : data['rol'],
			'status' : old_data['status']
		}	

		if new_data['rol'] == 'admin':
			new_data['block'] = True



		self.db.users.update(old_data,new_data)

		return 'Usuario '+old_data['first_name'] + ' ' + old_data['last_name'] +' editado correctamente.' 	

