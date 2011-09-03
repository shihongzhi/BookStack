from django.conf.urls.defaults import patterns, include, url
from mysite.auth.views import signup_view,login_view,logout_view
from mysite.views import upload,upload_result,home,search_result,subject,download,about,contact
from django.contrib import admin
admin.autodiscover()

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
)
