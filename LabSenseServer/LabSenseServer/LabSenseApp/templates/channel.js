{% extends "generic_channel.html" %}

{% block socketio %}

    var socket;

    var Sensor = Backbone.Model.extend({
        set: function(values) {

            //if(values === undefined || values === {}) 
            if(JSON.stringify(values) === "{}")
                return;
            data = values.data;
            name = values.name;

            if(name == undefined){
                console.log("UNDEFINED");
                return;
            }

            console.log("name: "+ name);

            channel_measurement_id = name.split("_");


            console.log("Channel: "+ channel_measurement_id[0]);
            console.log("Measurement: " + channel_measurement_id[1]);
            console.log("Id: "+ channel_measurement_id[2]);
            channel = channel_measurement_id[0];
            measurement = channel_measurement_id[1];
            sensor_number = channel_measurement_id[2];

            if(channel_measurement_id.length == 2) {

                counter = 1;
                for(value in data) {
                    if(chart_channel == "") {
                        console.log("Chart channel is null");
                        changeChart(channel, measurement, counter);

                        // Matches graph name, so graph
                        timestamp = new Date(parseFloat(values["timestamp"])) 
                        utc = Date.UTC(timestamp.getFullYear(), timestamp.getMonth(), 
                                       timestamp.getDay(), timestamp.getHours(), timestamp.getMinutes(), 
                                       timestamp.getSeconds());
                        chart1.series[0].addPoint([utc,  parseFloat(data[0])]);
                    }
                    else if(chart_channel == channel && chart_measurement == measurement && counter == chart_sensor_number) {
                        console.log("Chart_ChanneL: " + chart_channel);
                        console.log("measurement: " + measurement);
                        // Matches graph name and number, so graph
                        timestamp = new Date(parseFloat(values["timestamp"])) 
                        utc = Date.UTC(timestamp.getFullYear(), timestamp.getMonth(), 
                                       timestamp.getDay(), timestamp.getHours(), timestamp.getMinutes(), 
                                       timestamp.getSeconds());
                        chart1.series[0].addPoint([utc,  parseFloat(data[counter-1])]);

                    }

                    console.log(value + ": " + data[value]);
                    $("#" + measurement + "-table > td.sensor_table_class").eq((counter)).html(data[value]);
                    counter += 1;
                };
            }
            else if(channel_measurement_id.length == 3) {

                if(chart_channel == "") {
                    chart_channel = channel;
                    chart_sensor_number = sensor_number;
                    changeChart(channel, measurement, sensor_number);

                    // Matches graph name, so graph
                    timestamp = new Date(parseFloat(values["timestamp"])) 
                    utc = Date.UTC(timestamp.getFullYear(), timestamp.getMonth(), 
                                   timestamp.getDay(), timestamp.getHours(), timestamp.getMinutes(), 
                                   timestamp.getSeconds());
                    chart1.series[0].addPoint([utc,  parseFloat(data[0])]);
                }
                else if(chart_channel == channel && chart_measurement == measurement && chart_sensor_number == sensor_number) {
                    // Matches graph name and number, so graph
                    timestamp = new Date(parseFloat(values["timestamp"])) 
                    utc = Date.UTC(timestamp.getFullYear(), timestamp.getMonth(), 
                                   timestamp.getDay(), timestamp.getHours(), timestamp.getMinutes(), 
                                   timestamp.getSeconds());
                    chart1.series[0].addPoint([utc,  parseFloat(data[0])]);

                }

                $("#" + measurement + "-table > td.sensor_table_class").eq((sensor_number)).html(data[0]);
            }
            else {
                console.log("Length: " + channel_measurement_id.length);

                console.log("Problem: Received more data than expected");
            }

        }
    });

    var Sensors = new Sensor();

    var connected = function() {
        socket.send({channel: window.channel});
    };

    var disconnected = function() {
        setTimeout(start, 1000);
    };

    var messaged = function(data) {
        Sensors.set(data);
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