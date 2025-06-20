from sqlalchemy.orm import Session
from app.models.user import User
from app.requests.user_request import UserCreateRequest, UserUpdateRequest
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_data: UserCreateRequest):
        # Hash password (seperti Hash::make di Laravel)
        hashed_password = pwd_context.hash(user_data.password)
        
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user(self, user_id: int, user_data: UserUpdateRequest):
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None
        
        # Update hanya field yang diberikan
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False