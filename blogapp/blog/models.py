from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{ self.user.username } Profile'

    def save(self):
        super().save()
        img=Image.open(self.image.path)
        if img.height > 500 or img.width >500 :
            output_size=(400,400)
            img.thumbnail(output_size)
            img.save(self.image.path)


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

# Create your models here.
from taggit.managers import TaggableManager
class Post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=256)
    slug=models.SlugField(max_length=264,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.DO_NOTHING)
    body=models.TextField()
    likes=models.ManyToManyField(User,related_name='likes',blank=True)
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects=CustomManager()
    tags=TaggableManager()

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_view',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])


    #def get_absolute_url(self):
        #return reverse('detail_view',args=[self.id,self.slug])

    def total_likes(self):
        return self.likes.count()

#model related to comments section
class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.DO_NOTHING,)
    #user=models.ForeignKey(User,related_name='users',on_delete=models.DO_NOTHING,)
    name=models.CharField(max_length=64)
    reply=models.ForeignKey('Comment',null=True,related_name="replies",on_delete=models.DO_NOTHING,)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=('-created',)

    def __str__(self):
        return 'Commented By {} on {}'.format(self.name,self.post)



class Contact(models.Model):
    name=models.CharField(max_length=256)
    email=models.EmailField()
    phone=models.IntegerField()
    body=models.TextField()
