from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

from main.models import PostModel, CustomUserModel
from main.helpers.helpers import SITE_NAME
from main.forms import SearchPageForm


class HomePage(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    template_name = 'web/sidebar/home.html'
    paginate_by = 10
    
    def get_queryset(self):
        _user = self.request.user
        posts = PostModel.objects.filter(
            Q(publisher__in=_user.get_followings()) | Q(publisher=_user)
        )
        posts = posts.order_by('-publish_date')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_name'] = SITE_NAME
        return context

class SearchPage(LoginRequiredMixin, FormView):
    form_class = SearchPageForm #
    template_name = 'web/sidebar/search.html'

    def post(self, request, *args, **kwargs) -> HttpResponse:
        searched_user = request.POST.get('searched_user')
        if searched_user:
            results = CustomUserModel.objects.filter(username__icontains=searched_user).order_by('username')
            return render(request, self.template_name, {'searched': True, 'is_search_page': True, 'results': results, 'site_name': SITE_NAME})
        return render(request, self.template_name, {'searched': False, 'is_search_page': True, 'results': [ ], 'site_name': SITE_NAME})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_search_page'] = True
        context['site_name'] = SITE_NAME
        return context
    
class ExplorePage(LoginRequiredMixin, ListView):
    queryset = PostModel.objects.all().order_by('likes')
    context_object_name = 'posts'
    template_name = 'web/sidebar/explore.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_name'] = SITE_NAME
        return context
    
class NotificationPage(LoginRequiredMixin, ListView):
    template_name = 'web/sidebar/notification.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        _user = self.request.user
        notifications = _user.notifications.order_by('-creation_date')
        return notifications
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_name'] = SITE_NAME
        return context