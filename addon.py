##############################################################################
#
# WorldStarHipHop - Addon for XBMC
# http://worldstarhiphop.com/
#
# Coding by Skipmode A1
# 
# Credits:
#   * Dan Dar3                                   - Gamespot xbmc plugin [http://dandar3.blogspot.com]
#   * Worldstarhiphop                                                   [http://worldstarhiphop.com/]
#   * Team XBMC @ XBMC.org                                              [http://xbmc.org/]
#   * Leonard Richardson <leonardr@segfault.org> - BeautifulSoup 3.0.7a [http://www.crummy.com/software/BeautifulSoup/]
#

# 
# Constants
#
#also in ..._const
__addon__       = "plugin.video.worldstarhiphop"
__date__        = "01 july 2015"
__version__     = "1.0.1"

#
# Imports
#
import os
import re
import sys
import urllib
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

BASEURL = "http://www.worldstarhiphop.com"

LIB_DIR = xbmc.translatePath( os.path.join( xbmcaddon.Addon(id=__addon__).getAddonInfo('path'), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

# Get plugin settings
DEBUG = xbmcaddon.Addon(id='plugin.video.worldstarhiphop').getSetting('debug')

if (DEBUG) == 'true':
    xbmc.log( "[ADDON] %s v%s (%s) is starting, ARGV = %s" % ( __addon__, __version__, __date__, repr(sys.argv) ), xbmc.LOGNOTICE )

# Parse parameters...
if len(sys.argv[2]) == 0:
    #
    # Main menu
    #
    import worldstarhiphop_list as plugin
else:
    action = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['action'][0]
    #
    # List
    #
    if action == 'list':
        import worldstarhiphop_list as plugin
    #
    # Play
    #
    elif action == 'play':
        import worldstarhiphop_play as plugin
    #
    # Search
    #
    elif action == 'search':
        import worldstarhiphop_search as plugin  

plugin.Main() 