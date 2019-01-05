# Create your views here.

import subprocess
import os
import signal
import pprint
import sys
import zipfile
import psutil
#from xtreme.crawler import Crawler

from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from XtremeWebAPP.xtreme_server.models import *
from XtremeWebAPP.settings import SITE_ROOT

from django.contrib.auth.views import login, logout
from django.contrib.auth.models import User

#import pdfkit

FINISHED = 'Finished'
IN_PROGRESS = 'In Progress'
STOPPED = 'Stopped'

CRAWLERS = {}
COUNTERS={}
details={}
urll={}
msg={}
timestamp={}
Forms=[]
Form_list=[]
Report_string="<table class=table table-striped table-hover style=width:70%;position:absolute;left:20%;font-size:100%>"





FOLDER_NAME = os.path.dirname(os.path.realpath(__file__))

RUN_CRAWLER_FILE = os.path.join(SITE_ROOT, 'run_crawler.py')
root1=os.path.join(SITE_ROOT,'static')

root=os.path.join(root1,'css')
static_path=root1
css_folder_file1=os.path.join(root, 'bootstrap.css')
css_folder_file2=os.path.join(root, 'dashboard.css')

MANAGE_FILE_FOLDER = os.getcwd()
PRETTY_PRINTER = pprint.PrettyPrinter(indent=4)
List_vuln=[ "Tautology Attack with single quoted string (numeric)",
        "Tautology Attack with single quoted string (alpha)",
	"Tautology Attack with double quoted string (numeric)",
	"Tautology Attack with double quoted string (alpha)",
	"Tautology Attack with single quoted string (integer)",
	"Tautology Attack with double quoted string (integer)",
        "Special character injection (double quote)",
        "Special character injection (single quote)",
        "Meta character injection (<)",
        "Meta character injection (>)",
        "Meta character injection (&)",
        "Comment injection (<!--)",
        "Tag injection",
        "CDATA injection (]]>)",
	"CDATA injection with script tag",
	"CDATA injection with tautology string (single quote)",
	"CDATA injection with tautology string (double quote)",
	"External entity injection",
     "Convert function Single quote",
    "Convert function double quote",
	"Executable Function injection (single quote)",
	"Executable Function injection (double quote)",
    "Internal Server Error"

]
Len_List_vect=len(List_vuln)

def home(request):
 try:

    return render_to_response("index.html", {
            'page': 'overview',

        }, context_instance=RequestContext(request))
 except:
     return "error"

def home1(request):
 try:
    progress = get_progress()

    return render_to_response("xml_inj_overview.html", {
            'page': 'overview',
            'progress': progress
        }, context_instance=RequestContext(request))
 except:
     return "error"

def blind_overview(request):
    projects = BlindProject.objects.all()
    count = 0
    project_wise = []
    if len(projects):
        # Cool. We have projects!
        for project in projects:
            count += 1
	    this_project = {}
	    this_project['count'] = count
	    this_project['project_name'] = project.project_name
	    this_project['project_status'] = project.project_status
	    if project.success_flg == 'T':
		    this_project['success_flg'] = 'Yes'
	    if project.success_flg == 'F':
		    this_project['success_flg'] = 'No'
	    if project.success_flg == 'N':
		    this_project['success_flg'] = 'Error'
	    project_wise.append(this_project)

    return render_to_response("blind_overview.html", {
            'page': 'blind_overview',
            'projects': project_wise,
        }, context_instance=RequestContext(request))

def get_progress():
    # See if crawling has completed
 try:
    remove = []
    for project in CRAWLERS:
        if CRAWLERS[project].poll() >= 0:
            remove.append(project)
    for project in remove:
        CRAWLERS.pop(project)
        project = Project.objects.filter(project_name =
                                        str(project)).update(status = FINISHED)

    progress = {}

    # Total progress
    total = {}
    total['finished'] = Project.objects.filter(status = FINISHED).count()
    total['inprogress'] = Project.objects.filter(status = IN_PROGRESS).count()
    total['vulns'] = 0
    total['urls'] = 0
    total['processed'] = 0
    total['percentage'] = 0

    project_wise = []

    projects = Project.objects.all()
    count = 0

    if len(projects):
        # Cool. We have projects!
        for project in projects:
            count += 1

            if str(project.status) in [FINISHED, IN_PROGRESS]:
                total['urls'] += project.get_no_of_urls_discovered()
                total['processed'] += project.get_no_urls_processed()

            total['vulns'] += project.get_vulnerabilities_found()

            this_project = {}
            this_project['count'] = count
            this_project['name'] = project.project_name
            this_project['status'] = project.status
            this_project['urls'] = project.get_no_of_urls_discovered()
            this_project['processed'] = project.get_no_urls_processed()
            this_project['vulns'] = project.get_vulnerabilities_found()

            project_wise.append(this_project)

    if total['urls']:
        total['percentage'] = total['processed'] * 100 / total['urls']

    progess = {
        'total': total,
        'projects': project_wise
    }

    return progess
 except:
     return "error"


def tour(request):
 try:
     return render_to_response("tour.html", {

        }, context_instance=RequestContext(request))
 except:
     return "error"

def progress(request):
 try:
    return render_to_response("progress.html", {
            'progress': get_progress()
        }, context_instance=RequestContext(request))
 except:
     return "error"

def new_scans(request):
     return render_to_response("scans.html", {
                'page': 'new_scan',
                'settings': get_renderable_settings()
            }, context_instance=RequestContext(request))

def xml_inj(request):
 #try:
    progress = get_progress()

    return render_to_response("xml_inj_overview.html", {
            'page': 'xml_overview',
            'progress': get_progress()
        }, context_instance=RequestContext(request))
 #except:
     #return "error"

def new_scan(request):
 if True:
    if request.method == "POST":
        try:
            settings = get_new_settings(request)
        except:
            settings = get_settings()

        queueName="-1"
        project_name = str(request.POST['projectName'])
        start_url = str(request.POST['startURL'])
        query_url = str(request.POST['startURL'])
        login_url = str(request.POST['loginURL'])
        logout_url = str(request.POST['logoutURL'])
        username_field=str(request.POST['toAuthUsernameField'])
        username=str(request.POST['toAuthUsername'])
        password_field=str(request.POST['toAuthPasswordField'])
        password=str(request.POST['toAuthPassword'])
        auth_parameters=str(request.POST['authParameters'])
        redisIP=str(request.POST['redisIP'])
        if (request.POST['queueName']):
            queueName=str(request.POST['queueName'])

        if Project.objects.filter(project_name = project_name).count():
            lol = True
        else:
            lol = False

        if not project_name or not start_url or not query_url or lol:
            return render_to_response("new.html", {
                'success': 'False',
                'settings': get_renderable_settings()
            }, context_instance=RequestContext(request))

        else:
            project = Project()
            project.project_name = project_name
            project.start_url = start_url
            project.query_url = query_url
            project.login_url = login_url
            project.logout_url = logout_url
            project.allowed_extensions = str(settings['allowed_extensions'])
            project.allowed_protocols = str(settings['allowed_protocols'])
            project.consider_only = str(settings['consider_only'])
            project.exclude_fields = str(settings['exclude'])
            project.username = username
            project.password = password
            project.auth_mode = str(settings['auth_mode'])
            project.username_field=username_field
            project.password_field=password_field
            project.auth_parameters=auth_parameters
            project.queueName=queueName
            project.redisIP=redisIP
            project.status = IN_PROGRESS
            project.save()
        if 'remember' in request.POST and len(str(request.POST['remember'])):
            save_settings(settings)
        cmd_str = project_name
        log_file = open(project_name+'.txt', 'w')
	RUN_CRAWLER_FILE = os.path.join(SITE_ROOT, 'run_crawler.py')
        if  sys.platform.startswith('win32'):
            process = subprocess.Popen('python "%s" "%s"' %(RUN_CRAWLER_FILE, cmd_str),shell=True,
                                    stdout = log_file,
                                    stderr = log_file,
                                    stdin = subprocess.PIPE)
        else:
            process = subprocess.Popen('exec python2 "%s" "%s"' %(RUN_CRAWLER_FILE, cmd_str),
                                    shell=True,
                                    stdout = log_file,
                                    stderr = log_file,
                                    stdin = subprocess.PIPE)




        CRAWLERS[project_name] = process
        return HttpResponseRedirect("/details?proj_name=%s&just=true" % (project_name))

    else:
        return render_to_response("new.html", {
                'page': 'new_scan',
                'settings': get_renderable_settings()
            }, context_instance=RequestContext(request))


def settings(request):
 try:
    if request.method == "GET":
        return render_to_response("settings.html", {
                'page': 'settings',
                'settings': get_renderable_settings()
            }, context_instance=RequestContext(request))

    elif request.method == "POST":
        save_settings(get_new_settings(request))
        return render_to_response("settings.html", {
                'page': 'settings',
                'settings': get_renderable_settings(),
                'updated': True
            }, context_instance=RequestContext(request))
 except:
     return "error"



def get_new_settings(request):
 try:
    a = {}
    a['consider_only'] = []
    for i in request.POST.getlist('toConsider[]'):
        a['consider_only'].append(str(i.strip()))

    a['exclude'] = []
    for i in str(request.POST['toExclude']).split(','):
        a['exclude'].append(str(i.strip()))

    a['allowed_extensions'] = []
    for i in str(request.POST['allowedExtensions']).split(','):
        a['allowed_extensions'].append(str(i.strip()))

    a['allowed_protocols'] = []
    for i in request.POST.getlist('allowedProtocols[]'):
        a['allowed_protocols'].append(str(i.strip()))

    a['username'] = []
    a['username'] = request.POST['toAuthUsername']

    a['password'] = []
    a['password'] = request.POST['toAuthPassword']

    a['auth_mode'] = []
    a['auth_mode'] = request.POST['toAuthMode']

    return a
 except:
     return "error"



def get_renderable_settings(settings = None):
 try:
    if not settings:
        #print('inside if')
        settings = get_settings()
    settings['allowed_extensions'] = ', '.join(settings['allowed_extensions'])
    settings['exclude'] = ', '.join(settings['exclude'])
    #settings['username'] = ', '.join(settings['username'])
    #settings['password'] = ', '.join(settings['password'])
    #settings['auth_mode'] = ', '.join(settings['auth_mode'])
    return settings
 except:
     return "error"



def get_settings():
 try:
    if Settings.objects.all():
        setting = Settings.objects.get(pk=1)
    else:
        setting = Settings()
        setting.allowed_extensions = "['asp', 'aspx', 'cfm', 'cfml', 'htm', 'html', 'jhtml', 'jsp', 'php', 'php3', 'php4', 'php5', 'phtm', 'phtml', 'pl', 'py', 'shtm', 'shtml', 'txt', 'xht', 'xhtm', 'xhtml', 'xml']"
        setting.allowed_protocols = "['http', 'https']"
        setting.consider_only = "['textareas', 'checkboxes', 'selects', 'inputs']"
        setting.exclude_fields = "['csrftoken', 'csrfmiddlewaretoken']"
        setting.username = "nushafreen"
        setting.password = "nushafreen"
        setting.auth_mode = "Q8fZUKGdyX7zMOkiJfisR2ae26xcWaYs"
        setting.save()

    b = {}
    b['allowed_extensions'] = eval(str(setting.allowed_extensions))
    b['allowed_protocols'] = eval(str(setting.allowed_protocols))
    b['consider_only'] = eval(str(setting.consider_only))
    b['exclude'] = eval(str(setting.exclude_fields))
    b['username'] = setting.username
    b['password'] = setting.password
    b['auth_mode'] = setting.auth_mode
    return b
 except:
     return "error"



def save_settings(new_settings):
 try:
    settings = get_settings()

    update = False
    for i in settings:
        if sorted(settings[i]) != sorted(new_settings[i]):
            update = True
            settings[i] = new_settings[i]

    if update:
        setting = Settings.objects.get(pk=1)
        setting.allowed_extensions = str(new_settings['allowed_extensions'])
        setting.allowed_protocols = str(new_settings['allowed_protocols'])
        setting.consider_only = str(new_settings['consider_only'])
        setting.exclude_fields = str(new_settings['exclude'])
        setting.username = str(new_settings['username'])
        setting.password = str(new_settings['password'])
        setting.auth_mode = str(new_settings['auth_mode'])
        setting.save()
 except:
     update=False
     # def add_new_crawler(request):
     # PROJECT_NAME = 'Xtreme1%d' % (random.randint(100, 20000))
     # START_URL = 'http://localhost:9090/'
     # cmd_line_string = PROJECT_NAME + '$$$' + START_URL

     # log_file = open(PROJECT_NAME+'.txt', 'w')

     # process = subprocess.Popen('python "%s"' %(RUN_CRAWLER_FILE), shell=True, stdout = log_file, stderr = log_file, stdin = subprocess.PIPE)
     # process.stdin.write(cmd_line_string)
     # out, err = process.communicate(cmd_line_string)
     # process.stdin.close()

     # CRAWLERS.append(PROJECT_NAME)
     # length = len(CRAWLERS)
     # return HttpResponse(str(length) + 'lol check' + cmd_line_string)






def kill_scan(request):
    #print("inside kill scan")
 try:
    lol = False
    try:
        project_name = str(request.GET['project_name'])
        #print("project_name")
        #print(project_name)
        if not len(project_name):
            lol = True
    except:
        lol = True

    if lol:
        return render_to_response('alert.html', {
                'error': True,
                'text': 'Missing Parameter!'
            }, context_instance=RequestContext(request))

    #print(CRAWLERS)
    if project_name in CRAWLERS:
        pro = CRAWLERS[project_name]
        #print('process id in kill')
        #print(pro.pid)
        #print(signal.SIGTERM)
        #os.kill(pro.pid, signal.SIGTERM)
        pro.kill()
        CRAWLERS.pop(project_name)
        project = Project.objects.get(project_name = project_name)
        project.status = STOPPED
        project.save()

        return render_to_response('alert.html', {
                'error': False,
                'text': 'Successfully stopped project scanning'
        }, context_instance=RequestContext(request))
    else:
        return render_to_response('alert.html', {
                'error': True,
                'text': 'The project scanning is already stopped!'
            }, context_instance=RequestContext(request))
 except:
     return "error"


def get_details(request):
# try:
 if True :
    get_progress()
    if 'proj_name' in request.GET and len(str(request.GET['proj_name'])):
        project_name = str(request.GET['proj_name'])
        if Project.objects.filter(project_name = project_name).count():
            #projectss = Project.objects.filter(project_name__contains= project_name)
            project = Project.objects.get(project_name = project_name)
            setting = {}
            setting['allowed_extensions'] = eval(str(project.allowed_extensions))
            setting['allowed_protocols'] = eval(str(project.allowed_protocols))
            setting['consider_only'] = eval(str(project.consider_only))
            setting['exclude'] = eval(str(project.exclude_fields))
            setting['username'] = project.username
            setting['password'] = project.password
            setting['auth_mode'] = project.auth_mode

            a = get_renderable_settings(setting)
            a['allowed_protocols'] = ', '.join(a['allowed_protocols'])
            a['consider_only'] = ', '.join(a['consider_only'])

            urls_found = project.get_no_of_urls_discovered()
            urls_processed = project.get_no_urls_processed()
            vulns_found = project.get_vulnerabilities_found()

            percentage = 0
            if urls_found>0:
                percentage = urls_processed * 100/urls_found

            if 'just' in request.GET and str(request.GET['just']) == 'true':
                just = True
            else:
                just = False

            if 'update' in request.GET and str(request.GET['update']) =='1':
                template = 'details_update.html'
            else:
                template = 'details.html'

            return render_to_response(template, {
                'project': project,
                'settings': a,
                'page': 'reports',
                'urls_found': urls_found,
                'urls_processed': urls_processed,
                'vulns_found': vulns_found,
                'percentage': percentage,
                'just': just
            }, context_instance=RequestContext(request))

    return render_to_response('alert.html', {
                'error': True,
                'text': 'Your search didn\'t give any results. Please check the overview section for your project.'
            }, context_instance=RequestContext(request))
 #except:
     #return "error"

def blind_scan(request):
    if request.method == "POST":
	project_name = request.POST['projectName']
	public_IP = request.POST['publicIP']
	blind_URL = request.POST['blindURL']
	method = request.POST['method']
	param_name = request.POST['paramName']
	param_value = request.POST['paramValue']
	match_string = request.POST['matchString']

	#create project blind and save to db
	blind_proj = BlindProject()
	blind_proj.project_name = project_name
	blind_proj.public_IP = public_IP
	blind_proj.method = method
	blind_proj.blind_URL = blind_URL
	blind_proj.param_name = param_name
	blind_proj.param_value = param_value
	blind_proj.match_string = match_string
	blind_proj.project_status = 'In Progress'
	blind_proj.success_flg = 'N'
	blind_proj.save()

	log_file = open(project_name + '_blindLog.txt', 'a')

	process = subprocess.Popen('xcat --public-ip=' + public_IP + ' --method=' + method + ' ' + blind_URL + ' "' + param_name + '=' + param_value + '" ' + param_name + ' "' + match_string + '" run retrieve', shell=True, stdout = log_file, stderr = log_file, stdin = subprocess.PIPE)
	process_id = process.pid

	return HttpResponseRedirect("/blind_details?projectName=%s&page='blind_scan'&processID=%s" % (project_name,process_id))
    else:
	return render_to_response("blind.html", {
                'page': 'blind_scan',
            }, context_instance=RequestContext(request))

def blind_details(request):
    project_name = request.GET['projectName']
    if 'processID' in request.GET:
	process_id = eval(request.GET['processID'])
	project = BlindProject.objects.get(project_name = project_name)
	#project = request.POST['project']
	p = psutil.Process(process_id)
	print(p.status)

	#process has terminated, check log for result of xpath scan
	if(p.status!='sleeping' and p.status!='running'):
		line = subprocess.check_output(['tail', '-1', project_name + '_blindLog.txt'])
		if 'Successfully retrieved XML' in line:
			BlindProject.objects.filter(project_name =
		                                project_name).update(project_status = 'Completed',success_flg='T')
		else:
			BlindProject.objects.filter(project_name =
		                                project_name).update(project_status = 'Completed',success_flg='F')

	return render_to_response('blind_details.html', {
			    'page': 'blind_details',
		            'project': BlindProject.objects.get(project_name = project_name),
		            'processID': process_id,
			    }, context_instance=RequestContext(request))
    else:
	return render_to_response('blind_details.html', {
			    'page': 'blind_details',
		            'project': BlindProject.objects.get(project_name = project_name),
			    }, context_instance=RequestContext(request))


def blind_report(request):
    if 'projectName' in request.GET and len(request.GET['projectName']):
	project_name = request.GET['projectName']
	project =BlindProject.objects.get(project_name = project_name)
	report_lines = []
     	with open(project_name+'_blindLog.txt', 'r') as f:
	     for line in f.readlines():
		report_lines.append(str(line))

	return render_to_response("blind_report.html", {
                'page' : 'blind_report',
		'project' : project,
		'reportLines' : report_lines,
            }, context_instance=RequestContext(request))
    else:
	projects = BlindProject.objects.all()
    	proj = []
    	for project in projects:
        	if project.project_status == 'Completed':
            		proj.append(project.project_name)
    	return render_to_response('blind_report.html', {
            'page': 'blind_report',
            'projectnames':proj,
            }, context_instance=RequestContext(request))


def resume_scan(request):
 try:
    got_option = False
    try:
        if 'projectName' in request.GET and len(request.GET['projectName']):
            got_option = True
            project_name = request.GET['projectName']
    except:
        return HttpResponseRedirect('/resume')
    if got_option:
        try:
            project = Project.objects.get(project_name = project_name)
        except:
            project = None
        a = []
        if not project:
            error = True
        else:
            error = False
            project = Project.objects.get(project_name = project_name)
            setting = {}
            setting['allowed_extensions'] = eval(str(project.allowed_extensions))
            setting['allowed_protocols'] = eval(str(project.allowed_protocols))
            setting['consider_only'] = eval(str(project.consider_only))
            setting['exclude'] = eval(str(project.exclude_fields))

            a = get_renderable_settings(setting)
            a['allowed_protocols'] = ', '.join(a['allowed_protocols'])
            a['consider_only'] = ', '.join(a['consider_only'])

        return render_to_response('resume.html', {
            'page': 'resume_scan',
            'details': a,
            'project':project,
            'error': error,
            }, context_instance=RequestContext(request))

    projects = Project.objects.all()
    proj = []
    for project in projects:
        if project.status != IN_PROGRESS:
            proj.append(str(project.project_name))
    return render_to_response('resume.html', {
            'page': 'resume_scan',
            'projects':proj,
            }, context_instance=RequestContext(request))
 except:
     return "error"



def modify_scan(request):
 #try:
    if request.method == "POST":
        try:
            settings = get_new_settings(request)
        except:
            settings = get_settings()

        project_name = str(request.POST['projectName'])
        start_url = str(request.POST['startURL'])
        query_url = str(request.POST['startURL'])
        login_url = str(request.POST['loginURL'])
        logout_url = str(request.POST['logoutURL'])
        username_field=str(request.POST['toAuthUsernameField'])
        username=str(request.POST['toAuthUsername'])
        password_field=str(request.POST['toAuthPasswordField'])
        password=str(request.POST['toAuthPassword'])
        auth_parameters=str(request.POST['authParameters'])
        auth_mode=str(request.POST['toAuthMode'])

        if Project.objects.filter(project_name = project_name).count() == 1:
            lol = True
        else:
            lol = False

        if not project_name or not start_url or not query_url or not lol:
            return render_to_response('alert.html', {
                'error': True,
                'text': 'Nice Try!'
            }, context_instance=RequestContext(request))

        else:
            Project.objects.filter(project_name =
                                        project_name).update(status = IN_PROGRESS,
                                                    start_url = start_url,
                                                    query_url = query_url,
                                                    login_url = login_url,
                                                    logout_url = logout_url,
                                                    allowed_extensions = str(settings['allowed_extensions']),
                                                    allowed_protocols = str(settings['allowed_protocols']),
                                                    consider_only = str(settings['consider_only']),
                                                    exclude_fields = str(settings['exclude']),
                                                    username = username,
                                                    password = password,
                                                    auth_mode = auth_mode,
                                                    username_field = username_field,
                                                    password_field = password_field,
                                                    auth_parameters = auth_parameters)

            project = Project.objects.get(project_name = project_name)

        # Did the user ask us to remember the settings?
        if 'remember' in request.POST and len(str(request.POST['remember'])):
            save_settings(settings)

        if 'force' in request.POST and len(str(request.POST['force'])):
            print 'forcing'
            Page.objects.filter(project = project).delete()
            Form.objects.filter(project = project).delete()

        if Page.objects.filter(URL = start_url, project = project).count():
            Page.objects.filter(URL = start_url, project = project).delete()
            Form.objects.filter(form_found_on = start_url, project = project).delete()

        cmd_str = project_name

        log_file = open(project_name+'.txt', 'a')

        process = subprocess.Popen('python "%s" "%s"' %(RUN_CRAWLER_FILE, cmd_str),
                                    shell=True,
                                    stdout = log_file,
                                    stderr = log_file,
                                    stdin = subprocess.PIPE)

        CRAWLERS[project_name] = process

        return HttpResponseRedirect("/details?proj_name=%s&mod=True" % (project_name))

    else:
        return HttpResponseRedirect('/')
# except:
    #return "error"


def display_reports(request):
 try:
    got_option = False

    try:
        if 'projectName' in request.GET and len(request.GET['projectName']):
            got_option = True
            project_name = request.GET['projectName']
    except:
        return HttpResponseRedirect('/reports')
    if got_option:
        try:
            project = Project.objects.get(project_name = project_name)
        except:
            project = None
        det = []
        if not project:
            error = True
        else:
            error = False
            #with open(project_name+'.txt', 'r') as f:
             #   det = parse_reports(f.readlines())


            project = Project.objects.get(project_name = project_name)
            setting = {}
            setting['allowed_extensions'] = eval(str(project.allowed_extensions))
            setting['allowed_protocols'] = eval(str(project.allowed_protocols))
            setting['consider_only'] = eval(str(project.consider_only))
            setting['exclude'] = eval(str(project.exclude_fields))
            setting['username'] = project.username
            setting['password'] = project.password
            setting['auth_mode'] = project.auth_mode

            a = get_renderable_settings(setting)
            a['allowed_protocols'] = ', '.join(a['allowed_protocols'])
            a['consider_only'] = ', '.join(a['consider_only'])

            urls_found = project.get_no_of_urls_discovered()
            urls_processed = project.get_no_urls_processed()
            vulns_found = project.get_vulnerabilities_found()

        return render_to_response('reports.html', {
            'option_given': True,
            'page': 'reports',
            #'details': det,
            'project': project,
            'settings': a,
            'vulns': get_parsed_vulns(project_name),
            'urls_found': urls_found,
            'urls_processed': urls_processed,
            'vulns_found': vulns_found,
            'error': error,
            'counters':get_counters(),
            'list_vul':List_vuln,
            'report_string':Report_string,
            'vul_forms':get_vulnerebleForms(),
            }, context_instance=RequestContext(request))

    projects = Project.objects.all()
    proj = []
    for project in projects:
        if project.status != IN_PROGRESS:
            proj.append(str(project.project_name))
    return render_to_response('reports.html', {
            'page': 'reports',
            'projects':proj,
            }, context_instance=RequestContext(request))
 except:
     return "error"



def generate_pdf_view(request):
 try:
    """
    try:
        # create an API client instance
        client = pdfcrowd.Client("nushafreen", "1a1dd7a47f7506742c64a949e9a108f7")
        print(request.GET)
        if 'projectName' in request.GET and len(request.GET['projectName']):
            got_option = True
            project_name = request.GET['projectName']

        # convert a web page and store the generated PDF to a variable
        #pdf = client.convertURI("/reports?projectName=%s" %(project_name))

        output_file = open('%s/XtremeWebAPP/%s.pdf' %(MANAGE_FILE_FOLDER,str(project_name)), 'wb')
        client.convertFile('%s/XtremeWebAPP/%s_report.html' %(MANAGE_FILE_FOLDER,str(project_name)), output_file)
        output_file.close()

        # set HTTP response headers
        response = HttpResponse(mimetype="application/pdf")
        response["Cache-Control"] = "max-age=0"
        response["Accept-Ranges"] = "none"
        response["Content-Disposition"] = "attachment; filename=%s/XtremeWebAPP/%s.pdf" %(MANAGE_FILE_FOLDER,str(project_name))

        # send the generated PDF
        #response.write(pdf)
        response.write(output_file)
    except pdfcrowd.Error, why:
        response = HttpResponse(mimetype="text/plain")
        response.write(why)
    return response
    """
    if 'projectName' in request.GET and len(request.GET['projectName']):
        project_name = request.GET['projectName']

    #pdfkit.from_file('%s/XtremeWebAPP/%s_report.txt' %(MANAGE_FILE_FOLDER,str(project_name)), '%s/XtremeWebAPP/%s.pdf' %(MANAGE_FILE_FOLDER,str(project_name)))
    #subprocess.check_call('enscript %s/XtremeWebAPP/%s_report.txt -o - | ps2pdf - %s/XtremeWebAPP/%s.pdf' %(MANAGE_FILE_FOLDER,str(project_name),MANAGE_FILE_FOLDER,str(project_name)) , shell=True)


    return render_to_response('generatedpdf.html', {
            'project_name':str(project_name)
            }, context_instance=RequestContext(request))
 except:
     return "error"


def parse_reports(report_lines):
    try :
     parsed_report = []
     for line in report_lines:
        a = {}
        timestamp, remaining = line.split(' - ', 1)
        a['timestamp'] = timestamp.strip()[1:-1]
        msg_type, msg = remaining.split(':', 1)
        a['msg_type'] = msg_type.strip()
        a['msg'] = msg.strip()
        parsed_report.append(a)

     return parsed_report
    except:
     return "error"




def get_parsed_vulns(project_name):
 try:
    #global COUNTERS
    #COUNTERS={}
    #global details={}
   # global urll={}
    #global msg={}
    #timestamp={}
    global Form_list
    Form_list=[]
    i=0
    count=0
    while i <Len_List_vect :
        COUNTERS[List_vuln[i]]=count
        details[List_vuln[i]]="Details :\n"
        urll[List_vuln[i]]="Urls : \n"
        msg[List_vuln[i]]=""
        timestamp[List_vuln[i]]=""

        i+=1
    #print "counters are "+str(COUNTERS)
    i=0
    vulns = Vulnerability.objects.filter(project = project_name) #returns all rows,in form of dictionary i.e key and value
    vulnsList=[]
    for vuln in vulns:
            flg=0
            for v in vulnsList:
                if v.url == vuln.url and v.form.input_field_list == vuln.form.input_field_list and v.re_attack == vuln.re_attack and v.auth!=vuln.auth:
                        flg=1
                        break
            if flg==0:
                vulnsList.append(vuln)

    #vulnsList.sort()
    for v_stored in vulnsList:
         for v in List_vuln :
             #print("message is " + v_stored.msg_type)
             if v_stored.msg_type == v :
                COUNTERS[v]+=1
                details[v]=""+str(details[v])+"\n Description :  "+str(v_stored.msg_type)+"\n\n"+"URL : "+str(v_stored.url)+"\n\n"+"Form name :  "+str(v_stored.form.form_name)+"\nMethod :  "+str(v_stored.form.form_method)+"\nAction :  "+str(v_stored.form.form_action)+"\n\n"+"Malicious Query : \n"+str(v_stored.details)+"\n"
                details[v]=""+str(details[v])+"--------------------------------------------------------------------------------------------------------------------"
                urll[v]=str(urll[v])+"\n"+str(v_stored.url)+"\n"
                timestamp[v]=str(timestamp[v])+"\n"+str(v_stored.timestamp)+"\n"
                #print v_stored.timestamp
                msg[v]=str(msg[v])+"\n"+str(v_stored.msg)+"\n"
                Forms.append("\n URL : "+str(v_stored.url)+" \n Form name :  "+str(v_stored.form.form_name)+"\nMethod :  "+str(v_stored.form.form_method)+"\nAction:  "+str(v_stored.form.form_action)+"\n")




    for f in Forms:
        flg=0
        for ff in Form_list:
            if ff ==f :
                flg=1
                break
        if flg==0:
            Form_list.append(f)
            Form_list.append("--------------------------------------------------------------------------------------------------------------------")

    vulnsList.sort()
    #Forms=Form_list
    print (Form_list)

    return vulnsList
 except:
     return "error"

def get_counters():
    try:
        i=1
        temp={}
        global Report_string
        Report_string=""
        links_data=""
        vul_counter=[]
        for line in COUNTERS:
             #print(line)
             #print(str(COUNTERS[line]))
             a = {}

             a['vul_type'] =str(line)
             a['counter_var']=0
             if COUNTERS[line] > 0 :

                links_data="<a href=#! onclick=get_details('"+str(i)+"'); style=text-decoretion:none>"+str(COUNTERS[line])+"</a>"
                other_data=str(details[line])
                urls=str(urll[line])
                #print links_data
                a['vul_no'] =links_data
                a['other_details']=str(other_data)
             else :
                a['vul_no'] = str(COUNTERS[line])

             i+=1

             a['counter_var']+=i

             vul_counter.append(a)
             Report_string+="<tr><td>"+str(timestamp[line])+"</td><td>"+str(line)+"</td><td>"+str(COUNTERS[line])+"</td><td>"+str(details[line])+"</td></tr>"
             #Report_string.append(a)

        Report_string+="</table>"
        #print("hello "+Report_string)
        #vul_counter.sort()
        return vul_counter





    except:
        print "error occured myan "
        return "error"

def get_counterss():
    try:
        vul_counter=[]
        for l in List_vuln :
            if l in COUNTERS :
                strr=str(l)+"   " + str(COUNTERS[l])
                vul_counter.append(strr)
        return vul_counter


    except:
        return "error"


def get_vulnerebleForms():
    try:
        return Form_list

    except:
        return "error"




def disp404(request):
    try :
      return render_to_response('alert.html', {
                'error': True,
                'text': 'The page you are looking for is not found! Please help us write it for you by letting us know how you arrived here!'
            }, context_instance=RequestContext(request))
    except:
     return ""


def scripts(request):
    try :

         data="a"
         with open(css_folder_file1, 'r') as f:
                #print(f.readlines())
                data=f.read()
         with open(css_folder_file2, 'r') as f:
                #print(f.readlines())
                data=data+f.read().replace('\n', '')


         if request.method == "GET":

            # print("page content is "+str(request.GET['content']))

             #with open(css_folder_file2, 'r') as f:
                #print(f.readlines())
                #data=data+f.read().replace('\n', '')




                #os.makedirs(directory)
             return render_to_response("script.html", {

                'page': 'settings',
                'method_id': str(request.GET['method_id']),
                'content':str(request.GET['content']),
                'data':data


            }, context_instance=RequestContext(request))

         elif request.method == "POST":

             #save_settings(get_new_settings(request))

             return render_to_response("script.html", {
                'page': 'settings',
                'updated': True,
                'method_id': str(request.GET['method_id']),
                'content':str(request.GET['content']),
                'data':data
            }, context_instance=RequestContext(request))
    except:
         print ("some error ")
         return "error"



