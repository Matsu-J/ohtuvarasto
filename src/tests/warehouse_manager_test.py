import unittest
from warehouse_manager import WarehouseManager


class TestWarehouseManager(unittest.TestCase):
    def setUp(self):
        self.manager = WarehouseManager()

    def test_add_warehouse(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        self.assertEqual(warehouse_id, 1)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertIsNotNone(warehouse)
        self.assertEqual(warehouse['name'], 'Test')
        self.assertAlmostEqual(warehouse['varasto'].tilavuus, 100)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 0)

    def test_get_all_warehouses(self):
        self.manager.add_warehouse('Test1', 100, 0)
        self.manager.add_warehouse('Test2', 200, 0)
        warehouses = self.manager.get_all_warehouses()
        self.assertEqual(len(warehouses), 2)

    def test_update_warehouse(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        result = self.manager.update_warehouse(warehouse_id, 'Updated')
        self.assertTrue(result)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertEqual(warehouse['name'], 'Updated')

    def test_update_nonexistent_warehouse(self):
        result = self.manager.update_warehouse(999, 'Test')
        self.assertFalse(result)

    def test_delete_warehouse(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        result = self.manager.delete_warehouse(warehouse_id)
        self.assertTrue(result)
        self.assertIsNone(self.manager.get_warehouse(warehouse_id))

    def test_delete_nonexistent_warehouse(self):
        result = self.manager.delete_warehouse(999)
        self.assertFalse(result)

    def test_update_warehouse_capacity(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        self.manager.add_item(warehouse_id, 'Apples', 50)
        result = self.manager.update_warehouse(warehouse_id, 'Test', 200)
        self.assertTrue(result)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse['varasto'].tilavuus, 200)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 50)

    def test_update_warehouse_capacity_adjusts_saldo(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        self.manager.add_item(warehouse_id, 'Apples', 80)
        result = self.manager.update_warehouse(warehouse_id, 'Test', 50)
        self.assertTrue(result)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse['varasto'].tilavuus, 50)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 50)

    def test_add_item(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        item_id = self.manager.add_item(warehouse_id, 'Apples', 10)
        self.assertIsNotNone(item_id)
        item = self.manager.get_item(warehouse_id, item_id)
        self.assertEqual(item['name'], 'Apples')
        self.assertAlmostEqual(item['amount'], 10)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 10)

    def test_add_item_reduces_capacity(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        self.manager.add_item(warehouse_id, 'Apples', 30)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse['varasto'].paljonko_mahtuu(), 70)

    def test_add_item_exceeds_capacity(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        result = self.manager.add_item(warehouse_id, 'Apples', 150)
        self.assertIsNone(result)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 0)

    def test_add_item_to_nonexistent_warehouse(self):
        result = self.manager.add_item(999, 'Apples', 10)
        self.assertIsNone(result)

    def test_update_item(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        item_id = self.manager.add_item(warehouse_id, 'Apples', 10)
        result = self.manager.update_item(warehouse_id, item_id, 'Oranges', 20)
        self.assertTrue(result)
        item = self.manager.get_item(warehouse_id, item_id)
        self.assertEqual(item['name'], 'Oranges')
        self.assertAlmostEqual(item['amount'], 20)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 20)

    def test_update_item_decrease_amount(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        item_id = self.manager.add_item(warehouse_id, 'Apples', 50)
        self.manager.update_item(warehouse_id, item_id, None, 20)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 20)
        self.assertAlmostEqual(warehouse['varasto'].paljonko_mahtuu(), 80)

    def test_update_nonexistent_item(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        result = self.manager.update_item(warehouse_id, 999, 'Apples', 10)
        self.assertFalse(result)

    def test_delete_item(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        item_id = self.manager.add_item(warehouse_id, 'Apples', 10)
        result = self.manager.delete_item(warehouse_id, item_id)
        self.assertTrue(result)
        self.assertIsNone(self.manager.get_item(warehouse_id, item_id))

    def test_delete_item_returns_capacity(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        item_id = self.manager.add_item(warehouse_id, 'Apples', 30)
        self.manager.delete_item(warehouse_id, item_id)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 0)
        self.assertAlmostEqual(warehouse['varasto'].paljonko_mahtuu(), 100)

    def test_delete_nonexistent_item(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        result = self.manager.delete_item(warehouse_id, 999)
        self.assertFalse(result)
