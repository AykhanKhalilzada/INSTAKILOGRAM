# import json
from typing import Iterable
from requests import get as send_req_n_get
from urllib.parse import urlparse, parse_qs, unquote

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from .helpers.helpers import (
    MAX_TEXT_LENGTH,
    MAX_USERNAME_LENGTH,
    create_slug
)


#User Model
class CustomUserModel(AbstractUser):
    slug = models.SlugField(null=True, blank=True)
    name = models.CharField(max_length=MAX_USERNAME_LENGTH, null=True, blank=True)
    bio = models.CharField(max_length=MAX_TEXT_LENGTH, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to='instakilogram/uploads/pp/',
        default='/web/static/img/default-profile.png',
        null=True, blank=True,
    )
    is_public_account = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    def get_name(self) -> str:
        if self.name:
            return f'{self.name} (@{self.username})'
        return f'@{self.username}'
    
    def __str__(self) -> str:
        return f'{self.get_name()}'

    def clean(self) -> None:
        return super().clean()
    
    def save(self, *args, **kwargs) -> None:
        self.username = self.username.lower()
        self.slug = slugify(self.username)
        if not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        if not self.profile_image:
            self.profile_image = '/web/static/img/default-profile.png'
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self) -> str:
        return reverse_lazy('web:user-profile', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def get_followers(self) -> list:
        _followers = [ ]
        relations = self.followers.all()
        for relation in relations:
            _followers.append(relation.follower)
        return _followers

    def get_followings(self) -> list:
        _followings = [ ]
        relations = self.following.all()
        for relation in relations:
            _followings.append(relation.following)
        return _followings
    
    def get_tagged_posts(self) -> list:
        _tagged_posts = [ ]
        posts = self.tags.all()
        for tag in posts:
            _tagged_posts.append(tag.post)
        return _tagged_posts
    
    def get_saved_posts(self) -> list:
        _saved_posts = [ ]
        saves = self.saved_posts.all()
        for save in saves:
            _saved_posts.append(save.post)
        return _saved_posts
    
    def get_liked_posts(self) -> list:
        _liked_posts = [ ]
        likes = self.liked_posts.all()
        for like in likes:
            _liked_posts.append(like.post)
        return _liked_posts

#Post Model
class PostModel(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True)
    post = models.ImageField(upload_to='instakilogram/uploads/posts/')
    caption = models.CharField(max_length=MAX_TEXT_LENGTH, null=True, blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    publisher = models.ForeignKey(CustomUserModel, related_name='posts', on_delete=models.CASCADE)
    location_url = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=MAX_TEXT_LENGTH, null=True, blank=True)

    @property
    def likes_count(self) -> int: # For Admin Page
        return self.likes.count()

    def get_tagged_users(self) -> str:
        users = self.tagged_users.all()
        names = [user.__str__() for user in users]
        return f'{', '.join(names)}' if users else None

    def get_name(self) -> str:
        return f"""
            Post by {self.publisher.get_name()} on
            {self.publish_date.strftime('%b %d, %Y')}
            tagged -> {self.get_tagged_users()}
        """

    def __str__(self):
        return f'{self.get_name()}'
    
    def get_location(self) -> str:
        if self.location_url:
            final_url = urlparse(send_req_n_get(self.location_url).url)
            if 'place' in final_url.path:
                path_parts = final_url.path.split('/')
                if len(path_parts) > 2:
                    place_name = path_parts[3].replace('+', ' ')
            elif 'q' in parse_qs(final_url.query):
                query_params = parse_qs(final_url.query)
                place_name = query_params.get('q', [None])[0]
            if place_name:
                place_name = unquote(place_name)
                self.location = place_name

    def save(self, *args, **kwargs) -> None:
        if not self.location:
            self.get_location()
        if not self.slug:
            self.slug = create_slug()
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse_lazy('web:post-detail', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def get_comments(self) -> list:
        return self.comments.all()
    
#Comment Relation
class CommentUserPostRelation(models.Model):
    text = models.CharField(max_length=MAX_TEXT_LENGTH)
    publish_date = models.DateTimeField(auto_now_add=True)
    
    post = models.ForeignKey(PostModel, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUserModel, related_name='comments', on_delete=models.CASCADE)
    
    def get_name(self) -> str:
        return f'"{self.text}" by {self.user}'

    def __str__(self):
        return f'{self.get_name()}'
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


#Follow Relation
class FollowUserRelation(models.Model):
    follower = models.ForeignKey(CustomUserModel, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUserModel, related_name='followers', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_name(self) -> str:
        return f'{self.follower} -> {self.following}'
    
    def __str__(self):
        return f'{self.get_name()}'

    def clean(self):
        if self.follower == self.following:
            raise ValidationError('Follower and Following cannot be the same user.')
        
    def save(self, *args, **kwargs) -> None:
        if self.follower != self.following:
            return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        unique_together = ['follower', 'following']


#Like Relation
class LikePostRelation(models.Model):
    post = models.ForeignKey(PostModel, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUserModel, related_name='liked_posts', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_name(self) -> str:
        return f'{self.user} liked "{self.post}"'
    
    def __str__(self):
        return f'{self.get_name()}'
    
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ['user', 'post']


#Save Relation
class SavePostRelation(models.Model):
    post = models.ForeignKey(PostModel, related_name='saves', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUserModel, related_name='saved_posts', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_name(self) -> str:
        return f'{self.user} saved "{self.post}"'
    
    def __str__(self):
        return f'{self.get_name()}'
    
    class Meta:
        verbose_name = 'Save'
        verbose_name_plural = 'Saves'
        unique_together = ['user', 'post']

#Tag Relation
class TagUserPostRelation(models.Model):
    post = models.ForeignKey(PostModel, related_name='tagged_users', on_delete=models.CASCADE)
    tagged_user = models.ForeignKey(CustomUserModel, related_name='tags', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_name(self) -> str:
        return self.tagged_user
    
    def __str__(self):
        return f'{self.get_name()}'
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        unique_together = ['tagged_user', 'post']

class NotificationModel(models.Model):
    FOLLOW = 'follow'
    LIKE = 'like'
    COMMENT = 'comment'
    SAVE = 'save'
    TAG = 'tag'

    NOTIFICATION_CHOICES = [
        (FOLLOW, 'Follow'),
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
        (SAVE, 'Save'),
        (TAG, 'Tag'),
    ]

    key = models.CharField(max_length=MAX_TEXT_LENGTH, choices=NOTIFICATION_CHOICES)
    creation_date = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(CustomUserModel, related_name='notifications', on_delete=models.CASCADE)
    committer = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    
    text = models.CharField(max_length=MAX_TEXT_LENGTH, null=True, blank=True)
    post = models.ForeignKey(PostModel, on_delete=models.SET_NULL, null=True, blank=True)

    def get_name(self):
        return f'{self.text} -> {self.recipient}'
    
    def __str__(self):
        return f'{self.get_name()}'
    
    def clean(self):
        post_required_keys = [self.LIKE, self.COMMENT, self.SAVE, self.TAG]
        if (self.key in post_required_keys) and (self.post is None):
            raise ValidationError(f'Post cannot be None for {self.key} notifications.')
        super().clean()
    
    def save(self, *args, **kwargs) -> None:
        self.detect_text()
        self.clean()
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def detect_text(self):
        text_choises = {
            'follow': f'{self.committer} started following you.',
            # 'private_follow': f'{self.committer} wants to follow you.',
            'like': f'{self.committer} liked your post.',
            'save': f'{self.committer} saved your post.',
            'tag': f'{self.committer} tagged you on post.',
        }
        self.text = text_choises[self.key]