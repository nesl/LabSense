local time = os.time()
sendToLabSense("DoorSensor", "128.97.93.90", 8000, 0, time)
sendToLabSense("DoorSensor", "128.97.93.90", 8000, 1, time + 1)
sendToLabSense("DoorSensor", "128.97.93.190", 8000, 0, time)
sendToLabSense("DoorSensor", "128.97.93.190", 8000, 1, time + 1)
return True
