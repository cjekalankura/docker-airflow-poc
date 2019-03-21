import airflow  
from builtins import range  
from airflow.operators.bash_operator import BashOperator  
from airflow.operators.dummy_operator import DummyOperator  
from airflow.operators.postgres_operator import PostgresOperator  
from airflow.operators.python_operator import PythonOperator  
from airflow.models import DAG  
from datetime import timedelta  
from pprint import pprint


args = {  
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1)
}

dag = DAG(dag_id='tutorial_nolan_sql',default_args=args,  
    schedule_interval=None)

def print_context(ds, **kwargs):  
    pprint(kwargs)
    print(ds)
    return 'Whatever you return gets printed in the logs'

run_this = PythonOperator(  
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag)

t1 = PostgresOperator(task_id='nolan_playing_with_sql', sql="INSERT INTO dev.test VALUES (42, 'nolan', FALSE);", postgres_conn_id='my_postgres', autocommit=True, database="dev",dag=dag)

run_this.set_downstream(t1)
