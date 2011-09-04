#coding:utf-8
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response
import json,urllib2,datetime
from BookStack.books.models import Book
import re
from BookStack import settings
import os

def handle_uploaded_file(f,ISBN):
	if f.name.find('.') != -1:
		filename = ISBN+f.name[f.name.find('.'):]
	else:
		filename = ISBN+'.txt'
	print os.getcwd()
	destination = open('/home/shihongzhi/Documents/BookStack/uploadfile/'+filename,'wb')
	for chunk in f.chunks():
		destination.write(chunk)

def download(request, ISBN):
    filename = ISBN+'.pdf'
    response = HttpResponse(mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' %filename 
    response['X-Sendfile'] = 'uploadfile/'+filename
    return response

def upload(request):
	return render_to_response('upload.html',
                                      {'user':request.user })

def upload_result(request):
	if request.method == 'POST':
		ISBN = request.POST.get('ISBN','1').strip()
		file_obj = request.FILES.get('file',None)
		handle_uploaded_file(file_obj, ISBN)
	key = '04bbcb4043cc67600e3361c0cb653620'
	url = 'http://api.douban.com/book/subject/isbn/%s?apikey=%s&alt=json'%(ISBN,key)
	try:
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
	except urllib2.HTTPError:
		error = u'ISBN 不存在！'
		return render_to_response('error.html',{'error':error})
	html = json.loads(response.read())
	bookdict = {}
	for child in html['db:attribute']:
		bookdict[child['@name']] = child['$t']
	try:
		pubdate = map(int,bookdict.get('pubdate','1990-1-1').split('-'))
	except ValueError:
		p = re.compile('\d{4}')
		pubdate = map(int,p.findall(bookdict.get('pubdate','1990-1-1')))
	while len(pubdate)<3:
		if len(pubdate)==0:
			pubdate = [1990]
		pubdate.append(1)
	image_src = html['link'][2]['@href'].replace('spic','lpic')
	b1 = Book(title=bookdict.get('title','').encode('UTF-8'),author=bookdict.get('author',''),publisher=bookdict.get('publisher',''),publish_date=datetime.date(pubdate[0],pubdate[1],pubdate[2]),pages=int(bookdict.get('pages','0')),ISBN=bookdict.get('isbn13',''),image_src = image_src)
	try:
		b1.save()
	except IntegrityError:
		error = u'这本书已经存在！'
		return render_to_response('error.html',{'error':error})
	return render_to_response('subject.html',{'book':b1}) 

def home(request):
    books = Book.objects.all()
    return render_to_response('home.html',
                                      {'user':request.user })

def search_result(request):
	if 's' in request.GET:
		keys = request.GET['s']
	else:
		keys = ''
	if keys == '':
		error = u'搜索为空'
		return render_to_response('error.html',{'error':error})
	dict = {}
	for key in keys.split():
		books = Book.objects.filter(title__icontains = key)
		for book in books:
			dict[book] = dict.get(book, 0) + len(key)

	'''
	total = len(dict)
	if total == 0:
		return render_to_response('error.html',{'error':u'没有结果'})
	if dict.values()[0] < len(''.join(keys.split()))*0.8:
		Tips = 'No book fits well , so we list %d probable ~' %total
	else:
		Tips = 'There is %d books found :' % total
	'''
	books = [k for k,v in sorted(dict.items(),lambda x, y: -cmp(x[1], y[1]))]
	return render_to_response('search_result.html',{"books":books,'user':request.user})

def subject(request, isbn):
	try:
		print isbn
		book = Book.objects.get(ISBN = isbn)
		print book,isbn
	except :
		return render_to_response('error.html')
	return render_to_response('subject.html', {'book':book,'user':request.user})

# add comment to a subject book
def subject_comment(request, isbn):
    if request.user.is_authenticated:
        try:
            book = Book.objects.get(ISBN=isbn)
            pub_date = datetime.date.today()
            user = request.user
            if request.method == 'POST':
                content = request.POST['comment']
            else:
                content = None
            if content:
                Comment.objects.create(author=user,
                                       book=book,
                                       pub_date=pub_date,
                                       content=content)

        except :
            print 'except'
    return HttpResponseRedirect("/subject/%s/" % isbn)
def about(request):
        return render_to_response('about.html', {'user':request.user})
# contact
def contact(request):
        return render_to_response('contact.html', {'user':request.user})
