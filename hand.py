import time
import math
from typing import Literal

# Unitree DDS imports
from unitree_sdk2py.core.channel import ChannelPublisher, ChannelFactoryInitialize # type: ignore
from unitree_sdk2py.idl.unitree_go.msg.dds_ import MotorCmds_ # type: ignore
from unitree_sdk2py.idl.default import unitree_go_msg_dds__MotorCmd_ # type: ignore

class Dex1Controller:
    def __init__(self, domain_id: int = 1):
        """Initialize the DDS node and publishers."""
        ChannelFactoryInitialize(domain_id)
        
        self.left_pub = ChannelPublisher("rt/dex1/left/cmd", MotorCmds_)
        self.left_pub.Init()
        
        self.right_pub = ChannelPublisher("rt/dex1/right/cmd", MotorCmds_)
        self.right_pub.Init()
        
        print(f"Dex1 Gripper Controller initialized on Domain {domain_id}. Waiting for DDS discovery...")
        time.sleep(1.5)  # Give CycloneDDS time to discover the simulator nodes

    def send_command(
        self, 
        side: Literal["left", "right", "both"], 
        position: float, 
        kp: float = 30.0, 
        kd: float = 1.0
    ):
        # Create the outer message
        cmd_msg = MotorCmds_()
        
        # Create the inner motor command
        motor_cmd = unitree_go_msg_dds__MotorCmd_()
        motor_cmd.q = float(position)
        motor_cmd.dq = 0.0          
        motor_cmd.tau = 0.0         
        motor_cmd.kp = float(kp)    
        motor_cmd.kd = float(kd)    

        # Append to the IDL sequence instead of overriding it
        cmd_msg.cmds.append(motor_cmd)

        # Publish
        if side in ["left", "both"]:
            self.left_pub.Write(cmd_msg)
        if side in ["right", "both"]:
            self.right_pub.Write(cmd_msg)

    def open_gripper(self, side: Literal["left", "right", "both"] = "both"):
        print(f"Opening {side} gripper(s)...")
        # Value might need tweaking
        self.send_command(side, position=2.0)

    def close_gripper(self, side: Literal["left", "right", "both"] = "both"):
        print(f"Closing {side} gripper(s)...")
        # Value might need tweaking
        self.send_command(side, position=0.0)


if __name__ == "__main__":
    gripper_controller = Dex1Controller(domain_id=1)
    time.sleep(2.0)

    # Close the grippers
    gripper_controller.close_gripper()
    time.sleep(10.0)

    # Open the left gripper
    gripper_controller.open_gripper(side="left")
    time.sleep(10.0)

    # Close the left gripper and open the right gripper
    gripper_controller.close_gripper(side="left")
    gripper_controller.open_gripper(side="right")
    time.sleep(10.0)
    

