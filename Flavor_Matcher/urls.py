from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Flavor_Matcher.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^Rest_Farmington/', include('Rest_Farmington.urls',namespace="Rest_Farmington")),
	url(r'^admin/', include(admin.site.urls)),
)
