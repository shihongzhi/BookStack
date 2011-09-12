#coding:utf-8
from django.db import IntegrityError
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import json,urllib2,datetime
from BookStack.books.models import Book,Comment
import re
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
    if request.user.is_authenticated:
        if request.method == 'POST':
            ISBN = request.POST.get('ISBN','1').strip()
            file_obj = request.FILES.get('file',None)
            #handle_uploaded_file(file_obj, ISBN)
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
        user = request.user
        b1 = Book(title=bookdict.get('title','').encode('UTF-8'),author=bookdict.get('author',''),publisher=bookdict.get('publisher',''),publish_date=datetime.date(pubdate[0],pubdate[1],pubdate[2]),pages=int(bookdict.get('pages','0')),ISBN=bookdict.get('isbn13',''),image_src = image_src, user= user, upload_date=datetime.datetime.today())
        try:
            b1.save()
        except IntegrityError:
            error = u'这本书已经存在！'
            #return render_to_response('error.html',{'error':error})
            return HttpResponseRedirect("/subject/%s/" % ISBN)
        handle_uploaded_file(file_obj, ISBN)
        return HttpResponseRedirect("/subject/%s/" % ISBN)
    else:
        error = u'还没有登录'
        return render_to_response('error.html',{'error':error})
 

def home(request):
    return render_to_response('home.html',
                                      {'user':request.user })

def search_result(request):
	if 's' in request.GET:
		keys = request.GET['s']
	else:
		keys = ''
	if keys == '':
		#error = u'搜索为空'
		#return render_to_response('error.html',{'error':error})
                render_to_response('home.html', {'user':request.user })
	dict = {}
	for key in keys.split():
		books = Book.objects.filter(title__icontains = key)
		for book in books:
			dict[book] = dict.get(book, 0) + len(key)


        total = len(dict)
        # no book found
        if total == 0:
            Tips = '没有找到相关书籍'
            return render_to_response('search_result.html',{"books":None,"Tips":Tips,'user':request.user})
        if dict.values()[0] < len(keys)*0.8:
            Tips = '没有搜索到匹配的书 , 可能这 %d 本书中有你喜欢的 ~' %total
        else:
            Tips = '总共找到 %d 本书' % total
        # sort
	books = [k for k,v in sorted(dict.items(),lambda x, y: -cmp(x[1], y[1]))]
	return render_to_response('search_result.html',{"books":books,'user':request.user,'Tips':Tips})
def about(request):
        return render_to_response('about.html', {'user':request.user})
# contact
def contact(request):
        return render_to_response('contact.html', {'user':request.user})
