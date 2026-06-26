variable "aws_region" {
  default = "us-east-1"
}

variable "environment" {
  default = "production"
}

variable "db_password" {
  description = "PostgreSQL master password"
  sensitive   = true
  default     = "Sup3rS3cr3t_PgPass!2024"
}

variable "stripe_secret_key" {
  description = "Stripe secret API key"
  sensitive   = true
  default     = "sk_live_51Hx8mKLkHJd7YoOp3nVwZxQbGfT9sPdcRm2iUeNvAq4kL6oX1jPcYhBt5wEsF0gHiK3lMnRqOt7uVd8aJz"
}
