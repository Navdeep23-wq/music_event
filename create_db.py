# create_db.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    contact_number = db.Column(db.String(20))
    street_address = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    events_created = db.relationship('Event', backref='creator', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    
    def __repr__(self):
        return f'<User {self.first_name} {self.surname}>'

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False)  # Open, Inactive, Sold Out, Cancelled
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    bookings = db.relationship('Booking', backref='event', lazy=True)
    comments = db.relationship('Comment', backref='event', lazy=True)
    
    def __repr__(self):
        return f'<Event {self.title}>'

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<Booking {self.id} for Event {self.event_id}>'

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comment {self.id} by User {self.user_id}>'

def create_test_data():
    # Create test users
    admin = User(
        first_name='Admin',
        surname='User',
        email='admin@example.com',
        password=generate_password_hash('admin123', method='pbkdf2:sha256'),
        contact_number='0412345678',
        street_address='123 Admin St, Brisbane',
        is_admin=True
    )
    
    user1 = User(
        first_name='John',
        surname='Doe',
        email='john@example.com',
        password=generate_password_hash('password123', method='pbkdf2:sha256'),
        contact_number='0423456789',
        street_address='456 User Ave, Brisbane'
    )
    
    user2 = User(
        first_name='Jane',
        surname='Smith',
        email='jane@example.com',
        password=generate_password_hash('password123', method='pbkdf2:sha256'),
        contact_number='0434567890',
        street_address='789 Customer Rd, Brisbane'
    )
    
    db.session.add_all([admin, user1, user2])
    db.session.commit()
    
    # Create test events
    event1 = Event(
        title='Tech Conference 2025',
        description='Annual technology conference featuring the latest innovations',
        date=datetime(2025, 7, 15, 9, 0),
        location='Brisbane Convention Centre',
        image='tech_conference.jpg',
        status='Open',
        capacity=200,
        price=150.00,
        creator_id=admin.id
    )
    
    event2 = Event(
        title='Music Festival',
        description='Weekend music festival with multiple stages',
        date=datetime(2025, 8, 20, 12, 0),
        location='Riverstage, Brisbane',
        image='music_festival.jpg',
        status='Open',
        capacity=5000,
        price=99.50,
        creator_id=user1.id
    )
    
    event3 = Event(
        title='Art Exhibition',
        description='Local artists showcase their work',
        date=datetime(2025, 6, 10, 10, 0),
        location='Queensland Art Gallery',
        image='art_exhibition.jpg',
        status='Inactive',
        capacity=100,
        price=25.00,
        creator_id=user2.id
    )
    
    db.session.add_all([event1, event2, event3])
    db.session.commit()
    
    # Create test bookings
    booking1 = Booking(
        user_id=user1.id,
        event_id=event1.id,
        quantity=2,
        booking_date=datetime(2025, 5, 1, 14, 30),
        total_price=300.00
    )
    
    booking2 = Booking(
        user_id=user2.id,
        event_id=event2.id,
        quantity=4,
        booking_date=datetime(2025, 5, 15, 10, 15),
        total_price=398.00
    )
    
    db.session.add_all([booking1, booking2])
    db.session.commit()
    
    # Create test comments
    comment1 = Comment(
        user_id=user1.id,
        event_id=event1.id,
        text='Looking forward to this event!',
        created_at=datetime(2025, 5, 2, 9, 0)
    )
    
    comment2 = Comment(
        user_id=user2.id,
        event_id=event2.id,
        text='The lineup looks amazing!',
        created_at=datetime(2025, 5, 16, 11, 30)
    )
    
    db.session.add_all([comment1, comment2])
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Create test data if the database is empty
        if not User.query.first():
            create_test_data()
            print("Database created successfully with test data!")
        else:
            print("Database already exists. No test data was added.")