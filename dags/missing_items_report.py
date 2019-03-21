#!/usr/bin/env python
# encoding: utf-8

import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from porthole import BasicReport
from datetime import datetime, timedelta
from time import sleep

def runnit():
    report = BasicReport(
        report_title='Missing Items'
    )
    report.build_file()
    report.create_worksheet_from_query(sheet_name='Sheet1', query={'filename': 'missing_report'})
    report.subject = "Report: Missing Items"
    report.message = """Good morning,

Attached is a list of missing items.

Thanks!

Sincerely,

Reporting"""
    report.execute()
    return "success!"

args = {
    'owner': 'airflow',
    'start_date': datetime(2019, 3, 19),
    # 'email': ['<fill>'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
    'sla': timedelta(minutes=1)
}

dag = DAG(
    dag_id='missing_items',
    default_args=args,
    schedule_interval='*/15 * * * *',
)

def wait_too_long():
    sleep(120)
    return "that was a long nap"


run_this = PythonOperator(
    task_id='missing_items_task',
    python_callable=runnit,
    dag=dag,
    sla=timedelta(minutes=1)
)

run_long = PythonOperator(
    task_id='missing_items_timeout',
    python_callable=wait_too_long,
    dag=dag,
    sla=timedelta(minutes=1)
)

run_long >> run_this
# [END howto_operator_python]
