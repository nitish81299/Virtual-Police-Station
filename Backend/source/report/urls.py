from django.urls import path

from . import views
app_name = 'report'

urlpatterns = [
    path('create/', views.report_create_view, name='create'),
    path('done/', views.PDFView.as_view(), name='done'),
    path('pdf/', views.pdf_view, name='pdf'),
]
