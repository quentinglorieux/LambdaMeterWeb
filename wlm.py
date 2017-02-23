"""
Module to work with Angstrom WS7 wavelength meter
"""

import ctypes, os, sys, random, time

class WavelengthMeter:

    def __init__(self, dllpath="C:\Windows\System32\wlmData.dll", debug=False):
        """
        Wavelength meter class.
        Argument: Optional path to the dll. Default: "C:\Windows\System32\wlmData.dll"
        """
        self.channels = []
        self.dllpath = dllpath
        self.debug = debug
        if not debug:
            self.dll = ctypes.WinDLL(dllpath)
            self.dll.GetWavelengthNum.restype = ctypes.c_double
            self.dll.GetFrequencyNum.restype = ctypes.c_double
            self.dll.GetSwitcherMode.restype = ctypes.c_long

    def GetExposureMode(self):
        if not self.debug:
            return (self.dll.GetExposureMode(ctypes.c_bool(0))==1)
        else:
            return True

    def SetExposureMode(self, b):
        if not self.debug:
            return self.dll.SetExposureMode(ctypes.c_bool(b))
        else:
            return 0

    def GetWavelength(self, channel=1):
        if not self.debug:
            return self.dll.GetWavelengthNum(ctypes.c_long(channel), ctypes.c_double(0))
        else:
            return round(100*channel + 180.03300 + int(random.uniform(0,100)) / 10000.0, 4)

    def GetFrequency(self, channel=1):
        if not self.debug:
            return self.dll.GetFrequencyNum(ctypes.c_long(channel), ctypes.c_double(0))
        else:
            return 38434900

    def GetAll(self):
        return {
            "debug": self.debug,
            "wavelength": self.GetWavelength(),
            "frequency": self.GetFrequency(),
            "exposureMode": self.GetExposureMode()
        }

    @property
    def wavelengths(self):
        return [self.GetWavelength(i) for i in range(1,9)]

    @property
    def wavelength(self):
        return self.GetWavelength(1)

    @property
    def switcher_mode(self):
        if not self.debug:
        	return self.dll.GetSwitcherMode(ctypes.c_long(0))
        else:
            return 0

    @switcher_mode.setter
    def switcher_mode(self, mode):
        if not self.debug:
        	self.dll.SetSwitcherMode(ctypes.c_long(int(mode)))
        else:
            pass

if __name__ == '__main__':

    debug_mode = ('--debug' in sys.argv)

    wlm = WavelengthMeter(debug=debug_mode)

    for i, l in enumerate(wlm.wavelengths):
        print("Wavelength at channel %d:\t%.4f nm" % (i+1, l))

    old_mode = wlm.switcher_mode

    wlm.switcher_mode = True

    print(wlm.wavelengths)
    time.sleep(0.1)
    print(wlm.wavelengths)

    wlm.switcher_mode = old_mode

