from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.conf import settings

from main.models import CustomUserModel, PostModel
from main.helpers.helpers import SITE_NAME

# User Profile Pages
class ProfilePage(LoginRequiredMixin, DetailView):
    model = CustomUserModel
    context_object_name = 'userprofile'
    template_name = 'web/detail-pages/user-profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['site_name'] = f'{self.object} • {SITE_NAME}'
        context['is_tagged_page'] = False
        context['is_saved_page'] = False
        context['posts'] = self.object.posts.all()
        context['url_header'] = settings.URL_HEADER
        return context

class TaggedPostsProfilePage(LoginRequiredMixin, DetailView):
    model = CustomUserModel
    context_object_name = 'userprofile'
    template_name = 'web/detail-pages/user-profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['site_name'] = f'{self.object} • {SITE_NAME}'
        context['is_tagged_page'] = True
        context['is_saved_page'] = False
        context['posts'] = self.object.get_tagged_posts()
        context['url_header'] = settings.URL_HEADER
        return context
    
class SavedPostsProfilePage(LoginRequiredMixin, DetailView):
    model = CustomUserModel
    context_object_name = 'userprofile'
    template_name = 'web/detail-pages/user-profile.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['site_name'] = f'{self.object} • {SITE_NAME}'
        context['is_tagged_page'] = False
        context['is_saved_page'] = True
        context['posts'] = self.object.get_saved_posts()
        context['url_header'] = settings.URL_HEADER
        return context

# Post Page
class PostDetailPage(LoginRequiredMixin, DetailView):
    model = PostModel
    context_object_name = 'post'
    template_name = 'web/detail-pages/post-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['site_name'] = f'{self.object.caption if self.object.caption else f'Post by {self.object.publisher}'} • {SITE_NAME}'
        context['url_header'] = settings.URL_HEADER
        return context