variable "lambda-role" {
    default = ""
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
    default = ""
}
variable "security-group-ids" {
    default = ""
}
variable "host_address" {
  default = ""
}
variable "host_port" {
  default = ""
}
variable "db_user_name" {
  default = "transport_mgmt_owner"
}
variable "db_password" {
  default = ""
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
