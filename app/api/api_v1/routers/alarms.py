"""Endpoints for resources associated to alarms"""
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Response
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.config import Tags
# Schemas
from app.schemas import alarms as alarm_schemas
# Models
from app.models import alarms as alarm_models
from app.models import users as user_models
# Crud
from app.core.controller.alarms import CrudAlarm
from app.core.controller.alarms import CheckAlarms
# Dependency injections
from app.core.controller.users import get_current_active_user

router = APIRouter(
    prefix="/alarms",
    tags=[Tags.ALARMS],
)


@router.get("/", response_model=list[alarm_schemas.AlarmDBSchema], status_code=status.HTTP_200_OK)
def get_alarms(
    current_user: user_models.UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crud = CrudAlarm(db=db)
    # current_user returns a user model which we can use to retreive user_id.
    return crud.get(user_id=current_user.id)


@router.post("/", response_model=alarm_schemas.AlarmDBSchema, status_code=status.HTTP_201_CREATED)
def create_alarm(
    alarm: alarm_schemas.AlarmCreateSchema,
    current_user: user_models.UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Validate alarm doesn't currently exist
    check = CheckAlarms(db=db)
    check.exists(
        user_id=current_user.id,
        schema=alarm,
    )
    # If not exists, go ahead and create
    crud = CrudAlarm(db=db)
    
    return crud.create(user_id=current_user.id,schema=alarm)


@router.delete("/{alarm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alarm(
    alarm_id: int,
    current_user: user_models.UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check alarm exists
    check = CheckAlarms(db=db)
    check.not_exists_with_id(
        alarm_id=alarm_id,
        user_id=current_user.id,
        )
    # Delete Alarm
    crud = CrudAlarm(db=db)
    crud.delete(
        alarm_id=alarm_id
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{alarm_id}", status_code=status.HTTP_200_OK, response_model=alarm_schemas.AlarmDBSchema)
def update_alarm(
    alarm_id: int,
    alarm: alarm_schemas.AlarmUpdateSchema, 
    current_user: user_models.UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
    ):

    # Check the alarm exists
    check = CheckAlarms(db=db)
    check.not_exists(
        user_id=current_user.id,
        schema=alarm
    )

    # Update alarm
    crud = CrudAlarm(db=db)
    model: alarm_models.AlarmModel = crud.update(
        alarm_id=alarm_id,
        schema=alarm,
    )

    return model 