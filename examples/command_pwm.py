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

def set_pwm(cf, pwm):
    cf.param.set_value('motorPowerSet.m1', pwm[0])
    cf.param.set_value('motorPowerSet.m2', pwm[1])
    cf.param.set_value('motorPowerSet.m3', pwm[2])
    cf.param.set_value('motorPowerSet.m4', pwm[3])


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='Thrust', period_in_ms=10)
    lg_stab.add_variable('stabilizer.thrust', 'float')
    lg_stab.add_variable('motor.m1', 'float')
    lg_stab.add_variable('pwm.m1_pwm', 'float')
    pwm = [30000]*4

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf
        cf.log.add_config(lg_stab)
        cf.param.set_value('motorPowerSet.enable', 1)
        time.sleep(0.01)
        for i in range(300):
            set_pwm(cf, pwm)
            lg_stab.data_received_cb.add_callback(log_stab_callback)
            lg_stab.start()
            time.sleep(0.01)
        set_pwm(cf, [0]*4)
        cf.commander.send_stop_setpoint()
        lg_stab.stop()
