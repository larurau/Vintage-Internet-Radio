import usb.core
import usb.util

class MouseDevice:
    def __init__(self, id_vendor, id_product):

        #vendor and product values
        self.dev = usb.core.find(idVendor=id_vendor, idProduct=id_product)
        if self.dev is None:
            raise ValueError("Device not found")

        # first endpoint
        self.interface = 0
        self.endpoint = self.dev[0][(0,0)][0]

        # detach device, if the OS kernel already claimed the device
        # http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
        if self.dev.is_kernel_driver_active(self.interface) is True:
            self.dev.detach_kernel_driver(self.interface)
            usb.util.claim_interface(self.dev, self.interface)

    def read_movement(self):
        while True: 
            try:
                data = self.dev.read(self.endpoint.bEndpointAddress,self.endpoint.wMaxPacketSize)
                velocity = int(data[2])
                if data[3] == 255:
                    velocity = (velocity-256)
                
                return velocity
                
            except usb.core.USBError as e:
                if e.args == ('Operation timed out',):
                    continue

    def close(self):
        # release the device
        usb.util.release_interface(self.dev, self.interface)
        # reattach the device to the OS kernel
        self.dev.attach_kernel_driver(self.interface)