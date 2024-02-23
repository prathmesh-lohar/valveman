"""
URL configuration for valveman project.

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
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.index, name="index"),
    path("all_tanks",views.all_tanks, name="all_tanks"),
    path("draw_line",views.draw_line, name="draw_line"),
    path("save_markers",views.save_markers, name="save_markers"),
    path("extend",views.extend, name="extend"),
    path("delete_marker/<int:path_id>/<int:point_id>",views.delete_marker, name="delete_marker"),
    
    
    path("get_markers",views.get_markers, name="get_markers"),
    path("login",views.login, name="login"),
    path("get_existing_marker",views.get_existing_marker, name="get_existing_marker"),
    
    path('save_marker_point_id', views.save_marker_point_id, name='save_marker_point_id'), 

    path('logout', views.logout, name='logout'), 
    
    
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
