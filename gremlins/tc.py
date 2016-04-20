from gremlins import procutils
import random
import logging

# use the 'tc' command from the iproute2 package to inject and remove faults to/from the network interface

def tc(iface, args):
    return "tc qdisc add dev %s parent 1:3 handle 30: %s"%(iface, args)

def die(msg):
    logging.error(msg)
    exit(1)

def clear_faults():
    """undo all currently enabled faults"""
    logging.info("Clearing network faults")
    for iface in ['eth0']:
        procutils.run(("tc qdisc del dev %s root" % (iface)).split(" "), assert_return_code_zero=False)

def _add_fault(fault):
    """add a network fault"""
    logging.info("Adding network fault: %s" % (fault))
    for iface in ['eth0']:
        procutils.run(("tc qdisc add dev %s root %s" % (iface, fault)).split(" "), assert_return_code_zero=False)

def introduce_packet_loss(packet_loss_percentage=random.randint(1, 100)):
    """introduce pocket loss"""
    clear_faults()
    _add_fault("netem loss %d%%" % (packet_loss_percentage))

def introduce_partition():
    """introduce network partition"""
    introduce_packet_loss(100)

class Latency:
    # Add latency to all packets

    def __init__(self):
        # per-packet delay in ms
        self.latency = random.randint(100, 1000)

    def action(self):
        return "netem delay %dms"%(self.latency)

    def desc(self):
        return "delay of %dms"%(self.latency)

class Reorder:
    # Reorder packets

    def __init__(self):
        # probability of continuing the delay
        self.correlation = 50

        # initial packet delay
        self.delay = 10

        # probability of reordering a packet
        self.reorder = random.randint(10, 75)

    def action(self):
        return "netem delay %sms reorder %d%% %d%%" % (self.delay, 100-self.reorder, self.correlation)

    def desc(self):
        return "reorder after delay of %dms with probability %d and correlation %d" % (self.delay, 100-self.reorder, self.correlation)

