from varasto import Varasto


class WarehouseManager:
    """Manages multiple warehouses with names."""

    def __init__(self):
        self._warehouses = {}
        self._next_id = 1
        self._next_item_id = 1

    def add_warehouse(self, name, capacity, initial_balance=0):
        """Add a new warehouse and return its id."""
        warehouse_id = self._next_id
        self._warehouses[warehouse_id] = {
            'id': warehouse_id,
            'name': name,
            'varasto': Varasto(capacity, initial_balance),
            'stored_items': {}
        }
        self._next_id += 1
        return warehouse_id

    def get_warehouse(self, warehouse_id):
        """Get a warehouse by its id."""
        return self._warehouses.get(warehouse_id)

    def get_all_warehouses(self):
        """Get all warehouses."""
        return list(self._warehouses.values())

    def update_warehouse(self, warehouse_id, name, capacity=None):
        """Update a warehouse's name and optionally capacity."""
        if warehouse_id in self._warehouses:
            self._warehouses[warehouse_id]['name'] = name
            if capacity is not None and capacity > 0:
                old_varasto = self._warehouses[warehouse_id]['varasto']
                new_saldo = min(old_varasto.saldo, capacity)
                self._warehouses[warehouse_id]['varasto'] = Varasto(
                    capacity, new_saldo
                )
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

    def add_item(self, warehouse_id, item_name, amount):
        """Add a named item to a warehouse."""
        warehouse = self.get_warehouse(warehouse_id)
        if warehouse and item_name and amount > 0:
            item_id = self._next_item_id
            warehouse['stored_items'][item_id] = {
                'id': item_id,
                'name': item_name,
                'amount': amount
            }
            self._next_item_id += 1
            return item_id
        return None

    def get_item(self, warehouse_id, item_id):
        """Get an item from a warehouse."""
        warehouse = self.get_warehouse(warehouse_id)
        if warehouse:
            return warehouse['stored_items'].get(item_id)
        return None

    def update_item(self, warehouse_id, item_id, name=None, amount=None):
        """Update an item's name and/or amount."""
        warehouse = self.get_warehouse(warehouse_id)
        if warehouse and item_id in warehouse['stored_items']:
            if name is not None:
                warehouse['stored_items'][item_id]['name'] = name
            if amount is not None and amount >= 0:
                warehouse['stored_items'][item_id]['amount'] = amount
            return True
        return False

    def delete_item(self, warehouse_id, item_id):
        """Delete an item from a warehouse."""
        warehouse = self.get_warehouse(warehouse_id)
        if warehouse and item_id in warehouse['stored_items']:
            del warehouse['stored_items'][item_id]
            return True
        return False
