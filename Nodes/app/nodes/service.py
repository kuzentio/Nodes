from Nodes.app.nodes import models
from django.db.models import Q


class Node(object):
    def __init__(self, name):
        self.name = name
        self.relations = set()

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "<%s>" % self.name

    def add_relation(self, other_node):
        self.relations.add(other_node)
        other_node.relations.add(self)


class NodeRelation(object):
    def __init__(self, node):
        self.node = node
        self.path_nodes = []

    def __hash__(self):
        return hash(self.node)

    def __eq__(self, other):
        if isinstance(other, NodeRelation):
            other == other.node
        return self.node == other

    def add_path_node(self, node):
        self.path_nodes.append(node)

    def __repr__(self):
        return "<node: %s, path_nodes: %s>" % (self.node, self.path_nodes)


def get_node_relations(start_node):
    result_relations = set()

    def _walk_node_relations(node):
        node_relations = []

        for related_node in node.relations:
            if related_node in result_relations or related_node == start_node:
                continue

            relation = NodeRelation(related_node)
            result_relations.add(relation)
            node_relations.append(relation)

            for _relation in _walk_node_relations(related_node):
                _relation.add_path_node(related_node)
                node_relations.append(_relation)

        return node_relations

    _walk_node_relations(start_node)

    return result_relations


def get_connected_nodes(start_node, result_nodes=None):
    result_nodes = result_nodes or {start_node}

    relations = models.Relationship.objects.filter(Q(start=start_node) | Q(end=start_node))

    for relation in relations:
        connected_node = relation.end if relation.start == start_node else relation.start

        if connected_node in result_nodes:
            continue

        result_nodes.add(connected_node)
        result_nodes.update(
            get_connected_nodes(connected_node, result_nodes=result_nodes)
        )

    return result_nodes - {start_node}


def get_direct_connected_nodes(start_node):
    relations = models.Relationship.objects.filter(Q(start=start_node) | Q(end=start_node))

    result_nodes = []
    for relation in relations:
        connected_node = relation.end if relation.start == start_node else relation.start
        result_nodes.append(connected_node)

    return result_nodes


def setup_actual_relations(node, actual_nodes_ids):
    current_connected_nodes = get_connected_nodes(node)
    current_connected_nodes_ids = []

    for current_connected_node in current_connected_nodes:
        current_connected_nodes_ids.append(current_connected_node.id)

    new_relations_ids = find_different_elements(actual_nodes_ids, current_connected_nodes_ids)
    for new_relation in new_relations_ids:
        models.Relationship.objects.create(start=node, end=models.Unit.objects.get(id=new_relation), value=1)

    not_actual_ids = find_different_elements(current_connected_nodes_ids, actual_nodes_ids)

    for not_actual_id in not_actual_ids:
        not_actual_relation = relation_between_nodes(node, models.Unit.objects.get(id=not_actual_id))
        if not_actual_relation:
            not_actual_relation.delete()


def find_different_elements(list1, list2):
    different_elements = []
    for element in list1:
        if element not in list2:
            different_elements.append(element)
    return different_elements


def relation_between_nodes(node1, node2):
    try:
        return models.Relationship.objects.get(
            (Q(start=node1) & Q(end=node2))
            |
            (Q(start=node2) & Q(end=node1))
        )
    except models.Relationship.DoesNotExist:
        pass










