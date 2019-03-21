#!/usr/bin/env python
# encoding: utf-8

import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from porthole import BasicReport

def runnit():
    report = BasicReport(
        report_title='Subfolder Nested DAG'
    )
    report.build_file()
    report.create_worksheet_from_query(sheet_name='Sheet1', query={'filename': 'missing_items'})
    report.subject = "Report: Missing Items"
    report.message = """Good morning,

Attached is a list of missing items.

Thanks!

Sincerely,

report"""
    report.execute()
    return "success!"

args = {
    'owner': 'airflow',
    'start_date': '2019-03-19',
}

dag = DAG(
    dag_id='subf_nested_report',
    default_args=args,
    schedule_interval=None,
)

run_this = PythonOperator(
    task_id='subf_nested_report_item',
    python_callable=runnit,
    dag=dag,
)
# [END howto_operator_python]
