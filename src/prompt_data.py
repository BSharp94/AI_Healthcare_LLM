

class AdmissionData:
    def __init__(self, 
        admission_time,
        admission_type,
        admission_location,
        insurance,
        ethnicity,
        diagnosis,
        death_time,
        death_occurred):

        self.admission_time = admission_time
        self.admission_type = admission_type
        self.admission_location = admission_location
        self.insurance = insurance
        self.ethnicity = ethnicity
        self.diagnosis = diagnosis
        self.death_time = death_time
        self.death_occurred = death_occurred

    # Returns the data as an XML string    
    def __str__(self):
        return f"""
        <admission>
            <admission_time>{self.admission_time}</admission_time>
            <admission_type>{self.admission_type}</admission_type>
            <admission_location>{self.admission_location}</admission_location>
            <insurance>{self.insurance}</insurance>
            <ethnicity>{self.ethnicity}</ethnicity>
            <diagnosis>{self.diagnosis}</diagnosis>
            <death_time>{self.death_time}</deatch_time>
            <death_occurred>{self.death_occurred}</death_occurred>
        </admission>
        """

class CalloutEvent:
    def __init__(self,
        callout_time,
        callout_outcome,
        callout_service,
        ):
        self.callout_time = callout_time
        self.callout_outcome = callout_outcome
        self.callout_service = callout_service

    # Returns the data as an XML string
    def __str__(self):
        return f"""
        <callout>
            <callout_time>{self.callout_time}</callout_time>
            <callout_outcome>{self.callout_outcome}</callout_outcome>
            <callout_service>{self.callout_service}</callout_service>
        </outcome>
        """
    

class CalloutEvents:
    def __init__(self, callout_events):
        self.callout_events = callout_events

    # Returns the data as an XML string
    def __str__(self):
        callout_strings = [str(callout) for callout in self.callout_events]
        return f"""
        <callouts>
            {"\n".join(callout_strings)}
        </callouts>
        """

class Prescription:
    def __init__(self,
        name,
        prescription_strength,
        route,
        start_time,
        end_time):
        self.name = name
        self.prescription_strength = prescription_strength
        self.route = route
        self.start_time = start_time
        self.end_time = end_time
        
    # Returns the data as an XML string
    def __str__(self):
        return f"""
        <prescription>
            <name>{self.name}</name>
            <prescription_strength>{self.prescription_strength}</prescription_strength>
            <route>{self.route}</route>
            <start_time>{self.start_time}</start_time>
            <end_time>{self.end_time}</end_time>
        </prescription>
        """

class Prescriptions:

    def __init__(self, prescription_events):
        self.prescription_events = prescription_events

    # Returns the data as an XML string
    def __str__(self):
        prescription_strings = [str(prescription) for prescription in self.prescription_events]
        return f"""
        <prescriptions>
            {"\n".join(prescription_strings)}
        </prescriptions>
        """


class NoteEvent:
    def __init__(self, note_time, note_summary):
        self.note_time = note_time
        self.note_summary = note_summary

    # Returns the data as an XML string
    def __str__(self):
        return f"""
        <note>
            <note_time>{self.note_time}</note_time>
            <note_summary>{self.note_summary}</note_summary>
        </note>
        """
    
class NoteEvents:
    def __init__(self, note_events):
        self.note_events = note_events

    # Returns the data as an XML string
    def __str__(self):
        note_strings = [str(note) for note in self.note_events]
        return f"""
        <notes>
            {"\n".join(note_strings)}
        </notes>
        """
    

class PromptData:

    def __init__(self, admission_data, callout_events, prescription_events, note_events):
        self.admission_data = admission_data
        self.callout_events = callout_events
        self.prescription_events = prescription_events
        self.note_events = note_events

    # Returns the data as an XML string
    def __str__(self):
        return f"""
        <data>
            {self.admission_data}
            {self.callout_events}
            {self.prescription_events}
            {self.note_events}
        </data>
        """
    