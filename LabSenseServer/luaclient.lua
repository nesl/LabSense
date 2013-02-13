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

function sendToLabSense(IP, PORT, data)
    local socket = require("socket")

    client = socket.connect(IP, PORT)

    client.send("HELLO")
