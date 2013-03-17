# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
import requests
from django.core.urlresolvers import reverse
import json

def issues(request):
    if request.user.is_authenticated():
        return HttpResponse("Thanks for coming")
    else:
        return HttpResponse("Thanks for coming,Now go back")

def list_issues(request):
    if request.user.is_authenticated():
        if request.POST.has_key('repo'):
            r = requests.get('https://api.github.com/repos/'+request.POST['repo']+'/issues')
            if(r.ok):
                issues =  json.loads(r.text)
                return render(request,"issues/listissues.html",{'issue': issues,"state" : 'Repo Accesse '+ r.url})
            else:
                issues = ''
                return render(request,"issues/listissues.html",{'issue' : issues , "state" : 'https://api.github.com/repos/'+request.POST['repo']+'/issues' })
        else:
            issues = ''
            return render(request,"issues/listissues.html",{ 'issue':issues, "state" :"Please provide repo name to see issues" })
    else:
        return HttpResponseRedirect(reverse("login",kwargs={"state":"Please Login"}))

def autherize(request):
    return HttpResponseRedirect("https://github.com/login/oauth/authorize?client_id=2857c183e61cec5c9cbf")

def getaccesstoken(request,cod):
    return requests.post("https://github.com/login/oauth/access_token?client_id=2857c183e61cec5c9cbf&client_secret=801498fe33c9c1af73a7863fe3c5e52441b28e44&code="+cod)
    

