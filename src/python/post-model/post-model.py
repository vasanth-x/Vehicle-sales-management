"""
 # @Python program
 # @Lambda Name: academy_vsm_lambda_post_model_vasanth
 # @File Name: post-model.py
 # @Since: 
 # @Author: Vasanth
 # @Version: 1.0
 # @To add the new data in Model table. 
"""

import json,os,logging
from . import Session
from models import Models
from common import Validation,LambdaException,constants

def lambda_handler(event,context):
    """
    Title:
        Function to add an model data in MODEL table
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
        request_payload = event["body-json"]
        logger.info("Connection Successfull")
        models = Models()
        validator = Validation()
        validator_info = validator.post_model_validator(request_payload)
        if validator_info :
            raise LambdaException
        models.post_model(request_payload)
        session.add(models)
        session.commit()
        return constants.POST_MODEL_MESSAGE
    except LambdaException as e:
        logger.info(str(e))
        raise LambdaException("Missing / wrong details in",validator_info)
    except Exception as e:
        logger.info(str(e))
        raise LambdaException("Internal server error")
    finally:
        session.close()

    

