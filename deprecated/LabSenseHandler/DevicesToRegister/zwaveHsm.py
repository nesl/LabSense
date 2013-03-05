body = """
    "deviceprofile": { 
        "devicename": "NESL_Zwave_HSM", 
        "location": "BH1762/UCLA", 
        "tags": "LabSense", 
        "IP": "128.97.93.90", 
        "latitude": 34.069, 
        "longitude": -118.443, 
        "sensors": [ 
            { "name": "Readings", 
                "sid": "1", 
                "channels": [ 
                    { "name": "Motion", 
                        "type": "Bool", 
                        "unit": "Motion/No Motion", 
                        "samplingperiod": 60
                    },
                    { "name": "Temperature", 
                        "type": "Integer", 
                        "unit": "Fahrenheit", 
                        "samplingperiod": 60
                    },
                    { "name": "Luminance", 
                        "type": "Integer", 
                        "unit": "Perecent", 
                        "samplingperiod": 60
                    }
                ] 
            }
        ] 
    }"""
