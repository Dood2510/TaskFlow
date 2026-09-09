terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "taskflow_bucket" {
  bucket = "abdullah-taskflow-bucket-2026"

  tags = {
    Name        = "TaskFlow Bucket"
    Environment = "Learning"
  }
}
