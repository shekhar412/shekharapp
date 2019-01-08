from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post,Comment,Contact
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from blog.forms import CommentForm,ContactForm,PostAddForm
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,JsonResponse,Http404
from blog.forms import SignUpForm,UserUpdateForm,ProfileUpdateForm,PostUpdateForm,UserAddForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.loader import render_to_string

#from django.conf import settings

# Post List your views here.

def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    query=request.GET.get("q")
    if query:
        post_list=post_list.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(publish__icontains=query)).distinct()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__name__in=[tag])
    paginator=Paginator(post_list,3)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list,'tag':tag})
    #return render(request,'blog/post_list.html')

#Submit Contact Form
def contact_view(request):
    form=ContactForm()
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request,f' Message Send Successfully !')
            return redirect(contact_view)
    return render(request,'blog/contact.html',context={'form':form})

def index(request):
    return render(request,'blog/index.html')

#About View
def about_view(request):
    return render(request,'blog/about.html')

#Poat Detail View..
@login_required
def post_detail_view(request,post,year,month,day):
    post=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
            messages.success(request,f' Post Created Successfully !')
    else:
        form=CommentForm()
    is_liked=False
    if post.likes.filter(id=request.user.id).exists():
        is_liked=True
    return render(request,'blog/detail_view.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments,'is_liked':is_liked,'total_likes':post.total_likes()})



#Like & Dislike
def like_post(request):
    #post=get_object_or_404(Post,id=request.POST.get('post_id'))
    post=get_object_or_404(Post,id=request.POST.get('id'))
    is_liked=False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked=True
    context={'post':post,'is_liked':is_liked,'total_likes':post.total_likes()}
    if request.is_ajax():
        html=render_to_string('blog/like_section.html',context,request=request)
        return JsonResponse({'form':html})
    #return HttpResponseRedirect(post.get_absolute_url())




#Mial Sending Functionality
from django.core.mail import send_mail
from blog.forms import EmailSendForm

def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='{}({}) recommends you to read"{}"'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message='Read Post At:\n {}\n\n{}\'s Comments:\n {}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'suman@blog.com',[cd['to']],fail_silently=False,)
            sent=True
    else:
        form=EmailSendForm()
    return render(request,'blog/sharebymail.html',{'form':form,'post':post,'sent':sent})

#Profile View
@login_required
def profile_view(request):
    if request.method=='POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your Account has been Updated Successfully !')
            return redirect(profile_view)
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
    context={'u_form':u_form,'p_form':p_form}
    return render(request,'blog/profile.html',context)

#Adding a post from frontend..
@login_required
def add_post(request):
    author = Post.objects.all().values('author')
    if request.method=='POST':
        form=PostAddForm(request.POST)
        if form.is_valid():
            post_add=form.save(commit=False)
            post_add.author=request.user
            post_add.save()
            #If, when saving a form, you use the commit=False option you’ll need to call save_m2m() on the form
            # after you save the object, just as you would for a form with normal many to many fields on it:
            form.save_m2m()
            messages.success(request,f'Your Post has been Added Successfully !')
            return redirect(post_list_view)
    else:
        form=PostAddForm()
    return render(request,'blog/add_post.html',{'form':form})

#add profile details
@login_required
def add_profile(request):
    #author = Post.objects.all().values('author')
    if request.method=='POST':
        form=UserAddForm(request.POST)
        p_form=ProfileUpdateForm(request.POST,request.FILES)
        if form.is_valid() and p_form.is_valid():
            post_add=form.save(commit=False) and p_form.save(commit=False)
            post_add.user=request.user
            post_add.save()

            messages.success(request,f'Your Profile has been Added Successfully !')
            return redirect(post_list_view)
    else:
        form=UserAddForm()
        p_form=ProfileUpdateForm()
    return render(request,'blog/add_profile.html',{'form':form,'p_form':p_form})

#Update Post..
@login_required
def update_post(request,id):
    post=get_object_or_404(Post,id=id)
    if request.method=='POST':
        form=PostUpdateForm(request.POST or None,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your Post has been Updated Successfully !')
            return redirect(post_list_view)
    else:
        form=PostUpdateForm(instance=post)
    return render(request,'blog/update_post.html',{'form':form,'post':post})

#delete operation
def post_delete(request,id):
    post=get_object_or_404(Post,id=id)
    if request.user != post.author:
        raise Http404()
    post.delete()
    return redirect(post_list_view)


#Logout
def logout_view(request):
    messages.success(request,f' Logout Successfully !')
    return render(request,'blog/logout.html')

#Sign Up
def signup_view(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            user=form.save()
            user.set_password(user.password)
            user.save()
            messages.success(request,f' Account Created Successfully for {username} ! Now you can Login')
            return HttpResponseRedirect('/accounts/login')
    return render(request,'blog/signup.html',{'form':form})

#Change Password
@login_required
def change_password(request):
    #form=PasswordChangeForm()
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            update_session_auth_hash(request,form.user)
            form.save()
            messages.success(request,f' Your Password has been Successfully Changed')
            return redirect(profile_view)
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'blog/change_password.html',{'form':form})



#Password Reset
def password_reset_done(request):
    return render(request,'blog/password_reset_done.html')
