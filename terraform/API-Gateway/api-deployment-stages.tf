#creating dev deployment stage
resource "aws_api_gateway_deployment" "dev-stage-deployment-vsm" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  stage_name = "dev"
  stage_description = "development phase deployment"
  triggers = {
    redeployment = sha1(local.time)
  }
  lifecycle {
    create_before_destroy = true
  }
}
#creating api key
resource "aws_api_gateway_api_key" "api-key" {
    name = "api-key-vsm-vasanth"
    description = " Creating API key for validating the client"
}
#creating usage plan for the rest api we are using
resource "aws_api_gateway_usage_plan" "api-key-usage-plan" {
  name = "api-usage-plan-vsm-vasanth"
  api_stages {
    api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
    stage = aws_api_gateway_deployment.dev-stage-deployment-vsm.stage_name
  }
}
#integrating usage plan with the API key
resource "aws_api_gateway_usage_plan_key" "api-key-usage-plan-key" {
  key_id = aws_api_gateway_api_key.api-key.id
  key_type = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.api-key-usage-plan.id
}
