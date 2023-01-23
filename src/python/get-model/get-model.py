import json,os,logging,uuid
from . import Session
from models import Models
from sqlalchemy import exc
from common import LambdaException

"""
 # @Python program
 # @Lambda Name: academy_vsm_lambda_get_model_vasanth
 # @File Name: get-model.py
 # @Since: 
 # @Author: Vasanth
 # @Version: 1.0
 # @To get the details of model.
"""

def lambda_handler(event,context):
    """
    Title:
        Function to get an model data from MODEL table
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
        event_query_params = event["params"]["querystring"]
        model_id = event_query_params["modelId"]
        logger.info("Connection Successfull")
        results = session.query(Models).filter(Models.model_id == model_id).one()
        return results.get_payload()
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
