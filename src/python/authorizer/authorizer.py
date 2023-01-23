from models import User
from . import Session
from sqlalchemy import exc
import logging

"""
 # @Python program
 # @Lambda Name: academy_lambda_authorizer_vsm_vasanth
 # @File Name: authorizer.py
 # @Since: 
 # @Author: Vasanth
 # @Version: 1.0
 # @To get the details of model.
"""

def lambda_handler(event,context):
    """
    Title:
        The main function to authorize the credentials of the user to let them access or deny the resource
    Args:
        event: Parameter to receive event in JSON format.
        context: Parameter for Runtime information from LambdaContext type.
    Returns:
        Status as JSON Response
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    email = event["headers"]["email"]
    Password = event["headers"]["Password"]
    MethodArn = event["methodArn"]
    method = event["httpMethod"]
    auth = "Deny"
    try:
        session = Session()
        user_info = session.query(User).filter(User.email == email).one()
        if user_info.password == Password and user_info.is_admin :
            auth = "Allow"
        elif user_info.password == Password and method == "GET" :
            auth = "Allow"
        else:
            auth = "Deny"
        logger.info("connection successful")
    except exc.SQLAlchemyError as err:
        logger.info(str(err))
    except Exception as err:
        logger.info(str(err))
    finally:
        session.close()
    return{
          "principalId": "apigateway.amazonaws.com",
          "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
              {
                "Action": "execute-api:Invoke",
                "Effect": auth,
                "Resource": MethodArn
              }
            ]
          }
        }   
