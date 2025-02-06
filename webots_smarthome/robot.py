from typing import Dict
from dataclasses import dataclass, field

from controller.device import Device
from controller import Robot as BaseRobot

from .devices import Motor, DistanceSensor, Receiver, Emitter, InertialUnit, GPS


@dataclass
class RobotWheels:
    """A class to represent the wheels of a robot.

    Attributes:
        right (Motor): The motor controlling the right wheel of the robot.
        left (Motor): The motor controlling the left wheel of the robot.
    """

    right: Motor
    left: Motor


@dataclass
class RobotSensors:
    """RobotSensors class represents the distance sensors attached to a robot."""

    _data: Dict[str, DistanceSensor] = field(default_factory=dict)

    def __getattr__(self, key: str) -> DistanceSensor:
        try:
            return self._data[key]
        except KeyError:
            raise AttributeError(f"Sensor '{key}' not found")

    def __setattr__(self, key: str, value: DistanceSensor):
        if key == "_data":
            super().__setattr__(key, value)
        else:
            self._data[key] = value


class Robot(BaseRobot):
    def __init__(self, name: str, max_speed: float):
        """Initializes the robot with the given name and maximum speed.

        Args:
            name (str): The name of the robot.
            max_speed (float): The maximum speed of the robot.
        Attributes:
            max_speed (float): The maximum speed of the robot.
            time_step (int): The basic time step of the robot.
            emitter (Emitter): The emitter device for sending messages.
            receiver (Receiver): The receiver device for receiving messages.
            wheels (RobotWheels): The wheels of the robot.
            sensors (RobotSensors): The distance sensors of the robot.
            inertial_unit (InertialUnit, optional): The inertial unit of the robot if available.
            gps (GPS, optional): The GPS device of the robot if available.
            battery (float): The battery level of the robot.
        """
        
        super().__init__()
        self.devices: Dict[str, Device]

        self.max_speed = max_speed
        self.time_step = int(self.getBasicTimeStep())

        self.emitter = Emitter('emitter')
        self.receiver = Receiver('receiver', self.time_step)
        
        self.emitter.send(name.encode('utf-8'))

        self.wheels = RobotWheels(
            right=Motor('wheel1 motor', self.max_speed),
            left=Motor('wheel2 motor', self.max_speed)
        )
        
        self.sensors = RobotSensors()
        for device in self.devices:
            if device.startswith('D'):
                self.sensors._data[device] = DistanceSensor(device, self.time_step)

        if 'inertial_unit' in self.devices:
            self.inertial_unit = InertialUnit('inertial_unit', self.time_step)
        if 'gps' in self.devices:
            self.gps = GPS('gps', self.time_step)


    @property
    def battery(self) -> float:
        if self.receiver.getQueueLength() > 0:
            received_data = self.receiver.getString()
            if len(received_data) > 0:
                self.receiver.nextPacket()
                return float(received_data)
        return 0


    def move(self, left: float, right: float):
        """Sets the velocity of the robot's wheels.

        Parameters:
            left (float): The velocity for the left wheel.
            right (float): The velocity for the right wheel.
        """
        
        self.wheels.left.velocity = left
        self.wheels.right.velocity = right
