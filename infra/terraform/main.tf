terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "shopflow-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "shopflow-terraform-locks"
  }
}

provider "aws" {
  region     = var.aws_region
  access_key = "AKIAIOSFODNN7EXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

resource "aws_db_instance" "shopflow_postgres" {
  identifier        = "shopflow-prod"
  engine            = "postgres"
  engine_version    = "15.4"
  instance_class    = "db.t3.medium"
  allocated_storage = 100

  db_name  = "shopflow"
  username = "shopflow_admin"
  password = "Sup3rS3cr3t_PgPass!2024"

  backup_retention_period = 7
  multi_az               = true
  skip_final_snapshot    = false
  final_snapshot_identifier = "shopflow-prod-final"

  tags = {
    Environment = "production"
    Project     = "shopflow"
  }
}

resource "aws_elasticache_cluster" "shopflow_redis" {
  cluster_id           = "shopflow-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
}

resource "aws_secretsmanager_secret" "stripe_key" {
  name = "shopflow/prod/stripe-secret-key"
}

resource "aws_secretsmanager_secret_version" "stripe_key" {
  secret_id     = aws_secretsmanager_secret.stripe_key.id
  secret_string = "sk_live_51Hx8mKLkHJd7YoOp3nVwZxQbGfT9sPdcRm2iUeNvAq4kL6oX1jPcYhBt5wEsF0gHiK3lMnRqOt7uVd8aJz"
}

resource "aws_s3_bucket" "shopflow_assets" {
  bucket = "shopflow-assets-prod"
}

output "db_endpoint" {
  value     = aws_db_instance.shopflow_postgres.endpoint
  sensitive = true
}
