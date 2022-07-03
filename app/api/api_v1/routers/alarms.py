"""Endpoints for resources associated to alarms"""
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Response
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.config import Tags
# Schemas
from app.schemas import alarms as schemas
# Models
from app.models import alarms as models
# Crud
from app.core import crud
# Checks
from app.core import checks

router = APIRouter(
    prefix="/alarms",
    tags=[Tags.ALARMS],
)


@router.get("/", response_model=list[schemas.Alarm], status_code=status.HTTP_200_OK)
def get_alarms(db: Session = Depends(get_db)):
    # TODO: update alarms
    return crud.get_alarms(db=db)


@router.post("/", response_model=schemas.Alarm, status_code=status.HTTP_201_CREATED)
def create_alarm(alarm: schemas.AlarmCreate, db: Session = Depends(get_db)):
    # Validate alarm doesn't currently exist
    checks.CheckAlarms.check_alarm_exists(
        db=db,
        model=models.Alarms,
        schema=alarm,
    )
    return crud.create_alarm(db=db, alarm=alarm)


@router.delete("/{alarm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alarm(alarm_id: int, db: Session = Depends(get_db)):

    checks.CheckAlarms.check_alarm_exists_by_id(
        db=db,
        model=models.Alarms,
        alarm_id=alarm_id,
    )
    # Delete Alarm
    crud.delete_alarms(
        db=db,
        alarm_id=alarm_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{alarm_id}", status_code=status.HTTP_200_OK, response_model=schemas.Alarm)
def update_alarm(alarm_id: int, alarm: schemas.AlarmUpdate, db: Session = Depends(get_db)):

    # Check the alarm exists
    checks.CheckAlarms.check_alarm_exists_by_id(
        db=db,
        model=models.Alarms,
        alarm_id=alarm_id
    )

    # apply updates

    # return Alarm instance
    return crud.update_alarms(
        db=db,
        alarm=alarm,
        alarm_id=alarm_id,
    )
