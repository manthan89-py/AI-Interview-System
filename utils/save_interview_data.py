import json
import os


def save_interview_data(interview_data, candidate_name):
    filename = f"{candidate_name}_interview_data.json"
    """Save interview data to Supbase Database"""

    ## Optioanl to save to local directory
    os.makedirs("outputs", exist_ok=True)
    filepath = f"outputs/{filename}"

    with open(filepath, "w") as f:
        json.dump(interview_data, f, indent=2)

    print(f"Interview data saved to {filepath}")
