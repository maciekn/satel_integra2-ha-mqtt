
import asyncio
import logging
import os
import json

from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo

from satel_integra2.satel_integra import AsyncSatel, AlarmState


logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()

configJson = json.loads(os.environ["MONITORING"])


device_info = DeviceInfo(name="Satel Integra ETHM custom",
                         identifiers="satel_integra_ethm_custom")
mqtt_settings = Settings.MQTT(host=os.environ["MQTT_HOST"])

outsensors = {}

for sensorId in configJson["outs"]:
    sensor_info = BinarySensorInfo(
        name="Satel Out "+str(sensorId), device_class="motion",
        unique_id="satel.integra.out_"+str(sensorId),
        device=device_info
    )

    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    outsensors[sensorId] = BinarySensor(settings)


zonesensors = {}
for zoneID in configJson["zones"]:
    sensor_info = BinarySensorInfo(
        name="Satel Zone "+str(zoneID), device_class="safety",
        unique_id="satel.integra.zone_"+str(zoneID),
        device=device_info
    )

    settings = Settings(mqtt=mqtt_settings, entity=sensor_info)
    zonesensors[zoneID] = BinarySensor(settings)

def outputChanged(status):
    for sensor in status['outputs']:
        outsensors[sensor].update_state(status['outputs'][sensor] == 1)


def alarmStatus(states):
    for sensor in zonesensors:
        zonesensors[sensor].update_state(sensor not in states[AlarmState.ARMED_MODE0])


stl = AsyncSatel(os.environ["ETHM_HOST"],
                 os.environ["ETHM_PORT"],
                 loop,
                 [],
                 configJson["outs"],
                 )


loop.run_until_complete(stl.connect())
loop.create_task(stl.keep_alive())
loop.create_task(stl.monitor_status(output_changed_callback=outputChanged,
                alarm_status_callback=alarmStatus,
                 monitoring_query=b'\x7F\x00\x04\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00'))

loop.run_forever()
loop.close()
