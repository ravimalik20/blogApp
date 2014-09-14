from django.conf.urls import include, patterns, url

urlpatterns = patterns( 'user_app.views',
	url(r'login/$', 'signin'),
	url(r'logout/$', 'signout'),
	url(r'signup/$', 'signup'),
)
