FROM python:3.12.0b3-slim@sha256:e5814ab91d853f9289ace149d6caab2e69073de926d5840928b2288602ced2e7 as build
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
	      build-essential gcc

WORKDIR .
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.12.0b3-slim@sha256:e5814ab91d853f9289ace149d6caab2e69073de926d5840928b2288602ced2e7
WORKDIR /venv
COPY --from=build /venv ./venv
COPY . .

ENV PATH="/venv/bin:$PATH"
CMD [ "python", "main.py" ]
