# AI in Healthcare - LLM Assignment

This project is intended to be the code for the AI in Healthcare - LLM Assignment

## Objective

The objective of this project to generate a readable overview of the care during an admission for the patient.
The output should be clear and understandable to the patient or the patient's care taker.

The project relies on the use of Claude 3 - Haiku. We access this model through the AWS Console.

In order to get a good overview, we use chain of thought prompting to summarize the note events before gathering the data for a final summary.

## Data overview

We use the following data within the prompt to 

**Admission Data**

<admission_time>
<death_time>
<death_occured>
<admission_type>
<admission_location>
<insurance>
<ethnicity>
<diagnosis>


**Callout**
<callout_time>
<callout_outcome>
<callout_service>

**Prescription**
<name>
<prescription_strength>
<route>
<start_time>
<end_time>

**Notes**
Currently we only use the discharge summary.
Before adding the note text to the data. We generate a summary of the note using the LLM Model.
<note_time>
<note_summary>


# Running

In order to run the script, you must first have AWS credentials that relates to an an AWS account with access to Claude 3 - Haiku.
You should set us the credentials with the AWS Cli tool.

You should also have the MIMIC III dataset setup with a local postgres database. We used docker to set this up locally.

Then run the following:

```
python main.py
```

This will choose a random admission from the first 1000 admission in the database. It will then print the resulting summary.





