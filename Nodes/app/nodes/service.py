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


def setup_actual_relations_old(node, actual_relations):
    current_connected_nodes = get_direct_connected_nodes(node)
    current_connected_nodes_ids = []
    actual_nodes_ids = []

    for actual_node_id in actual_relations.iterkeys():
        actual_nodes_ids.append(actual_node_id)

    for current_connected_node in current_connected_nodes:
        current_connected_nodes_ids.append(current_connected_node.id)

    not_actual_ids = find_different_elements(current_connected_nodes_ids, actual_nodes_ids)
    for not_actual_id in not_actual_ids:
        not_actual_relation = relation_between_nodes(node, models.Unit.objects.get(id=not_actual_id))
        if not_actual_relation:
            not_actual_relation.delete()

    entered_elements = find_entered_elements(current_connected_nodes_ids, actual_nodes_ids)
    for entered_element_id in entered_elements:
        models.Relationship.objects.update(start=node, end=models.Unit.objects.get(id=entered_element_id), value=actual_relations[entered_element_id])

    #direct_connected_nodes = get_direct_connected_nodes(node)


    new_related_unit_ids = find_different_elements(actual_nodes_ids, current_connected_nodes_ids)
    for new_relation_id in new_related_unit_ids:
        models.Relationship.objects.create(start=node, end=models.Unit.objects.get(id=new_relation_id), value=actual_relations[new_relation_id])


def setup_actual_relations(node, actual_node_weighs):
    current_connected_nodes_ids = set([n.id for n in get_connected_nodes(node)])
    current_direct_connected_nodes_ids = set([n.id for n in get_direct_connected_nodes(node)])
    actual_node_ids = set(actual_node_weighs.keys())

    nodes_to_delete = current_direct_connected_nodes_ids - actual_node_ids
    nodes_to_update = current_direct_connected_nodes_ids & actual_node_ids
    nodes_to_create = actual_node_ids - current_direct_connected_nodes_ids

    _delete_relations(node, nodes_to_delete)
    _update_relations(node, nodes_to_update, actual_node_weighs)
    _create_relations(node, nodes_to_create, actual_node_weighs)


def _delete_relations(node, nodes_to_delete):
    for node_to_delete in nodes_to_delete:
        old_node = models.Unit.objects.get(id=node_to_delete)
        models.Relationship.objects.get(Q(start=node, end=old_node) | Q(start=old_node, end=node)).delete()


def _update_relations(node, nodes_to_update, actual_node_weighs):

    for node_to_update in nodes_to_update:
        related_node = models.Unit.objects.get(id=node_to_update)
        relation = models.Relationship.objects.get(Q(start=node, end=related_node) |
                                        Q(start=related_node, end=node))
        relation.value = actual_node_weighs[node_to_update]
        relation.save()


def _create_relations(node, nodes_to_create, actual_node_weighs):
    for node_to_create in nodes_to_create:
        related_node = models.Unit.objects.get(id=node_to_create)
        models.Relationship.objects.create(start=node,
                                           end=related_node,
                                           value=actual_node_weighs[node_to_create])

def relation_between_nodes(node1, node2):
    try:
        return models.Relationship.objects.get(
            (Q(start=node1) & Q(end=node2)) | (Q(start=node2) & Q(end=node1)))
    except models.Relationship.DoesNotExist:
        pass


def find_weight_direct_relations(current_node, direct_related_nodes):
    related_nodes = {}
    for direct_related_node in direct_related_nodes:
        relation = models.Relationship.objects.filter(
            Q(start=direct_related_node, end=current_node) |
            Q(start=current_node, end=direct_related_node)
        )
        related_nodes[direct_related_node] = relation[0].value

    return related_nodes









