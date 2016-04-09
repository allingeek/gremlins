import signal

from gremlins import faults, metafaults, triggers

server_cmd = "nc.*4242"
nc_kill = faults.kill_processes([server_cmd], signal.SIGKILL)
nc_pause = faults.pause_processes([server_cmd], 5)

profile = [
    triggers.Periodic(
        10,
        metafaults.pick_fault([
            # kill -9s
            # (5, nc_kill),
            # pauses (simulate GC)
            (10, nc_pause),
        ])),
    #  triggers.WebServerTrigger(12321)
]

