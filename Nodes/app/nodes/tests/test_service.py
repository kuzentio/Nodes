from django.test import TestCase

from Nodes.app.nodes import models, service


class TestGetDirectConnectedNodes(TestCase):

    def test_return_1_node(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')

        models.Relationship.objects.create(start=node1, end=node2, value=11)
        models.Relationship.objects.create(start=node2, end=node3, value=12)

        result = service.get_direct_connected_nodes(node3)

        self.assertEqual(result, [node2])

    def test_return_2_nodes(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')

        models.Relationship.objects.create(start=node1, end=node2, value=11)
        models.Relationship.objects.create(start=node2, end=node3, value=12)

        result = service.get_direct_connected_nodes(node2)

        self.assertEqual(result, [node1, node3])


class TestCleanNotActualNodes(TestCase):

    def test_create_actual_relation(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')

        service.setup_actual_relations(node2, [node1.id, node3.id])

        self.assertEqual(len(models.Relationship.objects.all()), 2)

    def test_returning_different_elements(self):
        actual = [1, 2, 3]
        current = [3, 4, 5]

        res = service.find_different_elements(actual, current)

        self.assertEqual(res, [1, 2])

    def test_return_relation_between_nodes(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')

        models.Relationship.objects.create(start=node2, end=node1, value=11)

        result = service.relation_between_nodes(node1, node2)

        self.assertEqual(result, models.Relationship.objects.get(start=node2, end=node1))

    def test_deleting_not_actual_relations(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')

        models.Relationship.objects.create(start=node1, end=node2, value=11)
        models.Relationship.objects.create(start=node2, end=node3, value=14)

        service.setup_actual_relations(node2, [node3.id])

        self.assertEqual(len(models.Relationship.objects.all()), 1)

    def test_node_relations(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')
        node4 = models.Unit.objects.create(name='D')
        node5 = models.Unit.objects.create(name='E')

        models.Relationship.objects.create(start=node1, end=node2, value=11)
        models.Relationship.objects.create(start=node2, end=node3, value=14)
        models.Relationship.objects.create(start=node3, end=node4, value=14)

 #       result = service.get_node_relations(node1)

#        self.assertEqual(result, [])


class TestRelations(TestCase):

    def test_return_weight_of_relation(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')


        models.Relationship.objects.create(start=node1, end=node2, value=11)
        models.Relationship.objects.create(start=node2, end=node3, value=14)

        weight = service.find_weight_direct_relations(node2, [node1, node3])

        self.assertEqual(weight, {node1: 11, node3:14})

