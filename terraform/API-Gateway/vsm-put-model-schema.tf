#creating request body schema for update-model
resource "aws_api_gateway_model" "update-model-template" {
  name = "updateModelTemplate"
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  content_type = "application/json"
  schema = <<EOF
  {
    "type" : "object",
    "properties":{
        "modelId":{
            "type":"string"
        },
        "manufacturerId":{
            "type":"string"
        },
        "modelName":{
            "type":"string"
        },
        "otherDetails":{
            "type":"object"
        },
        "updatedBy":{
            "type":"string"
        }
    },
    "required":["modelId","manufacturerId","modelName","updatedBy"]
}
EOF 
}