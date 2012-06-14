$(function() {

    var name, started = false;

    var socket;

    var SensorValue = Backbone.Model.extend({
        defaults: {
            name: "",
            value: ""
        },
    });

    var SensorValueCollection = Backbone.Collection.extend({
        model: SensorValue
    });

    var connected = function() {
        socket.send({channel: window.channel});
    };

    var disconnected = function() {
        setTimeout(start, 1000);
    };

    var messaged = function(data) {
        var tokens = data["data"].split(" ");
        console.log(data["timestamp"]);
        console.log("Tokens: " + tokens)
        //timestamp = parseFloat(data["timestamp"])
        //timestamp = Date.getTime()
        //timestamp = parseFloat(data["timestamp"])
        timestamp = new Date(parseFloat(data["timestamp"])) 
            //timestamp = Date.UTC(new Date(parseFloat(data["timestamp"])))
        utc = Date.UTC(timestamp.getFullYear(), timestamp.getMonth(), timestamp.getDay(), timestamp.getHours(), timestamp.getMinutes(), timestamp.getSeconds());
        //console.log("Hours: " +  timestamp.getHours());
        chart1.series[0].addPoint([utc,  parseFloat(tokens[1])]);
        //chart1.series[0].addPoint([, parseFloat(tokens[2])]);
        //chart1.series[0].addPoint([, parseFloat(tokens[3])]);
        //chart1.series[0].addPoint([, parseFloat(tokens[4])]);
        //chart1.series[0].addPoint([, parseFloat(tokens[5])]);
        //chart1.series[0].addPoint([, parseFloat(tokens[6])]);
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

});
