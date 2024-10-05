FROM python:3.12.4
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ENV HOME /news-crawler-app

WORKDIR $HOME


ENV REQUIREMENTS $HOME/requirements
RUN mkdir REQUIREMENTS
COPY ./requirements REQUIREMENTS
RUN pip install --upgrade pip
RUN pip install -r REQUIREMENTS/prod.txt


COPY ./src $HOME

# Copy the start script and change rights
COPY ./compose/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh