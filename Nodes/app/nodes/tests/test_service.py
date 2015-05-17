from django.test import TestCase

from Nodes.app.nodes import models, service


class TestGetNodeRelations(TestCase):
    def test_1_relation(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')

        models.Relationship.objects.create(start=node1, end=node2, value=1)

        result = list(service.get_node_relations(node1))

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].node, node2)
        self.assertEqual(result[0].through_nodes, {node1})

    def test_2_relations(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')

        models.Relationship.objects.create(start=node1, end=node2, value=1)
        models.Relationship.objects.create(start=node3, end=node2, value=1)

        import ipdb; ipdb.set_trace()
        result = list(service.get_node_relations(node1))

        self.assertEqual(len(result), 2)

        for node_relation in result:
            if node_relation.node == node2:
                self.assertEqual(node_relation.through_nodes, {node1, node2})
            elif node_relation.node == node3:
                self.assertEqual(node_relation.through_nodes, {node2})
            else:
                raise Exception("Unexpected node: %s" % node_relation.node)

    def _test_test(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        # node3 = models.Unit.objects.create(name='C')
        # node4 = models.Unit.objects.create(name='D')

        models.Relationship.objects.create(start=node1, end=node2, value=1)
        # models.Relationship.objects.create(start=node3, end=node2, value=1)
        # models.Relationship.objects.create(start=node4, end=node3, value=1)

        result = service.get_node_relations(node1)

        self.fail(result)


class TestGetNodeRelationsOld(TestCase):
    def test_test(self):
        node1 = models.Unit.objects.create(name='A')
        node2 = models.Unit.objects.create(name='B')
        node3 = models.Unit.objects.create(name='C')
        node4 = models.Unit.objects.create(name='D')

        models.Relationship.objects.create(start=node1, end=node2, value=1)
        models.Relationship.objects.create(start=node3, end=node2, value=1)
        models.Relationship.objects.create(start=node4, end=node3, value=1)

        result = service.get_node_relations_old(node1)

        self.assertEqual(result, {node2, node3, node4})
