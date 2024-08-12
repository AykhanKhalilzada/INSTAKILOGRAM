from django.urls import path

from .views.sidebar_pages import (
    HomePage,
    SearchPage,
    ExplorePage,
    NotificationPage,
)
from .views.detail_pages import (
    ProfilePage,
    TaggedPostsProfilePage,
    SavedPostsProfilePage,
    PostDetailPage,
)
from .views.creating_pages import (
    newpostpage,
    followuserpage,
    likepostpage,
    commentpostpage,
    savepostpage,
    tagpostpage,
)
from .views.settings_pages import (
    SettingsPage,
    RegisterPage,
    LoginPage,
    LogoutPage,
)
from .views.edit_profile_pages import (
    SeeLikedPostsPage,
    SeeCommentedPostsPage,
    EditUserDetailsPage,
)

from .views.small_pages import (
    testsendmailpage, # Test email sending page for debugging.
    UserFollowerList,
    UserFollowingList,
)
app_name = 'web'


urlpatterns = [
# Home Page
    path('', HomePage.as_view(), name='home'),

# SideBar Pages
    path('search/', SearchPage.as_view(), name='search'),
    path('explore/', ExplorePage.as_view(), name='explore'),
    path('notify/', NotificationPage.as_view(), name='notify'),

# Detail Pages
    path('<slug:slug>/', ProfilePage.as_view(), name='user-profile'),
    path('<slug:slug>/tagged', TaggedPostsProfilePage.as_view(), name='user-profile-tagged'),
    path('<slug:slug>/saved', SavedPostsProfilePage.as_view(), name='user-profile-saved'),
    path('post/<slug:slug>/', PostDetailPage.as_view(), name='post-detail'),

# Requests Pages
    path('create/post/', newpostpage, name='create-post'),
    path('create/follow/', followuserpage, name='follow'),
    path('create/like/', likepostpage, name='like'),
    path('create/comment/', commentpostpage, name='comment'),
    path('create/save/', savepostpage, name='save'),
    path('create/tag/', tagpostpage, name='tag'),
    
# Settings Pages
    path('settings/profile/edit/', SettingsPage.as_view(), name='settings'),
    path('settings/register/', RegisterPage.as_view(), name='register'),
    path('settings/login/', LoginPage.as_view(), name='login'),
    path('settings/logout/', LogoutPage.as_view(), name='logout'),

# Edit Profile Pages
    path('settings/user/edit/', EditUserDetailsPage.as_view(), name='settings-user'),
    path('settings/profile/liked/', SeeLikedPostsPage.as_view(), name='settings-likes'),
    path('settings/profile/comments/', SeeCommentedPostsPage.as_view(), name='settings-comments'),

# Small Pages
    path('test/sendmail/', testsendmailpage, name='sendmail'),
    path('<slug:slug>/followers', UserFollowerList.as_view(), name='user-followers'),
    path('<slug:slug>/following', UserFollowingList.as_view(), name='user-following'),
]