import os
import sys

import grpc_tools.command

sys.path.append(os.path.dirname(__file__))

grpc_tools.command.build_package_protos("")
