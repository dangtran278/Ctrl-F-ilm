#!/bin/bash
set -e

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=${AWS_REGION:-us-east-2}
IMAGE_NAME="ctrl-film-serving"
ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE_NAME"

aws ecr get-login-password --region "$AWS_REGION" | \
  docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

docker build -t "$IMAGE_NAME" ./serving
docker tag "$IMAGE_NAME" "$ECR_URI:latest"
docker push "$ECR_URI:latest"

aws ecs update-service \
  --cluster ctrl-film \
  --service ctrl-film-serving \
  --force-new-deployment \
  --region "$AWS_REGION" \
  --output none
