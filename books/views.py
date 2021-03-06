# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from BookStack.books.models import Bookmark, Book, Comment,Tag
from django.views.generic.list_detail import object_list
import datetime
# Book

# One book one page
def subject(request, isbn):
    try:
        book = Book.objects.get(ISBN=isbn)
        comments = Comment.objects.filter(book=book)
    except Book.DoesNotExist:
        return render_to_response('error.html')
    return render_to_response('subject.html', {'book':book,
                                               'user':request.user,
                                               'comments':comments,
                                               'tags':book.tags.all()} )
# popular books
def popular_books(request):
    return object_list(request, queryset=Book.objects.most_bookmarked(),
                        template_name='popular_book.html',
                        paginate_by=20)

# show tags
def show_tags(request):
    return object_list(request,
                       queryset = Tag.objects.all(),
                       template_name = 'tags.html')
# show books with tags
def tag_books_list(request, tag):
    return object_list(request,
                       queryset = Tag.objects.get(tag=tag).book_set.all(),
                       template_name = 'books_with_tag.html',
                       extra_context = {'tag':tag},
                       paginate_by = 20)
# Comment

# add comment to a subject book
@login_required                  # decorators @
def subject_comment(request, isbn):
    if request.user.is_authenticated:
        print 'hello'
        try:
            book = Book.objects.get(ISBN=isbn)
            pub_date = datetime.datetime.today()
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

        except Book.DoesNotExist:
            print 'except'
    return HttpResponseRedirect("/subject/%s/" % isbn)


# Bookmark

# add bookmark
@login_required                  # decorators @
def add_bookmark(request, isbn):
    book = get_object_or_404(Book, ISBN=isbn)
    try:
        Bookmark.objects.get(user=request.user,
                             book=book)
    except Bookmark.DoesNotExist:
        bookmark = Bookmark.objects.create(user=request.user,
                                           book=book,
                                           date=datetime.datetime.now())
    return HttpResponseRedirect("/subject/%s/" % isbn)


# delete bookmark
@login_required                 #  decorators @
def delete_bookmark(request, isbn):
    if request.method == 'POST':
        book = get_object_or_404(Book, ISBN=isbn)
        Bookmark.objects.filter(user__pk=request.user.id,
                                book__pk=book.id).delete()
        return HttpResponseRedirect("/subject/%s/" % isbn)
    else:
        return render_to_response('confirm_bookmark_delete.html',
                                  { 'book': book })


# show user's bookmarks
@login_required                 #  decorators @
def get_bookmarks(request):
    user = request.user
    try:
        # bookmarks = user.books_bookmark.all()
        bookmarks = Bookmark.objects.filter(user__pk=user.id)
    except Bookmark.DoesNotExist:
        return render_to_response('error.html',{'user':user})
    return render_to_response('bookmarks.html',{'user':user,
                                                'bookmarks':bookmarks,})
