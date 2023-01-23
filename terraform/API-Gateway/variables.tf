variable "lambda-role" {
    default = "arn:aws:iam::754198558058:role/academy_lambda_access"
    description = "role for lambda"
}
data "local_file" "init"{
    filename = "templates/request_body.template"
}
data "template_file" "template_400" {
  template = file("templates/template_400.template")
}
data "template_file" "template_404" {
  template = file("templates/template_404.template")
}
data "template_file" "template_500" {
  template = file("templates/template_500.template")
}
variable "subnet-ids" {
    default = "subnet-0e5a4c5e0f4ca0065,subnet-0e785e0704a99e509,subnet-0f7b10e34cb5bfe74"
}
variable "security-group-ids" {
    default = "sg-094aaa57e16071d3c"
}
variable "host_address" {
  default = "acedamy-db.cluster-comqig7qvkr5.ap-southeast-1.rds.amazonaws.com"
}
variable "host_port" {
  default = "6581"
}
variable "db_user_name" {
  default = "transport_mgmt_owner"
}
variable "db_password" {
  default = "973eBYQ7i*9V"
}
variable "db_name" {
  default = "academy"
}
variable "db_schema" {
  default = "transport_mgmt"
}
locals {
  time = formatdate("DD MMM YYYY hh:mm:ss ZZZ",timestamp())
}