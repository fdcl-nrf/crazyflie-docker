import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

def log_stab_callback(timestamp, data, logconf):
    print("[{}][{}]: {}".format(timestamp, logconf.name, data))

if __name__ == '__main__':
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='Thrust', period_in_ms=10)
    #lg_stab.add_variable('stabilizer.thrust', 'float')
    #lg_stab.add_variable('motor.m1', 'float')
    lg_stab.add_variable('pwm.m1_pwm', 'float')
    lg_stab.add_variable('pwm.m2_pwm', 'float')
    lg_stab.add_variable('pwm.m3_pwm', 'float')
    lg_stab.add_variable('pwm.m4_pwm', 'float')

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf
        cf.log.add_config(lg_stab)
        cf.commander.send_setpoint(0.0, 0.0, 0, 0)
        time.sleep(0.01)
        for i in range(300):
            cf.commander.send_setpoint(30.0, 0.0, 0, 30000)
            lg_stab.data_received_cb.add_callback(log_stab_callback)
            lg_stab.start()
            time.sleep(0.01)
        cf.commander.send_stop_setpoint()
        lg_stab.stop()
