import time
import struct

import cflib
import csv
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from cflib.crazyflie import Crazyflie

# get URI
URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')


def log_IEKF_imu_callback(timestamp, data, logconf):
    #print(data)
    IEKF_imu = [0.0] * 8
    IEKF_imu[0] = data['acc.x']
    IEKF_imu[1] = data['acc.y']
    IEKF_imu[2] = data['acc.z']
    IEKF_imu[3] = data['gyro.x']
    IEKF_imu[4] = data['gyro.y']
    IEKF_imu[5] = data['gyro.z']
    IEKF_imu[6] = data['stabilizer.thrust']
    IEKF_imu[7] = data['stabilizer.yaw']

    print('IEKF_imu:', IEKF_imu)
     

def log_stateEstimate_callback(timestamp, data, logconf):
    poseStateEstimate = [0] * 10

    poseStateEstimate[0] = data['stateEstimate.x']
    poseStateEstimate[1] = data['stateEstimate.y']
    poseStateEstimate[2] = data['stateEstimate.z']
    poseStateEstimate[3] = data['stateEstimate.qw']
    poseStateEstimate[4] = data['stateEstimate.qx']
    poseStateEstimate[5] = data['stateEstimate.qy']
    poseStateEstimate[6] = data['stateEstimate.qz']
    poseStateEstimate[7] = data['stateEstimate.roll']
    poseStateEstimate[8] = data['stateEstimate.pitch']
    poseStateEstimate[9] = data['stateEstimate.yaw']

    print('poseStateEstimate:', poseStateEstimate)


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    # This will create a new NatNet client
    # streamingClient = NatNetClient()

    # # Configure the streaming client to call our rigid body handler on the emulator to send data out.
    # streamingClient.newFrameListener = receiveNewFrame
    # streamingClient.rigidBodyListener = receiveRigidBodyFrame


    global scf
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        logconf = LogConfig(name='Acc_Gyro_Thrust_Yaw', period_in_ms=10)
        logconf.add_variable('acc.x', 'FP16')
        logconf.add_variable('acc.y', 'FP16')
        logconf.add_variable('acc.z', 'FP16')
        logconf.add_variable('gyro.x', 'FP16')
        logconf.add_variable('gyro.y', 'FP16')
        logconf.add_variable('gyro.z', 'FP16')
        logconf.add_variable('stabilizer.thrust', 'FP16')
        logconf.add_variable('stabilizer.yaw', 'FP16')

        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_IEKF_imu_callback)

        logconf1 = LogConfig(name='stateEstimate', period_in_ms=10)
        logconf1.add_variable('stateEstimate.x', 'FP16')
        logconf1.add_variable('stateEstimate.y', 'FP16')
        logconf1.add_variable('stateEstimate.z', 'FP16')
        logconf1.add_variable('stateEstimate.qw', 'FP16')
        logconf1.add_variable('stateEstimate.qx', 'FP16')
        logconf1.add_variable('stateEstimate.qy', 'FP16')
        logconf1.add_variable('stateEstimate.qz', 'FP16')
        logconf1.add_variable('stateEstimate.roll', 'FP16')
        logconf1.add_variable('stateEstimate.pitch', 'FP16')
        logconf1.add_variable('stateEstimate.yaw', 'FP16')
        scf.cf.log.add_config(logconf1)
        logconf1.data_received_cb.add_callback(log_stateEstimate_callback)

        # Start up the streaming client now that the callbacks are set up.
        # This will run perpetually, and operate on a separate thread.
        # streamingClient.run()

        logconf.start()
        logconf1.start()
        time.sleep(10)
        logconf.stop()
        logconf1.stop()
