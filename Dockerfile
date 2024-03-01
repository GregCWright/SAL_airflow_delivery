# Base Image
FROM apache/airflow:2.8.2

# File Dependencies, requires `make setup` 
COPY requirements.txt /
COPY .env /
COPY rust /rust

# Rust Dependancies
USER root
RUN source /.env

# System Package Dependancies
RUN apt-get update \
  && apt-get install -y --no-install-recommends\
    build-essential\
    pkg-config\
    libssl-dev\
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Rust Dependancies
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Build SAL_extraction
RUN cargo build --manifest-path=/rust/Cargo.toml --release

# Install Python Packages
USER airflow
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
