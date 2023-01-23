"""
 # @Python program
 # @Lambda Name: academy_vsm_lambda_post_vehicle_vasanth
 # @File Name: post-vehicle.py
 # @Since: 
 # @Author: Vasanth
 # @Version: 1.0
 # @To add the new data in Vehicle table.
"""
import json,logging
from models import Vehicles
from . import Session
from common import Validation,LambdaException,constants

def lambda_handler(event,context):
    """
    Title:
        Function to add an vehicle data in VEHICLE table
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
        vehicles = Vehicles()
        request_payload = event['body-json']
        logger.info("Connection Successfull")
        validator = Validation()
        validator_info = validator.post_vehicle_validator(request_payload)
        if validator_info :
            raise LambdaException        
        vehicles.post_vehicle(request_payload)
        session.add(vehicles)
        session.commit()
        return constants.POST_VEHICLE_MESSAGE
    except LambdaException as e:
        logger.info(str(e))
        raise LambdaException("Missing / wrong details in",validator_info)
    except Exception as e:
        logger.info(str(e))
        raise Exception("Internal server error")
    finally:
        session.close()       
        