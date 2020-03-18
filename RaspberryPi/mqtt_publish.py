#-*-coding:utf-8-*-

# 导入 paho-mqtt 的 Client：
import paho.mqtt.client as mqtt

import time
import revpimodio2
unacked_sub = [] #未获得服务器响应的订阅消息 id 列表

# 用于响应服务器端 CONNACK 的 callback，如果连接正常建立，rc 值为 0
def on_connect(client, userdata, flags, rc):
    print("Connection returned with result code:" + str(rc))


# 用于响应服务器端 PUBLISH 消息的 callback，打印消息主题和内容
def on_message(client, userdata, msg):
    print("Received message, topic:" + msg.topic + "payload:" + str(msg.payload))

# 在连接断开时的 callback，打印 result code
def on_disconnect(client, userdata, rc):
    print("Disconnection returned result:"+ str(rc))

# 在订阅获得服务器响应后，从为响应列表中删除该消息 id
def on_subscribe(client, userdata, mid, granted_qos):
    unacked_sub.remove(mid)

if __name__ == "__main__":
    # 构造一个 Client 实例
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect= on_disconnect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    rpi = revpimodio2.RevPiModIO(autorefresh=True)
    rpi
    rpi.io.OutputValue_1.value=3500
    print("input 1 = "+str(rpi.io.InputValue_1.value))
    print(rpi.core.temperature)
    # 连接 broker
    # connect() 函数是阻塞的，在连接成功或失败后返回。如果想使用异步非阻塞方式，可以使用 connect_async() 函数。
    client.connect("47.100.113.117", 1883, 60)

    client.loop_start()

    # 订阅单个主题
    #result, mid = client.subscribe("hello", 0)
    #unacked_sub.append(mid)
    # 订阅多个主题
    #result, mid = client.subscribe([("temperature", 0), ("humidity", 0)])
    #unacked_sub.append(mid)

    while len(unacked_sub) != 0:
        time.sleep(1)

    client.publish("hello", payload = "Hello world!")
    #client.publish("Temperature", payload = "24.0")
    client.publish("humidity", payload = "65%")

    while True:
        re=client.publish("Node1_Input_1",payload=str(rpi.io.RTDValue_1.value))
        print(re)
        print("Node1_input 1  RTD = "+str(rpi.io.RTDValue_1.value))
        client.publish("Node1_Input_2",payload=str(rpi.io.InputValue_2.value))
        print("Node1_input 2 = "+str(rpi.io.InputValue_2.value))
        client.publish("Node1_Input_3",payload=str(rpi.io.InputValue_3.value))
        print("Node1_input 3 = "+str(rpi.io.InputValue_3.value))
        client.publish("Node1_Temperature",payload=str(rpi.core.temperature))
        print("Node1_Temperature = "+str(rpi.core.temperature))
        time.sleep(10)

    # 断开连接
    time.sleep(20) #等待消息处理结束
    client.loop_stop()
    client.disconnect()