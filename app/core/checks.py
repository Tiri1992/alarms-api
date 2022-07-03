"""Data validation checks on db. These will raise the appriopriate HTTP 
Errors if required."""
from fastapi import HTTPException
from fastapi import status
from calendar import day_name
from sqlalchemy.orm import Session
from app.models import alarms as model_alarm
from app.schemas import alarms as schema_alarm


class CheckAlarms:

    @staticmethod
    def check_alarm_exists(
        db: Session,
        model: model_alarm.Alarms,
        schema: schema_alarm.AlarmBase
    ) -> None:
        """check_alarm_exists _summary_

        ### TODO: FILL IN DOCSTRINGS

        Args:
            db (Session): _description_
            model (model_alarm.Alarms): _description_
            schema (schema_alarm.AlarmBase): _description_

        Raises:
            HTTPException: _description_
        """
        # Check for existing alarm
        response = db.query(model).filter(
            model.day_of_week == schema.day_of_week,
            model.hour == schema.hour
        ).first()

        if response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Current alarm starting on {day_name[schema.day_of_week - 1]} at {schema.hour}:00 already exists."
            )

    @staticmethod
    def check_alarm_exists_by_id(
        db: Session,
        model: model_alarm.Alarms,
        alarm_id: int,
    ) -> None:
        """check_alarm_exists_by_id _summary_

        ## TODO: FILL IN DOCSTRINGS

        Args:
            db (Session): _description_
            model (model_alarm.Alarms): _description_
            alarm_id (int): _description_

        Raises:
            HTTPException: _description_
        """

        response = db.query(model).filter(model.id == alarm_id).first()

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not find alarm for given {alarm_id=}"
            )
