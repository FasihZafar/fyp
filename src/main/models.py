from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models


class File(models.Model):
	name = models.CharField(max_length=200)
	url =  models.CharField(max_length=200)
	path = models.CharField(max_length=200)
	person = models.CharField(max_length=200)
	job = models.TextField()
	skills = models.TextField()

	skills_vector = SearchVectorField(null=True)
	job_vector = SearchVectorField(null=True)

	class Meta:
		indexes = [GinIndex(
				fields=[
					'skills_vector',
					'job_vector',
				]
			)
		]


	def __str__(self):
		return self.name

# class Person(models.Model):

# 	name = models.CharField(max_length=200)
# 	job = models.TextField()
# 	skills = models.TextField()


# 	skills_vector = SearchVectorField(null=True)
# 	job_vector = SearchVectorField(null=True)

# 	class Meta:
# 		indexes = [GinIndex(
# 				fields=[
# 					'skills_vector',
# 					'job_vector'
# 				]
# 			)
# 		]
			

# 	def __str__(self):
# 		return self.name