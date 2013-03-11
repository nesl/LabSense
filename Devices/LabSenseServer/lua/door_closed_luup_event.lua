local time = os.time()
local api_key = "6h8z-vpjKTBYjnt62cRh-f8yZ96SAKxoOTJjWWJkUm9uYz0g"
sendToLabSense("DoorSensor", "128.97.93.90", 8000, 1, time, api_key)
sendToLabSense("DoorSensor", "128.97.93.90", 8000, 0, time + 1, api_key)
sendToLabSense("DoorSensor", "128.97.93.190", 8000, 1, time, api_key)
sendToLabSense("DoorSensor", "128.97.93.190", 8000, 0, time + 1, api_key)
return True
