import unittest
from warehouse_manager import WarehouseManager


class TestWarehouseManager(unittest.TestCase):
    def setUp(self):
        self.manager = WarehouseManager()

    def test_add_warehouse(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 50)
        self.assertEqual(warehouse_id, 1)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertIsNotNone(warehouse)
        self.assertEqual(warehouse['name'], 'Test')
        self.assertAlmostEqual(warehouse['varasto'].tilavuus, 100)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 50)

    def test_get_all_warehouses(self):
        self.manager.add_warehouse('Test1', 100, 50)
        self.manager.add_warehouse('Test2', 200, 100)
        warehouses = self.manager.get_all_warehouses()
        self.assertEqual(len(warehouses), 2)

    def test_update_warehouse(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 50)
        result = self.manager.update_warehouse(warehouse_id, 'Updated')
        self.assertTrue(result)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertEqual(warehouse['name'], 'Updated')

    def test_update_nonexistent_warehouse(self):
        result = self.manager.update_warehouse(999, 'Test')
        self.assertFalse(result)

    def test_delete_warehouse(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 50)
        result = self.manager.delete_warehouse(warehouse_id)
        self.assertTrue(result)
        self.assertIsNone(self.manager.get_warehouse(warehouse_id))

    def test_delete_nonexistent_warehouse(self):
        result = self.manager.delete_warehouse(999)
        self.assertFalse(result)

    def test_add_to_warehouse(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 0)
        result = self.manager.add_to_warehouse(warehouse_id, 50)
        self.assertTrue(result)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 50)

    def test_add_to_nonexistent_warehouse(self):
        result = self.manager.add_to_warehouse(999, 50)
        self.assertFalse(result)

    def test_take_from_warehouse(self):
        warehouse_id = self.manager.add_warehouse('Test', 100, 50)
        taken = self.manager.take_from_warehouse(warehouse_id, 25)
        self.assertAlmostEqual(taken, 25)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 25)

    def test_take_from_nonexistent_warehouse(self):
        taken = self.manager.take_from_warehouse(999, 25)
        self.assertAlmostEqual(taken, 0.0)
