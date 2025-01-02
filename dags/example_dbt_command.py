import pendulum
import subprocess
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.hooks.base import BaseHook

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task

with DAG(
    dag_id="example_dbt",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    
    execute_dbt = BashOperator(
        task_id="execute_dbt"
        # , bash_command="dbt run -s +dim_time_series_daily"
        , bash_command="dbt debug --profiles-dir /bin/dbt_profiles/"
        , append_env=True
    )
    
    execute_dbt
