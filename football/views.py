from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from football.forms import UserForm

# Create your views here.

def home(request):
    render(request, home.html)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    context = {'registered': registered, 'user_form':user_form}
    return render(request, 'register.html', context)

def user_login(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # valid and active account
                login(request,user)
                return HttpResponseRedirect('/')

            else:
                #inactive user account
                return HttpResponse('Your account is disabled')
        else:
            # wrong login details
            print("Invalid username, password combination")
            return HttpResponse('Invalid Login details provided')
    else:
        # for method other then POST
        return render(request, 'login.html')

@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')