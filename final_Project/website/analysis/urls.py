from django.urls import path
from . import views
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt 
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="analysis"),
    path('rules/', views.rules, name='rules'),
    path('rule_generation_view/',  views.rule_generation_view, name='rule_generation_view'),
    path('upload_file/', views.upload_file, name="upload_file"),
    path('frequency_table/', views.frequency_table, name='frequency_table'),
    path('associationrule_table/', views.associationrule_table, name='associationrule_table'),
    path('scatterplot_view/', views.scatterplot_view, name='scatterplot_view'),
    path('barchart_view/', views.barchart_view, name='barchart_view'),
    path('heatmap_view/', views.heatmap_view, name='heatmap_view'),
    path('networkdiagram_view/', views.networkdiagram_view, name='networkdiagram_view'),
    path('parallelplot_view/', views.parallelplot_view, name='parallelplot_view'),
    path('contact/', views.contact, name='contact'),
    path('submit-contact/', views.submit_contact, name='submit_contact'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('delete_file_and_redirect/', views.delete_file_and_redirect, name='delete_file_and_redirect'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
