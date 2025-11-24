provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable Cloud Run API
resource "google_project_service" "run_api" {
  service = "run.googleapis.com"
}

# Create the Cloud Run Service
resource "google_cloud_run_service" "default" {
  name     = "smart-chem-app-tf"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/smart-chem-app:latest"
        ports {
            container_port = 8080
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}
