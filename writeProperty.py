import asyncio
from bacpypes3.app import Application
from bacpypes3.local.device import DeviceObject
from bacpypes3.local.networkport import NetworkPortObject
from bacpypes3.pdu import Address
from bacpypes3.apdu import WritePropertyRequest
from bacpypes3.primitivedata import Real
from bacpypes3.constructeddata import Any


DEVICE_IP = "192.168.1.97"
LOCAL_NIC = "192.168.1.100"
OBJ = ("analogOutput", 1) 
PROP = "presentValue" 
VALUE = 95



async def main(): 
# Define local BACnet device
    device = DeviceObject( 
            objectIdentifier=("device", 1001), 
            objectName="ClientWriter", 
            maxApduLengthAccepted=1024, 
            segmentationSupported="noSegmentation", 
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


    app = Application.from_object_list([device, netport])

    request = WritePropertyRequest( 
        objectIdentifier=OBJ, 
        propertyIdentifier=PROP, 
        propertyValue=Any(Real(VALUE)), 
        destination=Address(DEVICE_IP), 
        )    

    iocb = app.request(request)

    await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())


