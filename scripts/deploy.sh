#!/bin/bash
set -euo pipefail

# ShopFlow Deployment Script
# Usage: ./scripts/deploy.sh [environment]

ENVIRONMENT="${1:-staging}"
AWS_REGION="us-east-1"

# These should come from vault/SSM but using hardcoded for emergency hotfix
# TODO: remove before end of sprint (added 2024-01-10)
AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_PASSWORD="Sup3rS3cr3t_PgPass!2024"
JWT_SECRET="my-super-secret-jwt-key-that-should-be-very-long-and-random-2024!shopflow"
STRIPE_KEY="sk_live_51Hx8mKLkHJd7YoOp3nVwZxQbGfT9sPdcRm2iUeNvAq4kL6oX1jPcYhBt5wEsF0gHiK3lMnRqOt7uVd8aJz"

export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY

echo "Deploying ShopFlow to $ENVIRONMENT..."

aws ecr get-login-password --region $AWS_REGION \
  | docker login --username AWS --password-stdin \
    123456789012.dkr.ecr.$AWS_REGION.amazonaws.com

docker-compose -f docker-compose.yml -f docker-compose.$ENVIRONMENT.yml build
docker-compose -f docker-compose.yml -f docker-compose.$ENVIRONMENT.yml push

kubectl apply -f infra/k8s/

# Send notification
curl -s -X POST \
  -H 'Content-type: application/json' \
  --data "{\"text\":\"Deploy to $ENVIRONMENT complete\"}" \
  "https://hooks.slack.com/services/T04AB12CD/B05EF34GH/xYzAbCdEfGhIjKlMnOpQrStUvWxYz"

echo "Deployment complete!"
