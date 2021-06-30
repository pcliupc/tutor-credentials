FROM docker.io/ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
  apt install -y curl git-core language-pack-en gettext python3 python3-pip python3-venv \
  build-essential libffi-dev libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev libssl-dev
ENV LC_ALL en_US.UTF-8

ARG CREDENTIALS_REPOSITORY=https://github.com/edx/credentials.git
ARG CREDENTIALS_VERSION={{ OPENEDX_COMMON_VERSION }}
RUN mkdir -p /openedx/credentials && \
    git clone $CREDENTIALS_REPOSITORY --branch $CREDENTIALS_VERSION --depth 1 /openedx/credentials
WORKDIR /openedx/credentials

# Setup empty yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV CREDENTIALS_CFG /openedx/config.yml

# Install python venv
RUN python3 -m venv ../venv/
ENV PATH "/openedx/venv/bin:$PATH"
RUN pip install setuptools==44.1.0 pip==20.0.2 wheel==0.34.2

# Install a recent version of nodejs
RUN pip install nodeenv
RUN nodeenv /openedx/nodeenv --node=12.13.0 --prebuilt
ENV PATH /openedx/nodeenv/bin:${PATH}

# Install python and nodejs requirements
# This is identical to "make production-requirements" but it was split in multiple
# instructions to benefit from docker image caching
RUN pip install -r requirements.txt
ARG NPM_REGISTRY=https://registry.npmjs.org/
RUN npm install --verbose --registry=$NPM_REGISTRY

# Install django-redis for using redis as a django cache
RUN pip install django-redis==4.12.1

# Install uwsgi
RUN pip install uwsgi==2.0.19.1

# Use fira credentials themes
RUN git clone https://github.com/edx/credentials-themes.git ../credentials-themes
RUN pip install -e ../credentials-themes

# Collect static assets
COPY assets.py ./credentials/settings/assets.py
ENV DJANGO_SETTINGS_MODULE credentials.settings.assets
RUN make static

EXPOSE 8000
CMD uwsgi \
    --static-map /static=/openedx/credentials/credentials/assets \
    --static-map /media=/openedx/credentials/credentials/media \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=2 \
    --wsgi-file credentials/wsgi.py
