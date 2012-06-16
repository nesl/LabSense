{% extends "generic_channel.html" %}

{% block socketio %}

    var socket;

    var Sensor = Backbone.Model.extend({
        set: function(values) {

            if(values.multiple == "0") {
                if(JSON.stringify(values) === "{}")
                    return;
                data = values.data;
                name = values.name;

                if(name == undefined){
                    console.log("UNDEFINED");
                    return;
                }

                channel_measurement_id = name.split("_");

                console.log("Channel: "+ channel_measurement_id[0]);
                console.log("Measurement: " + channel_measurement_id[1]);
                console.log("Id: "+ channel_measurement_id[2]);

                channel = channel_measurement_id[0];
                measurement = channel_measurement_id[1];
                sensor_number = parseInt(channel_measurement_id[2]);

                if(channel_measurement_id.length == 3) {

                    if(typeof(data) == "string") {
                        data = eval(data);
                    }

                    console.log("DATA: " + data);

                    if(chart_channel == channel && chart_measurement == measurement && sensor_number == chart_sensor_number) {

                        console.log("CHART CHANNEL: " + chart_channel);
                        console.log("CHART MEASURMENT: " + chart_measurement);
                        console.log("CHART_SENSOR_NUMBER: " + chart_sensor_number);

                        // Matches graph name and number, so graph
                        timestamp = new Date(parseFloat(values["timestamp"])) 
                        utc = Date.UTC(timestamp.getFullYear(), timestamp.getMonth(), 
                                       timestamp.getDay(), timestamp.getHours(), timestamp.getMinutes(), 
                                       timestamp.getSeconds());
                        chart1.series[0].addPoint([utc,  parseFloat(data[0])]);

                    }

                    //console.log(value + ": " + data[value]);
                    console.log("#" + measurement + "-table");
                    $("#" + measurement + "-table > td.sensor_table_class").eq(sensor_number).html(data[0]);
                    //counter += 1;
                    //};
                }
                else {
                    console.log("Length: " + channel_measurement_id.length);

                    console.log("Problem: Received more data than expected");
                }
            }
            else {
                console.log("RECEIVED BULK MSG");
                name = values.name;
                timestamp = values.timestamp;
                multiple = values.multiple;

                console.log("Names: "+  name);
                console.log("Timestamp: " + timestamp)
                console.log("DATA: " + values.data);

                console.log("TYPE: " + typeof(values.data));
                if(typeof(values.data) == "string") {
                    values.data = eval(values.data);
                }

                console.log("VALUES DATA: " + values.data);

                data_counter = 1;
                for(data_val in values.data) {
                    data = values.data[data_val]

                    console.log("DATA : " + data);

                    if(JSON.stringify(values) === "{}")
                        return;

                    if(name == undefined){
                        console.log("UNDEFINED");
                        return;
                    }


                    channel_measurement_id = name.split("_");

                    //console.log("name: "+ name);
                    //console.log("Channel: "+ channel_measurement_id[0]);
                    //console.log("Measurement: " + channel_measurement_id[1]);
                    //console.log("Id: "+ channel_measurement_id[2]);
                    //console.log("Multiple: " + multiple)

                    channel = channel_measurement_id[0];
                    measurement = channel_measurement_id[1];
                    sensor_number = channel_measurement_id[2];

                    if(chart_channel == channel && chart_measurement == measurement && data_counter == chart_sensor_number) {
                            console.log("Chart_ChanneL: " + chart_channel);
                            console.log("measurement: " + measurement);
                            // Matches graph name and number, so graph
                            timestamp = new Date(parseFloat(timestamp));
                            utc = Date.UTC(timestamp.getFullYear(), timestamp.getMonth(), 
                                           timestamp.getDay(), timestamp.getHours(), timestamp.getMinutes(), 
                                           timestamp.getSeconds());
                            chart1.series[0].addPoint([utc,  parseFloat(data)]);

                        }

                        //console.log(value + ": " + data[value]);
                        $("#" + measurement + "-table > td.sensor_table_class").eq((data_counter)).html(data);
                    data_counter += 1;
                };
            }

        }
    });

    var Sensors = new Sensor();

    var connected = function() {
        chart_name = chart_channel + "_" + chart_measurement + "_" + chart_sensor_number;
        console.log("Connected");
        socket.send({action: "init", channel: window.channel, name: chart_name });
    };

    var disconnected = function() {
        setTimeout(start, 1000);
    };

    var messaged = function(data) {
        Sensors.set(data);
        socket.send({action: "done"});
    };

    var start = function() {
        socket = new io.Socket(window.location.hostname, {
            port: 8001,
            rememberTransport: false,
            transports: [
            'websocket',
            'flashsocket',
            'xhr-multipart',
            'xhr-polling'
            ]
        });
        socket.connect();
        socket.on('connect', connected);
        socket.on('disconnect', disconnected);
        socket.on('message', messaged);
    };

    start();

{% endblock %}
