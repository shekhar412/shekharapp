"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.post_list_view),
    path('add_post', views.add_post),
    path('add_profile', views.add_profile),
    path('like/', views.like_post,name='like_post'),
    path('update_post/<int:id>', views.update_post,name='update_post'),
    path('post_delete/<int:id>', views.post_delete,name='post_delete'),
    path('profile', views.profile_view),
    path('index', views.index),
    re_path(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list_view,name='post_list_by_tag_name'),
    path('contact/', views.contact_view),
    path('about/', views.about_view),
    #re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.post_detail_view, name='detail_view'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail_view,name='detail_view'),
    path('<int:id>/share/', views.mail_send_view),
    path('accounts/', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls',namespace='social')),
    path('logout/',views.logout_view),
    path('change_password/',views.change_password),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'),name='password_reset'),
    path('password_reset_comlete/',auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_comlete.html'),name='password_reset_comlete'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset/done',auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'),name='password_reset_done'),
    path('signup/',views.signup_view),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
