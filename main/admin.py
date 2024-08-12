from django.contrib import admin

from .helpers.helpers import SITE_NAME
from .helpers.admin_helpers import (
    make_verified,
    make_unverified,
    make_public_account,
    make_private_account,
    delete_location_info
)
from .models import (
    CustomUserModel,
    PostModel,
    CommentUserPostRelation,
    FollowUserRelation,
    LikePostRelation,
    SavePostRelation,
    TagUserPostRelation,
    NotificationModel,
)
admin.site.site_header = f'{SITE_NAME.upper()} ADMIN'

# Inlines
class LikePostInline(admin.TabularInline):
    model = LikePostRelation
    extra = 0
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
class TagUserPostInline(admin.TabularInline):
    model = TagUserPostRelation
    extra = 0
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
class CommentInline(admin.TabularInline):
    model = CommentUserPostRelation
    extra = 0
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'is_public_account', 'is_verified', 'is_staff', 'is_superuser')
    list_display_links = ('__str__', 'email')
    search_fields = ('username', 'name')
    list_filter = ('is_public_account', 'is_verified', 'is_staff', 'is_superuser')
    actions = [make_verified, make_unverified, make_public_account, make_private_account]
    # list_editable = ('is_public_account', 'is_verified', 'is_staff', 'is_superuser')
    fieldsets = (
        ('Essential', {'fields': ('username', 'email', 'password', 'slug')}),
        ('Profile', {'fields': ('name', 'profile_image', 'bio')}),
        ('Boolean', {'fields': ('is_public_account', 'is_verified', 'is_staff', 'is_superuser')}),
    )
admin.site.register(CustomUserModel, CustomUserAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'publish_date', 'likes_count', 'slug')
    list_display_links = ('__str__', 'slug')
    search_fields = ('slug',)
    list_filter = ('publish_date',)
    actions = [delete_location_info]
    fieldsets = (
        ('Essential', {'fields': ('post', 'caption', 'publisher', 'location_url', 'slug', 'location', 'publish_date')}),
    )
    readonly_fields = ('slug', 'location', 'publish_date')
    inlines = [LikePostInline, TagUserPostInline, CommentInline]
admin.site.register(PostModel, PostAdmin)

class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
    list_display_links = ('follower', 'following')
admin.site.register(FollowUserRelation, FollowAdmin)

class LikePostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    list_display_links = ('user', 'post')
admin.site.register(LikePostRelation, LikePostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'text')
admin.site.register(CommentUserPostRelation, CommentAdmin)

class SavePostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    list_display_links = ('user', 'post')
admin.site.register(SavePostRelation, SavePostAdmin)

class TagUserPostAdmin(admin.ModelAdmin):
    list_display = ('tagged_user', 'post')
    list_display_links = ('tagged_user', 'post')
admin.site.register(TagUserPostRelation, TagUserPostAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'key', 'committer', 'creation_date')
    list_display_links = ('recipient', 'key')
    fieldsets = (
        ('Essential', {'fields': ('committer', 'recipient', 'creation_date', 'post')}),
        ('Type', {'fields': ('key', 'text')}),
    )
    readonly_fields = ('creation_date', 'text')
admin.site.register(NotificationModel, NotificationAdmin)