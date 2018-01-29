FROM amazonlinux
RUN yum -y upgrade
RUN yum install -y python27-pip
RUN yum install -y libgomp
RUN pip install mxnet
RUN pip install boto3

COPY src/part2_pred_script.py /tmp/part2_pred_script.py

#ENTRYPOINT ["python", "/tmp/part2_pred_script.py"]
