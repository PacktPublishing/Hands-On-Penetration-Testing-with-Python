from django.db import models

class BlindProject(models.Model):
    project_name = models.CharField(max_length = 50, primary_key=True)
    public_IP = models.TextField()
    blind_URL = models.URLField()
    method = models.TextField()
    param_name = models.TextField()
    param_value = models.TextField()
    match_string = models.TextField()
    success_flg = models.TextField()
    project_status = models.TextField()

class Project(models.Model):
    project_name = models.CharField(max_length = 50, primary_key=True)
    start_url = models.URLField()
    query_url = models.URLField()
    allowed_extensions = models.TextField()
    allowed_protocols = models.TextField()
    consider_only = models.TextField()
    exclude_fields = models.TextField()
    status = models.CharField(max_length = 50, default = "Not Set")
    login_url = models.URLField()
    logout_url = models.URLField()
    username = models.TextField()
    password = models.TextField()
    username_field= models.TextField(default = "Not Set")
    password_field = models.TextField(default = "Not Set")
    auth_parameters=models.TextField(default = "Not Set")
    queueName=models.TextField(default="-1")
    redisIP=models.TextField(default="localhost")
    auth_mode = models.TextField(default = "Not Set")
    #models.
    #models.

    def __unicode__(self):
        return self.project_name

    def get_no_of_urls_discovered(self):
        return Page.objects.filter(project=self).count()

    def get_no_urls_processed(self):
        return Page.objects.filter(project=self, visited=True).count()

    def get_vulnerabilities_found(self):
            vulns = Vulnerability.objects.filter(project=self)
            vulnsList=[]
            count = 0
            for vuln in vulns:
                    flg=0
                    for v in vulnsList:
                        if v.url == vuln.url and v.form.input_field_list == vuln.form.input_field_list and v.re_attack == vuln.re_attack and v.auth!=vuln.auth:
                                flg=1
                                break
                    if flg==0:
                        count = count + 1
                        vulnsList.append(vuln)
            return count

class Page(models.Model):
    URL = models.URLField()
    content = models.TextField(blank = True)
    visited = models.BooleanField(default = False)
    auth_visited = models.BooleanField(default = False)
    status_code = models.CharField(max_length = 256, blank = True)
    connection_details = models.TextField(blank = True)
    project = models.ForeignKey(Project)
    page_found_on = models.URLField(blank = True)

    def __unicode__(self):
        return ' - '.join([self.project.project_name, self.URL])


class Form(models.Model):
    project = models.ForeignKey(Project)
    form_found_on = models.URLField()
    form_name = models.CharField(max_length = 512, blank = True)
    form_method = models.CharField(max_length = 10, default = 'GET')
    form_action = models.URLField(blank = True)
    form_content = models.TextField(blank = True)
    auth_visited = models.BooleanField(default = False)
    input_field_list = models.TextField(blank = True)

    def __unicode__(self):
        return ' + '.join([self.project.project_name, str(self.form_found_on),
                    'Auth: ' + str(self.auth_visited), 'Name: ' + self.form_name])


class InputField(models.Model):
    form = models.ForeignKey(Form)
    input_type = models.CharField(max_length = 256, default = 'input', blank = True)


class Vulnerability(models.Model):
    form = models.ForeignKey(Form)
    details = models.TextField(blank = True)

    #details = models.BinaryField(blank = True)
    url = models.TextField(blank = True)
    re_attack = models.TextField(blank = True)
    project = models.TextField(blank = True)
    timestamp = models.TextField(blank = True)
    msg_type = models.TextField(blank = True)
    msg = models.TextField(blank = True)
    #msg = models.BinaryField(blank = True)
    auth = models.TextField(blank = True)


class Settings(models.Model):
    allowed_extensions = models.TextField()
    allowed_protocols = models.TextField()
    consider_only = models.TextField()
    exclude_fields = models.TextField()
    username = models.TextField()
    password = models.TextField()
    auth_mode = models.TextField()

    def __unicode__(self):
        return 'Default Settings'

class LearntModel(models.Model):
    project = models.ForeignKey(Project)
    page = models.ForeignKey(Page)
    form = models.ForeignKey(Form)
    query_id = models.TextField()
    learnt_model = models.TextField(blank = True)

    def _unicode__(self):
        return ' + '.join([self.project.project_name, self.page.URL])
