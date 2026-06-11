from app.core.database import SessionLocal
from app.models.models import User
from app.core.security import get_password_hash

db = SessionLocal()
try:
    new_user = User(
        full_name="Demo Student",
        email="demo@user.com",
        password_hash=get_password_hash("password")
    )
    db.add(new_user)
    db.commit()
    print("User 'demo@user.com' created successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()