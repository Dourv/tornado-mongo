import calendar
import config
import hashlib
import json
import os
import pymongo
import tornado
from bson.objectid import ObjectId
from datetime import datetime, timedelta



class base( tornado.web.RequestHandler ):
	@property
	def db(self):
		return self.application.connect[config.database] 

	def _render(self,template,_data = None):
		return self.render('../templates/'+template,_data = _data ,errors = self.get_message(True),messages=self.get_message(),user=self.get_current_user_loged())

	def set_visitor_id(self):
		vid = self.get_cookie('visitor_id')
		if vid == None:
			ip = self.request.remote_ip
			date = datetime.now()
			und_id = str(ip) + str(date)
			und_id = hashlib.md5(und_id).hexdigest()
			self.set_cookie('visitor_id',und_id)
			return und_id
		else:
			return self.get_cookie('visitor_id')

	def set_message(self, message):	

		_INSERT = {
			'vid': self.set_visitor_id(),
			'message': message,
			'type':'message'
		}
		return self.db.messages.insert(_INSERT)

	def set_message_error(self,message):
		_INSERT = {
			'vid': self.set_visitor_id(),
			'message': message,
			'type':'Error'
		}
		return self.db.messages.insert(_INSERT)

	def get_message(self,type_m = False):
		vid = self.set_visitor_id()
		if type_m:
			_query = self.db.messages.find({'vid':vid,'type':'Error' }) 
		else:
			_query = self.db.messages.find({'vid':vid,'type':'message' }) 

		messages = list()
		
		for message in _query:
			messages.append(message['message'])
			self.db.messages.remove(message)

		return messages	

	def get_current_user(self):
		return self.get_secure_cookie("user")

	def get_current_user_loged(self):
		cookie = self.get_current_user()
		#print cookie
		if cookie == None:
			return None
		else:
			return self.db.users.find_one({'_id':ObjectId(cookie)})

	def set_loged_user(self,user):
		user = self.db.users.find_one({'username':user})
		return self.set_secure_cookie('user',str(user['_id']))
							
	
	""" 
		Metodo global para detectar si el usuario se encuentra logeado.
	"""	
	def is_login(self):
		if self.get_current_user_loged() != None: 
			return True
		else:
			return False	

	"""
		Metodo para verificar si el usuario posee el rol root admin.
	"""		
	def is_admin(self):
		user = self.get_current_user_loged()
		if user != None:
			if user['rol'] == 'admin':
				return True
			else:
				return False
		else:
			return False

	"""
		Verificar que un usuario posee un permiso en especifico
	"""		
	def has_permission(self,p):
		user = self.get_current_user_loged()
		if user != None:
			rol = self.db.rols.find_one({'name':user['rol']})
			if 'permissions' in rol:
				for permission in rol['permissions']:
					if p == permission:
						return True
				return False		
			else:
				return False	
		else:
			return False	
		

	
class no_found(base):
	def get(self):
		self.write('Objeto No encontrado')

