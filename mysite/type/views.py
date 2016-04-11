from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json,ast
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
import datetime
from django.utils import timezone
def post_status(request):
	paragraph = Paragraph.objects.all().order_by('-created_on')
	paragraph = paragraph[:5]
	user_name = request.user.username
	show_date = datetime.datetime.now().strftime('%A, %d. %B %Y')
	show_time = datetime.datetime.now().strftime('%H:%M')
	home_page = 'http://127.0.0.1:8000/admin/'
	change_password_page = 'http://127.0.0.1:8000/admin/password_change/'
	logout_page = 'http://127.0.0.1:8000/admin/logout/'
	return render_to_response(
        'admin/type/post_status.html',{ 'paragraph' : paragraph,'user_name':user_name,'show_time':show_time,'show_date':show_date,'home_page':home_page,'logout_page':logout_page,'change_password_page':change_password_page,'m':1
        },
    )

@csrf_exempt
def save_blog(request):
	try:
		if request.method == 'POST':
			context = {}
			data = request.POST.get('data')
			data = json.loads(data)
			print data
			paragraph = Paragraph()
			paragraph.title = data['status_title']
			paragraph.blog = data['status_message']
			paragraph.created_by = request.user.username
			paragraph.created_on = timezone.now()
			paragraph.save()
			context['status']='success'
			context['message']='successfully post blog!'
		else:
			context['status'] = 'failed'
			context['message']='something is wrong!' 
	except:
		context['status'] = 'failed'
		context['message']='something is wrong!' 
	return HttpResponse(json.dumps(context))

@csrf_exempt
def save_comment(request):
	if request.method == 'POST':
		context = {}
		data = request.POST.get('data')
		data = json.loads(data)
		print data;
		comment_message = data['comment']
		blog_id = data['blog_id']
		comment = Comment()
		comment.message_comment = comment_message
		comment.paragraph_id = int(blog_id)
		comment.created_by = request.user.username
		comment.created_on = timezone.now()
		comment.save()
		context['status'] = 'success'
		context['message'] = 'successfully post comment'
	else:
		context['status'] = 'failed'
		context['message'] = 'something is wrong'
	return HttpResponse(json.dumps(context))

@csrf_exempt
def all_comment_for_particular_blog(request,blog_id):
	if request.method == 'GET':
		paragraph = Paragraph.objects.get(id=int(blog_id))
		comments = Comment.objects.filter(paragraph_id=int(blog_id))
		user_name = request.user.username
		show_date = datetime.datetime.now().strftime('%A, %d. %B %Y')
		show_time = datetime.datetime.now().strftime('%H:%M')
		home_page = 'http://127.0.0.1:8000/admin/'
		change_password_page = 'http://127.0.0.1:8000/admin/password_change/'
		logout_page = 'http://127.0.0.1:8000/admin/logout/'
		context = {}
		context['comments'] = []
		for comment in comments:
			context['comments'].append(comment.message_comment)
		return render_to_response(
	        'admin/type/show_all_comment.html',{ 'paragraph':paragraph,'comments' : comments,'user_name':user_name,'show_time':show_time,'show_date':show_date,'home_page':home_page,'logout_page':logout_page,'change_password_page':change_password_page,
	        },
	    )

@csrf_exempt
def pagination(request,page_id):
	if request.method == 'GET': 
		page_id = int(page_id)
		length = len(Paragraph.objects.all())
		if page_id == 0:
			paragraph = Paragraph.objects.all().order_by('-created_on')[:5]
			m = 1
		else:
			paragraph = Paragraph.objects.all().order_by('-created_on')[5*page_id-5:5*page_id]
			m = page_id
		user_name = request.user.username
		show_date = datetime.datetime.now().strftime('%A, %d. %B %Y')
		show_time = datetime.datetime.now().strftime('%H:%M')
		home_page = 'http://127.0.0.1:8000/admin/'
		change_password_page = 'http://127.0.0.1:8000/admin/password_change/'
		logout_page = 'http://127.0.0.1:8000/admin/logout/'
		return render_to_response(
	        'admin/type/post_status.html',{ 'paragraph' : paragraph,'user_name':user_name,'show_time':show_time,'show_date':show_date,'home_page':home_page,'logout_page':logout_page,'change_password_page':change_password_page,'m':m
	        },
	    )






