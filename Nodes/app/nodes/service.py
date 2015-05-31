from django.db.models import Q

from Nodes.app.nodes import models


class NodeRelation(object):
    def __init__(self, node, weight):
        self.node = node
        self.path_nodes = []
        self.weight = weight

    def __hash__(self):
        return hash(self.node)

    def __eq__(self, other):
        if isinstance(other, NodeRelation):
            other == other.node
        return self.node == other

    def add_path_node(self, node, weight):
        self.path_nodes.append(node)
        self.weight = self.weight + weight


def get_node_relations(start_node):
    result_relations = set()

    def _walk_node_relations(node):
        node_relations = []

        for related_node, relation in get_direct_relations(node).items():
            if related_node in result_relations or related_node == start_node:
                continue

            node_relation = NodeRelation(related_node, relation.value)
            result_relations.add(node_relation)
            node_relations.append(node_relation)

            for _relation in _walk_node_relations(related_node):
                _relation.add_path_node(related_node, relation.value)
                node_relations.append(_relation)

        return node_relations

    _walk_node_relations(start_node)

    nodes_path_info = {}
    for result_relation in result_relations:
        result_relation.path_nodes.reverse()
        nodes_path_info[result_relation.node] = (result_relation.path_nodes, result_relation.weight)

    return nodes_path_info


def get_connected_nodes(start_node, result_nodes=None):
    # TODO: remove this function
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


def setup_actual_relations(node, actual_node_weighs):
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
        # TODO: use objects.update
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


def find_weight_direct_relations(node):
    # TODO: Remove this function
    related_nodes = get_direct_connected_nodes(node)
    weight = {}
    for related_node in related_nodes:
        weight[related_node] = models.Relationship.objects.get(Q(start=node, end=related_node) |
                                        Q(start=related_node, end=node)).value

    return weight


def get_direct_relations(node):
    relations = models.Relationship.objects.filter(Q(start=node) | Q(end=node))

    node_relations = {}
    for relation in relations:
        connected_node = relation.end if relation.start == node else relation.start
        node_relations[connected_node] = relation

    return node_relations


def get_direct_connected_nodes(start_node):
    return get_direct_relations(start_node).keys()
