import paho.mqtt.client as mqtt
from client import MQTT_Client_1
from state import Quiz, S1, S2, S3, t0, t1, t2, t3, t4

broker, port = "mqtt20.iik.ntnu.no", 1883

tick = Quiz()
tick_tock_machine = Quiz(transitions=[t0, t1, t2, t3, t4], states=[S1, S2, S3], obj=tick, name="tick_tock")
tick.stm = tick_tock_machine

driver = Driver()
driver.add_machine(tick_tock_machine)

myclient = MQTT_Client_1()
tick.mqtt_client = myclient.client
myclient.stm_driver = driver

driver.start()
myclient.start(broker, port)