from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils import timezone
from .models import Post, Tag, Comment, Message
from .forms import PostForm, CommentForm, MessageForm, UploadFileForm
import json, os

# Create your views here.

# Main Page
def main_page(request):
    return render(request, 'blog/main_page.html')

# Posts
def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'contacts': contacts})

def get_tag_post_list(request, tagname):
    tag = Tag.objects.filter(tag_name=tagname)[0]
    posts = tag.post_set.filter(published_date__isnull=False).order_by('-published_date')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'contacts': contacts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.visited += 1
    post.save()
    form = CommentForm()

    comment_list = Comment.objects.filter(post = post)
    comment_count = len(comment_list)
    if request.user.is_authenticated():
        for comment in comment_list:
            comment.has_read = True
            comment.save()
    return render(request, 'blog/post_detail.html',
            {'post': post, 'form': form, 'comment_list': comment_list, 'comment_count': comment_count})

def post_new_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.submit()
            return HttpResponse("success")
        else:
            return HttpResponse("error")

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tags = form.cleaned_data['tags']
            post.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.tags = form.cleaned_data['tags']
            post.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_publish(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.publish()
    return redirect('blog:post_detail', post_id=post.id)

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-create_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_remove(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('blog:post_list')

def post_like(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        post.like += 1
        post.save()
        return HttpResponse(post.like)

def post_dislike(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        post.dislike += 1
        post.save()
        return HttpResponse(post.dislike)


def recent_comments(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            if request.GET.get('action') == 'comments_count':
                return HttpResponse(len(Comment.objects.filter(has_read=False)))
            elif request.GET.get('action') == 'showlist':
                comment_list = Comment.objects.filter(has_read=False)
                return render(request, 'blog/recent_comments.html', {'comment_list': comment_list})



# Test Menu
def ajax_get_test(request):
    return HttpResponse("The data is from ajax get method")

def ajax_post_test(request):
    response_data = {};
    response_data['text'] = 'Hello ' + request.POST.get('data');
    response_data['extra'] = 'one';
    return JsonResponse(response_data);


# About Me
def about_me(request):
    return render(request, 'blog/about.html')

# Message Board
def message_board(request):
    messages = Message.objects.all().order_by('-date_time');
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.submit()
            return render(request, 'blog/message_board.html', {'form': MessageForm(), 'messages': messages})
    else:
        form = MessageForm()
    return render(request, 'blog/message_board.html', {'form': form, 'messages': messages})


# Sidebar
def get_tag_cloud_list(resuest):
    response_data = {};
    response_data['tag_list'] = [t.tag_name for t in Tag.objects.all()]
    response_data['count'] = [len(t.post_set.all()) for t in Tag.objects.all()]
    max_font_size = max(response_data['count'])
    response_data['size'] = [8.0 + 1.0 * sz / max_font_size * 10.0 for sz in response_data['count']]
    return JsonResponse(response_data)

def get_recent_posts_list(request):
    response_data = {};
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')[:5]
    response_data['title'] = [post.title for post in posts]
    response_data['id'] = [post.pk for post in posts]
    return JsonResponse(response_data)


# Upload file
@login_required
def upload_file(request):
    file_list = []
    for root, dirs, files in os.walk('media'):
        for f in files:
            file_list.append(os.path.join(root, f))
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            rescode = storage_file(request.FILES['file'], request.POST['filename'])
            response = redirect('blog:upload_file')
            if rescode == 0:
                return response
            elif rescode == 1:
                response['Location'] += '?error=repetition'
                return response
    else:
        form = UploadFileForm()
        if request.GET.get('error'):
            return render(request, 'blog/upload_file.html', {'form': form, 'file_list': file_list, 'error':'File exists'})
    return render(request, 'blog/upload_file.html', {'form': form, 'file_list': file_list})

def storage_file(file, filename):
    if os.path.exists(os.path.join('media', filename)):
        return 1
    with open(os.path.join('media', filename), 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return 0
