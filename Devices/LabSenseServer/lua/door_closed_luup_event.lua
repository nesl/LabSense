local time = os.time()
local api_key = "6h8z-vpjKTBYjnt62cRh-f8yZ96SAKxoOTJjWWJkUm9uYz0g"
local name = "NESL_DoorSensor"
sendToLabSense("DoorSensor", name, "128.97.93.90", 8000, 1, time, api_key)
sendToLabSense("DoorSensor", name, "128.97.93.90", 8000, 0, time + 1, api_key)
return True
