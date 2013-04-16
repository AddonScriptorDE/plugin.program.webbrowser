#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import subprocess
import xbmcplugin
import xbmcaddon
import xbmcgui

pluginhandle = int(sys.argv[1])
addonID = 'plugin.program.webbrowser'
addon = xbmcaddon.Addon(id=addonID)
translation = addon.getLocalizedString
isWin = xbmc.getCondVisibility('system.platform.windows')
userDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID)
browserPath = xbmc.translatePath('special://home/addons/'+addonID+'/resources/XBMC_WebBrowser/XBMC_WebBrowser.exe')
keyMapperPath = xbmc.translatePath('special://home/addons/'+addonID+'/resources/XBMC_WebBrowser/XBMC_WebBrowser_KeyMapper.exe')
siteFolder = os.path.join(userDataFolder, 'sites')
minMouseSpeed = addon.getSetting("minimumMouseSpeed")
maxMouseSpeed = addon.getSetting("maximumMouseSpeed")
magnifierWidth = addon.getSetting("magnifierWidth")

if not os.path.isdir(userDataFolder):
    os.mkdir(userDataFolder)
if not os.path.isdir(siteFolder):
    os.mkdir(siteFolder)


def index():
    files = os.listdir(siteFolder)
    for file in files:
        fh = open(os.path.join(siteFolder, file), 'r')
        title = ""
        url = ""
        thumb = ""
        zoom = ""
        stopPlayback = "yes"
        showPopups = "no"
        for line in fh.readlines():
            spl = line.split("=")
            if spl[0] == "title":
                title = spl[1].strip()
            elif spl[0] == "url":
                url = spl[1].strip()
            elif spl[0] == "thumb":
                thumb = spl[1].strip()
            elif spl[0] == "zoom":
                zoom = spl[1].strip()
            elif spl[0] == "stopPlayback":
                stopPlayback = spl[1].strip()
            elif spl[0] == "showPopups":
                showPopups = spl[1].strip()
        fh.close()
        addSiteDir(title, url, 'showSite', thumb, zoom, stopPlayback, showPopups)
    addDir("- "+translation(30001), "", 'addSite', "")
    addDir("- "+translation(30005), "", 'mapKeys', "")
    xbmcplugin.endOfDirectory(pluginhandle)


def addSite():
    keyboard = xbmc.Keyboard('', translation(30003))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        title = keyboard.getText()
        keyboard = xbmc.Keyboard('http://', translation(30004))
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            url = keyboard.getText()
            content = "title="+title+"\nurl="+url+"\nthumb=DefaultFolder.png\nzoom=100\nstopPlayback=yes\nshowPopups=no"
            fh = open(os.path.join(siteFolder, title+".link"), 'w')
            fh.write(content)
            fh.close()
    xbmc.executebuiltin("Container.Refresh")


def showSite(url, zoom, stopPlayback, showPopups):
    if isWin:
        subprocess.Popen(browserPath+' "'+userDataFolder+'" '+urllib.quote_plus(url)+' '+zoom+' '+showPopups+' '+minMouseSpeed+' '+maxMouseSpeed+' '+magnifierWidth, shell=False)
    else:
        subprocess.Popen("wine "+browserPath+' "'+userDataFolder+'" '+urllib.quote_plus(url)+' '+zoom+' '+showPopups+' '+minMouseSpeed+' '+maxMouseSpeed+' '+magnifierWidth, shell=True)
    if stopPlayback == "yes":
        xbmc.Player().stop()


def removeSite(title):
    os.remove(os.path.join(siteFolder, title+".link"))
    xbmc.executebuiltin("Container.Refresh")


def editSite(title):
    file = os.path.join(siteFolder, title+".link")
    fh = open(file, 'r')
    title = ""
    url = ""
    thumb = "DefaultFolder.png"
    zoom = "100"
    stopPlayback = "yes"
    showPopups = "no"
    for line in fh.readlines():
        spl = line.split("=")
        if spl[0] == "title":
            title = spl[1].strip()
        elif spl[0] == "url":
            url = spl[1].strip()
        elif spl[0] == "thumb":
            thumb = spl[1].strip()
        elif spl[0] == "zoom":
            zoom = spl[1].strip()
        elif spl[0] == "stopPlayback":
            stopPlayback = spl[1].strip()
        elif spl[0] == "showPopups":
            showPopups = spl[1].strip()
    fh.close()

    keyboard = xbmc.Keyboard(title, translation(30003))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        title = keyboard.getText()
        keyboard = xbmc.Keyboard(url, translation(30004))
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            url = keyboard.getText()
            keyboard = xbmc.Keyboard(zoom, translation(30008))
            keyboard.doModal()
            if keyboard.isConfirmed() and keyboard.getText():
                zoom = keyboard.getText()
                keyboard = xbmc.Keyboard(stopPlayback, translation(30009))
                keyboard.doModal()
                if keyboard.isConfirmed() and keyboard.getText():
                    stopPlayback = keyboard.getText()
                    keyboard = xbmc.Keyboard(showPopups, translation(30010))
                    keyboard.doModal()
                    if keyboard.isConfirmed() and keyboard.getText():
                        showPopups = keyboard.getText()
                        content = "title="+title+"\nurl="+url+"\nthumb="+thumb+"\nzoom="+zoom+"\nstopPlayback="+stopPlayback+"\nshowPopups="+showPopups
                        fh = open(os.path.join(siteFolder, title+".link"), 'w')
                        fh.write(content)
                        fh.close()
    xbmc.executebuiltin("Container.Refresh")


def mapKeys():
    if isWin:
        subprocess.Popen(keyMapperPath+' "'+userDataFolder+'"', shell=False)
    else:
        subprocess.Popen("wine "+keyMapperPath+' "'+userDataFolder+'"', shell=True)


def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict


def addDir(name, url, mode, iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+urllib.quote_plus(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addSiteDir(name, url, mode, iconimage, zoom, stopPlayback, showPopups):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+urllib.quote_plus(mode)+"&zoom="+urllib.quote_plus(zoom)+"&stopPlayback="+urllib.quote_plus(stopPlayback)+"&showPopups="+urllib.quote_plus(showPopups)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.addContextMenuItems([(translation(30006), 'RunPlugin(plugin://'+addonID+'/?mode=editSite&url='+urllib.quote_plus(name)+')',), (translation(30002), 'RunPlugin(plugin://'+addonID+'/?mode=removeSite&url='+urllib.quote_plus(name)+')',)])
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
zoom = urllib.unquote_plus(params.get('zoom', '100'))
stopPlayback = urllib.unquote_plus(params.get('stopPlayback', 'yes'))
showPopups = urllib.unquote_plus(params.get('showPopups', 'no'))

if mode == 'addSite':
    addSite()
elif mode == 'showSite':
    showSite(url, zoom, stopPlayback, showPopups)
elif mode == 'removeSite':
    removeSite(url)
elif mode == 'editSite':
    editSite(url)
elif mode == 'mapKeys':
    mapKeys()
else:
    index()
