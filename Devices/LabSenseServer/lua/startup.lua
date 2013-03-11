function sendToLabSense(device, IP, PORT, value, timestamp)
    local socket = require("socket")

    client = socket.connect(IP, PORT)

    local api_key = "6h8z-vpjKTBYjnt62cRh-f8yZ96SAKxoOTJjWWJkUm9uYz0g"

    local json_data = ""
    if device == "DoorSensor" then
        json_data = '{ "API_KEY": "' .. api_key .. '", "data": {"devicename": "NESL_DoorSensor", "channels": { "Door": { "units": "Open/Closed", "measurements": [ ["Door", ' .. value .. ']]}}, "timestamp": ' .. timestamp .. '}}'
    elseif device == "MotionSensor" then
        json_data = '{ "API_KEY": "' .. api_key .. '", "data": {"devicename": "NESL_MotionSensor", "channels": { "Motion": { "units": "Motion/No Motion", "measurements": [ ["Motion", ' .. value .. ']]}}, "timestamp": ' .. timestamp .. '}}'
    end

    client:send(json_data)
end
