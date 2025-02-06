# Webots Smart Home

This package provides a Python API to interact with and control a smart home simulation using Webots. It includes various classes and methods to control robots, sensors, and other devices within the simulation.

## Installation

```sh
pip install git+https://github.com/arrshad/webots_smarthome.git
```

## Usage

### Robot Control

The `Robot` class provides an interface to control a robot in the simulation. You can initialize a robot, control its movement, and access its sensors.

```python
from webots_smarthome import Robot

robot = Robot('robot_name')

while robot.step() != -1:
    robot.move(10, 10)  # Move forward
```

### Sensors

The package includes classes to interact with various sensors such as distance sensors, inertial units, and GPS.

```python
# Accessing distance sensors
front_distance = robot.sensors.D6.value

# Comparing distance sensor value
if robot.sensors.D6 > 100:
    print("Object detected within 100 units")

# Accessing inertial unit
rotation = robot.inertial_unit.rotation
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
