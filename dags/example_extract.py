import pendulum
import subprocess
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.hooks.base import BaseHook

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task

def execute_rust_binary(arguments, executable_location):
    print(f"Executing binary at {executable_location}")
    try:
        subprocess.check_call(f"{executable_location} {arguments}", shell=True)
    except subprocess.CalledProcessError as e:
        print("Error executing binary")
        print(e)
        exit(1)
    print(f"Executed binary at {executable_location} with {arguments}")

with DAG(
    dag_id="example_extract",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    create_target_dir = BashOperator(
        task_id="create_target_dir"
        , bash_command="mkdir -p /csv"
        , append_env=True
    )

    function = "TIME_SERIES_DAILY"
    symbol = "IBM"
    api_key = Variable.get("alphavantage_api_key")
    output = "/csv"

    execute_alphavantage = PythonOperator(
        task_id="execute_alphavantage",
        python_callable=execute_rust_binary,
        trigger_rule="all_success",
        provide_context=True,
        op_kwargs={
            "executable_location": "/bin/rust_apps/alphavantage_extractor",
            "arguments": f"-f {function} -s {symbol} -a {api_key} -o {output}"
        }
    )

    list_target_dir = BashOperator(
        task_id="list_target_dir"
        , bash_command="ls -a /csv"
        , append_env=True
    )

    sal_connection = BaseHook.get_connection("sal_dbt_postgres")
    username = sal_connection.login
    password = sal_connection.password
    host = sal_connection.host
    input_directory = output


    execute_csv_insert = PythonOperator(
        task_id="execute_csv_insert",
        python_callable=execute_rust_binary,
        trigger_rule="all_success",
        provide_context=True,
        op_kwargs={
            "executable_location": "/bin/rust_apps/csv_insertion_handler",
            "arguments": f"-u {username} -p {password} --host {host} -i {input_directory}"
        }
    )
    
    create_target_dir >> execute_alphavantage >> list_target_dir >> execute_csv_insert
