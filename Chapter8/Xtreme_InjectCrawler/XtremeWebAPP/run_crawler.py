import os
import sys
sys.path.append(os.getcwd())
from xtreme_server.models import *
from crawler import Crawler
from logger import Logger
project_name = sys.argv[1]
project = Project.objects.get(project_name = project_name)
start_url = str(project.start_url)
query_url = str(project.query_url)
login_url = str(project.login_url)
logout_url = str(project.logout_url)
username_field = str(project.username_field)
password_field = str(project.password_field)
auth_parameters=str(project.auth_parameters)
queueName=str(project.queueName)
redisIP=str(project.redisIP)
settings = {}
settings['allowed_extensions'] = eval(str(project.allowed_extensions))
settings['allowed_protocols'] = eval(str(project.allowed_protocols))
settings['consider_only'] = eval(str(project.consider_only))
settings['exclude'] = eval(str(project.exclude_fields))
settings['username'] = project.username
settings['password'] = project.password
settings['auth_mode'] = project.auth_mode
c = Crawler(crawler_name = project_name, start_url = start_url, query_url = query_url,login_url = login_url,logout_url = logout_url,
                allowed_protocols_list = settings['allowed_protocols'],
                allowed_extensions_list = settings['allowed_extensions'],
                list_of_types_to_consider = settings['consider_only'],
                list_of_fields_to_exclude = settings['exclude'],
                username = settings['username'],
                password = settings['password'],
                auth_mode = settings['auth_mode'],
                username_field=username_field,
                password_field =password_field,queueName=queueName,redisIP=redisIP,
                auth_parameters=auth_parameters)
c.start()

