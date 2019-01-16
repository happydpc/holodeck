"""Definition of all of the sensor information"""
import numpy as np


class SensorDef(object):

    def __init__(self, agent_name, sensor_name, sensor_type):
        self.agent_name = agent_name
        self.sensor_name = sensor_name
        self.type = sensor_type


class Sensor(object):

    def __init__(self, client, agent_name=None, name="DefaultSensor", custom_shape=None):
        self.name = name
        self._client = client
        self.agent_name = agent_name
        self._buffer_name = self.agent_name + "_" + self.name

        self._on_bool_buffer = self._client.malloc(self._buffer_name + "_sensor_on_flag", [1], np.uint8)
        self._sensor_data_buffer = self._client.malloc(self._buffer_name + "_sensor_data", self.data_shape, self.dtype)

    def set_sensor_enable(self, enable):
        self._on_bool_buffer = enable

    @property
    def sensor_data(self):
        return self._sensor_data_buffer

    @property
    def dtype(self):
        """The type of data in the sensor

        Returns:
            numpy dtype of sensor data
        """
        raise NotImplementedError("Child class must implement this property")

    @property
    def data_shape(self):
        """The shape of the sensor data

        Returns:
            tuple representing sensor data shape
        """
        raise NotImplementedError("Child class must implement this property")


class Terminal(Sensor):

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class Reward(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [1]


class ViewportCapture(Sensor):

    def __init__(self, client, agent_name, name="ViewportCapture", shape=(512, 512, 4)):
        self.shape = shape
        super(ViewportCapture, self).__init__(client, agent_name, name=name)

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class RGBCamera(Sensor):

    def __init__(self, client, agent_name, name="RGBCamera", shape=(256, 256, 4)):
        self.shape = shape
        super(RGBCamera, self).__init__(client, agent_name, name=name)

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class OrientationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3, 3]


class IMUSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2, 3]


class JointRotationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [94]


class RelativeSkeletalPositionSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [67, 4]


class LocationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class RotationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class VelocitySensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class CollisionSensor(Sensor):

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class PressureSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [48*(3+1)]


class SensorFactory(object):

    __sensor_keys__ = {"RGBCamera": RGBCamera,
                       "Terminal": Terminal,
                       "Reward": Reward,
                       "ViewportCapture": ViewportCapture,
                       "OrientationSensor": OrientationSensor,
                       "IMUSensor": IMUSensor,
                       "JointRotationSensor": JointRotationSensor,
                       "RelativeSkeletalPositionSensor": RelativeSkeletalPositionSensor,
                       "LocationSensor": LocationSensor,
                       "RotationSensor": RotationSensor,
                       "VelocitySensor": VelocitySensor,
                       "PressureSensor": PressureSensor,
                       "CollisionSensor": CollisionSensor}

    @staticmethod
    def _default_name(sensor_type):
        for k, v in SensorFactory.__sensor_keys__.items():
            if v is sensor_type:
                return k

    @staticmethod
    def build_sensor(client, sensor_def):
        if isinstance(sensor_def.type, str):
            sensor_def.type = SensorFactory.__sensor_keys__[sensor_def.type]
        if sensor_def.sensor_name is None:
            sensor_def.sensor_name = SensorFactory._default_name(sensor_def.type)

        return sensor_def.type(client, sensor_def.agent_name, sensor_def.sensor_name)
