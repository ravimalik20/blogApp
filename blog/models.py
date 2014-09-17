from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
	title = models.CharField(max_length = 100)
	url = models.CharField(max_length = 100)
	tagline = models.CharField(max_length = 500)
	owner = models.ForeignKey(User, related_name = "blog_owner")
	contributors = models.ManyToManyField(User, related_name = "blog_contributor")
	active = models.BooleanField(default = True)

	class Meta:
		unique_together = ('url', 'owner',)

	def __unicode__(self):
		return self.getCompleteURL()

	def getCompleteURL(self):
		return "%s.%s"%(self.owner.username, self.url)

class Post(models.Model):
	owner = models.ForeignKey(User, related_name = "post_owner")
	blog = models.ForeignKey(Blog)
	title = models.CharField(max_length = 100)
	contributors = models.ManyToManyField(User, related_name = "post_contributor")
	content = models.TextField()
	published_on = models.DateTimeField()
	visible = models.BooleanField(default = True)

	def __unicode__(self):
		return self.title
