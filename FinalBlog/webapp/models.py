from django.db import models
from django.contrib.auth.models import User   #User
from ckeditor.fields import RichTextField     #TextEditor
from tinymce.models import HTMLField          #TextEditor Html
#from django.utils.text import slugify         #Slugify
from django.template.defaultfilters import slugify
from django.utils import timezone             #TimeZone
import datetime                               #DateTime
from django.urls import reverse
from taggit.managers import TaggableManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='Profile_Pic/',blank = True,null = True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



#Category
class Category(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, max_length=26)

    def __str__(self):
        return self.title

    

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']


#Published Manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

#Article_Post
class Article(models.Model):
    STATUS_CHOICES = (('draft','Draft'),('published','Published'))
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=214,unique_for_date='publish')
    overview = models.TextField()
    article_image = models.ImageField(upload_to='Article/',blank = True,null = True)
    author = models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE,)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name="Category")
    body = RichTextField(verbose_name='Body')
    read = models.IntegerField(default = 0)
    publish = models.DateTimeField(default = timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    viewcount = models.IntegerField(default = 0)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()    

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish']

    def get_absolute_url(self):
        return reverse('article_details', args=[self.slug])  

    


#Comment
class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.name

