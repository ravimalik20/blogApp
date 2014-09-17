from django.shortcuts import render, HttpResponseRedirect
from blog.models import Post, Blog
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.contrib.auth.models import User
from blog.forms import PostContentForm
from django.utils import timezone

def home(request, blog_owner, blog_url):
	context = {}
	template = "blog/templates/home.html"

	_blog = get_object_or_404(Blog, owner__username = blog_owner, url = blog_url)

	posts = Post.objects.filter(blog = _blog).order_by("-published_on")[:3]
	context["posts"] = posts
	context["blog_title"] = _blog.title

	return render(request, template, context)

def blog_post(request, post_owner, blog_url, post_id):
	errors = []
	template = "blog/templates/post.html"
	try:
		post_id = int(post_id)
		post = get_object_or_404(Post, owner__username = post_owner, blog__url = blog_url, pk=post_id)
		if not post.visible:
			errors.append("Post is marked invisible.")
			post = None
	except ValueError:
		errors.append("Invalid post id.")

	context = {"errors": errors, "post": post}
	return render(request, template, context)

def user_home(request, username):
	errors = []
	template = "blog/templates/user_home.html"

	if "user" in request:
		user = request.user
	else:
		user = get_object_or_404(User, username = username)

	context = {}	
	context["user"] = user

	return render(request, template, {"username": username, "user": user})

def post_content(request, blog_owner, blog_url):
	errors = []
	template = "blog/templates/post_content.html"
	form = PostContentForm()
	_blog = Blog.objects.get(owner__username = blog_owner, url = blog_url)

	if userCanPost(request.user, _blog):
		if request.method == "POST":
			form = PostContentForm(request.POST)

			if form.is_valid():
				_post = Post(owner=request.user, blog = _blog )
				_post.title = form.cleaned_data["title"]
				_post.content = form.cleaned_data["content"]
				_post.published_on = timezone.now()
				_post.visible = True
				_post.save()
				_post.contributors.add(request.user)
				_post.save()

				return HttpResponseRedirect("/blog/%s/%s"%(blog_owner, blog_url))
				
	else:
		errors.append("Not an authorised user.")

	return render(request, template, {"errors":errors, "form": form})
			
def userCanPost(user, _blog):
	if user in _blog.contributors.all() or user == _blog.owner:
		return True
	else:
		return False
