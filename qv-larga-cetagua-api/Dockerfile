FROM  python:3.11

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gdal-bin libgdal-dev g++ \
    && pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt
EXPOSE 8001 

COPY ./ ./

RUN ["chmod","+x","./entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]



