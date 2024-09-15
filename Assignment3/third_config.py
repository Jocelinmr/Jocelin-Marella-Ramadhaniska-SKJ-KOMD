import m5
from m5.objects import *
from caches import *

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MB")]  # Create an address range

system.cpu = X86TimingSimpleCPU()

args = {
    'l1i_size': '16kB',
    'l1d_size': '64kB',
    'l2_size': '256kB'
}

# Initialize the L1 caches with the provided arguments
system.cpu.icache = L1ICache(args)
system.cpu.dcache = L1DCache(args)

# Create the L2 bus (crossbar)
system.l2bus = L2XBar()

# Connect L1 instruction cache (icache) and L1 data cache (dcache) to CPU and L2 bus
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Create and connect the L2 cache to the L2 bus and the memory bus
system.l2cache = L2Cache(args)
system.l2cache.connectCPUSideBus(system.l2bus)

# Create the memory bus (crossbar)
system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

# Connect the CPU interrupt controller to the memory bus
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Memory controller setup
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Connect system port
system.system_port = system.membus.cpu_side_ports

# Workload setup for Hello World application
binary = "gem5/tests/test-progs/hello/bin/x86/linux/hello"
system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]  # Command is a list starting with the executable
system.cpu.workload = process
system.cpu.createThreads()

# Root SimObject and start simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()

print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause()))
