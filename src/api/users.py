from fastapi import APIRouter, Depends
from src.schemas.user import UserModel
from src.services.auth import get_current_user
from src.db.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserModel)
async def me(user: User = Depends(get_current_user)):
    return user
