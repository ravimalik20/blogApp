from django.shortcuts import render
from blog.models import Post, Blog
from django.shortcuts import get_object_or_404, render
from django.http import Http404

def home(request, blog_owner, blog_url):
	context = {}
	template = "blog/templates/home.html"

	_blog = get_object_or_404(Blog, owner__username = blog_owner, url = blog_url)

	posts = Post.objects.filter(blog = _blog).order_by("-published_on")[:3]
	context["posts"] = posts
	context["blog_title"] = _blog.title

	return render(request, template, context)
	
