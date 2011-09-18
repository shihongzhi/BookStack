from django.conf.urls.defaults import patterns, include, url
from BookStack.auth.views import signup_view,login_view,logout_view
from BookStack.books.views import subject,get_bookmarks,add_bookmark,delete_bookmark,subject_comment,popular_books,show_tags,tag_books_list
from BookStack.views import upload,upload_result,home,search_result,download,about,contact
from django.contrib import admin
admin.autodiscover()
#url
urlpatterns = patterns('',
                       # Examples:
                           # url(r'^$', 'mysite.views.home', name='home'),
                       # url(r'^mysite/', include('mysite.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                           # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       (r'^upload/$', upload),
                       (r'^upload_result/$',upload_result),
                       (r'^$',home),
                       (r'^home/$',home),
                       (r'^search_result/$',search_result),
                       (r'^subject/(\w+)/$',subject),
                       (r'^download/(\w+)/$',download),
                       (r'^signup/$', signup_view),
                       (r'^login/$',login_view),
                       (r'^about/$',about),
                       (r'^contact/$',contact),
                       (r'^logout/$',logout_view),
                       (r'^subject/(\w+)/comment/$',subject_comment),
                       (r'^subject/(\w+)/add_bookmark/$',add_bookmark),
                       (r'^bookmarks/$',get_bookmarks),
                       (r'^popular/$',popular_books),
                       (r'^tags/$',show_tags),
                       (r'^tags/(\w+)/$', tag_books_list),
                       )
