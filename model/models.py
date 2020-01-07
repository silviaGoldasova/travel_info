from flask_sqlalchemy import SQLAlchemy

# Configure and initialize SQLAlchemy under this Flask webapp.
db = SQLAlchemy()

class Category(db.Model):
    def __init__(self, name):
        self.name = name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)


class Page(db.Model):
    def __init__(self, title, category):
        self.title = title
        self.category = category

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    category = db.Column(db.String(50), default='Other')

    """
    def __repr__(self): - for describing
        return 'Cafe(%d, %s, %s, %5.2f)' % (self.id, self.category, self.name, self.price)
            
    category = Column(Enum('tea', 'coffee', name='cat_enum'), default='coffee')
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    price = Column(Numeric(precision=5, scale=2))
    supplier = relationship('Supplier', backref='cafe_items', order_by=id)"""

class Section:
    def __init__(self, name, text):
        self.name = name
        self.text = text

class Section_form_obj():
    def __init__(self, name, text, id):
        self.name = name
        self.text = text
        self.id = id

class Place_obj():
    def __init__(self, title):
        self.title = title

def load_db(db):
    """Create database tables and insert records"""
    # Drop and re-create all the tables.
    db.drop_all()
    db.create_all()

    # Insert rows using add_all(list_of_instances).
    # Use the default constructor with keyword arguments.
    db.session.add_all([Category(name='Italy'), Category(name='France'), Category(name='Bratislava'), Category(name='Other')])    #list
    db.session.add_all([Page(title='Eifell Tower', category='France'), Page(title='BA Castle', category='Bratislava'), Page(title='Seina', category='France'), Page(title='Louvre', category='France'), Page(title='Devin Castle', category='Bratislava')])
    """Cafe(name='Cappuccino', price=3.29),
           Cafe(name='Green Tea', category='tea', price=2.99)])"""
    db.session.commit()  # Always commit after insert


