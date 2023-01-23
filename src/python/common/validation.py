from uuid import UUID

class Validation:
    def uuid_validation(self,uuid_value):
        try:
            UUID(uuid_value)
        except ValueError:
            return True
        else:
            return False

    def post_model_validator(self,request_payaload):
        """
        Title:
            validation of the details of the post model body
        Args:
            request_payload: the body json in the event
        Returns:
            Missing or Invalid details as a list
        """ 
        required_keys = ["manufacturerId","modelName","createdBy"]
        error_value = []
        for k,v in request_payaload.items():
            if k in required_keys:
                if k == 'manufacturerId':
                    if self.uuid_validation(v):
                        error_value.append(k)
                if k == 'modelName' and (len(v) > 200 or str(v).strip() == ""):
                    error_value.append(k)
                if k == 'createdBy' and (len(v) > 120 or str(v).strip() == ""):
                    error_value.append(k)
        return error_value

    def update_model_validator(self,request_payaload):
        """
        Title:
            validation of the details of the put model body
        Args:
            request_payload: the body json in the event
        Returns:
            Missing or Invalid details as a list
        """ 
        required_keys = ["modelId","manufacturerId","modelName","updatedBy"]
        error_value = []
        for k,v in request_payaload.items():
            if k in required_keys:
                if k == 'manufacturerId':
                    if self.uuid_validation(v):
                        error_value.append(k)
                if k == 'modelId':
                    if self.uuid_validation(v):
                        error_value.append(k)
                if k == 'modelName' and (len(v) > 200 or str(v).strip() == ""):
                    error_value.append(k)
                if k == 'updatedBy' and (len(v) > 120 or str(v).strip() == ""):
                    error_value.append(k)
        return error_value

    def post_vehicle_validator(self,request_payload):
        """
        Title:
            validation of the details of the post vehicle body
        Args:
            request_payload: the body json in the event
        Returns:
            Missing or Invalid details as a list
        """ 
        required_keys = ["modelId","vehicleStatus","createdBy"]
        error_value = []
        for k,v in request_payload.items():
            if k in required_keys:
                if k == 'modelId':
                    if self.uuid_validation(v):
                        error_value.append(k)  
                if k == 'createdBy' and (len(v) > 120 or str(v).strip() == ""):
                    error_value.append(k)
                if k == "vehicleStatus" and (len(v["vehicleStatusCode"]) > 20 or str(v["vehicleStatusCode"]).strip() == ""):
                    error_value.append("vehicleStatusCode")
        return error_value    

    def update_vehicle_validator(self,request_payload):
        """
        Title:
            validation of the details of the put vehicle body
        Args:
            request_payload: the body json in the event
        Returns:
            Missing or Invalid details as a list
        """ 
        required_keys = ["vehicleId","modelId","vehicleStatus","updatedBy"]
        error_value = []
        for k,v in request_payload.items():
            if k in required_keys:
                if k == 'vehicleId':
                    if self.uuid_validation(v):
                        error_value.append(k)
                if k == 'modelId':
                    if self.uuid_validation(v):
                        error_value.append(k)  
                if k == 'updatedBy' and (len(v) > 120 or str(v).strip() == ""):
                    error_value.append(k)
                if k == "vehicleStatus" and (len(v["vehicleStatusCode"]) > 20 or str(v["vehicleStatusCode"]).strip() == ""):
                    error_value.append("vehicleStatusCode")
        return error_value    
                    


