from ClWxSim.sim.Pressure import Pressure as p
from  ClWxSim.data.World import World as wld
from ClWxSim.utils.logging import Logger

tick_length = 1/25
logger = Logger(log_name="pressure_test")

logger.log("Starting test, creating a test world...")

test_wld = wld("pressure_test World", grid_size=5, starting_pressure=0.0)

test_wld.air_pressure[0,0] = 1.0

test_wld.air_pressure[4,4] = 1.0

logger.log("Test world successfully created")
logger.log("Test world pressure:\n{}\n".format(test_wld.air_pressure))

logger.log("Creating a Pressure sim utils instance...")

prs = p()

logger.log("Simulating pressure changes over one tick...")

test_wld = prs.tick(test_wld, tick_length)

logger.log("Test world pressure successfully simulated over 1 tick")
logger.log("Test world pressure:\n{}\n".format(test_wld.air_pressure))
# logger.log("Simulating pressure changes over 50 ticks...")
#
# for i in range(50):
#     test_wld = prs.tick(test_wld, tick_length)
#
# logger.log("Test world pressure successfully simulated over 50 ticks")
# logger.log("Test world pressure:\n{}".format(test_wld.air_pressure))

logger.log("ALL TESTS SUCCESSFULL")
