# Bob The Bouncer
>- 20230117.01 - updated housing of overall assembly (Raspi, sensor mounts, and added physical USB cable output interface)

- Sense, detect, and respond
- Workflow:
    1. Python runs pir.py which processes input signals from PIR sensor
    2. If motion detected, `Bob` takes a picture and sends it to a Slack channel

### Hardware : Sense and Detect
- Raspberry Pi 3 B+
- Raspberry Camera module
- Passive Infrared sensor

### Proof is in the pudding
![Camera module and PIR sensor](https://github.com/bencarpena/arcturus-py/blob/master/infra-camera.jpg)
![Slack mobile app output](https://github.com/bencarpena/arcturus-py/blob/master/slack-pir-res.jpg)

### Change log:
