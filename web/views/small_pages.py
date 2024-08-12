from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from main.helpers.helpers import SITE_NAME
from main.models import CustomUserModel

def testsendmailpage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        print(f'Sending email to {email} with subject: {subject} and message: {message}')
    return render(request, 'web/sidebar/send_mail.html')

class UserFollowerList(LoginRequiredMixin, DetailView):
    model = CustomUserModel
    template_name = 'web/sidebar/search.html'
    
    def get(self, request, *args, **kwargs) -> HttpResponse:
        profile = self.get_object()
        results = profile.get_followers()
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'searched': True,
                'results': results,
                'site_name': f'{profile}\'s followers • {SITE_NAME}'
            }
        )

class UserFollowingList(LoginRequiredMixin, DetailView):
    model = CustomUserModel
    template_name = 'web/sidebar/search.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        profile = self.get_object()
        results = profile.get_followings()
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'searched': True,
                'results': results,
                'site_name': f'{profile}\'s following • {SITE_NAME}'
            }
        )