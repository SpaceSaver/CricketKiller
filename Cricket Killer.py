from __future__ import unicode_literals

import os
import sys
from time import sleep
import PySimpleGUI as sg
from ppadb.client import Client as AdbClient


# This bit gets the taskbar icon working properly in Windows
if sys.platform.startswith('win'):
    import ctypes
    # Make sure Pyinstaller icons are still grouped
    if sys.argv[0].endswith('.exe') == False:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation') # Arbitrary string


def resource_path(relative_path=""):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        relative_path = relative_path.split('/')[-1]
    except AttributeError:
        base_path = os.path.dirname(os.path.realpath(__file__)) + "\\res\\"

    return os.path.join(base_path, relative_path)


def device_authorization_check(device):
    try:
        device.get_state()
        return True
    except RuntimeError:
        return False


window = sg.Window("Cricket Killer", [[sg.Text("This application will disable the bloatware installer \"Mobile Services\" "
                                               "from your Cricket device.")],
                                      [sg.Text("Cricket Killer is not responsible for any harm to come to your device "
                                               "while using this software.")],
                                      [sg.Text("Use is AT YOUR OWN RISK!")],
                                      [sg.Text("Would you like to continue?")],
                                      [sg.Button("Yes"), sg.Button("No")]],
                   icon=r"{}".format(resource_path("favicon.ico")))
event, values = window.read()
window.close()
if event in (sg.WIN_CLOSED, 'No'):
    window = sg.Window("Cricket Killer",
                       [[sg.Text("Maybe next time...")]],
                       no_titlebar=True,
                       icon=r"{}".format(resource_path("favicon.ico")))
    window.read(timeout=1000)
    window.close()
    sys.exit()

# gif1 = open(resource_path("usb debugging.gif"), "rb").read()\
print(resource_path()[:-1])
os.system("cd \"{}\" && adb start-server".format(resource_path()[:-1]))
client = AdbClient(host="127.0.0.1", port=5037)
print("Your ADB server version is {}.".format(client.version()))
devices = client.devices()
gif1 = []
for x in range(773):
    gif1.append(open(resource_path("debug/{}.png".format(x+1)), "rb").read())
if len(devices) == 0:
    window = sg.Window("Cricket Killer",
                       [[sg.Text("Please connect your Cricket (🦗) device to the computer and ensure that "
                                 "ADB debugging is enabled."),
                         sg.Image(data=gif1[0], key='-IMAGE-')]],
                       icon=resource_path('favicon.ico'))
x = 1
lgif1 = len(gif1)
while len(devices) == 0:
    event, values = window.read(timeout=15)
    print("run")
    if event == sg.WIN_CLOSED:
        os.system("adb kill-server")
        window.close()
        sys.exit()
    if x >= lgif1:
        x = 0
    window['-IMAGE-'].update(data=gif1[x])
    x += 1
    devices = client.devices()
window.close()
del gif1
if not device_authorization_check(devices[0]):
    window = sg.Window("Cricket Killer",
                       [[sg.Text("Check your phone to authorize this computer for \"USB Debugging\" "
                                 "which allows us to be able to disable Cricket's app (Mobile Services) that's been installing "
                                 "bloatware on your phone."),
                         sg.Image(data=open(resource_path('Authorize.png'), "rb").read())]],
                       icon=resource_path("favicon.ico"))
while not device_authorization_check(devices[0]):
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED:
        os.system("adb kill-server")
        window.close()
        sys.exit()
window.close()
window = sg.Window("Cricket Killer",
                   [[sg.Text("Disabling app...")]],
                   icon=resource_path('favicon.ico'),
                   no_titlebar=True)
window.read(timeout=1)
devices[0].shell("pm disable-user --user 0 com.dti.cricket")
window.close()
window = sg.Window("Cricket Killer",
                   [[sg.Text("App disabled!")],
                    [sg.Text("Enjoy your phone!")],
                    [sg.Button("Yay!")]],
                   icon=resource_path('favicon.ico'),
                   no_titlebar=True)
os.system("cd \"{}\" && adb kill-server".format(resource_path()[:-1]))
window.read()
window.close()
