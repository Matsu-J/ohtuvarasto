from varasto import Varasto


class WarehouseManager:
    """Manages multiple warehouses with names."""

    def __init__(self):
        self._warehouses = {}
        self._next_id = 1

    def add_warehouse(self, name, capacity, initial_balance=0):
        """Add a new warehouse and return its id."""
        warehouse_id = self._next_id
        self._warehouses[warehouse_id] = {
            'id': warehouse_id,
            'name': name,
            'varasto': Varasto(capacity, initial_balance)
        }
        self._next_id += 1
        return warehouse_id

    def get_warehouse(self, warehouse_id):
        """Get a warehouse by its id."""
        return self._warehouses.get(warehouse_id)

    def get_all_warehouses(self):
        """Get all warehouses."""
        return list(self._warehouses.values())

    def update_warehouse(self, warehouse_id, name):
        """Update a warehouse's name."""
        if warehouse_id in self._warehouses:
            self._warehouses[warehouse_id]['name'] = name
            return True
        return False

    def delete_warehouse(self, warehouse_id):
        """Delete a warehouse by its id."""
        if warehouse_id in self._warehouses:
            del self._warehouses[warehouse_id]
            return True
        return False

    def add_to_warehouse(self, warehouse_id, amount):
        """Add items to a warehouse."""
        warehouse = self.get_warehouse(warehouse_id)
        if warehouse:
            warehouse['varasto'].lisaa_varastoon(amount)
            return True
        return False

    def take_from_warehouse(self, warehouse_id, amount):
        """Take items from a warehouse."""
        warehouse = self.get_warehouse(warehouse_id)
        if warehouse:
            return warehouse['varasto'].ota_varastosta(amount)
        return 0.0
