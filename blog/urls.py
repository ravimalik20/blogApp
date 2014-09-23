from django.conf.urls import patterns, include, url
from blog.views import BlogHome, Home, UserHome

urlpatterns = patterns('blog.views',	
	url(r'new/$', "create_blog"),	
	url(r'(?P<post_owner>\w+)/(?P<blog_url>\w+)/(?P<post_id>\d+)/$', 'blog_post'),
	url(r'(?P<blog_owner>\w+)/(?P<blog_url>\w+)/post/$', 'post_content'),
	url(r'(?P<blog_owner>\w+)/(?P<blog_url>\w+)/$', Home.as_view()),
	url(r'(?P<username>\w+)/$', UserHome.as_view()),
	url(r'$', BlogHome.as_view()),
)
