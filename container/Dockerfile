FROM --platform=linux/amd64 amazonlinux:2

RUN yum check-update
RUN yum install -y amazon-linux-extras
RUN amazon-linux-extras install python3.8
RUN ln -s /usr/bin/python3.8 /usr/bin/python3
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install \
    mlflow==2.0.1 \
    pymysql==1.0.2 \
    boto3
RUN mkdir /mlflow/

EXPOSE 5000

CMD mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --default-artifact-root ${BUCKET} \
    --backend-store-uri mysql+pymysql://${USERNAME}:${PASSWORD}@${HOST}:${PORT}/${DATABASE}
