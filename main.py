# ─────────────────────────────────────────────
#  SQLAlchemy + MySQL — Full CRUD Demo
#  pip install sqlalchemy pymysql
# ─────────────────────────────────────────────

# Column        → represents a column in the table
# Integer       → int data type for column
# String        → varchar data type for column
# Boolean       → true/false data type for column
from sqlalchemy import Column, Integer, String, Boolean

# create_engine  → creates the connection to your database
# text           → lets you run raw SQL if needed
from sqlalchemy import create_engine, text

# declarative_base → gives you the Base class to build models from
from sqlalchemy.orm import declarative_base

# sessionmaker   → factory that creates Session objects (your DB middleman)
# Session        → type hint for the session
from sqlalchemy.orm import sessionmaker, Session


# ─── 1. DATABASE CONNECTION ───────────────────
# Format: "mysql+pymysql://username:password@host:port/database_name"
# mysql+pymysql  → use MySQL with pymysql driver
# root           → your MySQL username
# ""             → your MySQL password (empty here, change if you have one)
# localhost      → your MySQL is running on your own machine
# 3306           → default MySQL port
# mydb           → the database name (create this first in MySQL)

DATABASE_URL = "mysql+pymysql://root:Prsn2018%40t@localhost:3306/mydb"

# create_engine sets up the connection pool to your database
# echo=True means every SQL query gets printed to terminal (great for learning)
engine = create_engine(DATABASE_URL, echo=True)


# ─── 2. BASE CLASS ────────────────────────────
# declarative_base() gives us a Base class
# All our models (tables) will inherit from this Base
# It keeps track of all models so it can create their tables
Base = declarative_base()


# ─── 3. MODEL = TABLE ─────────────────────────
# This class represents the "users" table in MySQL
# Every attribute with Column() = one column in the table
class User(Base):

    # __tablename__ tells SQLAlchemy what to name the table in MySQL
    __tablename__ = "users"

    # primary_key=True → this is the unique identifier for each row
    # autoincrement happens automatically for Integer primary keys
    id = Column(Integer, primary_key=True)

    # String(100) → VARCHAR(100) in MySQL
    # nullable=False → this field is required, cannot be empty
    name = Column(String(100), nullable=False)

    # unique=True → no two users can have the same email
    email = Column(String(100), unique=True, nullable=False)

    # Boolean column, default value is True (user is active when created)
    is_active = Column(Boolean, default=True)

    # __repr__ is what prints when you do print(user)
    # helpful for debugging
    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, is_active={self.is_active})"


# ─── 4. CREATE TABLES ─────────────────────────
# create_all looks at all models that inherit from Base
# and creates their tables in MySQL if they don't exist yet
# Safe to run multiple times — won't recreate if table already exists
Base.metadata.create_all(bind=engine)


# ─── 5. SESSION FACTORY ───────────────────────
# sessionmaker creates a Session class bound to our engine
# autocommit=False → we manually call db.commit() to save changes (safer)
# autoflush=False  → don't auto-send changes to DB before commit
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create one session instance — this is our database middleman
db: Session = SessionLocal()


# ══════════════════════════════════════════════
#  CREATE — Add rows to the table
# ══════════════════════════════════════════════
print("\n--- CREATE ---")

# Create a Python object — this is NOT in the DB yet
user1 = User(name="Rahul Sharma", email="rahul@example.com", is_active=True)
user2 = User(name="Priya Mehta",  email="priya@example.com", is_active=True)
user3 = User(name="Arjun Das",    email="arjun@example.com", is_active=False)

# db.add() stages the object — tells SQLAlchemy "I want to insert this"
db.add(user1)
db.add(user2)
db.add(user3)

# db.commit() actually sends the INSERT queries to MySQL and saves
# Nothing is saved until you commit
db.commit()

# db.refresh() reloads the object from DB so we get the auto-generated id
db.refresh(user1)
db.refresh(user2)
db.refresh(user3)

print(f"Created: {user1}")
print(f"Created: {user2}")
print(f"Created: {user3}")


# ══════════════════════════════════════════════
#  READ — Fetch rows from the table
# ══════════════════════════════════════════════
print("\n--- READ ALL ---")

# db.query(User)      → SELECT * FROM users
# .all()              → fetch every row as a list of User objects
all_users = db.query(User).all()

for user in all_users:
    print(user)


print("\n--- READ ONE BY ID ---")

# .filter()           → WHERE clause
# User.id == 1        → WHERE id = 1
# .first()            → fetch only the first match (returns None if not found)
one_user = db.query(User).filter(User.id == 1).first()
print(f"Found: {one_user}")


print("\n--- READ WITH CONDITION ---")

# Filter by is_active == True → only active users
active_users = db.query(User).filter(User.is_active == True).all()
print(f"Active users: {active_users}")


# ══════════════════════════════════════════════
#  UPDATE — Modify an existing row
# ══════════════════════════════════════════════
print("\n--- UPDATE ---")

# First fetch the object you want to update
user_to_update = db.query(User).filter(User.id == 1).first()

if user_to_update:
    # Simply change the attribute on the Python object
    user_to_update.name = "Rahul Kumar"
    user_to_update.email = "rahulkumar@example.com"

    # commit() sends the UPDATE query to MySQL
    db.commit()

    # refresh to get latest data from DB
    db.refresh(user_to_update)
    print(f"Updated: {user_to_update}")


# ══════════════════════════════════════════════
#  DELETE — Remove a row
# ══════════════════════════════════════════════
print("\n--- DELETE ---")

# Fetch the row you want to delete
user_to_delete = db.query(User).filter(User.id == 3).first()

if user_to_delete:
    # db.delete() marks it for deletion
    db.delete(user_to_delete)

    # commit() sends the DELETE query to MySQL
    db.commit()
    print(f"Deleted user with id 3")


print("\n--- FINAL STATE ---")

# Confirm final state of the table
remaining = db.query(User).all()
for user in remaining:
    print(user)


# ─── CLOSE SESSION ────────────────────────────
# Always close the session when done
# In FastAPI this is handled automatically via Depends(get_db)
db.close()
print("\nDone. Session closed.")