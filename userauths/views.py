from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from userauths.models import *
from django.http import JsonResponse
from userauths.forms import *


def sign_up_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You're already Logged In.")
        return redirect('home:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hello {username}, your account created successfully.")
            new_user = authenticate(username=form.cleaned_data.get('email'),
                                    password=form.cleaned_data.get('password1'))
            login(request, new_user)
            return redirect('home:home')
    else:
        form = SignUpForm()
    return render(request, 'userauths/sign_up.html', {'form': form})


def sign_in_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You're already Logged In.")
        return redirect('home:home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            messages.success(request, f"You're logged in successfully.")
            login(request, user)
            return redirect('home:home')
        else:
            messages.warning(request, "User doesn't exist, create account.")
    return render(request, 'userauths/sign_in.html', {})


def sign_out_view(request):
    logout(request)
    messages.success(request, "You're logged out successfully.")
    return redirect('home:home')


def contact_us(request):
    return render(request, 'userauths/contact_us.html', {})


def ajax_contact_us(request):
    full_name = request.GET.get('full_name')
    email = request.GET.get('email')
    phone = request.GET.get('phone')
    subject = request.GET.get('subject')
    message = request.GET.get('message')
    ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message
    )
    return JsonResponse({
        'boolean': True
    })


def edit_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('home:dashboard')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'userauths/edit-profile.html', {'form': form, 'profile': profile})


def change_password(request):
    if request.method == 'POST':
        form1 = ChangePasswordForm(request.POST)
        email = request.user.email
        if form1.is_valid():
            user = request.user
            user.password = form1.cleaned_data.get('password1')
            user.save()
            logout(request)
            return redirect('userauths:sign-in')
    else:
        form1 = ChangePasswordForm()
    return render(request, 'userauths/change-password.html', {'form1': form1})
