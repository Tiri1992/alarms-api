"""Crud controller for alarms"""
from app.core.controller.base import CrudController
from app.core.controller.base import CheckController
from sqlalchemy.orm import Session
# Schemas
from app.schemas.alarms import AlarmCreateSchema
from app.schemas.alarms import AlarmDeleteSchema
from app.schemas.alarms import AlarmUpdateSchema
# Models
from app.models.alarms import AlarmModel
# Exceptions
from app.core.errors.alarms import ALARM_EXISTS_CONFLICT
from app.core.errors.alarms import ALARM_NOT_FOUND
# Utils
from datetime import datetime

class CrudAlarm(CrudController):

    def __init__(self, db: Session):
        self._db = db
        self._model = AlarmModel

    def find(self, alarm_id: id) -> AlarmModel:
        """Responsible for checking the database if an existing
        alarm object exists before user attempts to recreate it.

        Different to `get` which will consume all existing alarms
        for current user.
        """
        return self._db.query(self._model).filter(
            self._model.id == alarm_id
            ).first()

    def get(self, user_id: int) -> list[AlarmModel]:
        return self._db.query(self._model).filter(self._model.user_id == user_id).all()
 
    def create(self, user_id: int, schema: AlarmCreateSchema) -> AlarmModel:
        record = self._model(**schema.dict(), user_id=user_id)
        # Write record to db
        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record

    def delete(self, alarm_id: int) -> None:
        """Delete alarm record by using alarm_id."""
        record = self._db.query(self._model).filter(
            self._model.id == alarm_id
        )
        record.delete(synchronize_session=False)
        self._db.commit()
    
    def update(self, alarm_id: int, schema: AlarmUpdateSchema) -> AlarmModel:
        record = self._db.query(self._model).filter(self._model.id == alarm_id)
        # Updates record with current time
        # Update http request requires all information 
        schema.updated_at = datetime.now()
        record.update(schema.dict(), synchronize_session=False)
        self._db.commit()
        return record.first()

class CheckAlarms(CheckController):

    def __init__(self, db: Session) -> None:
        self._db = db 
        self._model = AlarmModel

    def not_exists_with_id(self, alarm_id: int, user_id: int) -> None:
        """Checks if alarm does not exist from the alarm_id."""
        res = self._db.query(self._model).filter(
            self._model.id == alarm_id,
            self._model.user_id == user_id
            ).first()
        if not res:
            raise ALARM_NOT_FOUND

    def exists(self, user_id: int, schema: AlarmCreateSchema) -> None:
        """Checks if alarm exists in db and if so, will raise a HTTP conflict 409 exception."""
        # Uniquely define the alarm based on user_id, time and day of week.
        res = self._db.query(self._model).filter(
            self._model.user_id == user_id,
            self._model.time == schema.time,
            self._model.day_of_week == schema.day_of_week
        ).first()
        if res:
            raise ALARM_EXISTS_CONFLICT

    def not_exists(self, user_id: int, schema: AlarmDeleteSchema) -> None:
        """Checks if alarm does not exists in db and if so, will raise a HTTP not found 404 exception.
        
        NOTE: This is the reverse logic of the method .exists() which will raise an error
            if it does find a record.
        """
        res = self._db.query(self._model).filter(
            self._model.user_id == user_id,
            self._model.time == schema.time,
            self._model.day_of_week == schema.day_of_week
        ).first()

        if not res:
            raise ALARM_NOT_FOUND