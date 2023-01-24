# variable "api-key-source" {
#   default = "HEADER"
#   type = string
#   description = " API key of incoming request for validating "
# }
variable "access_key" {
    description = "access key"
    default = ""
}
variable "secret_key" {
    description = "secret key"
    default = ""
}
variable "region" {
    description = "region"
    default = "ap-southeast-1" 
}
