from Nodes.app.nodes import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.main),
    url(r'^nodes/(?P<node_id>\d+)/delete/$', views.remove_node, name='delete-node'),
    url(r'^nodes/(?P<node_id>\d+)/edit/$', views.edit_node, name='edit-node'),
    url(r'^nodes/create/$', views.create_node, name='create-node'),
]
