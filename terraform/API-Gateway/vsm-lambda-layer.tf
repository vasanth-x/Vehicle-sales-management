#zipping the layer .py file for pushing into S3
module "lambda_layers_sqlalchemy" {
  source = "../modules/terraform-aws-lambda-1.47.0"
  create_layer = true
  layer_name = "SQLalchemy_package"
  compatible_runtimes = [ "python3.8", "python3.9" ]
  s3_bucket = "academy-terraform-lambda-source-code-v2"
  store_on_s3 = true
  artifacts_dir = "academy2022/Vasanth/lambda_layer"
  source_path = { pip_requirements = "../requirements.txt",      
                  prefix_in_zip = "python"      
                }
  runtime = "python3.9"
}
