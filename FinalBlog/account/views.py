from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField
from django.contrib.auth import authenticate, login, logout
from account.forms import SignUpForm,LoginForm,UserForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.models import Group
from webapp.models import Article
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

# Create your views here.

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('dashboard')

        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# SignUp
def signupview(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations...!! You have became an Author')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            return HttpResponseRedirect('/accounts/login')
    else:
        form = SignUpForm()
    context = {'form':form}
    return render(request, 'accounts/signup.html', context)

# SignUp
def signupadminview(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations...!! You have became an Admin')
            user = form.save()
            group = Group.objects.get(name='Admin')
            user.groups.add(group)
            return HttpResponseRedirect('/accounts/login')
    else:
        form = SignUpForm()
    context = {'form':form}
    return render(request, 'accounts/signupadmin.html', context)

# Login
def loginview(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    request.session.set_expiry(300)
                    messages.success(request, 'Logged in Successfully..!!')
                    return redirect('/accounts/login')
        else:
            form = LoginForm()
        return render(request, 'accounts/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/accounts/dashboard')

# LogOut
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        article = Article.objects.all()
        user = request.user
        full_name = user.get_full_name()
        grps = user.groups.all()
        context = {'article':article, 'full_name':full_name, 'groups':grps}
        return render(request, 'accounts/dashboard.html', context)
    else:
        return HttpResponseRedirect('/acconts/login')

        