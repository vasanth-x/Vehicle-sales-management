import json,os,logging,uuid
from models import Vehicles
from . import Session
from sqlalchemy import exc

"""
 # @Python program
 # @Lambda Name: academy_vsm_lambda_get_vehicle_vasanth
 # @File Name: get-vehicle.py
 # @Since: 
 # @Author: Vasanth
 # @Version: 1.0
 # @To get the details of vehicle.
"""

def lambda_handler(event,context):
    """
    Title:
        Function to get an vehicle data from VEHICLE table
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
        event_query_params = event['params']['querystring']
        vehicle_id = uuid.UUID(event_query_params['vehicleId'])
        logger.info("Connection Successfull")
        result = session.query(Vehicles).filter(Vehicles.vehicle_id == vehicle_id).one()
        return result.get_payload()
    except exc.NoResultFound as e:
        logger.info(str(e))
        raise Exception("Model not found")
    except ValueError as e:
        logger.info(str(e))
        raise Exception("Missing details")
    except Exception as e:
        logger.info(str(e))
        raise Exception("Internal server error",e)     
    finally:
        session.close() 