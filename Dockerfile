FROM alpine:latest

EXPOSE 3031

RUN apk add --no-cache \
        uwsgi-python \
        python

RUN python -m ensurepip
RUN pip install --upgrade pip

RUN apk update \
  && apk add --virtual build-deps gcc python-dev musl-dev \
  && apk add postgresql-dev jpeg-dev zlib-dev lcms2-dev openjpeg-dev \
  && pip install psycopg2 Pillow \
&& apk del build-deps

COPY app /app
WORKDIR /app
RUN python -m pip install --no-cache-dir -r require.pip
RUN mv erofeimarkov/settings_prod.py erofeimarkov/settings.py

RUN apk add nodejs git
COPY frontend /frontend
WORKDIR /frontend
RUN npm install bower brunch
RUN npm install
RUN ./node_modules/.bin/bower install --allow-root
RUN ./node_modules/.bin/brunch build
RUN sed -i -e 's/images\/ui-/..\/images\/ui-/g' ../app/static/stylesheets/style.css

RUN apk del nodejs git

# stubs for database, so we can run manage.py
ENV DATABASE_HOST 127.0.0.1
ENV DATABASE_NAME postgres
ENV DATABASE_USERNAME postgres
ENV DATABASE_PASSWORD password

WORKDIR /app
RUN python manage.py collectstatic --noinput
RUN rm -rf /frontend

CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
               "--uid", "uwsgi", \
               "--plugins", "python", \
               "--protocol", "uwsgi", \
               "--wsgi", "erofeimarkov.wsgi:application" ]