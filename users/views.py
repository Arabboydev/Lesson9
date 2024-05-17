from django.shortcuts import render, redirect
from django.views import View
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserForm, ProfileUpdateForm

from .forms import CustomUserForm


class RegisterView(View):
    def get(self, request):
        create_form = CustomUserForm()
        context = {
            'form': create_form
        }
        return render(request, 'register.html', context=context)

    def post(self, request):
        create_form = CustomUserForm(data=request.POST, files=request.FILES)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'register.html', context=context)


# class RegisterView(View):
#     def get(self, request):
#         return render(request, 'register.html')
#
#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']
#         email = request.POST['email']
#         last_name = request.POST['last_name']
#         first_name = request.POST['first_name']
#
#         user = CustomUser.objects.create_user(
#             username=username,
#             email=email,
#             first_name=first_name,
#             last_name=last_name
#         )
#         user.set_password(password)
#         user.save()
#
#         return redirect('users:login')


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            'form': login_form
        }
        return render(request, 'login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('landing_page')
        else:
            context = {
                'form': login_form
            }
            return render(request, 'login.html', context=context)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')


class ProfileView(View):
    def get(self, request):
        return render(request,'profile.html', context={'user':request.user})


class ProfileUpdateView(View):
    def get(self, request):
        update_form = ProfileUpdateView(instance=request.user)
        return render(request, 'profile_update.html', context={'user':update_form})

    def post(self, request):
        update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('user:profile')
        else:
            return render(request,'profile_update.html',context={'form':update_form})