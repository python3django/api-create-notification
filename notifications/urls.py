from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'ckeditor/',
        include('ckeditor_uploader.urls'),
    ),

    path(
        'api/v1/',
        include(('api.urls', 'api'), namespace='v1'),
    ),
]
