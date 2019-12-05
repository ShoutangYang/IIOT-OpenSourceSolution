import  paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import datetime

def persists(topic,msg):
    current_time = datetime.datetime.utcnow().isoformat()
    json_body = [
        {
            "measurement": topic,
            "tags": {
                "host":"pi_1",
                "type":"ai"
                },
            "time": current_time,
            "fields": {
                "Float_value": int(msg.payload)
            }
        }
        
    ]
    print(json_body)
    print(influx_client.write_points(json_body))

# 用于响应服务器端 CONNACK 的 callback，如果连接正常建立，rc 值为 0
def on_connect(client, userdata, flags, rc):
    print("Connection returned with result code:" + str(rc))
    
    # result, mid = client.subscribe("Node2_Input_1", 0)
    # print(".........subscribe Node2_Input_1 "+str(result))
    # result, mid  = client.subscribe("Node2_Input_2",0)
    # result,mid = client.subscribe("Node2_Input_3",0)
    # result.mid = client.subscribe("Node2_Temperature",0)
    # result, mid = client.subscribe("Input_1", 0)
    # print("subscribe Input_1 "+str(result))
    # result, mid  = client.subscribe("Input_2",0)
    # result,mid = client.subscribe("Input_3",0)
    # result.mid = client.subscribe("Temperature",0)
    #订阅多个主题 
    result, mid = client.subscribe([("Input_1", 0),("Input_2",0),("Input_3",0),("Temperature",0),("Node2_Input_1",0),("Node2_Input_2",0),("Node2_Input3",0),("Node2_Temperature", 0)])
    print("subscribe items result is  "+str(result))

# 用于响应服务器端 PUBLISH 消息的 callback，打印消息主题和内容
def on_message(client, userdata, msg):
    print("Received message, topic:" + msg.topic + "payload:" + str(msg.payload))
    persists(msg.topic,msg)

# 在连接断开时的 callback，打印 result code
def on_disconnect(client, userdata, rc):
    print("Disconnection returned result:"+ str(rc))

influx_client = InfluxDBClient(host="150.168.1.76",port=8086,username='root',password='root',database="DB")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("150.168.1.76",1883,60)

client.loop_forever()