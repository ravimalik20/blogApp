from django import forms

class PostContentForm(forms.Form):
	title = forms.CharField(max_length = 100)
	content = forms.CharField(widget = forms.Textarea())
	
