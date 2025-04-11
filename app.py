from flask import Flask, render_template, request
from google.cloud import bigquery
from vertexai.generative_models import GenerativeModel
import vertexai
import pandas as pd
import json

app = Flask(__name__)

vertexai.init(project="917938169120", location="us-central1")
gemini = GenerativeModel("gemini-1.5-pro-002")
# gemini = GenerativeModel("gemini-2.0-flash-lite-001")

def load_data():
    client = bigquery.Client()
    query = "SELECT * FROM `ford_demo_dataset_2.recall_data`"
    return client.query(query).to_dataframe()

@app.route("/", methods=["GET", "POST"])
def dashboard():
    result_html = ""
    prompt = ""

    if request.method == "POST":
        prompt = request.form.get("prompt")
        try:
            df = load_data()
            if 'Report_Received_Date' in df.columns:
                df['Year'] = pd.to_datetime(df['Report_Received_Date'], errors='coerce').dt.year

            schema_info = df.dtypes.astype(str).to_dict()
            column_descriptions = {
                "Report_Received_Date": "Date the recall was officially received",
                "NHTSA_ID": "Unique recall identifier assigned by NHTSA",
                "Recall_Link": "Link to the full recall report",
                "Manufacturer": "Company responsible for the recall",
                "Subject": "Headline or topic of the recall",
                "Component": "Vehicle system or part involved in the recall",
                "Mfr_Campaign_Number": "Manufacturer-specific campaign number",
                "Recall_Type": "Classification of the recall (e.g., safety, compliance)",
                "Potentially_Affected": "Number of vehicles potentially impacted",
                "Recall_Description": "Detailed description of the recall",
                "Consequence_Summary": "Possible consequences if the defect is not addressed",
                "Corrective_Action": "Steps taken to remedy the issue",
                "Park_Outside_Advisory": "Indicates if vehicles should be parked outside",
                "Do_Not_Drive_Advisory": "Indicates if vehicles should not be driven"
            }
            json_sample = df.sample(min(len(df), 25), random_state=42).to_dict(orient="records")

            gemini_prompt = f"""You are a data analyst. Analyze this dataset to generate insights, trends, and recommendations.

Schema:
{json.dumps(schema_info, indent=2, default=str)}

Descriptions:
{json.dumps(column_descriptions, indent=2, default=str)}

Sample:
{json.dumps(json_sample, indent=2, default=str)}

User Prompt:
"{prompt}"

Generate a complete HTML dashboard including:
- KPI cards (class="kpi") with calculated metrics
- One or more Plotly charts (output as valid Plotly JSON)
- An HTML data table summarizing key statistics or breakdowns
- A written summary of key insights, trends, or anomalies
- Suggested next steps or follow-up questions for the user to explore

All charts must use valid Plotly JSON format, and the table must be a valid <table> HTML element.
"""

            response = gemini.generate_content(gemini_prompt)
            result_html = response.text if hasattr(response, "text") else "<p>No content returned from Gemini.</p>"

        except Exception as e:
            result_html = f"<p style='color:red;'>Error: {e}</p>"

    return render_template("dashboard.html", dashboard=result_html, prompt=prompt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)