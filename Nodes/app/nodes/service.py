from Nodes.app.nodes import models
from django.db.models import Q


class NodeRelation(object):
    def __init__(self, node, through_nodes=None):
        self.node = node
        self.through_nodes = set(list(through_nodes or []))

    def add_through_node(self, node):
        self.through_nodes.add(node)

    def remove_through_node(self, node):
        self.through_nodes -= node

    def __hash__(self):
        return hash(self.node)

    def __eq__(self, other):
        return self.node == other.node

    def __repr__(self):
        return '<node: %s, through_nodes: %s>' % (self.node, self.through_nodes)


def get_node_relations(start_node, result_nodes=None):
    result_nodes = result_nodes or {NodeRelation(start_node)}
    new_nodes = []

    relations = models.Relationship.objects.filter(Q(start=start_node) | Q(end=start_node))

    for relation in relations:
        connected_node = relation.end if relation.start == start_node else relation.start

        if NodeRelation(connected_node) in result_nodes:
            continue

        new_nodes.append(NodeRelation(connected_node, through_nodes=[start_node]))

        found_relations = get_node_relations(connected_node, result_nodes=result_nodes)
        [found_relation.add_through_node(start_node) for found_relation in found_relations]

        result_nodes.update(found_relations)

    return new_nodes


def get_node_relations_old(start_node, result_nodes=None):
    result_nodes = result_nodes or {start_node}

    relations = models.Relationship.objects.filter(Q(start=start_node) | Q(end=start_node))

    for relation in relations:
        connected_node = relation.end if relation.start == start_node else relation.start

        if connected_node in result_nodes:
            continue

        result_nodes.add(connected_node)
        result_nodes.update(
            get_node_relations_old(connected_node, result_nodes=result_nodes)
        )

    return result_nodes - {start_node}
