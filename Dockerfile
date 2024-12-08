FROM python:3.10.12

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY . /app/  

# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt
# RUN apt-get update && apt-get install -y --no-install-recommends make=4.3-4 && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

CMD [ "python", "src/app.py" ]