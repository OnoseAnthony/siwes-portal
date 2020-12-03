from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.forms import RegisterForm, EditSiwesForm, EditProfileForm
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def user_login(request):
    context = {}
    if request.method == 'POST':
        matric_no = request.POST['matric_no']
        a = matric_no.upper()
        password = request.POST['password']
        user = authenticate(request, matric_no=a, password=password)

        if user:
            # correct username and password login the user
            login(request, user)
            return HttpResponseRedirect(reverse('accounts:view_profile'))
        else:
            context['error'] = "Provide Valid Credentials !!"
            return render(request, 'accounts/login.html', context)

    else:
        return render(request, 'accounts/login.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:user_login'))

    else:
        form = RegisterForm()

    args = {'form': form}
    return render(request, 'accounts/reg_form.html', args)

def user_logout(request):
    if request.method == "POST":
        logout(request)
    else:
        logout(request)
        return HttpResponseRedirect(reverse('accounts:user_login'))


@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)


        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
        else:
            return redirect('/accounts/profile/edit')
    else:
        form = EditProfileForm(instance=request.user)

    args = {'form': form}
    return render(request, 'accounts/edit_profile.html', args)


@login_required
def edit_details(request):
    if request.method == 'POST':
        form = EditSiwesForm(request.POST, request.FILES, instance=request.user.siwesinformation)


        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
        else:
            return redirect('/accounts/profile/siwes')
    else:
        form = EditSiwesForm(instance=request.user.siwesinformation)

    args = {'form': form}
    return render(request, 'accounts/edit_siwes.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            return redirect('/accounts/change-password')
    else:
        form = PasswordChangeForm(user=request.user)

    for field in form.fields.values():
        field.help_text = None

    args = {'form': form}
    return render(request, 'accounts/change_password.html', args)

@login_required
def payments(request):
    args = {'user': request.user}
    return render(request, 'accounts/payment.html', args)
