FROM python:2.7

RUN mkdir -p /app
WORKDIR /app
VOLUME ["/app/gremlins/profiles"]

ADD gremlins /app/gremlins
ADD setup.py /app/setup.py
RUN python setup.py develop

ADD entrypoint.sh /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gremlins","-m","gremlins.profiles.entropy","-p","entropy.profile"]
