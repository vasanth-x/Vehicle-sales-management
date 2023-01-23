#creating request body schema for update-vehicle
resource "aws_api_gateway_model" "update-vehicle-template" {
  rest_api_id = aws_api_gateway_rest_api.api-gateway-vsm.id
  name = "updateVehicleTemplate"
  content_type = "application/json"
  schema =<<EOF
 {
        "type": "object",
        "properties": {
          "vehicleId": {
                "type": "string"
            },
            "modelId": {
                "type": "string"
            },
            "vehicleStatus":{
              "type": "object",
              "properties": {
                "vehicleStatusCode": {
                  "type": "string"
                },
                "description": {
                  "type": "string"
                }
              },
              "required": [
                "vehicleStatusCode",
                "description"
              ]
            },
            "currentPrice":{
              "type": "string"
            },
            "currentMileage":{
              "type": "string"
            },
            "dateReceived":{
              "type": "string"
            },
            "dateOfManufacture":{
              "type": "string"
            },
            "otherDetails" : {
                "type" : "object"
            },
            "updatedBy" :{
                "type" : "string"
            }   
        },
        "required" : [
          "modelId",
          "vehicleStatus",
          "currentPrice",
          "currentMileage",
          "dateReceived",
          "dateOfManufacture",
          "updatedBy"
        ]
    }
EOF
}