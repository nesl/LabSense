local time = os.time()
sendToLabSense("MotionSensor", "128.97.93.90", 8000, 0, time)
sendToLabSense("MotionSensor", "128.97.93.90", 8000, 1, time + 1)

sendToLabSense("MotionSensor", "128.97.93.190", 8000, 0, time)
sendToLabSense("MotionSensor", "128.97.93.190", 8000, 1, time + 1)

luup.call_delay("fallingEdge", 3)
 
function fallingEdge()
    local time = os.time()
    sendToLabSense("MotionSensor", "128.97.93.90", 8000, 1, time)
    sendToLabSense("MotionSensor", "128.97.93.90", 8000, 0, time + 1)

    sendToLabSense("MotionSensor", "128.97.93.190", 8000, 1, time)
    sendToLabSense("MotionSensor", "128.97.93.190", 8000, 0, time + 1)
end

return True
