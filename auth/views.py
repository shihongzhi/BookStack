# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from mysite.auth.models import SignupForm,LoginForm
from django.contrib.auth import authenticate, login,logout 

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/login")
    else:
        form = SignupForm()
    return render_to_response('signup.html',
                                      { 'form': form, 'user':request.user })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/home')
        else:
            # Return a 'disabled account' error message
            return render_to_response('login.html',  { 'form':form, 'user':request.user })
    else:
        # Return an 'invalid login' error message.
	form = LoginForm()
        return render_to_response('login.html',{'form':form, 'user':request.user})

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/home")
