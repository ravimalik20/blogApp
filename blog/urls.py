from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
	url(r'(?P<blog_owner>\w+)/(?P<blog_url>\w+)/$', 'home'),
)
