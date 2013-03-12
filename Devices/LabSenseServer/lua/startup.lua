function sendToLabSense(device, devicename, IP, PORT, value, timestamp, api_key)
    local socket = require("socket")

    client = socket.connect(IP, PORT)

    local json_data = ""
    if device == "DoorSensor" then
        json_data = '{ "API_KEY": "' .. api_key .. '", "data": {"devicename": "' .. devicename .. '", "channels": { "Door": { "units": "Open/Closed", "measurements": [ ["Door", ' .. value .. ']]}}, "timestamp": ' .. timestamp .. '}}'
    elseif device == "MotionSensor" then
        json_data = '{ "API_KEY": "' .. api_key .. '", "data": {"devicename": "NESL_MotionSensor", "channels": { "Motion": { "units": "Motion/No Motion", "measurements": [ ["Motion", ' .. value .. ']]}}, "timestamp": ' .. timestamp .. '}}'
    end

    client:send(json_data)
end
