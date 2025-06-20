from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.controllers.user_controller import UserController
from app.requests.user_request import UserCreateRequest, UserUpdateRequest, UserResponse
from app.config.database import get_db

router = APIRouter(prefix="/api", tags=["API"])

# User routes (seperti Route::resource di Laravel)
router.add_api_route(
    "/users",
    UserController.index,
    methods=["GET"],
    response_model=List[UserResponse]
)

router.add_api_route(
    "/users/{user_id}",
    UserController.show,
    methods=["GET"],
    response_model=UserResponse
)

router.add_api_route(
    "/users",
    UserController.store,
    methods=["POST"],
    response_model=UserResponse
)

router.add_api_route(
    "/users/{user_id}",
    UserController.update,
    methods=["PUT"],
    response_model=UserResponse
)

router.add_api_route(
    "/users/{user_id}",
    UserController.destroy,
    methods=["DELETE"]
)