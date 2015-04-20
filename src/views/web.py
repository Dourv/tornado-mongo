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



class home(base.base):
	def get(self):
		self._render('index.html')