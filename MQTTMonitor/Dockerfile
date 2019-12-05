FROM python:3.7.0

# 设置工作路径
RUN mkdir -p /usr/src/app
#  切换到工作路径
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

# 添加应用
ADD .  /usr/src/app

CMD [ "python","MQTT_Monitor.py"]
