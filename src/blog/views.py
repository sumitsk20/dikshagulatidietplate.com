# Create your views here.
try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category, Tag, Faq
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from comments.forms import CommentForm
from comments.models import Comment


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()  # when user is not admin
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()  # when use is admin

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "post_list": queryset,
        "title": "Blog",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "blog/blog.html", context)


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if not post.publish_this_post:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(post.content)

    initial_data = {
        "content_type": post.get_content_type,
        "object_id": post.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()  # comment user for parent comment

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        try:
            if parent_obj.user.id == request.user.id:
                return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
        except:
            pass

        template = get_template('comments/comment_posted.txt')
        context = Context({
            'user': request.user,
            'content_title': new_comment.content_object.title,
            'content_url': request.build_absolute_uri(),
            'content': content_data,
            'parent': parent_obj,
        })
        content = template.render(context)
        email = EmailMessage(
            subject="[DietPlate] New comment",
            body=content,
            from_email="DietPlate <info@dikshagulatidietplate.com>",
            to=['dietplate.dp@gmail.com'],  # main id of dietplate
            bcc=['diksha.gulati1310@gmail.com'],  # bcc gmail id of dietplate
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = post.comments
    context = {
        "title": post.title,
        "post": post,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "blog/post.html", context)


def category_list_view(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    cat_post_list = category.post_set.all()
    if not cat_post_list:
        raise Http404()
    context = {
        'cat_post_list': cat_post_list,
        'title': 'Categories',
    }
    return render(request, "blog/category_list_view.html", context)


def tag_list_view(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    tag_post_list = tag.post_set.all()
    if not tag_post_list.count > 0:
        raise Http404("No MyModel matches the given query.")
    context = {
        'tag_post_list': tag_post_list,
        'title': 'Tags',
    }
    return render(request, "blog/tag_list_view.html", context)


def faq(request):
    faqs = Faq.objects.active()
    context = {
        'faqs': faqs,
        'title': 'Frequenty Asked Questions'
    }
    return render(request, "blog/faq.html", context)
