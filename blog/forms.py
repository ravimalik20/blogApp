from django import forms

class PostContentForm(forms.Form):
	title = forms.CharField(max_length = 100)
	content = forms.CharField(widget = forms.Textarea())

class CreateBlogForm(forms.Form):
	title = forms.CharField(max_length = 100)
	url = forms.CharField(max_length = 100)
	tagline = forms.CharField(max_length = 500)
