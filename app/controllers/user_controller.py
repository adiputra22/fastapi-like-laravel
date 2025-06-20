from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.services.user_service import UserService
from app.requests.user_request import UserCreateRequest, UserUpdateRequest, UserResponse

class UserController:
    
    @staticmethod
    def index(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[UserResponse]:
        """Get all users (seperti UserController@index)"""
        service = UserService(db)
        users = service.get_all_users(skip=skip, limit=limit)
        return [UserResponse.model_validate(user) for user in users]
    
    @staticmethod
    def show(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
        """Get user by ID (seperti UserController@show)"""
        service = UserService(db)
        user = service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)
    
    @staticmethod
    def store(user_data: UserCreateRequest, db: Session = Depends(get_db)) -> UserResponse:
        """Create new user (seperti UserController@store)"""
        service = UserService(db)
        
        # Check if email already exists
        if service.get_user_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        user = service.create_user(user_data)
        return UserResponse.model_validate(user)
    
    @staticmethod
    def update(user_id: int, user_data: UserUpdateRequest, db: Session = Depends(get_db)) -> UserResponse:
        """Update user (seperti UserController@update)"""
        service = UserService(db)
        user = service.update_user(user_id, user_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)
    
    @staticmethod
    def destroy(user_id: int, db: Session = Depends(get_db)):
        """Delete user (seperti UserController@destroy)"""
        service = UserService(db)
        if not service.delete_user(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}