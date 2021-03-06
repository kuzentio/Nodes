from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from Nodes.app.nodes.forms import NodeForm
from Nodes.app.nodes import models
from Nodes.app.nodes import service


def main(request):
    nodes = models.Unit.objects.all()
    return render_to_response('nodes.html', {'nodes': nodes})


def edit_node(request, node_id):

    current_node = get_object_or_404(models.Unit, id=node_id)
    other_nodes = models.Unit.objects.all().exclude(id=node_id)
    direct_connected_nodes = service.get_direct_relations(current_node).keys()
    relations = service.get_node_relations(current_node)

    node_name_form = NodeForm(request.POST or None, instance=current_node)

    context = {
        'node_name_form': node_name_form,
        'other_nodes': other_nodes,
        'current_node': current_node,
        'direct_connected_nodes': direct_connected_nodes,
        'relations': relations,
    }

    if request.method == 'POST':
        if not node_name_form.is_valid():
            return render_to_response('edit.html', context=context)
        node_name_form.save()

        actual_weights = {}
        for id, weight in request.POST.iteritems():
            try:
                actual_weights[int(id)] = int(weight)
            except ValueError:
                continue

        service.setup_actual_relations(current_node, actual_weights)
        return redirect('/')
    return render_to_response('edit.html', context=context)


def create_node(request):
    node_name_form = NodeForm(request.POST or None)

    nodes = models.Unit.objects.all()

    context = {
        'node_name_form': node_name_form,
        'other_nodes': nodes,
    }

    if request.method == 'POST':
        if not node_name_form.is_valid():
            return render_to_response('edit.html', context=context)
        current_node = models.Unit.objects.create(name=node_name_form.cleaned_data['name'])

        actual_weights = {}
        for id, weight in request.POST.iteritems():
            try:
                actual_weights[int(id)] = int(weight)
            except ValueError:
                continue

        service.setup_actual_relations(current_node, actual_weights)
        return redirect('/')

    return render_to_response('edit.html', context)


def weight_table(request):
    nodes = models.Unit.objects.all()
    relations = {}

    for node in nodes:
        relations[node] = service.get_node_relations(node)

    context = {
        'nodes': nodes,
        'relations': relations,
    }

    return render_to_response('weight_table.html', context)


@require_POST
def remove_node(request, node_id):
    models.Unit.objects.get(id=node_id).delete()
    return redirect('/')

