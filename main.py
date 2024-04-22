import os
import boto3
import json
import pandas as pd
from src.database import Database
from src.prompt_data import PromptData, AdmissionData, CalloutEvent, CalloutEvents, Prescription, Prescriptions, NoteEvent, NoteEvents

def get_note_summary(note_text):
    client = boto3.client(
        service_name="bedrock-runtime", region_name="us-east-1"
    )
    
    prompt = f"""
    Give a brief summary of the note text.

    {note_text}
    """

    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 50000,
                        "messages": [
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": prompt}],
                            }
                        ],
                    }
                ),
            )
    
    response_body = json.loads(response["body"].read())
    summary = response_body["content"][0]["text"]
    return summary

def collect_admission_data(target_admission, database):

    subject_id = target_admission.subject_id.values[0]
    admission_id = target_admission.hadm_id.values[0]

    # Admission
    admission_data = AdmissionData(
        admission_time = target_admission.admittime.values[0],
        admission_type = target_admission.admission_type.values[0],
        admission_location = target_admission.admission_location.values[0],
        insurance = target_admission.insurance.values[0],
        ethnicity = target_admission.ethnicity.values[0],
        diagnosis = target_admission.diagnosis.values[0],
        death_time = target_admission.deathtime.values[0],
        # deatch_occurred is if the deatch_time is not null
        death_occurred= not pd.isnull(target_admission.deathtime.values[0])
    )

    # Callouts
    callouts = database.get_callouts_by_admission(admission_id, subject_id)
    outcome_events = []
    for _, row in callouts.iterrows():
        outcome_events.append(CalloutEvent(
            callout_time = row.outcometime,
            callout_outcome = row.callout_outcome,
            callout_service = row.callout_service
        ))
    
    callout_events = CalloutEvents(outcome_events)

    # prescriptions
    prescriptions = database.get_prescriptions_by_admission(admission_id, subject_id)
    prescription_events = []
    for _, row in prescriptions.iterrows():
        prescription_events.append(Prescription(
            name = row.drug,
            prescription_strength = row.prod_strength,
            route = row.route,
            start_time = row.startdate,
            end_time = row.enddate
        ))

    prescriptions = Prescriptions(prescription_events)

    # notes
    note_data = database.get_discharge_note_events(admission_id, subject_id)
    note_events = []
    for _, row in note_data.iterrows():
        note_summary = get_note_summary(row.text)

        note_events.append(NoteEvent(
            note_time = row.charttime,
            note_summary = note_summary
        ))

    note_events = NoteEvents(note_events)


    prompt_data = PromptData(admission_data, callout_events, prescriptions, note_events)
 
    prompt = f"""
    Give a summary of the patient's admission. Give the explanation in a way that is understandable to a layperson.
    {prompt_data}
    """

    # get the summary
    client = boto3.client(
            service_name="bedrock-runtime", region_name="us-east-1"
        )
    
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 50000,
                        "messages": [
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": prompt}],
                            }
                        ],
                    }
                ),
            )
    
    response_body = json.loads(response["body"].read())
    summary = response_body["content"][0]["text"]
    print(summary)




def main():
    
    host = 'localhost'
    dbname = 'mimic'
    user = os.environ.get('MIMIC_USER') or 'postgres'
    password = os.environ.get('MIMIC_PASSWORD') or 'testing'

    
    database = Database(host, dbname, user, password)
    
    # get a list of possible admission
    admission = database.get_admissions()
    target_admission = admission.sample(1)



    collect_admission_data(target_admission, database)    



if __name__ == "__main__":

    main()    
