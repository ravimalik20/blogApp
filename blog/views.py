from django.shortcuts import render, HttpResponseRedirect
from blog.models import Post, Blog
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.contrib.auth.models import User
from blog.forms import PostContentForm, CreateBlogForm
from django.utils import timezone

from django.views.generic import View
from django.views.generic.edit import FormView

class TemplateView(View):
	template = ""

	def get(self, request, *args, **kwargs):
		context = {"request": request}

		return render(request, self.template, context)

class BlogHome(TemplateView):
	template = "blog/templates/blog_home.html"

class Home(View):
	template = "blog/templates/home.html"

	def get(self, request, blog_owner, blog_url, *args, **kwargs):
		context = {}

		_blog = get_object_or_404(Blog, owner__username = blog_owner, 
			url = blog_url)
		posts = Post.objects.filter(blog = _blog).order_by("-published_on")[:3]

		context["posts"] = posts
		context["blog_title"] = _blog.title
		context["blog_owner"] = blog_owner
		context["user"] = request.user

		return render(request, self.template, context)

def blog_post(request, post_owner, blog_url, post_id):
	errors = []
	template = "blog/templates/post.html"
	context = {}

	try:
		post_id = int(post_id)
		post = get_object_or_404(Post, owner__username = post_owner,
			blog__url = blog_url, pk=post_id)
		if not post.visible:
			errors.append("Post is marked invisible.")
			post = None
	except ValueError:
		errors.append("Invalid post id.")

	context = {"errors": errors, "post": post, "user": request.user}

	return render(request, template, context)

class UserHome(View):
	template = "blog/templates/user_home.html"

	def get(self, request, *args, **kwargs):
		context={}
		username = kwargs["username"]

		blog_owner = get_object_or_404(User, username = username)

		context["blog_owner"] = blog_owner
		context["username"] = username
		context["user"] = request.user

		return render(request, self.template, context)

def post_content(request, blog_owner, blog_url):
	errors = []
	template = "blog/templates/post_content.html"
	context = {}

	form = PostContentForm()
	_blog = Blog.objects.get(owner__username = blog_owner,
		url = blog_url)

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

				return HttpResponseRedirect("/blog/%s/%s/"%(blog_owner, blog_url))
				
	else:
		errors.append("Not an authorised user.")

	context["errors"] = errors
	context["form"] = form
	context["blog_owner"] = blog_owner
	context["user"] = request.user

	return render(request, template, context)

def create_blog(request):
	errors = []
	template = "blog/templates/create_blog.html"
	context = {}
	
	form = CreateBlogForm()
	user = request.user

	if not user.is_authenticated():
		raise Http404

	if request.method == "POST":
		form = CreateBlogForm(request.POST)

		if form.is_valid():
			try:
				data = form.cleaned_data
				_blog = Blog()
				_blog.title = data["title"]
				_blog.owner = user
				_blog.url = data["url"]
				_blog.tagline = data["tagline"]
				_blog.active = True
				_blog.save()
				_blog.contributors.add(user)
				_blog.save()
				return HttpResponseRedirect("/blog/%s/"%user.username)
			except:
				errors.append("Blog URL already taken.")

	context["errors"] = errors
	context["form"] = form
	context["user"] = user

	return render(request, template, context)

def userCanPost(user, _blog):
	if user in _blog.contributors.all() or user == _blog.owner:
		return True
	else:
		return False
