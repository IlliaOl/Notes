from django.db import models
from django.contrib.auth import get_user_model


class Note(models.Model):
	text = models.CharField(max_length=120)
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(
		get_user_model(),
		on_delete=models.CASCADE,
		)



