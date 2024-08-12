from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import render

from main.models import (
    CustomUserModel,
    PostModel,
    CommentUserPostRelation,
    FollowUserRelation,
    LikePostRelation,
    SavePostRelation,
    TagUserPostRelation,
    NotificationModel,
)
from main.helpers.helpers import SITE_NAME
from main.forms import NewPostForm


@login_required
@csrf_exempt
def newpostpage(request):
    if request.method == 'POST':
        if request.POST.get('deletion_token'):
            post_id = request.POST.get('deletion_token')
            post = PostModel.objects.get(id=post_id)
            if post.publisher == request.user:
                post.delete()
                return redirect(reverse_lazy('web:user-profile', kwargs={'slug': post.publisher.slug}))
            else:
                return JsonResponse({'success': False, 'error': 'You are not authorized to delete this post'})
        created_post = PostModel.objects.create(
            publisher=request.user,
            post=request.FILES.get('post'),
            caption=request.POST.get('caption'),
            location_url=request.POST.get('location_url')
        )
        return redirect(created_post.get_absolute_url())
    else:
        form = NewPostForm()
        return render(request, 'web/sidebar/new_post.html', {'form': form, 'site_name': f'New Post • {SITE_NAME}'})

@login_required
@csrf_exempt
def followuserpage(request):
    if request.method == 'POST':
        following_id = request.POST.get('following_id')
        following_user = CustomUserModel.objects.get(id=following_id)
        follow_relation, is_created = FollowUserRelation.objects.get_or_create(
            follower=request.user,
            following=following_user
        )
        if not is_created:
            follow_relation.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def likepostpage(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = PostModel.objects.get(id=post_id)
        like, is_created = LikePostRelation.objects.get_or_create(
            post=post,
            user=request.user
        )
        if not is_created:
            like.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def commentpostpage(request):
    if request.method == 'POST':
        deletion_token = request.POST.get('deletion_token')

        if deletion_token:
            comment_id = request.POST.get('deletion_token')
            comment = CommentUserPostRelation.objects.get(id=comment_id)
            if comment.user == request.user:
                comment.delete()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'You are not authorized to delete this comment'})

        else:
            post_id = request.POST.get('post_id')
            post = PostModel.objects.get(id=post_id)
            text = request.POST.get('comment')
            if text:
                CommentUserPostRelation.objects.create(
                    post=post,
                    user=request.user,
                    text=text
                )
            redirect_url = request.POST.get('redirect_url')
            return redirect(redirect_url)

@login_required
@csrf_exempt
def savepostpage(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = PostModel.objects.get(id=post_id)
        save, is_created = SavePostRelation.objects.get_or_create(
            post=post,
            user=request.user
        )
        if not is_created:
            save.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def tagpostpage(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = PostModel.objects.get(id=post_id)
        tag, is_created = TagUserPostRelation.objects.get_or_create(
            post=post,
            user=request.user
        )
        if not is_created:
            tag.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})