from dataclasses import dataclass

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
    """
    RobotSensors class represents the distance sensors attached to a robot.

    Attributes:
        front_left (DistanceSensor): Sensor located at the front left of the robot.
        front_right (DistanceSensor): Sensor located at the front right of the robot.
        right_front (DistanceSensor): Sensor located at the right front of the robot.
        right_back (DistanceSensor): Sensor located at the right back of the robot.
        back_left (DistanceSensor): Sensor located at the back left of the robot.
        back_right (DistanceSensor): Sensor located at the back right of the robot.
        left_front (DistanceSensor): Sensor located at the left front of the robot.
        left_back (DistanceSensor): Sensor located at the left back of the robot.
    """
    
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
        """Sets the velocity of the robot's wheels.

        Parameters:
            left (float): The velocity for the left wheel.
            right (float): The velocity for the right wheel.
        """
        
        self.wheels.left.velocity = left
        self.wheels.right.velocity = right
