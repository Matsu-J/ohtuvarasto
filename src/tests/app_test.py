import unittest
from app import app, manager


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        manager._warehouses.clear()
        manager._next_id = 1
        manager._next_item_id = 1

    def test_index_empty(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No warehouses yet', response.data)

    def test_add_warehouse_get(self):
        response = self.client.get('/warehouse/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add New Warehouse', response.data)

    def test_add_warehouse_post(self):
        data = {
            'name': 'Test Warehouse',
            'capacity': '100',
            'initial_balance': '50'
        }
        response = self.client.post('/warehouse/add', data=data)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertIn(b'Test Warehouse', response.data)

    def test_view_warehouse(self):
        manager.add_warehouse('Test', 100, 50)
        response = self.client.get('/warehouse/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test', response.data)

    def test_view_nonexistent_warehouse(self):
        response = self.client.get('/warehouse/999')
        self.assertEqual(response.status_code, 302)

    def test_edit_warehouse_get(self):
        manager.add_warehouse('Test', 100, 50)
        response = self.client.get('/warehouse/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Warehouse', response.data)

    def test_edit_warehouse_post(self):
        manager.add_warehouse('Test', 100, 50)
        response = self.client.post('/warehouse/1/edit', data={'name': 'New'})
        self.assertEqual(response.status_code, 302)
        warehouse = manager.get_warehouse(1)
        self.assertEqual(warehouse['name'], 'New')

    def test_delete_warehouse(self):
        manager.add_warehouse('Test', 100, 50)
        response = self.client.post('/warehouse/1/delete')
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(manager.get_warehouse(1))

    def test_add_items(self):
        manager.add_warehouse('Test', 100, 0)
        response = self.client.post(
            '/warehouse/1/add-items',
            data={'amount': '25'}
        )
        self.assertEqual(response.status_code, 302)
        warehouse = manager.get_warehouse(1)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 25)

    def test_take_items(self):
        manager.add_warehouse('Test', 100, 50)
        response = self.client.post(
            '/warehouse/1/take-items',
            data={'amount': '25'}
        )
        self.assertEqual(response.status_code, 302)
        warehouse = manager.get_warehouse(1)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 25)

    def test_edit_warehouse_capacity(self):
        manager.add_warehouse('Test', 100, 50)
        response = self.client.post(
            '/warehouse/1/edit',
            data={'name': 'Test', 'capacity': '200'}
        )
        self.assertEqual(response.status_code, 302)
        warehouse = manager.get_warehouse(1)
        self.assertAlmostEqual(warehouse['varasto'].tilavuus, 200)

    def test_add_named_item(self):
        manager.add_warehouse('Test', 100, 0)
        response = self.client.post(
            '/warehouse/1/items/add',
            data={'item_name': 'Apples', 'item_amount': '10'}
        )
        self.assertEqual(response.status_code, 302)
        warehouse = manager.get_warehouse(1)
        self.assertEqual(len(warehouse['stored_items']), 1)

    def test_edit_named_item(self):
        manager.add_warehouse('Test', 100, 0)
        manager.add_item(1, 'Apples', 10)
        response = self.client.post(
            '/warehouse/1/items/1/edit',
            data={'item_name': 'Oranges', 'item_amount': '20'}
        )
        self.assertEqual(response.status_code, 302)
        item = manager.get_item(1, 1)
        self.assertEqual(item['name'], 'Oranges')
        self.assertAlmostEqual(item['amount'], 20)

    def test_delete_named_item(self):
        manager.add_warehouse('Test', 100, 0)
        manager.add_item(1, 'Apples', 10)
        response = self.client.post('/warehouse/1/items/1/delete')
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(manager.get_item(1, 1))
