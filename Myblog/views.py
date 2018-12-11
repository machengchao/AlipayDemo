from django.shortcuts import render
from .models import *
from django.shortcuts import render_to_response
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import redirect


# Create your views here.


def index(request):
    banners = Banner.objects.all()
    topArticle = Article.objects.filter(top=True).all()
    articles = Article.objects.order_by('-pub_time').all()
    categorys = Catgory.objects.all()
    friendlink = FriendLink.objects.all()
    Comments_all = Comment.objects.order_by('-create_time').all()
    count = Article.objects.count()
    article_ids = []  # 装文章的ID
    comments = []  # 装处理后的ID

    for comment in Comments_all:
        if comment.article.id not in article_ids:
            article_ids.append(comment.article.id)
            comments.append(comment)

    comments = comments[:7]

    return render(request, 'index.html', locals())


def list(request, cid=-1, tid=-1):
    if cid != -1:
        try:
            categorys = Catgory.objects.get(pk=cid)
            articles = categorys.article_set.all()
        except Catgory.DoesNotExist:
            return render(request, '404.html')
    elif tid != -1:
        try:

            tag = Tags.objects.get(pk=tid)
            articles = tag.article_set.all()
        except Tags.DoesNotExist:
            return render(request, '404.html')
    else:
        articles = Article.objects.order_by('-pub_time').all()
    tags = Tags.objects.all()
    d = Comment.objects.order_by('-create_time').all()

    Comments_all = Comment.objects.order_by('-create_time').all()
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(articles, per_page=2, request=request)

    articles_list = p.page(page)

    article_ids = []  # 装文章的ID
    comments = []  # 装处理后的ID

    for comment in Comments_all:
        if comment.article.id not in article_ids:
            article_ids.append(comment.article.id)
            comments.append(comment)

    ctx = {
        'articles_list': articles_list, 'tags': tags, 'd': d, 'articles': articles, 'comments': comments[:7]
    }

    return render(request, 'list.html', ctx)


def show(request, id):
    # d = Comment.objects.all()
    Comments_all = Comment.objects.order_by('-create_time').all()
    articles = Article.objects.order_by('-pub_time').all()
    count = Article.objects.count()
    article_ids = []  # 装文章的ID

    comments = []  # 装处理后的ID

    for comment in Comments_all:
        if comment.article.id not in article_ids:
            article_ids.append(comment.article.id)
            comments.append(comment)
    try:

        article = Article.objects.get(pk=id)
        d = article.comment_set.order_by('-create_time').all()

        article.read_num += 1
        article.save()
        # 把文字对应的标签取出来
        tags = article.tags.all()
        # 去除文章对应的文章
        recommends = []  # 相关推荐的文章
        for tag in tags:
            recommends.extend(tag.article_set.all())

    except Exception as e:
        return render(request, '404.html')
    comments = comments[:7]

    return render(request, 'show.html', locals())


class Search(View):
    def get(self, request):
        kw = request.GET.get('kw')
        search_list = Article.objects.filter(Q(title__icontains=kw) | Q(content__icontains=kw))
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(search_list, per_page=2, request=request)

        articles_list = p.page(page)
        return render(request, 'list.html', locals())


class CommentArticle(View):
    def post(self, request, id):
        comment_content = request.POST.get('comment_content')
        comment = Comment()
        comment.content = comment_content
        comment.article = Article.objects.get(id=id)
        comment.user = request.user
        comment.save()
        return redirect('/blog/' + id)
