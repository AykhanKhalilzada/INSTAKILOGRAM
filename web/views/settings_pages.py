from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings

from main.helpers.helpers import SITE_NAME
from main.models import CustomUserModel


class SettingsPage(LoginRequiredMixin, FormView):
    template_name = 'web/settings/settings_edit/edit-profile.html'

    def post(self, request, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.bio = request.POST.get('bio')
        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES.get('profile_image')
        user.save()
        return redirect(reverse_lazy('web:user-profile', kwargs={'slug': user.slug}))

    def get_context_data(self, *args, **kwargs):
        context = { }
        context['site_name'] = f'Edit Profile • {SITE_NAME}'
        return context
    
class RegisterPage(LoginView):
    template_name = 'web/settings/register.html'
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs) -> HttpResponse:
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                username = request.POST.get('username')
                email = request.POST.get('email')
                # profile_image = request.FILES.get('profile_image')
                registered_user = CustomUserModel.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    # profile_image=profile_image
                )
                # self.send_mail(username, email)
                return redirect(reverse_lazy('web:user-profile', kwargs={'slug': registered_user.slug}))
        return redirect('web:home')

    def send_mail(self, username, email, *args, **kwargs):
        subject = 'Registered Successfully'
        message = 'Your Instakilogram account has been successfully registered. You can now log in with your email'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        print(f'{username}\' has been registered and an email has been sent to {email} with the login details.')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['site_name'] = f'Register • {SITE_NAME}'
        return context
    
class LoginPage(LoginView):
    template_name = 'web/settings/login.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['site_name'] = f'Log in • {SITE_NAME}'
        return context
    
class LogoutPage(LoginRequiredMixin, LogoutView):
    template_name = 'web/settings/logout.html'