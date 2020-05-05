import ClWxSim.sim.Pressure as p
import ClWxSim.data.World as wld
from ClWxSim.utils.logging import Logger

tick_length = 0.1
self.logger = Logger(log_name="pressure")

logger.log("Starting test, creating a test world...")

test_wld = wld("pressure_test World")

logger.log("Test world successfully created")
logger.log("Test world pressure: {}".format(test_wld.air_pressure))
logger.log("Simulating pressure changes over one tick...")

test_wld = p.tick(test_wld, tick_length)

logger.log("Test world pressure successfully simulated over 1 tick")
logger.log("Test world pressure: {}".format(test_wld.air_pressure))
logger.log("Simulating pressure changes over 50 ticks...")

for i in range(50):
    test_wld = p.tick(test_wld, tick_length)

logger.log("Test world pressure successfully simulated over 50 ticks")
logger.log("Test world pressure: {}".format(test_wld.air_pressure))

logger.log("ALL TESTS SUCCESSFULL")
