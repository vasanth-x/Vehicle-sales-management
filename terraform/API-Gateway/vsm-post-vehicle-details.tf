#creating api resource post-vehicle
resource "aws_api_gateway_resource" "post-vehicle" {
    rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
    parent_id = aws_api_gateway_resource.transport.id
    path_part = "vehicle"
}
#creating post method for resource post-vehicle
resource "aws_api_gateway_method" "post-vehicle-method" {
    rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
    resource_id = aws_api_gateway_resource.post-vehicle.id
    http_method = "POST"
    authorization = "CUSTOM"
    authorizer_id = aws_api_gateway_authorizer.lambda-authorizer-vsm.id
    api_key_required = true
    request_parameters = {
      "method.request.header.email" = true
      "method.request.header.Password" = true
    }
    request_models = {
      "application/json" = aws_api_gateway_model.post-vehicle-template.name
    }
    request_validator_id = aws_api_gateway_request_validator.post-vehicle-method-validator.id
}
#validator for body and parameter
resource "aws_api_gateway_request_validator" "post-vehicle-method-validator" {
  name = "post-vehicle-method-validator"
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  validate_request_body = true
  validate_request_parameters = true  
}
#zipping the .py file for pushing into S3
module "post-vehicle-zip" {
  source = "../modules/terraform-aws-lambda-1.47.0"
  runtime         = "python3.9"
  create_function = false
  store_on_s3 = true
  s3_bucket = "academy-terraform-lambda-source-code-v2"
  artifacts_dir  = "academy2022/Vasanth/lambda/post-vehicle"
  source_path = [
    {
      path          = "../src/python/post-vehicle",
      prefix_in_zip = "post-vehicle"
      patterns = [
        "!/src/python/post-vehicle/__pycache__/?.*"
      ]
    },
    {
     path = "../src/python/models"
     prefix_in_zip = "models" 
    },
    {
      path = "../src/python/service"
      prefix_in_zip = "service"
    },
    {
      path = "../src/python/common"
      prefix_in_zip = "common"
    }
  ]
}
#creating lambda function
resource "aws_lambda_function" "lambda-post-vehicle" {
    function_name = "academy_vsm_lambda_post_vehicle_vasanth"
    description = "lambda for adding vehicle details"
    role = var.lambda-role
    memory_size = "128"
    timeout = "180"
    s3_bucket = module.post-vehicle-zip.s3_object.bucket
    s3_key = module.post-vehicle-zip.s3_object.key
    runtime = "python3.9"
    handler = "post-vehicle.post-vehicle.lambda_handler" 
    depends_on = [
      module.post-vehicle-zip
    ]  
    vpc_config {
      subnet_ids = split(",",var.subnet-ids)
      security_group_ids =split(",",var.security-group-ids)
    } 
    tags = {
        "OWNER" = "VASANTH"
        "PROJECT" = "VEHICLE SALES MANAGEMENT"
        "RUN-TIME" = "Python 3.9"
        "REGION-NAME" = "ap-southeast-1"
    }
    layers = [module.lambda_layers_sqlalchemy.this_lambda_layer_arn]
    environment {
      variables = {
        "DB_HOSTNAME" :var.host_address,
        "DB_PORT" : var.host_port,
        "DB_USERNAME": var.db_user_name,
        "DB_PASSWORD": var.db_password,
        "DB_NAME": var.db_name,
        "DB_SCHEMA":var.db_schema
      }
    }
}
resource "aws_lambda_permission" "lambda-permission-post-vehicle"{
    action = "lambda:InvokeFunction"
    statement_id = "AllowExecutionFunctionFromLambda"
    function_name = aws_lambda_function.lambda-post-vehicle.arn
    principal = "apigateway.amazonaws.com"
    source_arn = "${aws_api_gateway_rest_api.api-gateway-vsm.execution_arn}/*/${aws_api_gateway_method.post-vehicle-method.http_method}${aws_api_gateway_resource.post-vehicle.path}"
}
#integrating lambda and Api gateway
resource "aws_api_gateway_integration" "integrate-lambda-post-vehicle" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  resource_id = aws_api_gateway_resource.post-vehicle.id
  http_method = aws_api_gateway_method.post-vehicle-method.http_method
  integration_http_method = "POST"
  uri = aws_lambda_function.lambda-post-vehicle.invoke_arn 
  type = "AWS"
  request_parameters = {
    "integration.request.header.email"="method.request.header.email" 
    "integration.request.header.Password"="method.request.header.Password"
  }
  request_templates = {
    "application/json"= data.local_file.init.content
  }
  passthrough_behavior = "WHEN_NO_TEMPLATES"
  timeout_milliseconds = "15000"
}
#creating method response for post-vehicle method
resource "aws_api_gateway_method_response" "post-vehicle-method-response-200" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  resource_id = aws_api_gateway_resource.post-vehicle.id
  http_method = aws_api_gateway_method.post-vehicle-method.http_method
  status_code = 200
  response_models = {
    "application/json" = "Error"
  }
}
resource "aws_api_gateway_method_response" "post-vehicle-method-response-400" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  resource_id = aws_api_gateway_resource.post-vehicle.id
  http_method = aws_api_gateway_method.post-vehicle-method.http_method
  status_code = 400
  response_models = {
    "application/json" = "Error"
  }
}
resource "aws_api_gateway_method_response" "post-vehicle-method-response-500" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  resource_id = aws_api_gateway_resource.post-vehicle.id
  http_method = aws_api_gateway_method.post-vehicle-method.http_method
  status_code = 500
  response_models = {
    "application/json" = "Error"
  }
}
#creating integration response for post-vehicle method
resource "aws_api_gateway_integration_response" "post-vehicle-integration-response-200" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  resource_id = aws_api_gateway_resource.post-vehicle.id
  http_method = aws_api_gateway_method.post-vehicle-method.http_method
  status_code = aws_api_gateway_method_response.post-vehicle-method-response-200.status_code
  selection_pattern = "-"
  response_templates = {
    "application/json" = "$input.json('$')"
  }
  depends_on = [
    aws_api_gateway_method_response.post-vehicle-method-response-200
  ]
}
resource "aws_api_gateway_integration_response" "post-vehicle-integration-response-400" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  resource_id = aws_api_gateway_resource.post-vehicle.id
  http_method = aws_api_gateway_method.post-vehicle-method.http_method
  status_code = aws_api_gateway_method_response.post-vehicle-method-response-400.status_code
  selection_pattern = ".*Missing.*"
  response_templates = {
    "application/json" = data.template_file.template_400.template
  }
  depends_on = [
    aws_api_gateway_method_response.post-vehicle-method-response-400
  ]
}
resource "aws_api_gateway_integration_response" "post-vehicle-integration-response-500" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  resource_id = aws_api_gateway_resource.post-vehicle.id
  http_method = aws_api_gateway_method.post-vehicle-method.http_method
  status_code = aws_api_gateway_method_response.post-vehicle-method-response-500.status_code
  selection_pattern = "Internal server error"
  response_templates = {
    "application/json" = data.template_file.template_500.template
  }
  depends_on = [
    aws_api_gateway_method_response.post-vehicle-method-response-500
  ]
}