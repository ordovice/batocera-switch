from abc import ABCMeta, abstractmethod
import subprocess

class Generator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate(self, system, rom, playersControllers, gameResolution):
        pass

    def getResolutionMode(self, config):
        return config['videomode']

    def getMouseMode(self, config, rom=None):
        # Check if /usr/bin/batocera-version exists
        if subprocess.call(['which', 'batocera-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            return False
        else:
            # Get batocera version and compare
            process = subprocess.Popen(['batocera-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if process.returncode == 0 and out:
                version = int(out.decode('utf-8').strip()[:2])
                if version >= 39 and rom is not None:
                    return False
            return False

    def executionDirectory(self, config, rom):
        return None

    # mame or libretro have internal bezels, don't display the one of mangohud
    def supportsInternalBezels(self):
        return False

    # mangohud must be called by the generator itself (wine based emulator for example)
    def hasInternalMangoHUDCall(self):
        return False

    def getInGameRatio(self, config, gameResolution, rom):
        # put a default value, but it should be overridden by generators
        return 4/3
