#
# Imports
#
from BeautifulSoup import BeautifulSoup
from worldstarhiphop_const import __addon__, __settings__, __language__, __images_path__, __date__, __version__
from worldstarhiphop_utils import HTTPCommunicator
import os
import re
import sys
import urllib, urllib2
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
	#
	# Init
	#
	def __init__( self ) :
		# Get plugin settings
		self.DEBUG = __settings__.getSetting('debug')
		self.VIDEO = __settings__.getSetting('video')		
		
		if (self.DEBUG) == 'true':
			xbmc.log( "[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % ( __addon__, __version__, __date__, "ARGV", repr(sys.argv), "File", str(__file__) ), xbmc.LOGNOTICE )

		# Parse parameters...
		if len(sys.argv[2]) == 0:
			self.plugin_category = __language__(30000)
			self.video_list_page_url = "http://www.worldstarhiphop.com/videos/rss.php"
			self.next_page_possible = "False"
		else:
			self.plugin_category = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['plugin_category'][0]
			self.video_list_page_url = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['url'][0]
			self.next_page_possible = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['next_page_possible'][0]
		
		if self.next_page_possible == 'True':
		# Determine current item number, next item number, next_url
			pos_of_page		 			 	 = self.video_list_page_url.rfind('?page=')
			if pos_of_page >= 0:
				page_number_str			     = str(self.video_list_page_url[pos_of_page + len('?page='):pos_of_page + len('?page=') + len('000')])
				page_number					 = int(page_number_str)
				page_number_next			 = page_number + 1
				if page_number_next >= 100:
					page_number_next_str = str(page_number_next)
				elif page_number_next >= 10:
					page_number_next_str = '0' + str(page_number_next)
				else:				
					page_number_next_str = '00' + str(page_number_next)
				self.next_url = str(self.video_list_page_url).replace(page_number_str, page_number_next_str)
			
				if (self.DEBUG) == 'true':
					xbmc.log( "[ADDON] %s v%s (%s) debug mode, %s = %s" % ( __addon__, __version__, __date__, "self.next_url", str(urllib.unquote_plus(self.next_url)) ), xbmc.LOGNOTICE )
	
		#
		# Get the videos...
		#
		self.getVideos()

	
	#
	# Get videos...
	#
	def getVideos( self ) :
		#
		# Init
		#
		titles_and_thumbnail_urls_index = 0
		
		# 
		# Get HTML page...
		#
		html_source = HTTPCommunicator().get( self.video_list_page_url )

		# Parse response...
		soup = BeautifulSoup( html_source )
		
		# Get the items from the RSS feed
		# <item>
		#         <title>Sesame Street Doing ODB&amp;#039;s &amp;quot;Shimmy Shimmy YA&amp;quot;!</title>
		#         <link>http://www.worldstarhiphop.com/videos/video.php?v=wshh25oOXRG2R4jG2YAC</link>
		#         <description>
		#         <![CDATA[
		#         <table width="80%" border="0" cellspacing="0" cellpadding="0">
		#           <tr>
		#                 <td width=20%>
		#                 <img src="http://hw-static.worldstarhiphop.com/u/pic/2015/06/Vo4cwPN7Dbau.jpg" width="80" height="80" />
		#                 </td>
		#                 <td width=80% valign=top>By isthishowyougoviral</td>
		#           </tr>
		#         </table>
		#         ]]></description>
		# </item>
		#Sesame Street Doing ODB's "Shimmy Shimmy YA"!
		items = soup.findAll('item')
				
		if (self.DEBUG) == 'true':
			xbmc.log( "[ADDON] %s v%s (%s) debug mode, %s = %s" % ( __addon__, __version__, __date__, "len(items)", str(len(items)) ), xbmc.LOGNOTICE )
			
		for item in items :
			item_string = str(item)
			start_pos_url = item_string.find('http://www.worldstarhiphop.com/videos/video.php?v=' , 0)
			end_pos_url = start_pos_url + len ('http://www.worldstarhiphop.com/videos/video.php?v=') + len("wshh25oOXRG2R4jG2YAC")
			video_url = item_string[start_pos_url:end_pos_url]
			video_page_url = video_url
			
			if (self.DEBUG) == 'true':
				xbmc.log( "[ADDON] %s v%s (%s) debug mode, %s = %s" % ( __addon__, __version__, __date__, "video_url", str(video_url) ), xbmc.LOGNOTICE )

			#Get thumbnail url
			item_string = str(item)
			start_pos_url = item_string.find('http://hw-static.worldstarhiphop.com' , 0)
			end_pos_url = item_string.find('"' , start_pos_url)
			thumbnail_url = item_string[start_pos_url:end_pos_url]
						
			if (self.DEBUG) == 'true':
				xbmc.log( "[ADDON] %s v%s (%s) debug mode, %s = %s" % ( __addon__, __version__, __date__, "thumbnail_url", str(thumbnail_url) ), xbmc.LOGNOTICE )
	
			#Get title	
			title = item.title.string
			title = title.encode('utf-8')
			title = title.replace('-',' ')
			title = title.replace('/',' ')
			title = title.replace('&amp;#039;',"'")
  			title = title.replace('&amp;quot;','"')
			title = title.replace("&#039;","'")
  			title = title.replace('&amp;amp;','&')
			title = title.replace(' i ',' I ')
			title = title.replace(' ii ',' II ')
			title = title.replace(' iii ',' III ')
			title = title.replace(' iv ',' IV ')
			title = title.replace(' v ',' V ')
			title = title.replace(' vi ',' VI ')
			title = title.replace(' vii ',' VII ')
			title = title.replace(' viii ',' VIII ')
			title = title.replace(' ix ',' IX ')
			title = title.replace(' x ',' X ')
			title = title.replace(' xi ',' XI ')
			title = title.replace(' xii ',' XII ')
			title = title.replace(' xiii ',' XIII ')
			title = title.replace(' xiv ',' XIV ')
			title = title.replace(' xv ',' XV ')
			title = title.replace(' xvi ',' XVI ')
			title = title.replace(' xvii ',' XVII ')
			title = title.replace(' xviii ',' XVIII ')
			title = title.replace(' xix ',' XIX ')
			title = title.replace(' xx ',' XXX ')
			title = title.replace(' xxi ',' XXI ')
			title = title.replace(' xxii ',' XXII ')
			title = title.replace(' xxiii ',' XXIII ')
			title = title.replace(' xxiv ',' XXIV ')
			title = title.replace(' xxv ',' XXV ')
			title = title.replace(' xxvi ',' XXVI ')
			title = title.replace(' xxvii ',' XXVII ')
			title = title.replace(' xxviii ',' XXVIII ')
			title = title.replace(' xxix ',' XXIX ')
			title = title.replace(' xxx ',' XXX ')
			title = title.replace('  ',' ')
			title = title.replace('  ',' ')
			
			if (self.DEBUG) == 'true':
				xbmc.log( "[ADDON] %s v%s (%s) debug mode, %s = %s" % ( __addon__, __version__, __date__, "title", str(title) ), xbmc.LOGNOTICE )
							
			# Add to list...
			parameters = {"action" : "play", "video_page_url" : video_page_url}
			url = sys.argv[0] + '?' + urllib.urlencode(parameters)
			listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
			listitem.setInfo( "video", { "Title" : title, "Studio" : "WorldWideHipHop" } )
			folder = False
			xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ] ), url = url, listitem=listitem, isFolder=folder)

		# Next page entry...
		if self.next_page_possible == 'True':
			parameters = {"action" : "list", "plugin_category" : self.plugin_category, "url" : str(self.next_url), "next_page_possible": self.next_page_possible}
			url = sys.argv[0] + '?' + urllib.urlencode(parameters)
			listitem = xbmcgui.ListItem (__language__(30503), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(__images_path__, 'next-page.png'))
			folder = True
			xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ] ), url = url, listitem=listitem, isFolder=folder)
			
		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )