from dataclasses import dataclass

from controller import Robot as BaseRobot

from .devices import Motor, DistanceSensor, Receiver, Emitter, InertialUnit, GPS


@dataclass
class RobotWheels:
    right: Motor
    left: Motor


@dataclass
class RobotSensors:
    front_left: DistanceSensor
    front_right: DistanceSensor
    right_front: DistanceSensor
    right_back: DistanceSensor
    back_left: DistanceSensor
    back_right: DistanceSensor
    left_front: DistanceSensor
    left_back: DistanceSensor


class Robot(BaseRobot):
    def __init__(self, name: str, max_speed: float):
        super().__init__()
        self.max_speed = max_speed
        self.time_step = int(self.getBasicTimeStep())

        self.emitter = Emitter('emitter')
        self.receiver = Receiver('receiver', self.time_step)
        
        self.emitter.send(name.encode('utf-8'))

        self.wheels = RobotWheels(
            right=Motor('wheel1 motor', self.max_speed),
            left=Motor('wheel2 motor', self.max_speed)
        )

        self.sensors = RobotSensors(
            front_left=DistanceSensor('D1', self.time_step),
            front_right=DistanceSensor('D8', self.time_step),
            right_front=DistanceSensor('D7', self.time_step),
            right_back=DistanceSensor('D6', self.time_step),
            back_left=DistanceSensor('D3', self.time_step),
            back_right=DistanceSensor('D5', self.time_step),
            left_front=DistanceSensor('D2', self.time_step),
            left_back=DistanceSensor('D4', self.time_step)
        )

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
        self.wheels.left.velocity = left
        self.wheels.right.velocity = right
