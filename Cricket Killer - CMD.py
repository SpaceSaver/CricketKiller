from __future__ import unicode_literals

import os
import sys
from time import sleep

from ppadb.client import Client as AdbClient

print("This application will disable the bloatware installer \"Mobile Services\" from your Cricket device."
      "\nCricket Killer is not responsible for any harm to come to your device while using this software."
      "\nUse is AT YOUR OWN RISK!")
if input("Would you like to continue?  y or n?") == "n":
    print("Maybe next time...")
    sleep(1)
    sys.exit()


def resource_path(relative_path=""):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        relative_path = relative_path.split('/')[-1]
    except AttributeError:
        if sys.platform.startswith('linux'):
            base_path = os.path.dirname(os.path.realpath(__file__)) + "/res-Linux/"
        else:
            base_path = os.path.dirname(os.path.realpath(__file__)) + "/res/"

    return os.path.join(base_path, relative_path)


def device_authorization_check(device):
    try:
        device.get_state()
        return True
    except RuntimeError:
        return False


print(resource_path()[:-1])
if sys.platform.startswith('linux'):
    os.system('chmod +x \"' + resource_path('adb') + '\"')
if sys.platform.startswith('win'):
    adbloc = resource_path('adb.exe')
else:
    adbloc = resource_path('adb')
os.system("cd \"{}\" && \"{}\" start-server".format(resource_path()[:-1], adbloc))
client = AdbClient(host="127.0.0.1", port=5037)
print("Your ADB server version is {}.".format(client.version()))
devices = client.devices()
if len(devices) == 0:
    print("Please connect your Cricket (🦗) device and ensure that ADB debugging is enabled.")
while len(devices) == 0:
    devices = client.devices()
    sleep(1)
if not device_authorization_check(devices[0]):
    print("Check your phone to authorize this computer for \"USB Debugging\" which allows us to be able to disable "
          "Cricket's app (Mobile Services) that's been installing bloatware on your phone.")
while not device_authorization_check(devices[0]):
    sleep(1)
print("Disabling app...")
devices[0].shell("pm disable-user --user 0 com.dti.cricket")
print("App disabled!\nEnjoy your phone!")
os.system("cd \"{}\" && \"{}\" kill-server".format(resource_path()[:-1], adbloc))
sleep(5)
print("Bye!")
