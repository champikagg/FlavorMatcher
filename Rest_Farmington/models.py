from django.db import models

# Create your models here.
class Rest_Farmington_Hills(models.Model):
	old_rest = models.CharField(max_length=50)
	new_city = models.CharField(max_length=50)
	dist_miles=models.IntegerField(max_length=10)
	
	def __unicode__(self):
		return self.old_rest
		
