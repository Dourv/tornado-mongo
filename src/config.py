# -*- coding: utf-8 -*-
import os

# Allow configure the general path.
root = os.path.dirname(__file__) 

# Status of the project
# Values True or False
debug = True

# Database Configure 
# Base de datos para producción
psw = 'dourv_dev'
host = 'dourv.com'
user = 'root'
port = 27017



database = 'ext'



""" Permisos y Roles por defecto """


permissions = [
	{'name': 'admin::view_index','block':True},
	{'name': 'admin::view_users','block':True},
	{'name': 'admin::view_rols','block':True},
	{'name': 'admin::view_permissions','block':True},
	{'name': 'admin::edit_users','block':True},
	{'name': 'admin::edit_rols','block':True},
	{'name': 'admin::edit_permissions','block':True},
	{'name': 'admin::desactivate_users','block':True},
	{'name': 'admin::delete_rols','block':True},
	{'name': 'admin::delete_permissions','block':True},
	{'name': 'admin::debug_mode','block':True}

]


