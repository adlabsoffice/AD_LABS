#!/bin/bash

# Coqui XTTS v2 - Deployment Script for GCP Cloud Run
# Usage: ./deploy_gcp.sh YOUR_PROJECT_ID

set -e

# Check if project ID was provided
if [ -z "$1" ]; then
    echo "❌ Error: Project ID not provided."
    echo "Usage: ./deploy_gcp.sh YOUR_PROJECT_ID"
    exit 1
fi

PROJECT_ID=$1
SERVICE_NAME="coqui-xtts"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying Coqui XTTS v2 to Google Cloud Run..."
echo "   Project: ${PROJECT_ID}"
echo "   Region: ${REGION}"
echo ""

# Set active project
echo "📌 Setting active project..."
gcloud config set project ${PROJECT_ID}

# Build the Docker image
echo "🏗️  Building Docker image..."
gcloud builds submit --tag ${IMAGE_NAME}

# Deploy to Cloud Run
echo "☁️  Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --memory 4Gi \
  --cpu 2 \
  --timeout 300 \
  --allow-unauthenticated \
  --max-instances 3

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)')

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "📡 Service URL: ${SERVICE_URL}"
echo ""
echo "🧪 Test with:"
echo "   curl -X POST \"${SERVICE_URL}/tts\" \\"
echo "     -F \"text=Hello world\" \\"
echo "     -F \"language=en\" \\"
echo "     --output test.wav"
echo ""
echo "📚 API Docs: ${SERVICE_URL}/docs"
