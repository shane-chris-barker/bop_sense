# 🤖 Bop Sense
[![PR Checks](https://github.com/shane-chris-barker/bop_sense/actions/workflows/test.yml/badge.svg)](https://github.com/shane-chris-barker/bop_sense/actions/workflows/test.yml)

**Bop Sense** is the input processing module for **Bop**, a work-in-progress Raspberry Pi-powered robot pet project.

This is **one of three core repositories**:
- `bop_sense` - Listens to the world (mic, camera, sensors) and places AMQP or MQTT messages into a queue.

- `bop_brain` - Does not exist yet but when it does, will be responsible for processing the messages produced by `bop_sense` and making decisions based on their content.

- `bop_body` - Also does not exist yet but will subscribe and readt to commands produced by `bop_brain` and then take an action (motors, display, feedback etc)

> ⚠️ **Note**: This is an early, rough WIP and very much an experiment. Things will change, break, and improve rapidly. 

>I'm also very new to Python, so there are bound to be mistakes..

---

## ✅ What `bop_sense` Can Do Right Now

- **Detect if a microphone is activated** (via config flags)
- **Listen for voice input** when a mic is present
- **Send recognized voice messages to a message queue**
  - AMQP (RabbitMQ) or MQTT (Mosquitto) supported
- **Run headlessly** (e.g. on Raspberry Pi via SSH)

This is effectively `v0.1` — limited in scope but functional as a foundation.

---

## 🛠️ Planned Features

- Support for camera input (face recognition, object detection)
- Temperature and environmental sensor reading
- Configurable hardware abstraction
- Better feedback (LEDs/display/sound) for diagnostic info
- Pi-specific startup optimizations
- Diagrams of Bop and the Raspberry Pi configuration

---

## 🧪 Testing

We are adding tests as we go. Run them via:

```bash
pytest --cov=hardware_detection --cov-report=term-missing
```


## 🧾 Environment

**Python 3.12** (venv named `venv`)

Use .env files for environment variables (.env.dev, etc.)

A sample .env.example file is included

## 📡 Communication Types
Supports publishing to:

**AMQP** (e.g. RabbitMQ)

**MQTT** (e.g. Mosquitto)

**Mock publisher** (for local dev/testing)

Configure via your `.env` file

## 🚀 Getting Started
Clone this repo

Create a `.env.dev` file based on `.env.example`

Install dependencies:
```
pip install -r requirements.txt
```
Run locally:

```
$env:BOP_ENV="dev"; $env:COMM_TYPE="amqp"; python main.p
```

`COMM_TYPE` can be passed to override config values - valid options are:
```
amqp
mqtt
```