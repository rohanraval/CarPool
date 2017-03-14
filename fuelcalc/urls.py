from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^results/', views.results, name='results'),
	url(r'^ajax/validate_start_zip', views.is_start_zip_valid, name='validate_start_zip'),
	url(r'^ajax/validate_dest_zip', views.is_dest_zip_valid, name='validate_dest_zip'),
	url(r'^ajax/year_processing', views.year_processing, name='year_processing'),
	url(r'^ajax/get_models', views.get_models, name='get_models'),
	url(r'^venmo/', views.venmo, name='venmo'),
]
