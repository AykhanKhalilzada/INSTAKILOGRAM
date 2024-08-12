from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from main.helpers.helpers import SITE_NAME


class SeeLikedPostsPage(LoginRequiredMixin, ListView):
    template_name = 'web/settings/settings_edit/liked-photos.html'

    def get_queryset(self):
        posts = self.request.user.get_liked_posts()
        self.context_object_name = 'posts'
        return posts

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['site_name'] = f'Edit Profile • {SITE_NAME}'
        return context

class SeeCommentedPostsPage(LoginRequiredMixin, ListView):
    template_name = 'web/settings/settings_edit/comments.html'
    context_object_name = 'comments'

    def get_queryset(self):
        comments = self.request.user.comments.all()
        self.context_object_name = 'comments'
        return comments

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['site_name'] = f'Edit Profile • {SITE_NAME}'
        return context
    
class EditUserDetailsPage(LoginRequiredMixin, View):
    template_name = 'web/settings/settings_edit/edit-user.html'

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user.save()
        return redirect(reverse_lazy('web:user-profile', kwargs={'slug': user.slug}))

    def get_context_data(self, *args, **kwargs):
        context = { }
        context['site_name'] = f'Edit User • {SITE_NAME}'
        return context