from gremlins import procutils
import random
import logging
import subprocess

# use the 'tc' command from the iproute2 package to inject and remove faults to/from the network interface

def tc(iface, args):
    return "tc qdisc add dev %s parent 1:3 handle 30: %s"%(iface, args)

def die(msg):
    logging.error(msg)
    exit(1)

def call(cmd, exit_on_fail=True):
    logging.info(cmd)
    res = subprocess.call(cmd, shell=True, stderr=subprocess.STDOUT)
    if res != 0 and exit_on_fail:
        die("error: subprocess returned %d (not 0)"%(res))
        return res


def clear_faults():
    """undo all currently enabled faults"""
    logging.info("Clearing network faults")
    #for iface in settings.interfaces:
    for iface in ['eth0']:
        cmd = "tc qdisc del dev %s root" % (iface)
        call(cmd, exit_on_fail=False)
        #procutils.run(("tc qdisc del dev %s root" % (iface)).split(" "), assert_return_code_zero=False)

def _add_fault(fault):
    """add a network fault"""
    logging.info("Adding network fault: %s" % (fault))
    #for iface in settings.interfaces:
    for iface in ['eth0']:
        cmd = "tc qdisc add dev %s root %s" % (iface, fault)
        call(cmd, exit_on_fail=False)
        #procutils.run(("tc qdisc del dev %s root" % (iface)).split(" "), assert_return_code_zero=False)

def introduce_packet_loss():
    """introduce pocket loss"""
    _add_fault("netem loss %d%%"%(random.randint(5, 10)))

class Partition:
    # Partition the current server from all other servers

    def action(self):
        return "netem loss 100%"

    def desc(self):
        return "network partition"

class PacketLoss:
    # Drop packets with some probability

    def __init__(self):
        # percentage probability of dropping a packet
        self.loss = random.randint(5, 10)

    def action(self):
        return "netem loss %d%%"%(self.loss)

    def desc(self):
        return "drop packets with probability %d%%"%(self.loss)

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

