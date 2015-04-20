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

class admin(): 
	@property
	def db(self):
		if config.debug == True:
			client = MongoClient('localhost', 27017)
		else: 
			client = MongoClient('mongodb://'+config.__user+':'+config.__psw+'@'+config.__host, config.__port)	
		return client[config.database]




	def user_form(self):
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

	def form(self):
		form = self.user_form()
		del form['fields'][4]['options'][:]

		form['config']['action'] = '/install'
		form['fields'][4]['options'].append({
				'name':'admin',
				'selected': True
			})

		return form
