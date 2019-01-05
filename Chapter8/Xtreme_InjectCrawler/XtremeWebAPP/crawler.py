import os,math,random,hashlib,os.path,json
from xtreme_server.models import *
from urlparse import urlparse,urljoin
from bs4 import BeautifulSoup
from requests import get, post, request
from logger import Logger
from xtreme_server.xtreme.urls import Url
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from requests import Request, Session
import re ,string ,exrex ,sys 
from django.db import connection
connection.cursor()
FOLDER = os.path.dirname(os.path.realpath(__file__))
REPORT_FILE1 = os.path.join(FOLDER, 'file_report_urls.txt')
class Crawler(object):
 try:
    def __init__(   self,
             	    crawler_name = None,
                    start_url = None,
                    query_url = None,
                    login_url = None,
                    logout_url = None,
                    scope_urls_list = None,
                    should_include_base = True,
                    allowed_protocols_list = None,
                    allowed_extensions_list = None,
                    list_of_types_to_consider = None,
                    list_of_fields_to_exclude = None,
                    username = None,
                    password = None,
                    username_field=None,
                    password_field=None,
                    auth_mode = None,
                    queueName=None,
                    redisIP=None,
                    auth_parameters=None):
        """Initialize the Crawler"""
        self.logger = Logger()
        self.logger.log('Initializing the Crawler %s' % (crawler_name), 'crawler_info')
        self.crawler_name = crawler_name
        self.project = Project.objects.get(project_name = crawler_name)
        self.start_url = start_url
        self.query_url = query_url
        self.login_url = login_url
        self.logout_url = logout_url
        self.set_scope_urls(scope_urls_list, should_include_base)
        self.allowed_extensions_list = allowed_extensions_list
        self.allowed_protocols_list = allowed_protocols_list
        self.types_to_consider = list_of_types_to_consider
        self.fields_to_exclude = list_of_fields_to_exclude
        self.username = username
        self.password = password
        self.username_field=username_field
        self.password_field=password_field
        self.auth_mode = auth_mode
        self.queueName=queueName
        self.redisIP=redisIP
        self.auth_parameters=auth_parameters
	self.page_list=[]
        self.logger.log('Initialized the Crawler %s' % (crawler_name), 'crawler_info')


    def set_scope_urls(self, scope_urls_list, should_include_base):
        """Validates and adds the scopeurls defined in settings.py to scope"""

        self.scope_urls_list = []

        if should_include_base:
            start_urls = self.start_url.split(',')
            for start_url in start_urls:
                    self.add_url_to_scope(start_url)

        if not scope_urls_list:
            return

        if not isinstance(scope_urls_list, list):
            raise Exception('scope_urls_list must be a list.')

        for scope_url in set(scope_urls_list):
            self.add_url_to_scope(scope_url)


    def add_url_to_scope(self, url):
        """Given a url adds it to the scope"""


        url = Url(url)
        if url.parsed_url.netloc not in self.scope_urls_list:
            self.scope_urls_list.append(url.parsed_url.netloc)
            self.logger.log('Adding %s to scope' % (str(url.parsed_url.netloc)),
                                         'crawler_info')

    def is_url_in_scope(self, url):
        """Given a url, checks if this is the scopes defined till the call"""

        if url in self.scope_urls_list:
            return True

        url = Url(url)
        if url.parsed_url.netloc in self.scope_urls_list:
            return True

        return False


    def is_extension_allowed(self, extension):
        """Return true if extension is allowed"""

        if extension in self.allowed_extensions_list or extension is '':
            return True
        return False


    def is_protocol_allowed(self, protocol):
        """Return true if protocl is allowed"""

        if protocol in self.allowed_protocols_list:
            return True
        return False


    def set_src_folder(self, src_folder):
        """Sets the websrc folder"""

        if not src_folder:
            try:
                src_folder = settings.WEB_SRC_FOLDER
            except:
                src_folder = 'websrc'

        if not isinstance(src_folder, str):
            raise Exception("src_folder must be a string")

        import os
        current_dir = os.getcwd()
        self.src_folder = '\\'.join([current_dir, src_folder])


    def already_seen(self, url):
        """Checks if the URL is already visited or added"""

        if Page.objects.filter(URL = url, auth_visited=self.auth, project=self.project).count():
            return True
        return False


    def check_and_add_to_visit(self, curr_url,url):
        url = urljoin(str(curr_url),url)   
        self.logger.log("Found and checking the URL: %s" % (url), 'crawler_info')
        url = Url(url)
        if self.is_url_in_scope(url.get_domain()):
            if self.is_extension_allowed(url.get_extension()):
                # print "\tExtension Allowed"

                if self.is_protocol_allowed(url.get_protocol()):
                    # print "\tProtocol Allowed"

                    if not self.already_seen(url.url):
                        # print "\tAdding %s" % (url.url)
                        self.logger.log("Adding the URL and marking it as unvisited: %s"
                                        % (url.url), 'crawler_info')
                        with open(REPORT_FILE1, 'a') as f:
                          f.writelines("url found %s  \n" % (url.url))

                        page = Page()
                        page.URL = url.url
                        page.project = self.project
                        page.page_found_on = self.current_visiting.URL
                        page.auth_visited = self.auth
                        page.save()





    def there_are_pages_to_crawl(self):
        """Return True if there are unvisited pages"""

        if Page.objects.filter(visited = False, project = self.project, auth_visited = self.auth).count():
            return True
        return False


    def get_a_page_to_visit(self):
        """Return URL of an unvisited page"""

        return Page.objects.filter(visited = False, project=self.project, auth_visited = self.auth)[0]


    def process_form_action_url(self,curr_url, url):
        self.check_and_add_to_visit(curr_url,url)

        url = urljoin(str(curr_url),url)
        url = Url(url)
        url = Url(url.url)

        if self.already_seen(url.url):
            return Page.objects.get(URL = url.url, auth_visited = self.auth, project = self.project)

    def process_add_url(self,curr_url,url,string,pos1,pos2):
	
	if not(url.find('+')==-1):
			    
			    val_list=[]
			    parts=url.split('+')
			    url_str=""
			    for part in parts:
				if not('\'' in part or '\"' in part):
					#write page to file
					with open('pg.txt', 'w') as pgfile:
						pgfile.write(string)
					pgfile.close()
					#read line by line till you find the line containing the string window.location.href
					sub=string[pos1:pos2]
					#print sub
					with open('pg.txt','r') as pgfile:
						for line in pgfile.readlines():
							if sub in line:
								break
							with open('temp.txt','a') as tmpfile:
								tmpfile.write(line)

					pgfile.close()
					tmpfile.close()
					for line in reversed(open('temp.txt','r').readlines()):
						with open('temp1.txt','a') as tmpfile1:
							tmpfile1.write(line)
						if 'function' in line:
							break
					tmpfile1.close()
					if ('[' in part) and (']' in part):
						posx = line.find('[')
						var_name = part[0:posx-2]
						#print 'var_name %s' %(var_name)
						#part is arr var
						for line in open('temp1.txt').readlines():
							if var_name + '[' in line:
								#var would be var_name[*], need value on rhs of equal
								match=re.search(var_name+'\[[A-Za-z0-9]+\]',line,flags=0)
								#print 'match %s' %(match)
								if match:
									eqpos=line.find('=')
									endpos=line.find(';')
									value=line[eqpos+1:endpos]
									#print value
									if '\'' in value or '\"' in value:
										value=line[eqpos+2:endpos-1]
									val_list.append(value)
									#print 'val_list %s' %(val_list)
					else:
						#part is simple var
						var_name = part
						for line in open('temp1.txt').readlines():
							if var_name in line:
								eqpos=line.find('=')
								endpos=line.find(';')
								value=line[eqpos+1:endpos]
								#print value
								if '\'' in value or '\"' in value:
									value=line[eqpos+2:endpos-1]
								val_list.append(value)
								#print 'val_list %s' %(val_list)
				        #delete files
				        if os.path.isfile('pg.txt'):
					    	os.remove('pg.txt')
				        if os.path.isfile('temp.txt'):
					    	os.remove('temp.txt')
				        if os.path.isfile('temp1.txt'):
					    	os.remove('temp1.txt')

			    if len(val_list) ==0:
				    for part in parts:
					url_str=url_str + part[1:len(part)-1]
				    self.check_and_add_to_visit(curr_url,url_str)
			    else:
				    for val in val_list:
					for part in parts:
						if '\'' in part or '\"' in part:
							url_str=url_str+part[1:len(part)-1]
						else:
							url_str=url_str+val
					self.check_and_add_to_visit(curr_url,url_str)
					url_str=""
	else:
                    	    self.check_and_add_to_visit(curr_url,url[1:len(url)-1])

    def find_url_eq(self,search_string,curr_url,string,strlen):
        indices = [m.start() for m in re.finditer(search_string, string)]
        for index in indices:
                pos1 = index
                pos2 = string.find(';',pos1 + 1)
                sub = string[pos1 + strlen:pos2]
                url=sub
		self.process_add_url(curr_url,url,string,pos1,pos2)


    def find_url_fn(self,search_string,curr_url,string,strlen):
        indices = [m.start() for m in re.finditer(search_string, string)]
        for index in indices:
                pos1 = index
                pos2 = string.find(')',pos1 + 1)
                sub = string[pos1 + strlen:pos2]
                params = sub.split(',')
                url = params[0]
		self.process_add_url(curr_url,url,string,pos1,pos2)

    def add_other_urls(self, curr_url,string):
        string=string.replace(" ","")

	self.find_url_fn('window\.open\(',curr_url,string,12)
	self.find_url_fn('\.load\(',curr_url,string,6)
	self.find_url_fn('\.location\.assign\(',curr_url,string,17)
	self.find_url_eq('\.href=',curr_url,string,6)
	self.find_url_eq('\.action=',curr_url,string,8)
	self.find_url_eq('\.location=',curr_url,string,10)
	self.find_url_eq('\.src=',curr_url,string,5)

    def start(self, auth=False):
        self.logger.log("Starting the discovery process with auth: %s and seed URLs: %s"
                            % (str(auth), self.start_url), 'crawler_info')
	
        self.auth = auth
        REPORT_FILE = os.path.join(FOLDER, '%s_report.txt' %(self.project))
        if self.auth==False:
                with open(REPORT_FILE, 'wb') as f:
                    f.writelines("%s\n \n" % (self.project))
        if(self.auth==True):
                ss=Session()
                cookies = dict(csrftoken=self.auth_mode)
                xx=get(self.login_url)
                s = BeautifulSoup(xx.content,"html5lib")
                Login_form="none"
                Login_url="none"
                fs = s.findAll('form')
                data1 = {}
                payload={}
                flag1=False;flag2=False;flag3=False;flag4=False;flag5=False              
                counter_=0
                lengthforms=[0]*20
                matchforms=[None]*20
                actionforms=[None]*20
                payloadforms=[None]*20
                for f in fs:
                                data={}
                                action_url = self.login_url
                                if f.has_key('action'):
                                    action_url = f['action']
                                    if action_url.strip() == '' or action_url.strip() == '#':
                                        action_url = self.login_url
                                action_page = self.process_form_action_url(self.login_url,action_url)
                                if not action_page:
                                    action = ''
                                else:
                                    action = action_page.URL

                                form_content = str(f)
                                sp = BeautifulSoup(form_content,"html5lib")
                                #input type
                                tags=sp.findAll('input')
                                self.logger.log("reached here 3 %s  :  ",'crawler_info')
                                flag1=False
                                flag2=False
                                for tag in tags :

                                     self.logger.log("reached here 4 %s  :  ",'crawler_info')
                                     if tag.has_key('name'):
                                         data[tag['name']] = ''
                                         if tag['name']==self.username_field or tag['name']==self.password_field:
                                            Login_form=str(f)
                                            Login_url=str(action)
                                            if tag['name']==self.username_field :
                                               data[tag['name']]=self.username
                                               flag1=True
                                              
                                            else :
                                               data[tag['name']]=self.password
                                               flag2=True
                                            continue

                                         elif tag.has_key('value') and tag['value']!="":
                                             data[tag['name']] = tag['value']
                                         else:
                                            if tag.has_key('type'):

                                                input_type = tag['type']
                                                if input_type =="submit" :
                                                    data[tag['name']] =tag['value']
                                                elif input_type == "hidden":
                                                    if tag.has_key('value'):
                                                        data[tag['name']] = tag['value']
                                                    else:
                                                        data[tag['name']] = 'dummy'
                                                else:
                                                    data[tag['name']] = 'dummy data type'
                                     else:
                                        if tag.has_key('type'):
                                                input_type = tag['type']
                                                input_val='dummy value'
                                              
                                                if input_type =="submit" :
                                                    data[tag['type']] =tag['value']
                                                else:
                                                    data[tag['type']] ="dummy data submit"
                                if flag1==True and flag2==True :
                                    a=str(f)
                                    lengthforms[counter_]=len(a)
                                    actionforms[counter_]=action
                                    data['csrfmiddlewaretoken']=self.auth_mode
                                    payloadforms[counter_]=data
                                    counter_=counter_+ 1
                i=0;j=0
                if counter_ >1 :
                    while i <  counter_  :
                             j=i+1
                             while j<  counter_ :
                                if lengthforms[i]>lengthforms[j]:
                                    temp=lengthforms[i]
                                    temp1=actionforms[i]
                                    temp2=payloadforms[i]
                                    lengthforms[i]=lengthforms[j]
                                    actionforms[i]=actionforms[j]
                                    payloadforms[i]=payloadforms[j]
                                    lengthforms[j]=temp
                                    actionforms[j]=temp1
                                    payloadforms[j]=temp2
                                j+=1
                             i=i+1




              





                payload=payloadforms[0]
                if self.auth_parameters:
                        pairs = self.auth_parameters.split(',')
                        for pair in pairs:
                                field_value = pair.split(':')
                                print field_value
                                payload[field_value[0]]=field_value[1]


                x = ss.post(actionforms[0],data=payload,cookies=cookies)
                self.logger.log("login form is %s  :  "%(actionforms[0]),'crawler_info')
                self.logger.log("posted payload is %s  "%(str(payload)),'crawler_info')


        start_urls = self.start_url.split(',')
        for start_url in start_urls:
                if not self.already_seen(start_url):
                    page = Page()
                    page.URL = start_url
                    page.project = self.project
                    page.auth_visited = self.auth
                    page.save()

                while self.there_are_pages_to_crawl():
                    self.current_visiting = self.get_a_page_to_visit()
                    if (self.auth==False) or (self.auth==True and self.current_visiting.URL!=self.logout_url):
                            try:
                                self.logger.log("Visiting URL: %s with auth status: %s" %
                                        (self.current_visiting.URL, str(self.auth)), 'crawler_info')                                
                                if self.auth==True:
                                        self.logger.log("auth= true and username field : %s and username value is : %s:  "%(self.username_field,self.username),'crawler_info')                                       
                                        self.current_page_response = ss.get(self.current_visiting.URL,data=payload,cookies=cookies)
                                        for resp in self.current_page_response.history:
                                            self.logger.log("Response code auth true produced is %s" %(str(resp.status_code)), 'Crawler')
                                            if (resp.status_code == 302) or (resp.status_code == 301) or (resp.status_code == 303) :
                                               self.check_and_add_to_visit(self.current_visiting.URL,self.current_page_response.url)
                                        self.current_page_response = ss.get(self.current_visiting.URL,allow_redirects=False)
                                        self.logger.log("posted again  with auth= true on url %s:  "%(self.current_visiting.URL),'crawler_info')                                       
                                else:
                                        self.current_page_response = get(self.current_visiting.URL)  




                                        for resp in self.current_page_response.history:
                                            self.logger.log("Response code produced is %s" %(str(resp.status_code)), 'Crawler')
                                            if (resp.status_code == 302) or (resp.status_code == 301) or (resp.status_code == 303) :
                                               self.check_and_add_to_visit(self.current_visiting.URL,self.current_page_response.url)
                                        self.current_page_response = get(self.current_visiting.URL,allow_redirects=False)
                            except:
                                self.logger.log("Error occurred while visiting URL: %s with auth status: %s" %
                                        (self.current_visiting.URL, str(self.auth)), 'error')                               
                                Page.objects.filter(URL = self.current_visiting.URL, auth_visited=self.auth, project=self.project).update(visited = True, content = '', status_code = '0', connection_details = '')
                                continue                            
                            soup = BeautifulSoup(self.current_page_response.content,"html5lib")
			    base_url = None
			    bases = soup.findAll('base',href=True)
			    if bases:
				    base = bases[0]
				    base_url = base['href']
                            hrefs = soup.findAll('a', href=True)
                            for href in hrefs:
                                if href['href'][0:1].find("#")==-1 and href['href'].find("javascript:void(0)")==-1:
					if base_url:
						self.check_and_add_to_visit(base_url,href['href']) #initially called with start url
					else:
                                        	self.check_and_add_to_visit(self.current_visiting.URL,href['href']) #initially called with start url

                            #search frame src
                            hrefs = soup.findAll('frame', src=True)
                            for href in hrefs:
                                if href['src'][0:1].find("#")==-1 and href['src'].find("javascript:void(0)")==-1:
                                        self.check_and_add_to_visit(self.current_visiting.URL,href['src'])

			    #find iframe tag with src
			    hrefs = soup.findAll('iframe', src=True)
			    for href in hrefs:
				self.check_and_add_to_visit(self.current_visiting.URL,href['src'])
			    options = soup.findAll('option', value=True)
			    for option in options:
				if '/' in option['value']:
					self.check_and_add_to_visit(self.current_visiting.URL,option['value'])
			
                            #self.add_other_urls(self.current_visiting.URL,str(self.current_page_response.content))
                            # Lets create the form objects and check the action URLs
                            forms = soup.findAll('form')
                            for form in forms:
                                action_url = self.current_visiting.URL
                                if form.has_key('action'):
                                    action_url = form['action']
                                    if action_url.strip() == '':
                                        action_url = self.current_visiting.URL
                                action_page = self.process_form_action_url(self.current_visiting.URL,action_url)

                                if not action_page:
                                    action = ''
                                else:
                                    action = action_page.URL

                                form_name = 'Not specified'
                                if form.has_key('name'):
                                    form_name = form['name']
                                if form.has_key('id'):
                                    form_name = form['id']                                
                                form_method = 'GET'
                                if form.has_key('method'):
                                    form_method = form['method'].upper()
                                form_content = str(form)

                                #populate input_field_list
                                input_field_list = ""
                                soup = BeautifulSoup(form_content,"html5lib")
                                #input type
                                inputs = soup.findAll('input')
                                for inputfield in inputs:
                                        if inputfield.has_key('name') and inputfield.has_key('type'):
                                                input_field_list = input_field_list + inputfield['name'] + "," + inputfield['type'] + ","
                                        elif inputfield.has_key('id') and inputfield.has_key('type'):
                                                input_field_list = input_field_list + inputfield['id'] + "," + inputfield['type'] + ","
                                        else :
                                            if inputfield.has_key('type'):
                                                input_type = inputfield['type']                                           
                                                input_field_list = input_field_list+inputfield['type'] + "," + inputfield['value'] + ","
                                               
                                textareas = soup.findAll('textarea')
                                for textareafield in textareas:
                                        if textareafield.has_key('name'):
                                                input_field_list = input_field_list + textareafield['name'] + ",textarea,"
                                selects = soup.findAll('select')
                                for selectfield in selects:
                                        if selectfield.has_key('name'):
                                                input_field_list = input_field_list + selectfield['name'] + ",select,"
                                labels = soup.findAll('label')
                                for labelfield in labels:
                                        if labelfield.has_key('for'):
                                                input_field_list = input_field_list + labelfield['for'] + ",label,"
                              
                                existing_inputlist = Form.objects.filter(project = self.project,input_field_list = input_field_list, auth_visited = self.auth)
                                
                                if len(existing_inputlist)!=0:
                                        continue
                                f = Form()
                                f.project = self.project
                                f.form_found_on = self.current_visiting.URL
                                f.form_action = action
                                f.form_content = form_content
                                f.form_method = form_method
                                f.form_name = form_name
                                f.auth_visited = self.auth
                                f.input_field_list = input_field_list
                                f.save()
				dis={}
				dis["project"]=self.project.project_name
                                dis["form_found_on"] = self.current_visiting.URL
                                dis["form_action"] = action
                                dis["form_content"] = form_content
                                dis["form_method"] = form_method
                                dis["form_name"] = form_name
                                dis["auth_visited"] = self.auth
                                dis["input_field_list"] = input_field_list
				f=open("results/discovered"+str(self.project)+".json","a")
				json.dump(dis, f,sort_keys=True, indent=2)
				f.close()
                                self.logger.log("Found form on %s with action %s with auth status: %s" %
                                        (self.current_visiting.URL, form_method, str(self.auth)), 'crawler_info')
                    try:
                     Page.objects.filter(URL = self.current_visiting.URL, auth_visited=self.auth, project=self.project).update(visited = True,
                            content = self.current_page_response.content,
                            status_code = self.current_page_response.status_code,
                            connection_details = str(self.current_page_response.headers).replace('"', "'"))

                     self.logger.log("Finished processing the URL: %s with auth status: %s" %
                                (self.current_visiting.URL, str(self.auth)), 'crawler_info')
                     self.page_list.append(self.current_visiting.URL)
                    except:
                         Page.objects.filter(URL = self.current_visiting.URL, auth_visited=self.auth, project=self.project).update(visited = True,
                            content = "Cant be displayed !",
                            status_code = self.current_page_response.status_code,
                            connection_details = str(self.current_page_response.headers).replace('"', "'"))
                         

                         self.logger.log("Finished processing the URL: %s with auth status: %s" %
                                (self.current_visiting.URL, str(self.auth)), 'crawler_info')
        if self.auth==True:
                with open(REPORT_FILE, 'a') as f:
                     f.close()
        if not self.auth:
            self.start(auth = True)
        Project.objects.filter(project_name =
                                        self.project.project_name).update(status = "Finished")
        f= open("results/Pages_"+str(self.project.project_name),"w")
	for pg in self.page_list:
		f.write(pg+"\n")
	f.close()
 except:
    log=Logger()
    log.log("some error occurred in crawler",'crawler_info')

