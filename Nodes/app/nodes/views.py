from Nodes.app.nodes.forms import NodeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from Nodes.app.nodes import models
from Nodes.app.nodes import service


def main(request):
    nodes = models.Unit.objects.all()
    return render_to_response('nodes.html', {'nodes': nodes})


def edit_node(request, node_id):

    current_node = get_object_or_404(models.Unit, id=node_id)

    node_name_form = NodeForm(request.POST or None, instance=current_node)

    other_nodes = models.Unit.objects.all().exclude(id=node_id)
    connected_nodes = service.get_connected_nodes(current_node)

    direct_connected_nodes = service.get_direct_connected_nodes(current_node)
    weight_direct_nodes = service.find_weight_direct_relations(current_node, direct_connected_nodes)

    context = {
        'node_name_form': node_name_form,
        'other_nodes': other_nodes,
        'current_node': current_node,
        'connected_nodes': connected_nodes,
        'direct_connected_nodes': direct_connected_nodes,
        'weight_direct_nodes': weight_direct_nodes,
    }

    if request.method == 'POST':
        if not node_name_form.is_valid():
            return render_to_response('edit.html', context=context)
        else:
            node = models.Unit.objects.get(id=node_id)
            node.name = node_name_form.cleaned_data['name']
            node.save()


        actual_weights = {}
        for id, weight in request.POST.iteritems():
            try:
                actual_weights[int(id)] = int(weight)
            except:
                continue
        service.setup_actual_relations(current_node, actual_weights)
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

    all_nodes = models.Unit.objects.all()
    relations = {}
    context = {
        'relations': relations,
        'all_nodes': all_nodes,
    }
    render_to_response('weight_table.html', context)


@require_POST
def remove_node(request, node_id):
    models.Unit.objects.get(id=node_id).delete()
    return HttpResponseRedirect('/')

