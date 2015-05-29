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
        models.Relationship.objects.create(start=node2, end=node4, value=1)

        service.setup_actual_relations(node2, {node1.id: 5, node3.id: 3})

        self.assertEqual(len(models.Relationship.objects.all()), 2)

    def test_updating_actual_weight(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')
        node4 = models.Unit.objects.create(name='D')

        models.Relationship.objects.create(start=node1, end=node2, value=1)
        models.Relationship.objects.create(start=node2, end=node3, value=1)
        models.Relationship.objects.create(start=node2, end=node4, value=1)

        service.setup_actual_relations(node2, {node1.id: 2, node4.id: 3})

        self.assertEqual(models.Relationship.objects.get(end=node1.id).value, 2)
        self.assertEqual(models.Relationship.objects.get(end=node4.id).value, 3)

    def test_creating_new_relation(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')

        models.Relationship.objects.create(start=node1, end=node2, value=1)

        service.setup_actual_relations(node2.id, {node1.id: 2, node3.id:2})

        self.assertEqual(len(models.Relationship.objects.filter(start=node2, end=node3), 1))


class TestInnerFunction(TestCase):
    def test_delete_relations(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')

        models.Relationship.objects.create(start=node1, end=node2, value=1)
        models.Relationship.objects.create(start=node2, end=node3, value=1)

        service._delete_relations(node2, {node3.id})

        self.assertEqual(len(models.Relationship.objects.all()), 1)

    def test_updating_relations(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')

        models.Relationship.objects.create(start=node1, end=node2, value=1)
        models.Relationship.objects.create(start=node2, end=node3, value=1)

        service._update_relations(node2, {node3.id}, {node3.id: 7})

        self.assertEqual(models.Relationship.objects.all()[1].value, 7)

    def test_create_relations(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')

        models.Relationship.objects.create(start=node1, end=node2, value=1)

        service._create_relations(node2, {node3.id}, {node3.id: 3})

        self.assertEqual(len(models.Relationship.objects.all()), 2)


class TestSetup(TestCase):
    def test_deleting_relations(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')
        node4 = models.Unit.objects.create(name='D')

        models.Relationship.objects.create(start=node1, end=node2, value=1)
        models.Relationship.objects.create(start=node2, end=node3, value=1)
        models.Relationship.objects.create(start=node3, end=node4, value=1)

        service.setup_actual_relations(node2, {node3.id: 3})

    def test_creating_and_updating_new_relations(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')
        node4 = models.Unit.objects.create(name='D')

        models.Relationship.objects.create(start=node1, end=node2, value=1)

        service.setup_actual_relations(node2, {node3.id: 2, node4.id: 3})

        self.assertEqual(len(models.Relationship.objects.all()), 2)
        self.assertEqual(models.Relationship.objects.get(start=node2, end=node3).value, 2)
        self.assertEqual(models.Relationship.objects.get(start=node2, end=node4).value, 3)


class TestDirectRelations(TestCase):
    def test_direct_relations(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')
        node4 = models.Unit.objects.create(name='D')

        models.Relationship.objects.create(start=node1, end=node2, value=1)
        models.Relationship.objects.create(start=node2, end=node3, value=5)
        models.Relationship.objects.create(start=node3, end=node4, value=1)

        result = service.get_direct_relations(node2)

        self.assertEquals(result, {node1: models.Relationship.objects.get(start=node1,
                                                                          end=node2),
                                   node3: models.Relationship.objects.get(start=node2,
                                                                          end=node3)})







