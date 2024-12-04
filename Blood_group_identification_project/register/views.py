from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm



def register(request):

    if(request.user.is_authenticated):

        return redirect('/')

    if(request.method == "POST"):

        form = UserCreationForm(request.POST)

        if(form.is_valid()):

            form.save()

            un = form.cleaned_data.get('username')

            pw = form.cleaned_data.get('password1')

            return redirect('/login')

        else:

            return render(request,'register.html',{'form':form})

    else:

        form = UserCreationForm()

        return render(request,'register.html', {'form':form})

 