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
from forms import login, permissions, rols, users, admin



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
			html = html + '<div class="form-group'
			if 'form-group-class' in field:
				html += ' '+ field['form-group-class']

			html += '">'
			if field['widget'] in ('text', 'number','password', 'email','hidden') :
				if 'label' in field:
					if 'id' in field:
						html += '<label for="' + field['id']+'"'
						if 'class' in field['label']:
							html +=' class="'+field['label']['class']+'"'
						if 'attributes' in field['label']:
							html += ' '+ field['label']['attributes']	

						html += '>'+field['label']['text'] + '</label>'

				html += '<div'
				if 'parent-class' in field :
					html += ' class="'+field['parent-class']+'"'
				html += '>'		


				html += '<input'
				html += ' name="' + field['name'] +'"'
				html += ' type="' + field['widget']+'"'
				if 'class' in field:
					html += ' class="' + field['class']	+'"'
				if 'id' in field:
					html += ' id="' + field['id'] + '"'
				if 'required' in field:	
					if field['required'] == True:
						html += 'required'
				if 'placeholder' in	field:
					html += ' placeholder="' + field['placeholder'].decode('utf-8')+'"'
				if 'value' in field:
					html += ' value="' + field['value']+'"'
				if 'attributes' in	field:
					html += ' ' + field['attributes'].decode('utf-8')		
				html += ' />'	 


				html += '</div>'
			 
			if field['widget'] in ('checkbox'):
				html += '<div class="checkbox '
				if 'class' in field:
					html += field['class']

				html +='"><label>'
				html += '<input type="checkbox"'
				if 'attributes' in	field:
					html += ' ' + field['attributes']
				html += 'name="'+field['name']+'">'
				html += field['name'] + '</label></div>'				

			if field['widget']	in ('select'):
				if 'label' in field:
					if 'id' in field:
						html += '<label for="' + field['id']+'"'
						if 'class' in field['label']:
							html +=' class="'+field['label']['class']+'"'
						if 'attributes' in field['label']:
							html += ' '+ field['label']['attributes']	

						html += '>'+field['label']['text'] + '</label>'
						
				html += '<div '
				if 'parent_class' in field:
					html += 'class="'+ field['parent_class'] +'"'

				html += '>'	 
				html += '<select name="'+field['name'] +'" id="'+ field['name']+'"'
				if 'class' in field:
					html += 'class="'+field['class']+'"'

				html += '">' 	
				if 'placeholder' in field:
					html += "<option>" +field['placeholder']+ "</option>"
				if 'options' in field:
					for option in field['options']:
						html+="<option value='"+option['name'] +"'"
						if 'selected' in option:
							print option['selected']
							if option['selected']:
								html += ' selected'
						html += ">" + option['name'] + '</option>' 

				html+= "</select></div>"			

		
			if field['widget'] in ('submit'):
				html += '<input type="submit" '
				if 'class' in field:
					html += 'class="'+field['class']+'"' 
				if 'attributes' in	field:
					html += ' ' + field['attributes']
				html += ' value="' + field['value'].decode('utf-8') + '"/>'					
				if 'reset' in field:
					html += '<input type="reset" '
					if 'class' in field:
						html += 'class="'+field['reset']['class']+'"' 
					if 'attributes' in	field:
						html += ' ' + field['reset']['attributes']
					html += ' value="' + field['reset']['value'] + '"/>'		

			

			html = html + '</div>'
		html = html + '</form>'	

		return html