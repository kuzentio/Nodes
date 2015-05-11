from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.http import require_POST

from Nodes.app.nodes import models
from Nodes.app.nodes import service


def main(request):
    nodes = models.Unit.objects.all()
    return render_to_response('nodes.html', {'nodes': nodes})


def edit_node(request, node_id):
    this_node = models.Unit.objects.get(id=node_id)
    all_other_nodes = models.Unit.objects.all().exclude(id=node_id)
    connected_nodes = service.get_node_relations(this_node)
    

    context = {
        'nodes': all_other_nodes,
        'node': this_node,
        'connected_nodes': connected_nodes,
    }
    return render_to_response('edit.html', context=context)


def create_node(request):

    node = models.Unit.objects.create()
    return HttpResponseRedirect('/nodes/%s/edit' % node.id)


@require_POST
def remove_node(request, node_id):
    models.Unit.objects.get(id=node_id).delete()
    return HttpResponseRedirect('/')
