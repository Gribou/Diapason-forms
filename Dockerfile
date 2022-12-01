ARG GITLAB_DEPENDENCY_PROXY=""
# improve build time by pulling images from gitlab and not dockerhub

# React production files builder
FROM node:14 AS front-builder
# reduce image size by not having react dependencies in final image

ARG PROJECT_DIR=/app/
ARG ASSETS_DIR=/app/web/

ENV BUILD_TARGET_FOLDER=/app/api

WORKDIR $ASSETS_DIR

COPY ./web/package.json ./web/package-lock.json ./
RUN npm install --omit=optional --no-audit

COPY ./web ./

RUN mkdir -p $BUILD_TARGET_FOLDER
COPY ./scripts ../scripts

RUN rm -f .env*.local && npm run build

#------------------------------------------------------------------
#FROM python:3.9-slim as back-builder
FROM  registry.fedoraproject.org/f33/python3 as back-builder
# reduce image size by having only the required python dependencies in final image

ENV PIPENV_VENV_IN_PROJECT=1
ENV PATH="/app/api/.venv/bin:$PATH"

WORKDIR /app/api

RUN pip install -U pip pipenv
COPY ./api/Pipfile ./api/Pipfile.lock ./
RUN pipenv install

#------------------------------------------------------------------
#FROM python:3.9-slim as final
FROM  registry.fedoraproject.org/f33/python3 as back-builder
ARG HTTPS_PROXY=
ARG HTTP_PROXY=
ARG FTP_PROXY=
ARG NO_PROXY="localhost,127.0.0.1"
ARG VERSION_TAG="?"

ENV https_proxy=$HTTPS_PROXY
ENV http_proxy=$HTTP_PROXY
ENV ftp_proxy=$FTP_PROXY
ENV no_proxy=$NO_PROXY

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT=1
ENV PATH="/app/api/.venv/bin:$PATH"

WORKDIR /app/api

COPY ./scripts /app/scripts
RUN chmod +x /app/scripts/*.sh

# Copy the current directory contents into the container
COPY ./api ./
RUN chmod 0744 ./manage.py

# Copy built react files from builder into this container
COPY --from=front-builder /app/api/static_web /app/api/static_web
COPY --from=front-builder /app/api/templates_web /app/api/templates_web

# Copy Python dependencies from back-builder into this container
COPY --from=back-builder /app/api/.venv /app/api/.venv

# write version number in backend filetree to make it visible to django
RUN echo "__version__ = '${VERSION_TAG}'" >> /app/api/efneproject/version.py

RUN python manage.py collectstatic --noinput

# Additional dependencies (for weasyprint) + rsync for backups
#RUN apt-get update \
#  && apt-get install -y rsync curl \
#  python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 \
#  && apt-get clean autoclean && apt-get autoremove --yes --purge \
#  && rm -rf /var/lib/{apt,dpkg,cache,log}/

EXPOSE 8000

ENTRYPOINT /bin/bash /app/scripts/entrypoint.sh
