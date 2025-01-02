# Base Images
FROM rust as builder
WORKDIR /app
COPY rust /app
RUN cargo build --release

FROM apache/airflow:2.8.2

# File Dependencies, requires `make setup` 
COPY .env_conn /
COPY requirements.txt /

# Rust Dependencies
USER root
RUN source /.env_conn

# System Package Dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends\
    build-essential\
    pkg-config\
    libssl-dev\
    rustc\
    libpq-dev\
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python Packages
USER airflow
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

#Copy over compiled rust binaries
COPY --from=builder /app/target/release/alphavantage_extractor /bin/rust_apps/
COPY --from=builder /app/target/release/csv_insertion_handler /bin/rust_apps/

COPY ./dbt /bin/dbt
COPY profiles.yml /bin/dbt_profiles/profiles.yml