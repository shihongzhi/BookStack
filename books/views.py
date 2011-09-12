from django.http import HttpResponseRedirect
from django.shortcus import render_to_response
from BookStack.books.models import Book,Comment
import datetime

def subject(request, isbn):
    #try:
    book = Book.objects.get(ISBN=isbn)
    comments = Comment.objects.filter(book=book)
    #except :
        #return render_to_response('error.html')
    return render_to_response('subject.html', {'book':book,
                                               'user':request.user,
                                               'comments':comments} )

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

