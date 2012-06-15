$(function() {

    var name, started = false;

    var socket;

    var Sensor = Backbone.Model.extend({
        defaults: {
            name: "",
            timestamp: "",
            //value: ""
            data: []
        },
        set: function(values) {
            console.log("CHANGED: " + JSON.stringify(values));
            console.log(typeof values);

            counter = 1;
            data = values.data;
            for(value in data) {
                console.log(value + ": " + data[value]);
                //$("#sensor-" + (value+1)).html(data[value]);
                $("#Current-table > td.sensor_table_class").eq((counter)).html(data[value]);
                counter += 1;
            };
        }
    });




    //var Sensors = Backbone.Collection.extend({;
        //model: Sensor,
        //initialize: function() {;
            ////_.bindAll(this, "changeAll");

            ////_.bind("changeAll", this.changeAll);
            ////this.changeAll = _.bind(this.changeAll, this);
        //},
        //update: function(values) {
            //singleton.changeAll.apply(singleton, values);
        //},
        //changeAll: function(values) {
            //counter = 0;
            //console.log("Values: "+ values);
            //console.log("size: " + values.length);
            //if(typeof values === 'string')
                //values = [values];

            //_.each(values, function(values) {
                //console.log(counter);
                //var sv = this.get(counter);
                //console.log("THIS: " + JSON.stringify(sv));
                //sv.change(val);
                //counter += 1;

            //});
        //}



    //});

    //_.bindAll(Sensors, "changeAll");
    //var changeAll = Sensors.changeAll;
    //
    //var init_array = new Array();
    //var SensorArray = Array();
    //for (var i = 0; i < 2; i++) {
        ////sensor_val = {"name": "Sensor", "id": i, "value": i};
        ////init_array[i] = sensor_val;
        //SensorArray.push(Sensor({"name": "Sensor", "id": i, "value": i}));
    //}

    //updateSensors = function(values) {
        //var counter = 0;
        //for(val in values) {
            //SensorArray[counter].set({"value": val});
            //counter += 1;
        //};
        
    //};


    //var SensorView = new Backbone.View.extend({
        //tagName: "div",
        //className: "sensorview",
        //initialize: function() {
            //_.bindAll(this, "render", "changeAll");
            ////this.model.bind("change", this.changeAll);
            //var init_array = new Array();
            //for (var i = 0; i < 2; i++) {
                //sensor_val = {"name": "Sensor", "id": i, "value": i};
                //init_array[i] = sensor_val;
            //}
            //this.collection = new Sensors(init_array);
            //Sensors.bind("changeAll", this.changeAll);
            ////this.collection.bind("add", this.render, this);
            ////this.collection.bind("changeAll", _.bind(this.render, this));
        //},

        //changeAll: function(values) {
            //counter = 0;
            //_.each(values, function(val) {
                //var sv = Sensors.get(counter);
                //print("THIS: " + JSON.stringify(sv));
                //sv.change(val);
                //counter += 1;
            //});
        //},

        ////update: function(values) {
            ////console.log("Updated called");
            ////this.collection.changeAll(values);
        ////},

        //render: function() {
            //console.log("Render called");
        //}
    //});


    var Sensors = new Sensor();
    //var sensor = new Sensor({name: "Jason", id: 1, value: 22 });
    //var sensor = new Sensor({name: "Jason", id: 1, values: [22] });
    //console.log(sensor.get("name"));
    //console.log(sensor.get("id"));
    //console.log(sensor.get("values"));

    //sensor.set({"name": "Justin"});
    //sensor.set("values", [33]);
    //console.log(sensor.get("name"));
    //console.log(sensor.get("values"));


    //for (var i = 0; i < 3; i++) {
        //svc.add([{"name": "Sensor", "id": i, "value": i}]);
    //}

    var connected = function() {
        socket.send({channel: window.channel});
        //sv = new SensorValue;
        //sv.change({name: "Jason"});
    };

    var disconnected = function() {
        setTimeout(start, 1000);
    };

    var messaged = function(data) {
        //console.log(JSON.stringify(msg_data));
        //var data = JSON.parse(msg_data);
        var tokens = data["data"];
        console.log(data["timestamp"]);
        console.log("Tokens: " + tokens)
        //timestamp = parseFloat(data["timestamp"])
        //timestamp = Date.getTime()
        //timestamp = parseFloat(data["timestamp"])
        timestamp = new Date(parseFloat(data["timestamp"])) 
        utc = Date.UTC(timestamp.getFullYear(), timestamp.getMonth(), 
                       timestamp.getDay(), timestamp.getHours(), timestamp.getMinutes(), 
                       timestamp.getSeconds());
        //console.log("Hours: " +  timestamp.getHours());
        chart1.series[0].addPoint([utc,  parseFloat(tokens[0])]);
        //svc.changeAll(tokens)
        //S.update(tokens);

        var a = Array();
        a[0] = 1;
        a[1] = 2;
        a[2] = 3;
        Sensors.set(data);
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
