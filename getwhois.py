import asyncio
from bacpypes3.app import Application
from bacpypes3.local.device import DeviceObject
from bacpypes3.local.networkport import NetworkPortObject
from bacpypes3.pdu import Address
from bacpypes3.apdu import WritePropertyRequest
from bacpypes3.primitivedata import Real
from bacpypes3.constructeddata import Any
from bacpypes3.apdu import WhoIsRequest, IAmRequest
from bacpypes3.primitivedata import Unsigned
import threading

LOCAL_NIC = "192.168.1.100/24"


async def main(): 
    # Define local BACnet device
    this_device = DeviceObject(
        objectName='clientOnly',
        objectIdentifier=1000,
        maxApduLengthAccepted=1024,
        segmentationSupported='noSegmentation',
        vendorIdentifier=15,
    )

    # network port object
    netport = NetworkPortObject(
        LOCAL_NIC,
        objectIdentifier=("network-port", 1),
        objectName="NetworkPort-1",
        networkNumber=0,
        networkNumberQuality="configured",
    )



    # Define BACnet/IP application
    app = Application.from_object_list(
        [this_device,
        netport]  # local IP 
    )


    # Handle incoming I-Am responses
    async def indication(apdu):
        if isinstance(apdu, IAmRequest):
            print(f"I-AM from device {apdu.iAmDeviceIdentifier} at {apdu.pduSource}")


    app.indication = indication


    # Send Who-Is broadcast
    async def send_whois():
        print("Sending Who-Is request (broadcast)...")
        whois = WhoIsRequest()
        whois.pduDestination = Address("255.255.255.255")  
        app.request(whois)

    # Run sequence
    # await asyncio.sleep(3)  # brief pause to ensure app is ready
    await send_whois()
    await asyncio.sleep(3)
    # stop_after_delay(5)

print("Running BACpypes... waiting for I-Am responses...")
asyncio.run(main())
print("BACpypes stopped.")
