# Create your views here.
from django.shortcuts import render_to_response,render
from django.contrib.auth import authenticate,login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

def login_user(request):
    state = "Please log in window below"
    username =  password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            if user.is_active:
                login(request,user)
                state = "You are successfully Loggedin"
                return HttpResponseRedirect(reverse('issues:issueshome'))
            else:
                state= "Your account is not active,Please check with administrator"
        else:
            state = "Your account doesn't exist, please come later."
    return render(request, 'auth/auth.html', {'state': state })
#            return HttpResponse("comeing man")
