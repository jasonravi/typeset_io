from django.conf.urls import patterns, include, url

from django.contrib import admin
from type.views import *
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^post_status/$',post_status),
    url(r'^save_blog/$',save_blog),
    url(r'^save_comment/$',save_comment),
    url(r'^all_comment_for_particular_blog/(?P<blog_id>\d+)$',all_comment_for_particular_blog,name="all_comment_for_particular_blog")
)
