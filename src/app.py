from flask import Flask, render_template, request, redirect, url_for
from warehouse_manager import WarehouseManager


app = Flask(__name__)
manager = WarehouseManager()


@app.route('/')
def index():
    """Display all warehouses."""
    warehouses = manager.get_all_warehouses()
    return render_template('index.html', warehouses=warehouses)


@app.route('/warehouse/add', methods=['GET', 'POST'])
def add_warehouse():
    """Add a new warehouse."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        capacity = float(request.form.get('capacity', 0))
        initial_balance = float(request.form.get('initial_balance', 0))
        if name and capacity > 0:
            manager.add_warehouse(name, capacity, initial_balance)
        return redirect(url_for('index'))
    return render_template('add_warehouse.html')


@app.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    """View a specific warehouse."""
    warehouse = manager.get_warehouse(warehouse_id)
    if not warehouse:
        return redirect(url_for('index'))
    return render_template('view_warehouse.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    """Edit a warehouse."""
    warehouse = manager.get_warehouse(warehouse_id)
    if not warehouse:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            manager.update_warehouse(warehouse_id, name)
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

    return render_template('edit_warehouse.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    manager.delete_warehouse(warehouse_id)
    return redirect(url_for('index'))


@app.route('/warehouse/<int:warehouse_id>/add-items', methods=['POST'])
def add_items(warehouse_id):
    """Add items to a warehouse."""
    amount = float(request.form.get('amount', 0))
    if amount > 0:
        manager.add_to_warehouse(warehouse_id, amount)
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/take-items', methods=['POST'])
def take_items(warehouse_id):
    """Take items from a warehouse."""
    amount = float(request.form.get('amount', 0))
    if amount > 0:
        manager.take_from_warehouse(warehouse_id, amount)
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


if __name__ == '__main__':
    app.run(debug=True)
