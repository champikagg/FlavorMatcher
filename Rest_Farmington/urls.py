from django.conf.urls import patterns, url
from Rest_Farmington import views
from Rest_Farmington import final_app

urlpatterns = patterns('',url(r'^$', views.index, name='index'),
	url(r'^city/$',views.city, name='city'),
	url(r'^about/$',views.about, name='about'),
	url(r'^contactus/$',views.contactus, name='contactus'),
	url(r'^results/$',views.results, name='results'),
	url(r'^maps/$',final_app.maps, name='maps'),
	
)