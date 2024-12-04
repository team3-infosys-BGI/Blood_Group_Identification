
from django.shortcuts import render,redirect

from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

from django.contrib.auth import authenticate

from django.shortcuts import HttpResponseRedirect

def login(request):

    if(request.user.is_authenticated):

        return redirect('/')

    if(request.method == "POST"):

        un = request.POST['username']

        pw = request.POST['password']

        user = authenticate(request,username=un,password=pw)

        #authenticate() used to check for the valid statements given or not by linking with database automatically.

        #if the values are matched, then it will return the username

        #if the values are not matched, then it will return the 'None'

        if(user is not None):

            return redirect('/profiles')

        else:

            msg = 'Error in login. Invalid username/password'

            form = AuthenticationForm()

            # used to create a basic login page with username and password conditions

            return render(request,'login.html',{'form':form,'msg':msg})

    else:

        form = AuthenticationForm()

        # used to create a basic login page with username and password conditions

        return render(request,'login.html',{'form':form})