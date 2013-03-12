function risingEdge()
    local time = os.time()
    local api_key = "6h8z-vpjKTBYjnt62cRh-f8yZ96SAKxoOTJjWWJkUm9uYz0g"
    local name = "NESL_MotionSensor"
    sendToLabSense("MotionSensor", name, "128.97.93.90", 8000, 0, time, api_key)
    sendToLabSense("MotionSensor", name, "128.97.93.90", 8000, 1, time + 1, api_key)
end
 
function fallingEdge()
    local time = os.time()
    local api_key = "6h8z-vpjKTBYjnt62cRh-f8yZ96SAKxoOTJjWWJkUm9uYz0g"
    local name = "NESL_MotionSensor"
    sendToLabSense("MotionSensor", name, "128.97.93.90", 8000, 1, time, api_key)
    sendToLabSense("MotionSensor", name, "128.97.93.90", 8000, 0, time + 1, api_key)

end

risingEdge()
luup.call_delay("fallingEdge", 3)

return True
