from django.contrib import admin
from django.urls import path, include
from .views import AddData, AddDataWord, UploadData

urlpatterns = [
    path('add_company', AddData.as_view(), name='add_company'),
    path('add_company_word', AddDataWord.as_view(), name='add_company_word'),
    path('upload-file', UploadData.as_view(), name='upload-file'),
]
