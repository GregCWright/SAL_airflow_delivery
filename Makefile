update:
	rm -rf ./dbt
	rm -rf ./rust

	git clone https://github.com/GregorMonsonFD/SAL_dbt.git ./dbt
	git clone https://github.com/GregorMonsonFD/SAL_extraction.git ./rust

setup:
	rm -rf .env
	rm -rf ./dbt
	rm -rf ./rust

	echo AIRFLOW_VERSION=2.8.2 >> .env

	git clone https://github.com/GregorMonsonFD/SAL_dbt.git ./dbt
	git clone https://github.com/GregorMonsonFD/SAL_extraction.git ./rust

build-rust:
	cargo build --target x86_64-unknown-linux-gnu --manifest-path=rust/Cargo.toml --release

start:
	docker-compose up

start-headless:
	docker-compose up -d

stop:
	docker-compose down
