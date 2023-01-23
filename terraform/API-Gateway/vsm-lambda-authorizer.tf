#zipping the .py file for pushing into S3
module "lambda-authorizer-zip" {
  source = "../modules/terraform-aws-lambda-1.47.0"
  runtime = "python3.9"
  create_function = false
  store_on_s3 = true
  s3_bucket = "academy-terraform-lambda-source-code-v2"
  artifacts_dir  = "academy2022/Vasanth/authorizer"
  source_path = [
    {
        path ="../src/python/authorizer"
        prefix_in_zip= "authorizer"
    },
    {
     path = "../src/python/models"
     prefix_in_zip = "models" 
    },
    {
      path = "../src/python/service"
      prefix_in_zip = "service"
    }
  ]
}

#creating lambda function
resource "aws_lambda_function" "lambda-authorizer" {
  function_name = "academy_lambda_authorizer_vsm_vasanth"
  s3_bucket = module.lambda-authorizer-zip.s3_object.bucket
  s3_key = module.lambda-authorizer-zip.s3_object.key
  role = var.lambda-role
  timeout = 180
  memory_size = 128
  runtime = "python3.9"
  handler = "authorizer.authorizer.lambda_handler"
  depends_on = [
    module.lambda-authorizer-zip
  ]
  vpc_config {
      subnet_ids = split(",",var.subnet-ids)
      security_group_ids = split(",",var.security-group-ids)
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
#creating lambda authorizer
resource "aws_api_gateway_authorizer" "lambda-authorizer-vsm" {
  name = "vsm_lambda_authoriser"
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  identity_source = "method.request.header.email,method.request.header.Password"
  type = "REQUEST"
  authorizer_result_ttl_in_seconds = "0"
  authorizer_uri = aws_lambda_function.lambda-authorizer.invoke_arn
  authorizer_credentials = var.lambda-role
}

resource "aws_lambda_permission" "lambda-permission-authorizer"{
    action = "lambda:InvokeFunction"
    statement_id = "AllowExecutionFunctionFromLambda"
    function_name = aws_lambda_function.lambda-authorizer.arn
    principal = "apigateway.amazonaws.com"
    source_arn = "${aws_api_gateway_rest_api.api-gateway-vsm.execution_arn}/authorizers/${aws_api_gateway_authorizer.lambda-authorizer-vsm.id}"
}
