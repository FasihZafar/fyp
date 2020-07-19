from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
# from utils.ocr import textExtract
# from utils.ocr import textExtract 
from .models import File
from utils.helpers import *
import spacy
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
import time
import threading
import sys
import concurrent.futures
import timeit
import pdf2image
import pytesseract as pt


nlp = spacy.load(os.path.join( os.getcwd(), os.path.join( 'utils', 'final'))) #load spacy ner model


def home(request): #home page view
	context = {}
	context['count'] = File.objects.all().count()#total number of files in db
	return render(request, 'home.html', context)


def parseFile(file, url, path):#function to run in background for document parsing
	"""
	function parseFile() input: String file, String url, String path -> create a File object and adds to table File
	"""

	pages = None
	text = None
	
	start = timeit.default_timer()
	with concurrent.futures.ThreadPoolExecutor() as executor: #takes 3 seconds
		future = executor.submit(pdf2image.convert_from_path, path, dpi=300, thread_count=sys.maxsize)
		pages = future.result()
	
	with concurrent.futures.ThreadPoolExecutor() as executor: #takes 3 seconds
		text = [ pt.image_to_string( page, lang="eng", config="--psm 10 --psm 11 --psm 6 -c preserve_interword_spaces=1") for page in pages ]		

	text = " ".join(text)
	text = text.lower()


	doc = nlp(text)
	name = doc.ents[0]
	job = doc.ents[1]
	skills = doc.ents[2:]
	skills = "\n".join(map(str,skills))

	f = File(name=file, url=url, path=path, person=name, job=job, skills=skills)
	f.save()





def upload(request):
	context = {}
	context['count'] = File.objects.all().count()

	if request.method == 'POST':

		# fs = FileSystemStorage()
		
		try:
			if not request.FILES.getlist('document'): #check file exists
				context['error'] = "No file attached!" 
				raise Exception('No file attached!')
			
			if len( request.FILES.getlist('document') ) > 1: #check single uplad
				context['error'] = "Upload a single file!" 
				raise Exception('Upload a single file!')
			
			file = request.FILES.getlist('document').pop(0) 
			if not file.name.endswith('.pdf'): #check if file is pdf
				context['error'] = "Only PDF support available!" 
				raise Exception('Only PDF support available!')

						
		except Exception as e:
			print(e)
			return render(request, 'home.html', context)
		
		else:

			fs =  FileSystemStorage()
			file = request.FILES.getlist('document').pop(0)
			upload = fs.save(file.name, file)

			print('daemon started')
			t = threading.Thread(target=parseFile, args=[file.name, fs.url(upload), fs.path(upload)])
			t.start()


			return redirect(home)

	return render(request, 'home.html', context)



def search(request):
	context = {}

	if request.method == 'POST':
		q = str(request.POST.get('q').lower())
		q = q.replace('not','~').replace('and','&').replace('or','|')
		vector = SearchVector('skills_vector') + SearchVector('job_vector')
		query = SearchQuery(q, search_type='raw')
		files = File.objects.annotate(
			rank = SearchRank(vector, query),
		).filter(rank__gt=0.0).order_by('-rank')
		context['files'] = files
		context['count'] = File.objects.all().count()#total number of files in db

	return render(request, 'home.html', context)
