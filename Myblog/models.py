from django.db import models
from userapp.models import BlogUser


# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=20)
    img = models.ImageField(upload_to='Myblog/')
    position = models.IntegerField()
    url = models.CharField(max_length=502)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name


class Catgory(models.Model):
    name = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tags(models.Model):
    name = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=3000)
    user=models.ForeignKey(BlogUser)
    pub_time = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to='article/')
    category = models.ForeignKey(Catgory)
    tags = models.ManyToManyField(Tags)
    read_num = models.IntegerField(default=0)
    top = models.BooleanField(default=False)
    update_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class FriendLink(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=512)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    user = models.ForeignKey(BlogUser)
    article = models.ForeignKey(Article)
    content = models.CharField(max_length=200)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
