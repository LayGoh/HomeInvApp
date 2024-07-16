from flask import render_template, flash, redirect, url_for, request, send_file, make_response
from app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import ItemForm, SearchForm
from app.models import Item, User
from .decorators import admin_required
import csv
from io import StringIO
from datetime import datetime

# Admin route
@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)

# Toggle admin status route
@app.route('/toggle_admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    primary_admin = User.query.filter_by(username='admin').first()
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash('User admin status updated successfully!', 'success')
    return redirect(url_for('admin'))

# Home
@app.route('/')
def home():
    return render_template('home.html')

# Get distinct locations
def get_distinct_locations():
    locations = Item.query.with_entities(Item.location).distinct().all()
    return [loc[0] for loc in locations]

# Add item
@app.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_item():
    form = ItemForm()
    locations = get_distinct_locations()
    if form.validate_on_submit():
        item = Item(
            name=form.name.data,
            description=form.description.data,
            location=form.location.data,
            notes=form.notes.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Item added successfully!', 'success')
        return redirect(url_for('add_item'))
    return render_template('add_item.html', form=form, locations=locations)

# Edit item
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = ItemForm(obj=item)
    locations = get_distinct_locations()
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.location = form.location.data
        item.notes = form.notes.data
        db.session.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('view_items'))
    return render_template('edit_item.html', form=form, locations=locations)

# View items
@app.route('/items', methods=['GET', 'POST'])
@login_required
def view_items():
    form = SearchForm()
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'name')
    sort_order = request.args.get('sort_order', 'asc')
    if form.validate_on_submit():
        search_query = form.search.data
    items_query = Item.query.filter(
        (Item.name.contains(search_query)) | (Item.location.contains(search_query)) | (Item.description.contains(search_query))
    )
    if sort_order == 'asc':
        items_query = items_query.order_by(getattr(Item, sort_by).asc())
    else:
        items_query = items_query.order_by(getattr(Item, sort_by).desc())
    items = items_query.all()
    return render_template('view_items.html', items=items, form=form, sort_by=sort_by, sort_order=sort_order)

# Delete item
@app.route('/delete/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('view_items'))

# Export items
@app.route('/export', methods=['GET'])
@login_required
@admin_required
def export_items():
    items = Item.query.all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Name', 'Description', 'Location', 'Notes'])
    for item in items:
        cw.writerow([item.id, item.name, item.description, item.location, item.notes])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"inventory_{timestamp}.csv"
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename={filename}"
    output.headers["Content-type"] = "text/csv"
    return output

# Delete user account
@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.username == 'admin':
        flash('Primary admin cannot be deleted!', 'danger')
        return redirect(url_for('admin'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin'))
