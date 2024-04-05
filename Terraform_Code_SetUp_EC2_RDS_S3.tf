terraform {
  required_version = ">= 0.12"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.41.0"
    }
  }
}

provider "aws" {
  region     = "ap-south-1"
  profile    = "default"
}

variable "amiId" { 
  default = "ami-013168dc3850ef002"
}

variable "osName"{
  default = "myos1"
}

resource "aws_instance" "myos1" {
  ami           = var.amiId
  key_name      = "terraform"
  vpc_security_group_ids = [ "sg-00a1cc139b60b5850" ]
  instance_type = "t2.micro"  
  tags = {
    Name = var.osName
  }
}

resource "aws_s3_bucket" "my_bucket" {
  bucket_prefix = "your_s3_bucket_name"
  acl           = "private"
}

resource "aws_db_instance" "my_rds_instance" {
  identifier           = "my-rds-instance"
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "mydatabase"
  username             = "admin"
  password             = "your_rds_password"
  parameter_group_name = "default.mysql5.7"
  publicly_accessible  = true  # Make the RDS instance publicly accessible

  tags = {
    Name = "MyRDSInstance"
  }
}
