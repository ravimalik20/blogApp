from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
	url(r'(?P<post_owner>\w+)/(?P<blog_url>\w+)/(?P<post_id>\d+)/$', 'blog_post'),
	url(r'(?P<blog_owner>\w+)/(?P<blog_url>\w+)/post/$', 'post_content'),
	url(r'(?P<blog_owner>\w+)/(?P<blog_url>\w+)/$', 'home'),
	url(r'(?P<username>\w+)/$', 'user_home'),
)
