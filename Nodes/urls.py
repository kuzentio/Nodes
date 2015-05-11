from Nodes.app.nodes import views
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('Nodes.app.nodes.urls')),
    ]
