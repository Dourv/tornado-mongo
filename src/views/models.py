#!/usr/bin/env python
# -*- coding: utf-8 -*-
import calendar
import config
import hashlib
import json
import config
import pymongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from forms import *



class get_form():
	def get(self, form, id):
		form = eval(form)
		return form.form()	

	def admin(self):
		form = users.users()
		return form.form_admin()	

	def edit(self,form,id):
		form = eval(form)
		return form.form_edit(id)	

	def validation(self,form,data,edit=False):
		form = eval(form)
		return form.validation(data,edit)

	def delete(self,form,id):
		form = eval(form)
		return form.delete(id)	

	def render(self,form,id=None):
		if id == None:
			form = self.get(form,id)
		else:
			form = self.edit(form,id)	
		

		html = '<form class="'+form['config']['class']+'" method="'+form["config"]["method"]+'" action="'+form['config']['action']+'">'
		for field in form['fields']:
			html += '<div class="form-group '
			if 'form-group-class' in field:
				html += field['form-group-class'] 
			html +='">'

			if field['widget'] in ('text', 'number','password', 'email','hidden','submit','reset'):
				html += '<input type="'+field['widget'] +'" '
				for attribute in field['attributes']:
					html+= str(attribute) + '="'+field['attributes'][attribute].decode('utf-8')+'"'

				if 'required' in field and field['required'] == True:
					html += ' required '
				html += '/>'	 
			
			if field['widget'] == 'select':
				html += '<select '	
				for attribute in field['attributes']:
					html+= str(attribute) + '="'+field['attributes'][attribute].decode('utf-8')+'"'
				if 'required' in field and field['required'] == True:
					html += ' required '
				html += '>'	
				if 'options' in field:
					for option in field['options']:
						html += '<option '
						if 'selected' in option and option['selected'] == True:
							html += 'selected' 
						html += '>'+ option['name'] + '</option>'
				html+='</select>'	

			if field['widget'] in ('checkbox'):
				html += '<div class="checkbox '
			

				html +='"><label>'

				html += '<input type="checkbox"'
				for attribute in field['attributes']:
					html+= str(attribute) + '="'+field['attributes'][attribute].decode('utf-8')+'"'
				html += '>'
				html += field['attributes']['name'] + '</label></div>'				
	


			html += '</div>'		

		html += '</form>'	

		return html