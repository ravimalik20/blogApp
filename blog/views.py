from django.shortcuts import render
from blog.models import Post, Blog
from django.shortcuts import get_object_or_404, render
from django.http import Http404

def home(request, blog_id):
	context = {}
	template = "blog/templates/home.html"

	try:
		blog_id = int(blog_id)

		_blog = get_object_or_404(Blog, pk=blog_id)

		posts = Post.objects.filter(blog = _blog).order_by("-published_on")[:3]
		context["posts"] = posts
		context["blog_name"] = _blog.name
	except ValueError:
		raise Http404

	return render(request, template, context)
	
