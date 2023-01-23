"""
 # @Python program
 # @Lambda Name: academy_vsm_lambda_update_model_vasanth
 # @File Name: update-model.py
 # @Since: 
 # @Author: Vasanth
 # @Version: 1.0
 # @To update the data of Model table.
"""
import json,logging
from sqlalchemy import exc
from common import Validation,LambdaException,constants
from models import Vehicles
from . import Session

def lambda_handler(event,context):
    """
    Title:
        Function to update an vehicle data in VEHICLE table
    Args:
        event: Parameter to receive event in JSON format.
        context: Parameter for Runtime information from LambdaContext type.
    Returns:
        Status as JSON Response
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
        session = Session()
        request_payload = event['body-json']
        vehicle_id = event['body-json']['vehicleId']
        logger.info("Connection Successfull")
        validator = Validation()
        validator_info = validator.update_vehicle_validator(request_payload)
        if validator_info :
            raise LambdaException  
        update_vehicle = session.query(Vehicles).filter(Vehicles.vehicle_id == vehicle_id).one()
        update_vehicle.post_vehicle(request_payload)
        session.commit()
        return constants.PUT_VEHICLE_MESSAGE
    except exc.NoResultFound as e:
        logger.info(str(e))
        raise LambdaException("Vehicle not found")
    except LambdaException as e:
        logger.info(str(e))
        raise LambdaException("Missing / wrong details in",validator_info)
    except Exception as e:
        logger.info(str(e))
        raise Exception("Internal server error")
    finally:
        session.close() 


