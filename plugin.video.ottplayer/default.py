#############Imports###################
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import os,sys,urllib,re,base64,datetime,time
from datetime import date
from resources.modules import tools
#0.0.7#################################

import requests
import xbmcvfs
import urllib.parse

#############Defined Strings#############
ADDONTITLE	= 'Ottplayer'
addon_id	= 'plugin.video.ottplayer'
icon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/', 'icon.png'))
fanart		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/', 'fanart.jpg'))

accounticon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'account.png'))
livetvicon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'livetv.png'))
vodicon			= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'vod.png'))
seriesicon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'tv.png'))
currenticon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'current.png'))
allowedicon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'allowed.png'))
usericon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'user.png'))
passicon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'pass.png'))
dateicon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'date.png'))
statusicon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'status.png'))
searchicon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'search.png'))
settingsicon	= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'settings.png'))
dataicon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'meta.png'))
xxxicon			= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'xxx.png'))
cacheicon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'clear.png'))
advancedicon	= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'eas.png'))
speedicon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'speed.png'))
logouticon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'logout.png'))
catchupicon		= xbmcvfs.translatePath(os.path.join('special://home/addons/' + addon_id +'/resources/icons/', 'catchup.png'))

username	= xbmcaddon.Addon().getSetting('Username')
password	= xbmcaddon.Addon().getSetting('Password')

host	    = xbmcaddon.Addon().getSetting('Host')
port	    = xbmcaddon.Addon().getSetting('Port')

player_api	= '%s:%s/player_api.php?username=%s&password=%s'%(host,port,username,password)

advanced_settings			= xbmcvfs.translatePath('special://home/addons/'+addon_id+'/resources/advanced_settings')
advanced_settings_target	= xbmcvfs.translatePath(os.path.join('special://home/userdata','advancedsettings.xml'))

########################################

def start():
	user = xbmcaddon.Addon().getSetting('Username')
	passw = xbmcaddon.Addon().getSetting('Password')
	url = '%s:%s/player_api.php?username=%s&password=%s'%(host,port,user,passw)
	try:
		data = requests.get(url).json()
		if 'status' in data['user_info']:
			username = xbmcaddon.Addon().getSetting('Username')
			password = xbmcaddon.Addon().getSetting('Password')
			home()
	except:
		msg = "[B][COLOR lime]Por favor ingrese los detalles de inicio de sesion[/COLOR][/B]"
		xbmcgui.Dialog().ok('Attention', msg)
		user = xbmcgui.Dialog().input("Please Enter Username")
		passw = xbmcgui.Dialog().input("Please Enter Password")
		url = '%s:%s/player_api.php?username=%s&password=%s'%(host,port,user,passw)
		try:
			data = requests.get(url).json()
			if 'status' in data['user_info']:
				msg = "Login Successful\nWelcome to %s\n[B][COLOR orange]%s[/COLOR][/B]"%(ADDONTITLE,user)
				xbmcgui.Dialog().ok('Login', msg)
				xbmcaddon.Addon().setSetting('Username',user)
				xbmcaddon.Addon().setSetting('Password',passw)
				xbmc.executebuiltin('Container.Refresh')
				addonsettings('ADS2','')
				xbmc.executebuiltin('Container.Refresh')
				home()
		except:
			msg = "[B][COLOR red]Login Details Incorrect[/COLOR][/B]\n\nTry Again or Exit?"
			dialog = xbmcgui.Dialog()
			ret = dialog.yesno('Attention', msg, 'Try Again', 'Exit')
			if ret == True:
				xbmcaddon.Addon().setSetting('Username','')
				xbmcaddon.Addon().setSetting('Password','')
				xbmc.executebuiltin('ActivateWindow(Videos,addons://sources/video/)')
				xbmc.executebuiltin('Container.Refresh')
			else:
				start()


def home():
	url = '%s:%s/player_api.php?username=%s&password=%s&action=get_live_streams'%(host,port,username,password)
	catchup = ''
	live = ''
	try:
		data = requests.get(url).json()
		for a in data:
			tv_archive = a['tv_archive']
			if tv_archive == 1:
				catchup = True
			stream_type = a['stream_type']
			if stream_type == 'live':
				live = True
	except:pass
	if live == True:
		addDir('[B][COLOR lime]Canales de television[/COLOR][/B]','url',22,livetvicon,fanart,'Live Channels')
		live = ''
	url = '%s:%s/player_api.php?username=%s&password=%s&action=get_vod_streams'%(host,port,username,password)
	vod = ''
	try:
		data = requests.get(url).json()
		for a in data:
			stream_type = a['stream_type']
			if stream_type == 'movie':
				vod = True
	except:pass
	if vod == True:
		addDir('[B][COLOR lime]Peliculas[/COLOR][/B]','url',42,vodicon,fanart,'Movies')
		vod = ''
	url = '%s:%s/player_api.php?username=%s&password=%s&action=get_series'%(host,port,username,password)
	series = ''
	try:
		data = requests.get(url).json()
		for a in data:
				if a['series_id']:
					series = True
	except:pass
	if series == True:
		addDir('[B][COLOR lime]Series de tv[/COLOR][/B]','url',52,seriesicon,fanart,'TV Shows')
		series = ''
#	addDir('[B][COLOR white]Search[/COLOR][/B]','url',6,seriesicon,fanart,'Search')
	if catchup == True:
		addDir('[B][COLOR white]Catch Up TV[/COLOR][/B]','url',8,catchupicon,fanart,'Catch Up TV')
		catchup = ''
	addDir('[B][COLOR red]Configuraciones[/COLOR][/B]','url',7,settingsicon,fanart,'Tools')
	expiry = account_info('expiry')
	expiry = '[B][COLOR orange]Fecha de termino : %s[/COLOR][/B]' % (str(expiry))
	addDir(expiry,'url',1,accounticon,fanart,'Expiry Date')


def get_live_streams_all():#[21]
	url = '%s:%s/player_api.php?username=%s&password=%s&action=get_live_streams'%(host,port,username,password)
	data = requests.get(url).json()
	for a in data:
		stream_type = a['stream_type']
		stream_id = a['stream_id']
		name = a['name']
		thumb = a['stream_icon'] or ''
		fanart = ''
		short_epg = ''
		url1 = '%s:%s/%s/%s/%s/%s.ts'%(host,port,stream_type,username,password,stream_id)
		if xbmcaddon.Addon().getSetting('hidexxx')=='true':
			addDir(name,url1,999,livetvicon,fanart,str(short_epg))
		else:
			if not 'XXX' in name:
				if not 'Adult' in name:
					addDir(name,url1,999,livetvicon,fanart,str(short_epg))
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def get_live_categories():#[22]
	live_url = '%s:%s/player_api.php?username=%s&password=%s&action=get_live_categories'%(host,port,username,password)
	data = requests.get(live_url).json()
	addDir('[B][COLOR lime]Buscar canales por su nombre[/COLOR][/B]','LIVE',29,livetvicon,fanart,'Live Categories')
	#addDir('[B][COLOR grey]All Live Channels[/COLOR][/B]','LIVE',21,livetvicon,fanart,'Live Categories')
	for a in data:
		cat_id = a['category_id']
		name ='[B][COLOR orange]%s[/COLOR][/B]' % (a['category_name'])
		parent_id = a['parent_id']
		url1 = '%s:%s/player_api.php?username=%s&password=%s&action=get_live_streams&category_id=%s'%(host,port,username,password,cat_id)
		if xbmcaddon.Addon().getSetting('hidexxx')=='true':
			addDir(name,url1,23,livetvicon,fanart,'Live Categories','')
		else:
			if not 'XXX' in name:
				if not 'Adult' in name:
					addDir(name,url1,23,livetvicon,fanart,'Live Categories','')


def get_live_streams_category(url):#[23]
	data = requests.get(url).json()
	for a in data:
		num = a['num']
		name = a['name']
		stream_type = a['stream_type']
		thumb = a['stream_icon']
		stream_id = a['stream_id']
		short_epg = name
		url1 = '%s:%s/%s/%s/%s/%s.ts'%(host,port,stream_type,username,password,stream_id)
		if xbmcaddon.Addon().getSetting('hidexxx')=='true':
			addDir(name,url1,999,thumb,fanart,'test','')
		else:
			if not 'XXX' in name:
				if not 'Adult' in name:
					addDir(name,url1,999,thumb,fanart,'test','')

 
def search_live():#[29]
	text = xbmcgui.Dialog().input("Buscar")
	if not text:
		xbmcgui.Dialog().notification('Search Live','[COLOR orange][B]Search is Empty[/B][/COLOR]', xbmcgui.NOTIFICATION_ERROR, 4000)
		return
	url = '%s:%s/player_api.php?username=%s&password=%s&action=get_live_streams'%(host,port,username,password)
	data = requests.get(url).json()
	for a in data:
		stream_type = a['stream_type']
		stream_id = a['stream_id']
		name = a['name']
		thumb = a['stream_icon'] or ''
		fanart = ''
		short_epg = ''
		if text.lower() in name.lower():
			url1 = '%s:%s/%s/%s/%s/%s.ts'%(host,port,stream_type,username,password,stream_id)
			addDir(name,url1,999,thumb,fanart,str(short_epg))
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def get_short_epg(stream_id,limit):
	url_epg = '%s:%s/player_api.php?username=%s&password=%s&action=get_short_epg&stream_id=%s&limit=%s'%(host,port,username,password,stream_id,limit)
	data = requests.get(url_epg).json()
	now_next=[]
	for x in range(0, len(data['epg_listings'])):
		title = '[COLOR cyan]%s[/COLOR]' % (base64.b64decode(data['epg_listings'][x]['title']).decode('utf-8'))
		description = base64.b64decode(data['epg_listings'][x]['description']).decode('utf-8')
		startHM = data['epg_listings'][x]['start_timestamp']
		startHM = '[B][COLOR yellow]%s[/COLOR][/B]' % (datetime.datetime.fromtimestamp(int(startHM)).strftime('%H:%M'))
		now_next.append(startHM)
		now_next.append(title)
		now_next.append('\n')
		now_next.append(description)
		now_next.append('\n')
	str1 = " "
	return (str1.join(now_next))


def get_vod_streams_all():#[41]
	url = '%s:%s/player_api.php?username=%s&password=%s&action=get_vod_streams'%(host,port,username,password)
	data = requests.get(url).json()
	for a in data:
		if a['name']:
			name = a['name']
		else:
			name = 'No Name'
		stream_type = a['stream_type']
		stream_id = a['stream_id']
		container_extension = a['container_extension']
		if a['stream_icon']:
			iconimage = a['stream_icon']
		else:
			iconimage = ''
		rating = a['rating']
		rating_5based = a['rating_5based']
		description = '\n\n[B][COLOR cyan]Ratings:[/COLOR][/B] %s (%s/5)'%(str(rating),rating_5based)
		if xbmcaddon.Addon().getSetting('meta') == 'true':
			url1 = str(stream_id)
			if xbmcaddon.Addon().getSetting('hidexxx')=='true':
				addDir(name,url1,44,iconimage,fanart,description)
			else:
				if not 'XXX' in name:
					if not 'Adult' in name:
						addDir(name,url1,44,iconimage,fanart,description)
		else:
			url1 = '%s:%s/%s/%s/%s/%s.%s'%(host,port,stream_type,username,password,stream_id,container_extension)
			if xbmcaddon.Addon().getSetting('hidexxx')=='true':
				addDir(name,url1,99,iconimage,fanart,description)
			else:
				if not 'XXX' in name:
					if not 'Adult' in name:
						addDir(name,url1,99,iconimage,fanart,description)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def get_vod_categories():#[42]
	url = '%s:%s/player_api.php?username=%s&password=%s&action=get_vod_categories'%(host,port,username,password)
	data = requests.get(url).json()
	addDir('[B][COLOR lime]Buscar pelicula por su nombre[/COLOR][/B]','VOD',49,vodicon,fanart,'Movie Categories')
	#addDir('[B][COLOR grey]Cargar todas las peliculas[/COLOR][/B]','VOD',41,vodicon,fanart,'Movie Categories')
	for a in data:
		name = '[B][COLOR orange]%s[/COLOR][/B]' % (a['category_name'])
		cat_id = a['category_id']
		url1 = '%s:%s/player_api.php?username=%s&password=%s&action=get_vod_streams&category_id=%s'%(host,port,username,password,cat_id)
		description = 'Movie Categories'
		if xbmcaddon.Addon().getSetting('hidexxx')=='true':
			addDir(name,url1,43,vodicon,fanart,description)
		else:
			if not 'XXX' in name:
				if not 'Adult' in name:
					addDir(name,url1,43,vodicon,fanart,description)


def get_vod_streams_by_catagory(url):#[43]
	data = requests.get(url).json()
	for a in data:
		if a['name']:
			name = a['name']
		else:
			name = 'No Name!'
		stream_type = a['stream_type']
		stream_id = a['stream_id']
		container_extension = a['container_extension']
		if a['stream_icon']:
			iconimage = a['stream_icon']
		else:
			iconimage = ''
		rating = a['rating']
		rating_5based = a['rating_5based']
		description = '\n\n[B][COLOR cyan]Ratings:[/COLOR][/B] %s (%s/5)'%(str(rating),rating_5based)
		if xbmcaddon.Addon().getSetting('meta') == 'true':
			url1 = str(stream_id)
			if xbmcaddon.Addon().getSetting('hidexxx')=='true':
				addDir(name,url1,44,iconimage,fanart,description)
			else:
				if not 'XXX' in name:
					if not 'Adult' in name:
						addDir(name,url1,44,iconimage,fanart,description)
		else:
			url1 = '%s:%s/%s/%s/%s/%s.%s'%(host,port,stream_type,username,password,stream_id,container_extension)
			if xbmcaddon.Addon().getSetting('hidexxx')=='true':
				addDir(name,url1,99,iconimage,fanart,description)
			else:
				if not 'XXX' in name:
					if not 'Adult' in name:
						addDir(name,url1,99,iconimage,fanart,description)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def get_vod_info(stream_id):#[44]
	url_info = '%s:%s/player_api.php?username=%s&password=%s&action=get_vod_info&vod_id=%s'%(host,port,username,password,stream_id)
	data = requests.get(url_info).json()
	stream_type = 'movie'
	stream_id = data['movie_data']['stream_id']
	container_extension = data['movie_data']['container_extension']
	url1 = '%s:%s/%s/%s/%s/%s.%s'%(host,port,stream_type,username,password,stream_id,container_extension)
	if not data['info'].get('name'):
		name = data['movie_data']['name']
	else:
		name = data['info']['name']
	if not data['info'].get('movie_image'):
		thumb = ''
	else:
		thumb = data['info']['movie_image']
	if not data['info'].get('plot'):
		plot = ''
	else:
		plot = data['info']['plot']
	if not data['info'].get('director'):
		director = ''
	else:
		director = data['info']['director']
		
	if not data['info'].get('cast'):
		cast = ''
	else:
		cast = data['info']['cast']
		
	if not data['info'].get('rating'):
		ratin = ''
	else:
		ratin = data['info']['rating']
	if not data['info'].get('releasedate'):
		year = ''
	else:
		year = data['info']['releasedate']
	if not data['info'].get('genre'):
		genre = ''
	else:
		genre = data['info']['genre']
	if not data['info'].get('duration_secs'):
		runt = ''
	else:
		runt = data['info']['duration_secs']
	if not data['info'].get('tmdb_id'):
		tmdb_id = ''
	else:
		tmdb_id = data['info']['tmdb_id']
	if data['info'].get('backdrop'):
		fanart = data['info']['backdrop'].split('\r\n')[0]
	elif data['info'].get('backdrop_path'):
		fanart = data['info']['backdrop_path'][0]
	else:
		fanart = ''
	addDirMeta(str(name),url1,99,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(director).split(','),str(cast).split(','),ratin,runt,genre)


def search_vod():#[49]
	text = xbmcgui.Dialog().input("Buscar")
	if not text:
		xbmcgui.Dialog().notification('Search Movies','[COLOR orange][B]Search is Empty[/B][/COLOR]', xbmcgui.NOTIFICATION_ERROR, 4000)
		return
	url = '%s:%s/player_api.php?username=%s&password=%s&action=get_vod_streams'%(host,port,username,password)
	data = requests.get(url).json()
	for a in data:
		name = a['name'] or ''
		stream_type = a["stream_type"] or ''
		stream_id = a["stream_id"] or ''
		container_extension = a["container_extension"] or ''
		iconimage = a["stream_icon"] or ''
		description = 'Search Movies'
		if text.lower() in name.lower():
			if xbmcaddon.Addon().getSetting('meta') == 'true':
				url1 = str(stream_id)
				addDir(name,url1,44,iconimage,fanart,description)
			else:
				url1 = '%s:%s/%s/%s/%s/%s.%s'%(host,port,stream_type,username,password,stream_id,container_extension)
				addDir(name,url1,99,iconimage,fanart,description)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def get_series_streams_all():#[51]
	url = '%s:%s/player_api.php?username=%s&password=%s&action=get_series'%(host,port,username,password)
	data = requests.get(url).json()
	for a in data:
		series_id = a['series_id']
		url1 = '%s:%s/player_api.php?username=%s&password=%s&action=get_series_info&series_id=%s'%(host,port,username,password,series_id)
		name = a['name']
		thumb = a['cover'] or ''
		plot = a['plot']
		director = a['director']
		cast = a['cast']
		ratin = a['rating']
		year = a['releaseDate']
		runt = a['episode_run_time']
		genre = a['genre']
		if not a['backdrop_path']:
			fanart = fanart
		else:
			fanart = a['backdrop_path'][0]
		if xbmcaddon.Addon().getSetting('hidexxx')=='true':
			addDirMeta(str(name),url1,54,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(director).split(','),str(cast).split(','),ratin,runt,genre)
		else:
			if not 'XXX' in name:
				if not 'Adult' in name:
					addDirMeta(str(name),url1,54,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(director).split(','),str(cast).split(','),ratin,runt,genre)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def get_series_categories():#[52]
	series_url = '%s:%s/player_api.php?username=%s&password=%s&action=get_series_categories'%(host,port,username,password)
	data = requests.get(series_url).json()
	addDir('[B][COLOR lime]Buscar series por su titulo[/COLOR][/B]','SERIES',59,seriesicon,fanart,'TV Show Categories')
	#addDir('[B][COLOR grey]Cargar todas las series[/COLOR][/B]','SERIES',51,seriesicon,fanart,'TV Show Categories')
	for a in data:
		name = '[B][COLOR orange]%s[/COLOR][/B]' % (a['category_name'])
		cat_id = a['category_id']
		url1 = '%s:%s/player_api.php?username=%s&password=%s&action=get_series&category_id=%s'%(host,port,username,password,cat_id)
		description = 'TV Show Categories'
		if xbmcaddon.Addon().getSetting('hidexxx')=='true':
			addDir(name,url1,53,seriesicon,fanart,description)
		else:
			if not 'XXX' in name:
				if not 'Adult' in name:
					addDir(name,url1,53,seriesicon,fanart,description)


def get_series_by_category(url):#[53]
	data = requests.get(url).json()
	for a in data:
		name = a['name']
		series_id = a['series_id']
		url1 = '%s:%s/player_api.php?username=%s&password=%s&action=get_series_info&series_id=%s'%(host,port,username,password,series_id)
		thumb = a['cover']
		if not a['backdrop_path']:
			fanart = ''
		else:
			fanart = a['backdrop_path'][0]
		plot = a['plot']
		year = a['releaseDate']
		director = a['director']
		cast = a['cast']
		rating = a['rating']
		runt = a['episode_run_time']
		genre = a['genre']
		if xbmcaddon.Addon().getSetting('hidexxx')=='true':
			addDirMeta(str(name),url1,54,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(director).split(','),str(cast).split(','),rating,runt,genre)
		else:
			if not 'XXX' in name:
				if not 'Adult' in name:
					addDirMeta(str(name),url1,54,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(director).split(','),str(cast).split(','),rating,runt,genre)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def get_series_info(url):#[54]
	data = requests.get(url).json()
	try:
		for season in data['episodes']:
			name = '%s : Season %s' %(data['info']['name'],season)
			for episode in data['episodes'][season]:
				if 'plot' in episode['info']:
					if episode['info']['plot']:
						plot = episode['info']['plot']
					else:
						plot = ''
				else:
					plot = ''
				if not data['info']['backdrop_path']:
					fanart = ''
				else:
					fanart = data['info']['backdrop_path'][0]
				director = data['info']['director']
				cast = data['info']['cast']
				if 'rating' in episode['info']:
					rating = episode['info']['rating']
				else:
					rating = ''
				if 'duration_secs' in episode['info']:
					runt = episode['info']['duration_secs']
				else:
					runt = ''
				year = data['info']['releaseDate']
				genre = data['info']['genre']
				thumb = data['info']['cover']
				season_number = season
				xtra = season
				url1 = url
			if xbmcaddon.Addon().getSetting('hidexxx')=='true':
				addDirMeta(str(name),url1,55,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(director).split(','),str(cast).split(','),rating,runt,genre,xtra)
			else:
				if not 'XXX' in name:
					if not 'Adult' in name:
						addDirMeta(str(name),url1,55,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(director).split(','),str(cast).split(','),rating,runt,genre,xtra)
	except:pass


def get_series_episodes(url,season):#[55]
	data = requests.get(url).json()
	try:
		for item in data['episodes'][season]:
			stream_id = item['id']
			container_extension = item['container_extension']
			stream_type = 'series'
			name = item['title']
			url1 = '%s:%s/%s/%s/%s/%s.%s'%(host,port,stream_type,username,password,stream_id,container_extension)
			if not data['info']['backdrop_path']:
				fanart = ''
			else:
				fanart = data['info']['backdrop_path'][0]
			if 'movie_image' in item['info']:
				if item['info']['movie_image']:
					thumb = item['info']['movie_image']
				else:
					thumb = fanart
			else:
				thumb = ''
			if 'plot' in item['info']:
				plot = item['info']['plot']
			elif 'overview' in item['info']:
				plot = item['info']['overview']
			else:
				plot = ''
			if 'crew' in item['info']:
				cast = item['info']['crew']
			elif 'cast' in data['info']:
				cast = data['info']['cast']
			else:
				cast = ''
			if 'releasedate' in item['info']:
				year = item['info']['releasedate']
			elif 'release_date' in item['info']:
				year = item['info']['release_date']
			else:
				year = ''
			director = data['info']['director']
			rating = data['info']['rating']
			runt = item['info']['duration_secs']
			genre = data['info']['genre']
			if xbmcaddon.Addon().getSetting('hidexxx')=='true':
				addDirMeta(str(name),url1,99,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(director).split(','),str(cast).split(','),rating,runt,genre)
			else:
				if not 'XXX' in name:
					if not 'Adult' in name:
						addDirMeta(str(name),url1,99,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(director).split(','),str(cast).split(','),rating,runt,genre)
	except:pass


def search_series():#[59]
	text = xbmcgui.Dialog().input("Buscar")
	if not text:
		xbmcgui.Dialog().notification('Search TV Shows','[COLOR orange][B]Search is Empty[/B][/COLOR]', xbmcgui.NOTIFICATION_ERROR, 4000)
		return
	url = '%s:%s/player_api.php?username=%s&password=%s&action=get_series'%(host,port,username,password)
	data = requests.get(url).json()
	for a in data:
		series_id = a['series_id']
		name = a['name']
		thumb = a['cover'] or ''
		plot = a['plot']
		director = a['director']
		cast = a['cast']
		ratin = a['rating']
		year = a['releaseDate']
		runt = a['episode_run_time']
		genre = a['genre']
		if not a['backdrop_path']:
			fanart = fanart
		else:
			fanart = a['backdrop_path'][0]
		if text.lower() in name.lower():
			url1 = '%s:%s/player_api.php?username=%s&password=%s&action=get_series_info&series_id=%s'%(host,port,username,password,series_id)
			addDirMeta(str(name),url1,54,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(director).split(','), str(cast).split(','),ratin,runt,genre)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)


def catchup_channels():#[8]
	url = '%s:%s/player_api.php?username=%s&password=%s&action=get_live_streams'%(host,port,username,password)
	data = requests.get(url).json()
	for a in data:
		tv_archive = a['tv_archive']
		name ='[B][COLOR white]%s[/COLOR][/B]' % (a['name'])
		stream_id = a['stream_id']
		xtra =  a['stream_id']
		url1 = '%s:%s/player_api.php?username=%s&password=%s&action=get_simple_data_table&stream_id=%s'%(host,port,username,password,stream_id)
		if tv_archive == 1:
			if xbmcaddon.Addon().getSetting('hidexxx')=='true':
				addDir(name,url1,81,catchupicon,fanart,'Catch Up Channels',xtra)
			else:
				if not 'XXX' in name:
					if not 'Adult' in name:
						addDir(name,url1,81,catchupicon,fanart,'Catch Up Channels',str(xtra))


def catchup_programs(url,stream_id):#[81]
	days = 7
	now = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','')
	catchup_start_date = datetime.datetime.now() - datetime.timedelta(days)
	date = str(catchup_start_date)
	date = str(date).replace('-','').replace(':','').replace(' ','')
	data = requests.get(url).json()
	for a in data['epg_listings']:
		channel_id = (a['channel_id']).upper().replace('.',' - ')
		title = base64.b64decode(a['title']).decode('utf-8')
		start = a['start']
		end = a['end']
		description = base64.b64decode(a['description']).decode('utf-8')
		description = '[B]%s[/B]\n[COLOR cyan]%s[/COLOR]\n%s' % (channel_id,title,description)
		format = '%Y-%m-%d %H:%M:%S'
		has_archive = a['has_archive']
		if has_archive == 1:
			try:
				modend = dtdeep.strptime(end, format)
				modstart = dtdeep.strptime(start, format)
			except:
				modend = datetime.datetime(*(time.strptime(end, format)[0:6]))
				modstart = datetime.datetime(*(time.strptime(start, format)[0:6]))
			StreamDuration = modend - modstart
			modend_ts = time.mktime(modend.timetuple())
			modstart_ts = time.mktime(modstart.timetuple())
			FinalDuration = int(modend_ts-modstart_ts) / 60
			strstart = start
			Realstart = str(strstart).replace('-','').replace(':','').replace(' ','')
			start2 = start[:-3]
			editstart = start2
			start2 = str(start2).replace(' ',' - ')
			start = str(editstart).replace(' ',':')
			Editstart = start[:13] + '-' + start[13:]
			final_start = (start[:13] + '-' + start[13:]).replace('-:','-')
			if Realstart > date:
				if Realstart < now:
					url1 = '%s:%s/streaming/timeshift.php?username=%s&password=%s&stream=%s&start=%s&duration=%s'%(host,port,username,password,stream_id,final_start,FinalDuration)
					name = "[COLOR yellow]%s[/COLOR] | %s"%(start2,title)
					if xbmcaddon.Addon().getSetting('hidexxx')=='true':
						addDir(name,url1,99,catchupicon,fanart,description)
					else:
						if not 'XXX' in name:
							if not 'Adult' in name:
								addDir(name,url1,99,catchupicon,fanart,description)


########################################

def stream_video(stream_url):#[99][999]
	text = '/live/'
	description = ''
	if text.lower() in stream_url.lower():
		stream_id = stream_url.split('/')[-1].split('.')[0]
		limit = 2
		try:
			description = str(get_short_epg(stream_id,limit))
		except:pass
	try:
		resp = requests.post(url=stream_url,allow_redirects=False)
		url = resp.headers["location"]
	except:
		url = stream_url
	liz = xbmcgui.ListItem()
	liz.setArt({'icon': iconimage, 'thumb': iconimage})
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(url))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


def sub_menu_live():
	addDir('[B][COLOR white]Live Channels[/COLOR][/B]','url',22,livetvicon,fanart,'Live Channels')
	addDir('[B][COLOR white]Search Live Channels[/COLOR][/B]','url',29,searchicon,fanart,'Search Live Channels')


def sub_menu_vod():
	addDir('[B][COLOR white]All Movies[/COLOR][/B]','vod',41,vodicon,fanart,'All Movies')
	addDir('[B][COLOR white]Movie Categories[/COLOR][/B]','vod',42,vodicon,fanart,'Movie Categories')
	addDir('[B][COLOR white]Search Movies[/COLOR][/B]','url',49,searchicon,fanart,'Search Movies')


def sub_menu_series():
	addDir('[B][COLOR white]All TV Shows[/COLOR][/B]',url,51,seriesicon,fanart,'All TV Shows')
	addDir('[B][COLOR white]TV Show Categories[/COLOR][/B]',url,52,seriesicon,fanart,'TV Show Categories')
	addDir('[B][COLOR white]Search TV Shows[/COLOR][/B]',url,59,searchicon,fanart,'Search TV Shows')


def sub_menu_search():
	addDir('[B][COLOR white]Search Live Channels[/COLOR][/B]','url',29,searchicon,fanart,'Search Live Channels')
	addDir('[B][COLOR white]Search Movies[/COLOR][/B]','url',49,searchicon,fanart,'Search Movies')
	addDir('[B][COLOR white]Search TV Shows[/COLOR][/B]',url,59,searchicon,fanart,'Search TV Shows')


def sub_menu_tools():
	if xbmcaddon.Addon().getSetting('meta')=='true':
		META = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		META = '[B][COLOR red]OFF[/COLOR][/B]'
	if xbmcaddon.Addon().getSetting('epg')=='true':
		EPG = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		EPG = '[B][COLOR red]OFF[/COLOR][/B]'
	if xbmcaddon.Addon().getSetting('hidexxx')=='true':
		XXX = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		XXX = '[B][COLOR red]OFF[/COLOR][/B]'
	addDir('[B][COLOR white]Detalles de la cuenta[/COLOR][/B]','url',1,accounticon,fanart,'Account Details')
	addDir('[B][COLOR white]Metadatos de peliculas[/COLOR][/B] %s'%META,'META',10,dataicon,fanart,META)
	addDir('[B][COLOR white]Canales para adultos[/COLOR][/B] %s'%XXX,'XXX',10,xxxicon,fanart,XXX)
	addDir('[B][COLOR white]Limpiar la cahce del servidor[/COLOR][/B]','CC',10,cacheicon,fanart,'Clear Cache')
	addDir('[B][COLOR white]Detalles de la configuracion[/COLOR][/B]','AS',10,settingsicon,fanart,'Add-on Settings')
	addDir('[B][COLOR white]Ajustes del buffering[/COLOR][/B]','ADS',10,advancedicon,fanart,'Edit Advanced Settings')
	addDir('[B][COLOR white]Prueba de velocidad de Internet[/COLOR][/B]','ST',10,speedicon,fanart,'Run a Speed Test')
	addDir('[B][COLOR white]Eliminar la cuenta[/COLOR][/B]','LO',10,logouticon,fanart,'Log Out:\n[COLOR orange]This will remove username and password![/COLOR]')


###################################

def addonsettings(url,description):
	if url =="CC":
		tools.clear_cache()
	elif url =="AS":
		xbmc.executebuiltin('Addon.OpenSettings(%s)'%addon_id)
	elif url =="ADS":
		dialog = xbmcgui.Dialog().select('Editar configuracion avanzada', ['Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','Enable Nvidia Shield AS','Disable AS'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok(ADDONTITLE, 'Configuraciones del buffer creadas')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok(ADDONTITLE, 'Configuraciones del buffer creadas')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok(ADDONTITLE, 'Configuraciones del buffer creadas')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok(ADDONTITLE, 'Configuraciones del buffer creadas')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok(ADDONTITLE, 'Configuraciones del buffer creadas')
		elif dialog==5:
			advancedsettings('remove')
			xbmcgui.Dialog().ok(ADDONTITLE, 'Configuracion avanzadas eliminadas')
	elif url =="ADS2":
		dialog = xbmcgui.Dialog().select('Select Your Device Or Closest To', ['Fire TV Stick ','Fire TV','1GB Ram or Lower','2GB Ram or Higher','Nvidia Shield'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok(ADDONTITLE, 'Configuraciones del buffer creadas')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok(ADDONTITLE, 'Configuraciones del buffer creadas')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok(ADDONTITLE, 'Configuraciones del buffer creadas')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok(ADDONTITLE, 'Configuraciones del buffer creadas')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok(ADDONTITLE, 'Configuraciones del buffer creadas')
	elif url =="tv":
		dialog = xbmcgui.Dialog().select('Select a TV Guide to Setup', ['iVue TV Guide','PVR TV Guide','Both'])
		if dialog==0:
			ivueint()
			xbmcgui.Dialog().ok(ADDONTITLE, 'iVue Integration Complete')
		elif dialog==1:
			pvrsetup()
			xbmcgui.Dialog().ok(ADDONTITLE, 'PVR Integration Complete')
		elif dialog==2:
			pvrsetup()
			ivueint()
			xbmcgui.Dialog().ok(ADDONTITLE, 'PVR & iVue Integration Complete')
	elif url =="ST":
		xbmc.executebuiltin('Runscript("special://home/addons/%s/resources/modules/speedtest.py")' % addon_id)
	elif url =="META":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('meta','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('meta','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="EPG":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('epg','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('epg','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="XXX":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('hidexxx','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('hidexxx','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="LO":
		xbmcaddon.Addon().setSetting('Username','')
		xbmcaddon.Addon().setSetting('Password','')
		xbmc.executebuiltin('ActivateWindow(Videos,addons://sources/video/)')
		xbmc.executebuiltin('Container.Refresh')
	elif url =="UPDATE":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('update','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('update','true')
			xbmc.executebuiltin('Container.Refresh')


def advancedsettings(device):
	if device == 'stick':
		file = open(os.path.join(advanced_settings, 'stick.xml'))
	elif device == 'firetv':
		file = open(os.path.join(advanced_settings, 'firetv.xml'))
	elif device == 'lessthan':
		file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
	elif device == 'morethan':
		file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
	elif device == 'shield':
		file = open(os.path.join(advanced_settings, 'shield.xml'))
	elif device == 'remove':
		os.remove(advanced_settings_target)
	try:
		read = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(read)
		f.close()
	except:
		pass


###################################

def account_info(key):
	url = '%s:%s/player_api.php?username=%s&password=%s'%(host,port,username,password)
	try:
		data = requests.get(url).json()
		active = data['user_info']['active_cons']
		if key == 'expiry':
			expiry = data['user_info']['exp_date']
			expiry = datetime.datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
			expreg = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
			for day,month,year in expreg:
				month = tools.MonthNumToName(month)
				year = re.sub(' -.*?$','',year)
				key = month+' '+day+' - '+year
	except:pass
	return key


def accountinfo():#[1]
	try:
		data = requests.get(player_api).json()
		for a in data['user_info']:
			username = data['user_info']['username']
			password = data['user_info']['password']
			status = data['user_info']['status']
			connects = data['user_info']['max_connections']
			active = data['user_info']['active_cons']
			expiry = data['user_info']['exp_date']
			expiry = datetime.datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
			expreg = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
		for day,month,year in expreg:
			month = tools.MonthNumToName(month)
			year = re.sub(' -.*?$','',year)
			expiry = month+' '+day+' - '+year
		addDir('[B][COLOR red]Estado de la cuenta :[/COLOR][/B] %s'%status,'','',statusicon,fanart,'Account Status')
		addDir('[B][COLOR red]Fecha de termino del servicio:[/COLOR][/B] '+expiry,'','',dateicon,fanart,'Expiry Date')
		addDir('[B][COLOR red]Nombre de usuario :[/COLOR][/B] '+username,'','',usericon,fanart,'Username')
		addDir('[B][COLOR red]Clave de acceso :[/COLOR][/B] '+password,'','',passicon,fanart,'Password')
		addDir('[B][COLOR red]El maximo de equipos que puede conectar son:[/COLOR][/B] '+connects,'','',allowedicon,fanart,'Allowed Connections')
		addDir('[B][COLOR red]Equipos conectados en estos momentos:[/COLOR][/B] '+ active,'','',currenticon,fanart,'Current Connections')
	except:pass


########################################

def addDir(name,url,mode,iconimage,fanart,description,xtra="test_parm"):
	u=sys.argv[0]+"?url="+urllib.parse.quote(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote(name)+"&iconimage="+urllib.parse.quote(iconimage)+"&description="+urllib.parse.quote(description)+"&xtra="+urllib.parse.quote(xtra)
	ok=True
	xbmc.log(str(u))
	liz = xbmcgui.ListItem(name)
	liz.setIsFolder(True)
	liz.setArt({'icon': iconimage, 'thumb': iconimage})
	liz.setProperty('fanart_image', fanart)
	if mode==99:
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	elif mode==999:
		liz.setInfo( type="Video", infoLabels={"Title": name})
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	elif mode==71 or mode==10 or mode==17:
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	elif mode==4 or mode==41 or mode==42 or mode==49:
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	elif mode==5 or mode==51 or mode==52 or mode==59:
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	else:
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory


def addDirMeta(name,url,mode,iconimage,fanart,description,year,director,cast,rating,runtime,genre,xtra="meta"):
	u=sys.argv[0]+"?url="+urllib.parse.quote(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote(name)+"&iconimage="+urllib.parse.quote(iconimage)+"&description="+urllib.parse.quote(description)+"&xtra="+urllib.parse.quote(xtra)
	ok=True
	liz=xbmcgui.ListItem(name)
	liz.setArt({'icon': iconimage, 'thumb': iconimage, 'poster': iconimage, 'banner': fanart})
	liz.setInfo( 'video', {'title': name,'plot':description,'rating':rating,'year':year,'duration':runtime,'director':director,'cast':cast,'genre':genre})
	liz.setProperty('fanart_image', fanart)
	if mode==54 or mode==44 or mode ==55:
		liz.setProperty("IsPlayable","false")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	else:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok
	xbmcplugin.endOfDirectory


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param


########################################

params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
xtra=None

try:
	url=urllib.parse.unquote(params["url"])
except:
	pass
try:
	name=urllib.parse.unquote(params["name"])
except:
	pass
try:
	iconimage=urllib.parse.unquote(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.parse.unquote(params["description"])
except:
	pass
	
try:
	xtra=urllib.parse.unquote(params["xtra"])
except:
	pass


########################################

if mode==None or url==None or len(url)<1:
	xbmcplugin.setContent(int(sys.argv[1]), 'video')
	start()

elif mode==1:
	xbmcplugin.setContent(int(sys.argv[1]), 'video')
	accountinfo()

#############LIVE
elif mode==2:
	xbmcplugin.setContent(int(sys.argv[1]), 'video')
	sub_menu_live()

elif mode==21:
	xbmcplugin.setContent(int(sys.argv[1]), 'video')
	get_live_streams_all()

elif mode==22:
	xbmcplugin.setContent(int(sys.argv[1]), 'video')
	get_live_categories()

elif mode==23:
	xbmcplugin.setContent(int(sys.argv[1]), 'video')
	get_live_streams_category(url)

elif mode==29:
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	search_live()

#############MOVIES
elif mode==4:
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	sub_menu_vod()

elif mode==41:
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	get_vod_streams_all()

elif mode==42:
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	get_vod_categories()

elif mode==43:
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	get_vod_streams_by_catagory(url)

elif mode==44:
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	get_vod_info(url)

elif mode==49:
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	search_vod()

#############SERIES
elif mode==5:
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	sub_menu_series()

elif mode==51:
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	get_series_streams_all()

elif mode==52:
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	get_series_categories()

elif mode==53:
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	get_series_by_category(url)

elif mode==54:
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	get_series_info(url)

elif mode==55:
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	get_series_episodes(url,xtra)

elif mode==59:
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	search_series()

#############
elif mode==6:
	xbmcplugin.setContent(int(sys.argv[1]), 'video')
	sub_menu_search()

#############
elif mode==7:
	xbmcplugin.setContent(int(sys.argv[1]), 'video')
	sub_menu_tools()

#############CATCHUP
elif mode==8:
	xbmcplugin.setContent(int(sys.argv[1]), 'video')
	catchup_channels()

elif mode==81:
	xbmcplugin.setContent(int(sys.argv[1]), 'video')
	catchup_programs(url,xtra)

##############
elif mode==99 or mode==999:
	stream_video(url)

##############
elif mode==100:
	xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=%s)'% url)

elif mode==10:
	addonsettings(url,description)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
