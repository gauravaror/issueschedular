# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.shortcuts import render
import requests
from django.core.urlresolvers import reverse
import json

def issues(request,issuenumber):
    if request.user.is_authenticated():
        return get_url(request,"https://api.github.com/repos/"+request.session['repo']+"/issues/"+issuenumber,"issues/issue.html")
    else:
        return HttpResponse("Thanks for coming,Now go back and login please")

def update_issue(request,issuenumber):
    if request.user.is_authenticated():
        return get_url(request,"https://api.github.com/repos/"+request.session['repo']+"/issues/"+issuenumber,"issues/update.html")
    else:
        return HttpResponse("Thanks for coming,Now go back and login please")
        

def create_issue(request):
    if request.user.is_authenticated():
        return render(request,"issues/create.html")
        
def submit_issue(request):    
    if request.user.is_authenticated():
        if request.method == 'POST' or request.method == 'GET':
            return post_issue(request,"https://api.github.com/repos/"+request.session['repo']+"/issues")
#    return HttpResponseRedirect(reverse("login"))
    return HttpResponse(request.method)

def post_issue(request,url):
    if request.method == 'POST':
        data = { "title" : request.POST['title'],"body":request.POST['body'],"assignee":request.POST['assignee'],"milestone":request.POST['milestone'],"labels":request.POST['label']}
        jsondata = json.dumps(data)
        r = requests.post(url+"?"+request.session['access_token'],jsondata)
    elif request.method == 'GET':
        data = { "title" : request.GET['title'],"body":request.GET['body'],"assignee":request.GET['assignee'],"milestone":request.GET['milestone'],"labels":request.GET['label'],"state":request.GET['state']}
        jsondata = json.dumps(data)
        r = requests.patch(url+"/"+request.GET['number']+"?"+request.session['access_token'],jsondata)
    if (r.ok):
        resultdata = json.loads(r.text)
        return HttpResponseRedirect(reverse('issues:listissues'))
    else:
        if r.status_code == 422:
            return HttpResponseBadRequest("Unprocessable Entity,Please check input")
        else:
            return HttpResponseRedirect(reverse('issues:autherizationredirector'))


def list_issues(request):
    if request.user.is_authenticated():
        if request.POST.has_key('repo') or request.session.has_key('repo'):
            if request.POST.has_key('repo'):
                request.session['repo'] = request.POST['repo']
            return get_url(request,"https://api.github.com/repos/"+request.session['repo']+"/issues","issues/listissues.html")
        else:
            issues = ''
            return render(request,"issues/listissues.html",{ 'issue':issues, "state" :"Please provide repo name to see issues" })
    else:
        return HttpResponseRedirect(reverse("login",kwargs={"state":"Please Login"}))

def get_url(request,url,template):
    r = requests.get(url)
    if(r.ok):
        issues =  json.loads(r.text)
        return render(request,template,{'issue': issues,"state" : 'Repo Accesse '+ r.url})
    else:
        issues = ''
        return render(request,template,{'issue' : issues , "state" : 'No access to'+url })

     
def authorize(request):
    return HttpResponseRedirect("https://github.com/login/oauth/authorize?client_id=2857c183e61cec5c9cbf&scope=user,public_repo")

def get_accesstoken(request,cod):
    r = requests.post("https://github.com/login/oauth/access_token?client_id=2857c183e61cec5c9cbf&client_secret=801498fe33c9c1af73a7863fe3c5e52441b28e44&code="+cod)
    request.session['access_token'] = r.text
    return HttpResponse(r.text)
    

