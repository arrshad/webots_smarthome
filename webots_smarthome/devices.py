from controller import (
    Emitter as BaseEmitter, 
    Receiver as BaseReceiver, 
    Motor as BaseMotor, 
    InertialUnit as BaseInertialUnit, 
    DistanceSensor as BaseDistanceSensor, 
    GPS as BaseGPS
)


class Emitter(BaseEmitter):
    def __init__(self, name: str, channel: int = 1):
        super().__init__(name)
        self.channel = channel


class Receiver(BaseReceiver):
    def __init__(self, name: str, time_step: int, channel: int = 1):
        super().__init__(name)
        self.channel = channel
        self.enable(time_step)


class Motor(BaseMotor):
    def __init__(self, name: str, max_speed: float):
        super().__init__(name)
        self.target_position = float('inf')
        self.max_speed = max_speed
    
    @property
    def velocity(self) -> float:
        return self.target_velocity
    
    @velocity.setter
    def velocity(self, velocity: float):
        self.target_velocity = velocity * self.max_speed / 10


class InertialUnit(BaseInertialUnit):
    def __init__(self, name: str, time_step: int):
        super().__init__(name)
        self.enable(time_step)

    @property
    def rotation(self) -> float:
        return (((self.getRollPitchYaw()[2] / 3.14) * 180) + 360) % 360


class DistanceSensor(BaseDistanceSensor):
    def __init__(self, name: str, time_step: int):
        super().__init__(name)
        self.enable(time_step)

    @property
    def value(self) -> int:
        return int(super().value * 10 * 32)
    
    def __eq__(self, other) -> bool:
        return self.value == other
    
    def __ne__(self, other) -> bool:
        return self.value != other
    
    def __lt__(self, other) -> bool:
        return self.value < other
    
    def __le__(self, other) -> bool:
        return self.value <= other
    
    def __gt__(self, other) -> bool:
        return self.value > other
    
    def __ge__(self, other) -> bool:
        return self.value >= other

    
class GPS(BaseGPS):
    def __init__(self, name: str, time_step: int):
        super().__init__(name)
        self.enable(time_step)
