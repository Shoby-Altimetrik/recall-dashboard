This application is built using Google Cloud Run for deployment, Google Bigtable for data access, and Vertex AI with Gemini 1.5 Pro for generating analysis and insights. It utilizes the dataset from the U.S. Department of Transportation:
https://datahub.transportation.gov/Automobiles/Recalls-Data/6axg-epim/about_data

## Deployment Requirements

To run this application, you will need to set up your own Google Cloud environment:

1. **Google Cloud Project**  
   Create a new Google Cloud project via [Google Cloud Console](https://console.cloud.google.com/). Ensure billing is enabled.

2. **BigQuery / Bigtable Dataset**  
   This application is designed to query data using Google Bigtable or BigQuery. You will need to create and populate your own table containing recall data, either by importing from the [NHTSA dataset](https://datahub.transportation.gov/Automobiles/Recalls-Data/6axg-epim/about_data) or using your own structured dataset with a similar schema.

3. **Vertex AI Access**  
   Enable the Vertex AI API in your project and ensure you have access to use the Gemini 1.5 Pro model.

4. **Cloud Run Deployment**  
   Deploy the app using Google Cloud Run. During deployment, you must grant the necessary permissions to your Cloud Run service account to allow access to Bigtable and Vertex AI.

Be sure to update the project ID, dataset/table references, and authentication setup in the source code or your environment configuration before deploying.