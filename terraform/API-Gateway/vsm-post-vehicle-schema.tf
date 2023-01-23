#creating request body schema for post-vehicle
resource "aws_api_gateway_model" "post-vehicle-template" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  name = "postVehicleTemplate"
  content_type = "application/json"
  schema = <<EOF
  {
    "type":"object",
    "properties":{
      "modelId":{
        "type":"string"
      },
      "vehicleStatus":{
        "type":"object",
        "properties":{
          "vehicleStatusCode":{
            "type":"string"
          },
          "description":{
            "type":"string"
          }
        },
        "required":["vehicleStatusCode","description"]
      },
      "currentPrice":{
        "type":"string"
      },
      "currentMileage":{
        "type":"string"
      },
      "dateReceived":{
        "type":"string"
      },
      "dateOfManufacture":{
        "type":"string"
      },
      "otherDetails":{
        "type":"object"
      },
      "createdBy":{
        "type":"string"
      }
    },
    "required":["modelId","vehicleStatus","currentPrice","currentMileage",
                "dateReceived","dateOfManufacture","createdBy"]
  }
EOF
}