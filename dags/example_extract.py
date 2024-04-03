import pendulum
import subprocess
from airflow.operators.python import PythonOperator
from airflow.models import Variable

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
        , bash_command="mkdir -p /tmp/csv_output/"
        , append_env=True
    )

    function = "TIME_SERIES_DAILY"
    symbol = "IBM"
    api_key = Variable.get("alphavantage_api_key")
    output = "/tmp/csv_output/"

    execute_rust_binary = \
        PythonOperator(
                task_id="execute_rust_binary",
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
        , bash_command="ls -a /tmp/csv_output/"
        , append_env=True
    )
    
    create_target_dir >> execute_rust_binary >> list_target_dir
