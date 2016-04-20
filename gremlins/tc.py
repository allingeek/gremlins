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

def introduce_latency():
    latency = random.randint(100, 1000)
    _add_fault("netem delay %dms" % (latency))

def introduce_packet_reordering(delay_in_ms = 10, reorder_probability = 50, correlation=50):
    """
    :param delay_in_ms: initial packet delay in milliseconds
    :param reorder_probability: probability packets will be reordered, defaults to 50%
    :param correlation: probability of continuing the delay
    :return:
    """
    _add_fault("netem delay %sms reorder %d%% %d%%" % (delay_in_ms, 100 - reorder_probability, correlation))

