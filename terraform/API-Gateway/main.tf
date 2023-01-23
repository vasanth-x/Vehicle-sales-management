#creating api gateway 
resource "aws_api_gateway_rest_api" "api-gateway-vsm" {
    name = "academy_vehicle_sales_management_system_vasanth"
    description = "Final Project"
    endpoint_configuration {
      types = ["REGIONAL"]
    }
    tags = {
      "Author" = "Vasanth"
      "Project" = "Vehicle Sales Management"
    }
}
#creating root resource
resource "aws_api_gateway_resource" "v1" {
    rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
    parent_id = aws_api_gateway_rest_api.api-gateway-vsm.root_resource_id
    path_part = "v1"
}
#creating sub resource for parent v1
resource "aws_api_gateway_resource" "transport" {
    rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
    parent_id = aws_api_gateway_resource.v1.id
    path_part = "transport"
}
