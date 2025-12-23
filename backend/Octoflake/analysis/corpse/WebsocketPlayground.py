from  pixelblaze import Pixelblaze, PixelblazeEnumerator
import time


print()
pb = Pixelblaze("192.168.0.118")

print(pb.connected)


pbList = PixelblazeEnumerator()
print("Testing: PixelblazeEnumerator object created -- listening for Pixelblazes")
time.sleep(2)
print("Available Pixelblazes: ", pbList.getPixelblazeList())


organs = [
    "ExquisiteCorpse_Heart",
    "ExquisiteCorpse_Brain",
    "ExquisiteCorpse_Angler",
    "ExquisiteCorpse_Lungs"
]





for ip in pbList.getPixelblazeList():
    pass



pb.setBrightness(.1)
pb.waitForEmptyQueue(1000)

print(pb.connected)

print(pb.getHardwareConfig())


exit()