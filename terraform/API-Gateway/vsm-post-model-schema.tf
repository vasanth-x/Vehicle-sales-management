#creating request body schema for post-model
resource "aws_api_gateway_model" "post-model-template" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  name = "postModelTemplate"
  content_type = "application/json"
  schema = <<EOF
  {
    "type" : "object",
    "properties":{
        "manufacturerId":{
            "type":"string"
        },
        "modelName":{
            "type":"string"
        },
        "otherDetails":{
            "type":"object"
        },
        "createdBy":{
            "type":"string"
        }
    },
    "required":["manufacturerId","modelName","createdBy"]
}
EOF
}