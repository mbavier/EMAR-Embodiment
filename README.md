# EMAR-Embodiment
## TODO
* Further expand interfacing with motors for 

## Setup on Surface
1. Downlaod the R+ Manager 2.0 from Robotis website
    (Alternatively intall the VCP Driver from FTDI https://ftdichip.com/drivers/vcp-drivers/)
2. Install the python library included in here with command  "pip install ."
3. Determine the port the Dynamixel is plugged into
    Get more details on how to do this later, currently being done with Dyanmixel Wizard
4. Update the motorInitialize function to have that port, by default it is "COM4"