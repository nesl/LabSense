{% extends "generic_channel.html" %}

{% block socketio %}

    var name, started = false;

    var socket;

    var Sensor = Backbone.Model.extend({
        //defaults: {
            //name: "",
            //timestamp: "",
            ////value: ""
            //data: []
        //},
        set: function(values) {

            data = values.data;
            name = values.name;

            if(name == undefined){
                return;
            }

            console.log("name: "+ name);

            channel_measurement_id = name.split("_");

            measurement = channel_measurement_id[1];
            id = channel_measurement_id[2];

            console.log("Channel: "+ channel_measurement_id[0]);
            console.log("Measurement: " + channel_measurement_id[1]);
            console.log("Id: "+ channel_measurement_id[2]);

            counter = 1;
            for(value in data) {
                if(chart_series == "") {
                    chart_series = name;
                    chart_sensor_number = 1;
                    changeChart(name, chart_sensor_number);

                    // Matches graph name, so graph
                    timestamp = new Date(parseFloat(values["timestamp"])) 
                    utc = Date.UTC(timestamp.getFullYear(), timestamp.getMonth(), 
                                   timestamp.getDay(), timestamp.getHours(), timestamp.getMinutes(), 
                                   timestamp.getSeconds());
                    chart1.series[0].addPoint([utc,  parseFloat(data[0])]);
                }
                else if(chart_series == name && chart_sensor_number == counter) {
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

            // Register if not registered
            //if($.inArray(name, registered_series) == -1) {
                //alert("ADDINGO ONCLICK");
                //counter = 1;
                //for(value in data) {
                    //$("#" + measurement + "-table > td.sensor_table_class").eq((counter)).click(function() {
                            //alert("Clicked: " + name + "_" + counter);
                     //});
                    //counter += 1;
                //}
                //registered_series.push(name);
            //}
        }
    });

    var Sensors = new Sensor();

    //var SensorGroup = new Array();
    //{% for measurement in current_channel.measurement_set.all %}
    //SensorGroup.push(new Sensor({"name":"{{ measurement.slug }}", "timestamp": 0, "data": []}));
    //{% endfor %}

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
