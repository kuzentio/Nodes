from Nodes.app.nodes import models
from django.db.models import Q


def get_node_relations(start_node, result_nodes=None):
    result_nodes = result_nodes or {start_node}

    relations = models.Relationship.objects.filter(Q(start=start_node) | Q(end=start_node))

    for relation in relations:
        connected_node = relation.end if relation.start == start_node else relation.start

        if connected_node in result_nodes:
            continue

        result_nodes.add(connected_node)
        result_nodes.update(
            get_node_relations(connected_node, result_nodes=result_nodes)
        )

    return result_nodes - {start_node}
