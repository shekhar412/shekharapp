from django.contrib import admin
from blog.models import Post,Comment,Profile,Contact

# Register your models here.
class AdminPost(admin.ModelAdmin):
    list_display=['title','slug','author','created','updated','publish','status']
    list_filter=('status','author','publish',)
    search_fields=('title','body',)
    #raw_id_fields=('author',)
    date_hierarchy='publish'
    ordering=['status','publish']
    prepopulated_fields={'slug':('title',)}


admin.site.register(Post,AdminPost)


class AdminProfile(admin.ModelAdmin):
    list_display=['user','image']
admin.site.register(Profile,AdminProfile)


class AdminContact(admin.ModelAdmin):
    list_display=['id','name','email','phone','body']
admin.site.register(Contact,AdminContact)

class AdminComment(admin.ModelAdmin):
    list_display=['name','email','post','body','created','updated']
    list_filter=('active','created','body')
    search_fields=('name','email','body')

admin.site.register(Comment,AdminComment)
