#!/usr/bin/env python

import generators

# not the nicest way, possibly one of the faster i think
# some naming rules may allow to modify this function to less than 10 lines

from generators.yuzu.yuzuMainlineGenerator import YuzuMainlineGenerator	
from generators.yuzuearlyaccess.yuzuearlyaccessGenerator import YuzuEarlyAccessGenerator	
from generators.ryujinx.ryujinxMainlineGenerator import RyujinxMainlineGenerator	

def getGenerator(emulator):

    if emulator == 'yuzu':
        generators.yuzu.yuzuMainlineGenerator import YuzuMainlineGenerator	
        return YuzuMainlineGenerator()

    if emulator == 'yuzu-early-access':
        from generators.yuzuearlyaccess.yuzuearlyaccessGenerator import YuzuEarlyAccessGenerator
        return YuzuEarlyAccessGenerator()

    if emulator == 'ryujinx':
        from generators.ryujinx.ryujinxMainlineGenerator import RyujinxMainlineGenerator
        return RyujinxMainlineGenerator()

    if emulator == 'ryujinx-avalonia':
        from generators.ryujinx.ryujinxMainlineGenerator import RyujinxMainlineGenerator
        return RyujinxMainlineGenerator()

    raise Exception(f"no generator found for emulator {emulator}")
