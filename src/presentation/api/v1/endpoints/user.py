from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.domain.entities.models.user import User
from src.schemas.user_schemas import UserResponse, UserUpdate
from src.infrastructure.database.db import get_db
from src.infrastructure.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)  # This checks the token
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user) 
): # This checks the token:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields
    db_user.username = user.username
    db_user.email = user.email
    db_user.dob = user.dob
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):  # This checks the token:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}

@router.get("/",response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
