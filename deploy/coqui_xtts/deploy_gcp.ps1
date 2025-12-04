# Coqui XTTS v2 - Deployment Script for GCP Cloud Run (Windows PowerShell)
# Usage: .\deploy_gcp.ps1 YOUR_PROJECT_ID

param(
  [Parameter(Mandatory = $true)]
  [string]$ProjectId
)

$ErrorActionPreference = "Stop"

$SERVICE_NAME = "coqui-xtts"
$REGION = "us-central1"
$IMAGE_NAME = "gcr.io/$ProjectId/$SERVICE_NAME"

Write-Host "Deploying Coqui XTTS v2 to Google Cloud Run..." -ForegroundColor Cyan
Write-Host "   Project: $ProjectId"
Write-Host "   Region: $REGION"
Write-Host ""

# Set active project
Write-Host "Setting active project..." -ForegroundColor Yellow
gcloud config set project $ProjectId

# Build the Docker image
Write-Host "Building Docker image..." -ForegroundColor Yellow
gcloud builds submit --tag $IMAGE_NAME

# Deploy to Cloud Run
Write-Host "Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $SERVICE_NAME `
  --image $IMAGE_NAME `
  --platform managed `
  --region $REGION `
  --memory 4Gi `
  --cpu 2 `
  --timeout 300 `
  --allow-unauthenticated `
  --max-instances 3

# Get the service URL
$SERVICE_URL = gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)'

Write-Host ""
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Service URL: $SERVICE_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "Test with:"
Write-Host "   curl -X POST `"$SERVICE_URL/tts`" -F `"text=Hello world`" -F `"language=en`" --output test.wav"
Write-Host ""
Write-Host "API Docs: $SERVICE_URL/docs" -ForegroundColor Cyan
