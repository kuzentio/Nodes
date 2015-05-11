from django.db.models import Q

from Nodes.app.nodes import models


def get_node_relations(start_node, result_nodes=None):
    result_nodes = result_nodes or {start_node}

    nodes = models.Relationship.objects.filter(Q(start=start_node) | Q(end=start_node))

    for relation in nodes:
        other_node = relation.end if relation.start == start_node else relation.start
        if other_node in result_nodes:
            continue

        result_nodes.add(other_node)
        result_nodes.update(get_node_relations(other_node, result_nodes=result_nodes))

    return result_nodes - {start_node}
