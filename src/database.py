import psycopg2
import pandas as pd

class Database:
    def __init__(self, host, dbname, user, password):
        self.host = host 
        self.dbname = dbname 
        self.user = user 
        self.password = password 

        self.connect()

    def connect(self):
        conn_string = f"host='{self.host}' dbname='{self.dbname}' user='{self.user}' password='{self.password}'"
        self.conn = psycopg2.connect(conn_string)

    def query(self, sql):
        return pd.read_sql_query(sql, con = self.conn)

    def get_admissions(self, top_n=2000):
        sql = f"""
        SELECT *
        FROM mimiciii.admissions
        LIMIT {top_n};
        """
        return self.query(sql)

    def get_callouts_by_admission(self, admission_id, subject_id):
        sql = f"""
        SELECT *
        FROM mimiciii.callout
        WHERE hadm_id = {admission_id}
        AND subject_id = {subject_id};
        """
        return self.query(sql)

    def get_prescriptions_by_admission(self, admission_id, subject_id):
        sql = f"""
        SELECT *
        FROM mimiciii.prescriptions
        WHERE hadm_id = {admission_id}
        AND subject_id = {subject_id};
        """
        return self.query(sql)

    def get_discharge_note_events(self, admission_id, subject_id):
        sql = f"""
        SELECT *
        FROM mimiciii.noteevents
        WHERE hadm_id = {admission_id}
        AND subject_id = {subject_id}
        AND category = 'Discharge summary';
        """
        return self.query(sql)



    def close(self):
        self.conn.close()
