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


class TestSetupActualRelations(TestCase):

    def test_deleting_not_actual_relations(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')
        node4 = models.Unit.objects.create(name='D')

        models.Relationship.objects.create(start=node1, end=node2, value=2)
        models.Relationship.objects.create(start=node2, end=node3, value=12)
        models.Relationship.objects.create(start=node3, end=node4, value=77)

        service.setup_actual_relations_old(node2, {node1.id: 5})

        self.assertEqual(len(models.Relationship.objects.all()), 1)
        #self.assertEqual(models.Relationship.objects.get(start=node1, end=node2).value, 5)



class TestRelations(TestCase):

    def test_return_weight_of_relation(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')


        models.Relationship.objects.create(start=node1, end=node2, value=11)
        models.Relationship.objects.create(start=node2, end=node3, value=14)

        weight = service.find_weight_direct_relations(node2, [node1, node3])

        self.assertEqual(weight, {node1: 11, node3:14})

