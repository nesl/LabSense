--function my_send_cosm (feed, datastream, value, at_ostime)
  --local apikey = "9-Ab1uilTBVH-xC0u_AhuDh5V7iSAKxjTzY0WW83VXlWST0g"
  --local base_url = "http://api.cosm.com/v2/feeds/"
  --local method = "PUT"

  --require('ltn12')
  --local socket = require("socket")
  --local http = require("socket.http")

  --local json_data = '{ "version":"1.0.0","datastreams":[ {"id":"' .. datastream .. '", "at":"' .. os.date("!%Y-%m-%dT%H:%M:%SZ",at_ostime) .. '", "current_value":"' .. value .. '"}]}'
  --local response_body = {}
  --local response, status, header = http.request{
    --method = method,
    --url = base_url .. feed,
    --headers = {
      --["Content-Type"] = "application/json",
      --["Content-Length"] = string.len(json_data),
      --["X-ApiKey"] = apikey
    --},
    --source = ltn12.source.string(json_data),
    --sink = ltn12.sink.table(response_body)
  --}
--end
function sendToLabSense(device, IP, PORT, value, timestamp)
    local socket = require("socket")

    client = socket.connect(IP, PORT)

    -- local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ", ostime)

    if device == "DoorSensor" then
        local json_data = '{ "device": "DoorSensor", "devicename": "NESL_DoorSensor", "channels": { "Door": { "units": "Open/Closed", "measurements": [ ["Door", ' .. value .. ']]}}, "timestamp": ' .. timestamp .. '}'
    elseif device == "Motion" then
        local json_data = '{ "device": "MotionSensor", "devicename": "NESL_MotionSensor", "channels": { "Motion": { "units": "Motion/No Motion", "measurements": [ ["Motion", ' .. value .. ']]}}, "timestamp": ' .. timestamp .. '}'
    end

    client:send(json_data)
end
