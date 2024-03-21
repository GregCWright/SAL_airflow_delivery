import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task

with DAG(
    dag_id="example_bash",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    say_hello_and_create_a_secret_number = BashOperator(
        task_id="alphavantage"
        #, bash_command=". /opt/airflow/rust/alphavantage_extractor -f $FUNCTION -s $SYMBOL"
        , bash_command='cargo build --manifest-path=/opt/airflow/Cargo.toml --release'
        , env={"FUNCTION": "TIME_SERIES_DAILY", "SYMBOL": "IBM"}
        , append_env=True
    )