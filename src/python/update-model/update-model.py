"""
 # @Python program
 # @Lambda Name: academy_vsm_lambda_update_model_vasanth
 # @File Name: update-model.py
 # @Since: 
 # @Author: Vasanth
 # @Version: 1.0
 # @To update the data of Model table.
"""

import json,os,logging
from sqlalchemy import exc
from common import Validation,LambdaException,constants
from . import Session
from models import Models

def lambda_handler(event,context):
    """
    Title:
        Function to update an model data in MODEL table
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
        model_id = event['body-json']['modelId']
        logger.info("Connection Successfull")
        validator = Validation()
        validator_info = validator.update_model_validator(request_payload)
        if validator_info :
            raise LambdaException  
        update_model = session.query(Models).filter(Models.model_id == model_id).one()
        update_model.post_model(request_payload)
        session.commit()
        return constants.PUT_MODEL_MESSAGE
    except exc.NoResultFound as e:
        logger.info(str(e))
        raise LambdaException("Model not found")
    except LambdaException as e:
        logger.info(str(e))
        raise LambdaException("Missing / wrong details in",validator_info)
    except Exception as e:
        logger.info(str(e))
        raise LambdaException("Internal server error")
    finally:
        session.close() 