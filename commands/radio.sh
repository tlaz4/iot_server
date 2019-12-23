#!/bin/bash

curl -X PATCH -H "Content-Type: application/json" -d '{"status": false}' http://10.0.0.238:5000/api/devices/2
