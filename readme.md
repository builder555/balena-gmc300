### Balena Blocks: GMC-300/GMC-320 communicator

Reads CPM (counts per minute) value from a GMC3xx-series geiger counter and publishes it to MQTT endpoint, if it reaches a specified limit.
Automatically turns on the geiger counter, if it's off.

___Usage as a block___

Add the following to your `docker-compose.yaml`:

```yaml
  gmc300:
    privileged: true
    build: ./balena-gmc300
    restart: always
    environment:
      - MQTT_TOPIC=CPM_ALERT
      - CPM_LIMIT=50
      - MQTT_HOST=mqtt
```

Example published payload: `WARNING: 89CPM`

***NB**: When deploying a microservices application, use `balena push --multi-dockerignore <UUID>` to ensure that the `.dockerignore` file is processed.*


___Available variables___

| Environment Variable    | Default       | Description                                                                |
| ----------------------- | ------------- | -------------------------------------------------------------------------- |
| `READ_PERIOD`           |  5            | How often to read CPM values (seconds)                                     |
| `NOTIFICATION_COOLDOWN` |  30           | How many seconds to wait after a notification, before sending another one  |
| `CPM_LIMIT`             |  100          | Notify, if CPM reaches this value                                          |
| `MQTT_TOPIC`            |  'CPM_ALERT'  | MQTT topic, under which to publish                                         |
| `MQTT_HOST`             |  'mqtt'       | Broker hostname                                                            |
| `MQTT_USER`             |  ''           | Username to connect to MQTT broker                                         |
| `MQTT_PASS`             |  ''           | Password to connect to MQTT broker                                         |


___Tests___

```bash
$ PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
$ pipenv shell
$ pytest -vs
```
