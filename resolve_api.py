import os
import sys
from sys import platform

# Import davinci resolve api module
import DaVinciResolveScript as dvr_script

# Set environment variables for davinci resolve api
if platform == "linux" or platform == "linux2":
    # linux
    RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
    PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"

elif platform == "darwin":
    # OS X
    RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"

elif platform == "win32":
    # print(f"platform is windows: {platform}")
    sys.path.append("C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscripts")
    os.environ["PYTHONPATH"] = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscripts"
    os.environ["RESOLVE_SCRIPT_API"] = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscripts"

