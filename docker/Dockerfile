FROM ubuntu:18.04

ENV PYTHON_TGZ_URL https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz

COPY sources.list /etc/apt/sources.list
COPY localtime /etc/localtime

RUN set -x \
    && apt-get update \
    && apt-get install curl gcc python-dev make zlib1g-dev libbz2-dev libssl-dev libmysqlclient-dev -y \
    && curl -fSL "$PYTHON_TGZ_URL" -o python.tar.gz \
    && mkdir -p /usr/local/python \
	&& apt-get install tar -y \
    && tar -xvf python.tar.gz --strip-components=1 \
    && ./configure --prefix=/usr/local/python \
    && make \
    && make install \
    && ls /usr/local/python/bin \
    && rm -rf /usr/bin/python* /usr/bin/pip* \
	&& ln -s /usr/local/python/bin/python3 /bin/python \
    && ln -s /usr/local/python/bin/pip3 /bin/pip \
    && chmod 755 /bin/pip \
    && chmod 755 /bin/python \
	&& python -V \
    && echo 'Asia/Shanghai' /etc/timezone \
    && date

EXPOSE 8000
CMD ["python", "-V"]