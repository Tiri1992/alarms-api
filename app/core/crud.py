"""Reusable methods for CRUD executions.

As this project grows, there will be a need to create an independent
subpackage which separates the operations based on models.
"""

# Sqlalchemy
from sqlalchemy.orm import Session
from app.models import alarms as model_alarm
# Pydantic Schemas
from app.schemas import alarms as schema_alarm
from datetime import datetime

# Create alarm


def create_alarm(
    db: Session,
    alarm: schema_alarm.AlarmCreate
) -> model_alarm.Alarms:
    """Persists the creation of an alarm to db."""
    new_alarm = model_alarm.Alarms(**alarm.dict())
    # Persist to db
    db.add(new_alarm)
    db.commit()
    # This is to get the new representation of the obj
    # after persisting
    db.refresh(new_alarm)
    return new_alarm


def get_alarms(db: Session) -> list[model_alarm.Alarms]:
    alarms = db.query(model_alarm.Alarms).all()
    return alarms


def delete_alarms(db: Session, alarm_id: int) -> None:

    alarm = db.query(model_alarm.Alarms).filter(
        model_alarm.Alarms.id == alarm_id)
    alarm.delete(synchronize_session=False)
    db.commit()


def update_alarms(
    db: Session,
    alarm: schema_alarm.AlarmUpdate,
    alarm_id: int
) -> None:

    curr_alarm = db.query(model_alarm.Alarms).filter(
        model_alarm.Alarms.id == alarm_id
    )

    # Update curr_alarm instance with request data
    # and fill in the current datetime
    alarm.updated_at = datetime.now()

    curr_alarm.update(alarm.dict(), synchronize_session=False)
    # Commit changes
    db.commit()
    return curr_alarm.first()
