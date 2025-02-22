"""
URL configuration for guternberg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include 
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from books import views

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', views.book_list, name='book-list'),  
    path("testapi/",views.testapi,name="testapi"),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # OpenAPI Schema
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI 
]
