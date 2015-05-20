from Nodes.app.nodes.forms import NodeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.views.decorators.http import require_POST

from Nodes.app.nodes import models
from Nodes.app.nodes import service




def main(request):
    nodes = models.Unit.objects.all()
    return render_to_response('nodes.html', {'nodes': nodes})


def edit_node(request, node_id):
    node_form = NodeForm(request.POST or None)
    this_node = models.Unit.objects.get(id=node_id)
    all_other_nodes = models.Unit.objects.all().exclude(id=node_id)
    connected_nodes = {}

    for connected_node in service.get_node_relations(this_node):
        connected_nodes[connected_node] = service.is_direct_node(this_node, connected_node)

    node_form.initial = {'name': this_node.name}
    context = {
        'node_form': node_form,
        'nodes': all_other_nodes,
        'node': this_node,
        'connected_nodes': connected_nodes,
        }
    if node_form.is_valid():
        node = models.Unit.objects.get(id=node_id)
        node.name = node_form.cleaned_data['name']
        node.save()
        return redirect('/')

    return render_to_response('edit.html', context=context)


def create_node(request):
    node_form = NodeForm(request.POST or None)
    all_nodes = models.Unit.objects.all()
    context = {
        'node_form': node_form,
        'nodes': all_nodes,
            }
    if node_form.is_valid():
        models.Unit.objects.create(name=node_form.cleaned_data['name'])
        return redirect('/')

    return render_to_response('create.html', context)


def weight_table(request):
    pass


@require_POST
def remove_node(request, node_id):
    models.Unit.objects.get(id=node_id).delete()
    return HttpResponseRedirect('/')

