#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

import sys
import os
import string
import signal
import subprocess

import pyutilib.pyro
from pyomo.common._command import pyomo_command

@pyomo_command('pyomo_ns', "Launch a Pyro name server for Pyomo")
def pyomo_ns():
    pyutilib.pyro.start_ns()

@pyomo_command('pyomo_nsc', "Execute the Pyro name server control tool for Pyomo")
def pyomo_nsc():
    pyutilib.pyro.start_nsc()

@pyomo_command('kill_pyro_mip_servers', "Terminate Pyomo's MIP solvers using Pyro")
def kill_pyro_mip_servers():
    if len(sys.argv) > 2:
        print("***Incorrect invocation - use: kill_pyro_mip_servers pid-filename")
        sys.exit(1)

    pid_filename = "pyro_mip_servers.pids"
    if len(sys.argv) == 2:
        pid_filename = sys.argv[1]

    print("Killing pyro mip servers specified in file="+pid_filename)

    pid_file = open(pid_filename, "r")
    for line in pid_file.readlines():
        pid = eval(string.strip(line))
        print("KILLING PID="+str(pid))
        os.kill(pid, signal.SIGTERM)
    pid_file.close()

@pyomo_command('launch_pyro_mip_servers', "Launch Pyomo's MIP solvers using Pyro")
def launch_pyro_mip_servers():
    if len(sys.argv) != 2:
        print("***Incorrect invocation - use: launch_pyro_mip_servers num-servers")
        sys.exit(1)

    num_servers = eval(sys.argv[1])

    print("Number of servers to launch="+str(num_servers))

    server_pids = []

    for i in range(1, num_servers+1):
        print("Launching server number "+str(i))
        output_filename = "pyro_mip_server"+str(i)+".out"
        # the "exec" ensures that (at least for bash) that the server process
        # will be the process returned, i.e., it becomes the child process - no
        # shell process intermediate. more correctly, exec exits the current
        # process before it does so (no fork).
        pid=subprocess.Popen("exec pyro_mip_server >& pyro_mip_server."+str(i)+".out", shell=True).pid
        server_pids.append(pid)

    # perhaps a better place would be in the users home directory, but I'll
    # worry about that a bit later.
    pid_output_filename = "pyro_mip_servers.pids"
    pid_output_file = open(pid_output_filename,"w")
    for pid in server_pids:
        pid_output_file.write(str(pid)+'\n')
    pid_output_file.close()

    print("PIDs for launched servers recorded in file="+pid_output_filename)
