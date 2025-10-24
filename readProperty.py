import asyncio
import logging
from bacpypes3.local.device import DeviceObject
from bacpypes3.local.networkport import NetworkPortObject
from bacpypes3.app import Application
from bacpypes3.apdu import ReadPropertyRequest, ReadPropertyACK
from bacpypes3.pdu import Address
from bacpypes3.primitivedata import Real

logging.basicConfig(level=logging.INFO)

# configure here
LOCAL_NIC = "192.168.1.100/24"
DEVICE_IP = "192.168.1.97"
OBJ = ("analogOutput", 1)
PROP = "presentValue"
TIMEOUT = 5

async def main():
    # local device object
    device = DeviceObject(
        objectIdentifier=("device", 1000),
        objectName="MyBACnetDevice",
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

    # build application from object list  (binds link layers / transport)
    try:
        app = Application.from_object_list([device, netport])
    except Exception as e:
        print("Failed to create Application:", e)
        return

    # build and send readProperty
    req = ReadPropertyRequest(objectIdentifier=OBJ, propertyIdentifier=PROP)
    req.pduDestination = Address(DEVICE_IP)

    try:
        result = await asyncio.wait_for(app.request(req), timeout=TIMEOUT)
    except asyncio.TimeoutError:
        print("Timeout waiting for response")
        return
    except Exception as e:
        print("Request failed:", e)
        return

    # helper to extract value from Any/constructed result safely
    def extract_value(ack):
        pv = getattr(ack, "propertyValue", None)
        if pv is None:
            return None
        # try cast_out() first (some versions accept no args)
        try:
            return pv.cast_out(Real)
        except TypeError:
            # cast_out required a class; try to return raw value attribute
            if hasattr(pv, "value"):
                return pv.value
            # fallback: try indexing or repr
            try:
                return pv[0]
            except Exception:
                return repr(pv)

    # handle either direct ACK or IOCB with ioResponse
    if isinstance(result, ReadPropertyACK):
        print("Read value:", extract_value(result))
    elif hasattr(result, "ioResponse") and isinstance(result.ioResponse, ReadPropertyACK):
        print("Read value:", extract_value(result.ioResponse))
    else:
        print("Unexpected result:", result or result.ioError)


if __name__ == "__main__":
    asyncio.run(main())
