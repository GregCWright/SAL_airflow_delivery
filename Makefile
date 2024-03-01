update:
	rm -rf ./dbt
	rm -rf ./rust

	git clone https://github.com/GregorMonsonFD/SAL_dbt.git ./dbt
	git clone https://github.com/GregorMonsonFD/SAL_extraction.git ./rust

setup:
	rm .env
	rm -rf ./dbt
	rm -rf ./rust

	echo AIRFLOW_VERSION=2.8.2 >> .env

	git clone https://github.com/GregorMonsonFD/SAL_dbt.git ./dbt
	git clone https://github.com/GregorMonsonFD/SAL_extraction.git ./rust

start:
	docker-compose up

start-headless:
	docker-compose up -d

stop:
	docker-compose down