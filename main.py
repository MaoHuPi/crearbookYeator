import pygame as pg
import json
import asyncio, aiofiles
import math
import random
import time

BASIC_PATH = ''
BACKGROUND_COLOR = (0, 0, 0)
[vw, vh] = [1200, 800]; px = 1
[mx, my] = [-1, -1]; [mLClick, mLClickProcessed] = [False, True]; [mMClick, mMClickProcessed] = [False, True]; [mRClick, mRClickProcessed] = [False, True]; [mDBClick, mDBClickProcessed] = [False, True]
lastClickTime = 0; [lastClickX, lastClickY] = [-1, -1]
keyboardInput = ''
[mWheelX, mWheelY, mWheelZ] = [0, 0, 0]
totalTask = 0; loadingProcess = 0

def generateId():
    text = '0123456789abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choices(text, k=10))
def idList(page):
    return list(map(lambda layer: layer['id'], page))
def parseInput(text):
    text
    textSegmentList = list(text)
    while '\b' in textSegmentList:
        removeIndex = textSegmentList.index('\b')
        textSegmentList.pop(removeIndex)
        if removeIndex-1 >= 0:
            textSegmentList.pop(removeIndex-1)
    return ''.join(textSegmentList)

window = pg.display.set_mode([vw, vh], pg.RESIZABLE)
pg.display.set_caption('Crearbook Yeator')
def createAppIcon():
    def colorFunction(x, y):
        r = math.sqrt(x**2 + y**2)
        if  abs(r - 0.5) <= 0.02:
            return [255, 255, 255, 255]
        elif r > 0.5:
            return [0, 0, 0, 0]
        else:
            value = abs(math.sin(x)+y)/100*255000%255
            return [255-value, value*abs(x)*2, value*abs(y)*2, 255]
    width = 256
    surface = pg.Surface([width, width]).convert_alpha()
    for x in range(int(width)):
        for y in range(int(width)):
            [r, g, b, a] = colorFunction((x - width/2) / width, (y - width/2) / width)
            surface.set_at((x, y), [b, g, r, a])
    return surface
pg.display.set_icon(createAppIcon())
pg.font.init()

# data I/O function
theme = None
async def loadTheme():
    global theme, loadingProcess, totalTask
    totalTask += 1
    async with aiofiles.open(BASIC_PATH + 'data/theme.json', 'r', encoding='utf-8') as file:
        themeData = await file.read()
        theme = json.loads(themeData)
    loadingProcess += 1
project = False
currentPage = 0
def newProject():
    global project
    project = {
        'settings': {
            'pageSize': [5882, 4193], 
            'accessDirectory': './oriAccess/20240911_個人照/', 
            'proxiesImageQuality': 10, 
            'pageShow': 'all'
        }, 
        'pages': [
            [
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front1', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front2', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front3', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front4', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front5', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front6', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front7', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front8', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front9', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front10', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front11', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                # {
                #     'id': generateId(), 
                #     'type': 'full', 
                #     'name': 'front12', 
                #     'imagePath': 'p_29_1.JPG'
                # }, 
                {
                    'id': generateId(), 
                    'type': 'full', 
                    'name': 'background', 
                    'imagePath': 'p_29_1.JPG'
                }
            ]
        ]
    }

# render function
# deltaTime = 0

def createSurface(w, h):
    surface = pg.Surface([w, h]).convert_alpha()
    surface.fill([0, 0, 0, 0])
    return surface
    
textCache = {}
def renderText(content, size, color):
    content = str(content)
    size = int(size)
    id = content + '_s' + str(size)
    if id in textCache:
        return textCache[id]
    else:
        font = pg.font.SysFont('Consolas', size)
        text = font.render(content, False, color)
        textCache[id] = text
        return text
imageCache = {}
def getImage(path, quality):
    path = str(path)
    id = path + '_q' + str(quality)
    if id in imageCache:
        return imageCache[id]
    else:
        image = pg.image.load(path)
        image = pg.transform.scale_by(image, quality/100)
        imageCache[id] = image
        return image
def renderImage(image:pg.Surface, imageRect:pg.Rect, canvasRect:pg.Rect):
    if imageRect.width*imageRect.height > canvasRect.width*canvasRect.height:
        relativeLeft = canvasRect.left-imageRect.left
        relativeTop = canvasRect.top-imageRect.top
        relativeWidth = canvasRect.width
        relativeHeight = canvasRect.height
        horizontalScale = 1/imageRect.width*image.get_width()
        verticalScale = 1/imageRect.height*image.get_height()
        relativeLeft *= horizontalScale; relativeTop *= verticalScale
        relativeWidth *= horizontalScale; relativeHeight *= verticalScale

        cropLeft = math.floor(relativeLeft)
        cropTop = math.floor(relativeTop)
        cropWidth = round(relativeWidth)
        cropHeight = round(relativeHeight)
        croppedImage = pg.Surface([cropWidth, cropHeight]).convert_alpha()
        croppedImage.fill([0, 0, 0, 0])
        croppedImage.blit(image, [0, 0], [cropLeft, cropTop, cropWidth, cropHeight])
        croppedImage = pg.transform.scale(croppedImage, [canvasRect.width, canvasRect.height])

        return croppedImage
    else:
        image = pg.transform.scale(image, [imageRect.width, imageRect.height])
        croppedImage = pg.Surface([canvasRect.width, canvasRect.height]).convert_alpha()
        croppedImage.fill([0, 0, 0, 0])
        croppedImage.blit(image, [imageRect.left - canvasRect.left, imageRect.top - canvasRect.top])
        return croppedImage


def isHover(x, y, rect:pg.Rect):
    return x >= rect.left and x < rect.right and y >= rect.top and y < rect.bottom

def parseLength(string:str):
    for [unit, unitValue] in [
        ['px', px], 
        ['vw', vw], 
        ['vh', vh]
    ]:
        if string.endswith(unit):
            return float(string.replace(unit, ''))*unitValue

toolbar = createSurface(0, 0)
icon = {}
def renderIcon():
    global icon
    def createToolbarIcon(colorFunction):
        width = parseLength(theme['toolbar']['>']['button']['width'])
        height = parseLength(theme['toolbar']['height'])
        minEdge = min(width, height)
        surface = createSurface(width, height)
        for x in range(int(width)):
            for y in range(int(height)):
                colorChannelList = colorFunction((x - width/2) / minEdge, (y - height/2) / minEdge)
                if len(colorChannelList) == 3:
                    [r, g, b] = colorChannelList
                    a = 255
                elif len(colorChannelList) == 4:
                    [r, g, b, a] = colorChannelList
                surface.set_at((x, y), [b, g, r, a])
        return surface
    def designButtonColorFunction(x, y):
        value = math.sqrt(abs(((x/(abs(x)+1))**2) * ((y/(abs(y)+1))**2)))*25500%255
        return [value*min(1, abs(x)), value*min(1, abs(y)), value]
    icon['designButton'] = createToolbarIcon(designButtonColorFunction)
    def pageButtonColorFunction(x, y):
        value = (x**4 + y**4)*25500%255
        return [value*min(1, abs(y)), value, value*min(1, abs(x))]
    icon['pageButton'] = createToolbarIcon(pageButtonColorFunction)
    def renderButtonColorFunction(x, y):
        value = abs(y**2 + (x*math.sin(2*x))**3)*25500%255
        return [value, value*min(1, abs(x)), value*min(1, abs(y))]
    icon['renderButton'] = createToolbarIcon(renderButtonColorFunction)
    def settingsButtonColorFunction(x, y):
        value = abs(math.sqrt(x**2 + y**2)/(math.sqrt(x**2 + y**2)+1) - math.sin(8*math.atan2(y, x)))/10*25500%255
        return [value*min(1, abs(x)), value*min(1, abs(y)), value]
    icon['settingsButton'] = createToolbarIcon(settingsButtonColorFunction)
    def infoButtonColorFunction(x, y):
        value = (math.sinh(x*y - y) / (abs(y)+1))*25500%255
        return [value*min(1, abs(y)), value, value*min(1, abs(x))]
    icon['infoButton'] = createToolbarIcon(infoButtonColorFunction)
    icon['buttonMask'] = createToolbarIcon(lambda x, y: [0, 0, 0, 100])
toolbarOptionList = {
    'designButton': [
        'new design', 
        'open old project', 
        'save current project'
    ], 
    'pageButton': [
        'new page', 
        'sort pages'
        'set page size'
    ], 
    'renderButton': [
        'render clip box', 
        'render preview image', 
        'render final result'
    ], 
    'settingsButton': [
        'pick access directory', 
        'change proxies image quality', 
        'show all / one page at once'
    ], 
    'infoButton': [
        'about us'
    ]
}

toolbarUpdateAsideFlag = False
toolbarUpdateWorkspaceFlag = False
asideUpdateToolbarFlag = False
asideUpdateWorkspaceFlag = False
workspaceUpdateToolbarFlag = False
workspaceUpdateAsideFlag = False

toolbarMenuOpening = False
toolbarUpdateLastFrameFlag = False
def renderToolbar():
    global window, toolbar, icon, toolbarMenuOpening, mLClickProcessed, toolbarUpdateLastFrameFlag, toolbarUpdateAsideFlag, toolbarUpdateWorkspaceFlag
    toolbarUpdateAsideFlag = False
    toolbarUpdateWorkspaceFlag = False
    width = 100*vw
    height = parseLength(theme['toolbar']['height'])
    toolbarRect = pg.Rect(0, 0, 100*vw, height)
    toolbarUpdateFlag = asideUpdateToolbarFlag or workspaceUpdateToolbarFlag
    if isHover(mx, my, toolbarRect) or toolbarMenuOpening != False:
        toolbarUpdateFlag = True
    if toolbar.get_size() != (100*vw, 100*vh):
        toolbarUpdateFlag = True
        toolbar = createSurface(100*vw, 100*vh)
        def createToolbarBackground(colorFunction):
            surface = createSurface(width, height)
            for x in range(int(width)):
                for y in range(int(height)):
                    surface.set_at((x, y), colorFunction((x - width/2) / height, (y - height/2) / height))
            return surface
        def toolbarBackgroundColorFunction(x, y):
            value = abs(x/(abs(x)+1) + y**2)*25500%255
            return [value, value, value, 150]
        icon['toolbarBackground'] = createToolbarBackground(toolbarBackgroundColorFunction)
    if toolbarUpdateFlag or (toolbarUpdateLastFrameFlag and not toolbarUpdateFlag):
        toolbarUpdateLastFrameFlag = toolbarUpdateFlag
        toolbar.fill((0, 0, 0, 0))
        height = parseLength(theme['toolbar']['height'])
        buttonWidth = parseLength(theme['toolbar']['>']['button']['width'])
        pg.draw.rect(toolbar, [0, 0, 0], pg.Rect(0, 0, 100*vw, height))
        toolbar.blit(icon['toolbarBackground'], toolbarRect)
        hoverAnyFlag = False
        for [buttonIndex, buttonName] in enumerate([
            'designButton', 
            'pageButton', 
            'renderButton', 
            'settingsButton', 
            'infoButton'
        ]):
            hoverFlag = False
            buttonRect = pg.Rect(buttonWidth*buttonIndex, 0, buttonWidth, height)
            if isHover(mx, my, buttonRect):
                hoverFlag = True
                hoverAnyFlag = True
            toolbar.blit(icon[buttonName], buttonRect)
            if not hoverFlag and not toolbarMenuOpening == buttonName:
                toolbar.blit(icon['buttonMask'], buttonRect)
            elif hoverFlag and not mLClickProcessed and mLClick:
                mLClickProcessed = True
                toolbarMenuOpening = buttonName
            elif toolbarMenuOpening == buttonName:
                optionPadding = parseLength(theme['toolbar']['>']['option']['padding'])
                optionFontSize = parseLength(theme['toolbar']['>']['option']['font-size'])
                optionTextList = [renderText(optionName, optionFontSize, theme['toolbar']['>']['option']['color']) for optionName in toolbarOptionList[buttonName]]
                optionWidth = max(parseLength(theme['toolbar']['>']['option']['min-width']), *list(map(lambda text: text.get_size()[0], optionTextList))) + optionPadding*2
                optionHeight = parseLength(theme['toolbar']['>']['option']['height'])
                for [optionIndex, optionName] in enumerate(toolbarOptionList[buttonName]):
                    optionRect = pg.Rect(buttonRect.left, buttonRect.bottom + optionHeight*optionIndex, optionWidth, optionHeight)
                    pg.draw.rect(toolbar, theme['toolbar']['>']['option']['#'+buttonName][':hover']['background-color'] if isHover(mx, my, optionRect) else theme['toolbar']['>']['option']['background-color'], optionRect)
                    if optionIndex > 0 : pg.draw.line(toolbar, theme['toolbar']['>']['option']['border-color'], [optionRect.left + optionPadding, optionRect.top], [optionRect.right - optionPadding, optionRect.top])
                    toolbar.blit(optionTextList[optionIndex], [optionRect.left + optionPadding, optionRect.top + optionPadding])
                    if mLClick and not mLClickProcessed:
                        if buttonName == 'designButton':
                            if optionName == 'new design':
                                newProject()
                                toolbarUpdateAsideFlag = True
                                toolbarUpdateWorkspaceFlag = True
                            elif optionName == 'open old project': pass
                            elif optionName == 'save current project': pass
                        elif buttonName == 'pageButton':
                            if optionName == 'new page': pass
                            elif optionName == 'sort pages': pass
                            elif optionName == 'set page size': pass
                        elif buttonName == 'renderButton':
                            if optionName == 'render clip box': pass
                            elif optionName == 'render preview image': pass
                            elif optionName == 'render final result': pass
                        elif buttonName == 'settingsButton':
                            if optionName == 'pick access directory': pass
                            elif optionName == 'change proxies image quality': pass
                            elif optionName == 'show all / one page at once': pass
                        elif buttonName == 'infoButton':
                            if optionName == 'about us': pass

        if not hoverAnyFlag and mLClick:
            toolbarMenuOpening = False

aside = createSurface(0, 0)
asideUpdateLastFrameFlag = False
layerListScrollY = 0
dragScrollbarThumbFlag = False
draggingLayer = False
selectedLayer = False
layerRenameFlag = False
def renderAside():
    global window, aside, asideUpdateLastFrameFlag, asideUpdateToolbarFlag, asideUpdateWorkspaceFlag, mLClickProcessed, mRClickProcessed, mDBClickProcessed, keyboardInput
    global layerListScrollY, dragScrollbarThumbFlag, draggingLayer, selectedLayer, layerRenameFlag
    asideUpdateToolbarFlag = False
    asideUpdateWorkspaceFlag = False
    asideRect = pg.Rect(100*vw - parseLength(theme['aside']['width']), parseLength(theme['toolbar']['height']), parseLength(theme['aside']['width']), 100*vh - parseLength(theme['toolbar']['height']))
    asideUpdateFlag = toolbarUpdateAsideFlag or workspaceUpdateAsideFlag or layerRenameFlag
    if isHover(mx, my, asideRect):
        asideUpdateFlag = True
    if toolbar.get_size() != (100*vw, 100*vh):
        asideUpdateFlag = True
        aside = createSurface(100*vw, 100*vh)
    if asideUpdateFlag or (asideUpdateLastFrameFlag and not asideUpdateFlag):
        asideUpdateLastFrameFlag = asideUpdateFlag
        aside.fill((0, 0, 0, 0))
        pg.draw.rect(aside, theme['aside']['background-color'], asideRect)
        if project != False:
            asidePadding = parseLength(theme['aside']['padding'])

            # tiny view
            tinyViewWidth = asideRect.width - asidePadding*2
            tinyViewHeight = max(min(tinyViewWidth/project['settings']['pageSize'][0]*project['settings']['pageSize'][1], parseLength(theme['aside']['>']['tinyView']['max-height'])), parseLength(theme['aside']['>']['tinyView']['min-height']))
            tinyViewRect = pg.Rect(asideRect.left + asidePadding, asideRect.top + asidePadding, tinyViewWidth, tinyViewHeight)
            pg.draw.rect(aside, theme['aside']['>']['tinyView']['background-color'], tinyViewRect)

            # hr line
            pg.draw.line(aside, theme['aside']['>']['*']['border-color'], [tinyViewRect.left, tinyViewRect.bottom + asidePadding], [tinyViewRect.right, tinyViewRect.bottom + asidePadding])

            # layer button bar
            layerButtonBarHeight = parseLength(theme['aside']['>']['layerButtonBar']['height'])
            layerButtonBarRect = pg.Rect(tinyViewRect.left, asideRect.bottom - asidePadding - layerButtonBarHeight, tinyViewWidth, layerButtonBarHeight)
            pg.draw.rect(aside, theme['aside']['>']['layerButtonBar']['background-color'], layerButtonBarRect)
            pg.draw.line(aside, theme['aside']['>']['*']['border-color'], layerButtonBarRect.topleft, layerButtonBarRect.topright)
            layerButtonList = [
                'full', 
                'clip', 
                'delete'
            ]
            buttonWidth = layerButtonBarRect.width/len(layerButtonList)
            for [buttonIndex, buttonName] in enumerate(layerButtonList):
                buttonRect = pg.Rect(layerButtonBarRect.left + buttonWidth*buttonIndex, layerButtonBarRect.top, buttonWidth, layerButtonBarHeight)
                if buttonIndex > 0 : pg.draw.line(aside, theme['aside']['>']['*']['border-color'], buttonRect.topleft, buttonRect.bottomleft)
                buttonText = renderText(buttonName, parseLength(theme['aside']['>']['layerButtonBar']['font-size']), theme['aside']['>']['layerButtonBar']['color'])
                buttonTextSize = buttonText.get_size()
                aside.blit(buttonText, [buttonRect.left + (buttonRect.width - buttonTextSize[0])/2, buttonRect.top + (buttonRect.height - buttonTextSize[1])/2])
                if isHover(mx, my, buttonRect) and mLClick and (not mLClickProcessed):
                    if buttonName == 'full' or buttonName == 'clip':
                        insertIndex = len(project['pages'][currentPage])
                        if selectedLayer and (selectedLayer in idList(project['pages'][currentPage])):
                            insertIndex = idList(project['pages'][currentPage]).index(selectedLayer) + 1
                        newLayer = {
                            'id': generateId(), 
                            'type': {'full': 'full', 'clip': 'clip'}[buttonName], 
                            'name': 'new {layerType} layer'.format(layerType={'full': 'full', 'clip': 'clip'}[buttonName]), 
                            'imagePath': False
                        }
                        project['pages'][currentPage].insert(insertIndex, newLayer)
                        selectedLayer = newLayer['id']
                        # layerRenameFlag = False
                    elif buttonName == 'delete' and selectedLayer and (selectedLayer in idList(project['pages'][currentPage])):
                        project['pages'][currentPage].pop(idList(project['pages'][currentPage]).index(selectedLayer))
                        if draggingLayer == selectedLayer: draggingLayer = False
                        selectedLayer = False
                    mLClickProcessed = True

            # layer list
            layerListRect = pg.Rect(tinyViewRect.left, tinyViewRect.bottom + asidePadding*2, tinyViewWidth, asideRect.height - tinyViewHeight - layerButtonBarHeight - asidePadding*4)
            layerList = createSurface(layerListRect.width, layerListRect.height)
            pg.draw.rect(aside, theme['aside']['>']['layerList']['background-color'], layerListRect)
            layerHeight = parseLength(theme['aside']['>']['layerList']['>']['layer']['height'])
            layerListScrollY += -mWheelY * 500*deltaTime
            maxLayerListScrollY = layerHeight*len(project['pages'][currentPage]) - layerListRect.height
            layerListScrollY = max(min(layerListScrollY, maxLayerListScrollY), 0)

            scrollbarWidth = parseLength(theme['*']['scrollbar-width'])
            scrollbarRect = pg.Rect(layerListRect.right - scrollbarWidth, layerListRect.top, scrollbarWidth, layerListRect.height)
            pg.draw.rect(aside, theme['*']['scrollbar-color'][1], scrollbarRect)
            scrollbarThumbHeight = scrollbarRect.height*0.05
            scrollbarThumbRect = pg.Rect(scrollbarRect.left, scrollbarRect.top + (scrollbarRect.height - scrollbarThumbHeight)*(layerListScrollY/maxLayerListScrollY), scrollbarRect.width, scrollbarThumbHeight)
            if maxLayerListScrollY > 0:
                pg.draw.rect(aside, theme['*']['scrollbar-color'][0], scrollbarThumbRect)
                if isHover(mx, my, scrollbarThumbRect) and mLClick and not mLClickProcessed:
                    dragScrollbarThumbFlag = True
                    mLClickProcessed = True
                elif mLClick and mLClickProcessed and dragScrollbarThumbFlag:
                    layerListScrollY = (my - scrollbarRect.top) / scrollbarRect.height * maxLayerListScrollY
                    layerListScrollY = max(min(layerListScrollY, maxLayerListScrollY), 0)
                elif not mLClick:
                    dragScrollbarThumbFlag = False

            startIndex = math.floor(layerListScrollY/layerHeight)
            endIndex = startIndex + math.ceil(layerListRect.height/layerHeight) + 1
            if selectedLayer == False:
                layerRenameFlag = False
            for [relativeLayerIndex, layer] in enumerate(project['pages'][currentPage][startIndex:endIndex]):
                layerRectInLayer = pg.Rect(0, -(layerListScrollY%layerHeight) + layerHeight*relativeLayerIndex, layerListRect.width - scrollbarRect.width, layerHeight)
                layerRectInWindow = pg.Rect(layerListRect.left, layerListRect.top - layerListScrollY%layerHeight + layerHeight*relativeLayerIndex, layerRectInLayer.width, layerRectInLayer.height)
                pg.draw.rect(layerList, theme['aside']['>']['layerList']['>']['layer'][':checked']['background-color'] if layer['id'] == selectedLayer else theme['aside']['>']['layerList']['>']['layer']['background-color'], layerRectInLayer)
                if relativeLayerIndex > 0: pg.draw.line(layerList, theme['aside']['>']['*']['border-color'], layerRectInLayer.topleft, layerRectInLayer.topright)
                if layer['id'] == selectedLayer and layerRenameFlag:
                    layerPadding = parseLength(theme['aside']['>']['layerList']['>']['layer']['padding'])
                    pg.draw.line(layerList, theme['aside']['>']['*']['border-color'], [layerRectInLayer.left + layerPadding, layerRectInLayer.bottom - layerPadding], [layerRectInLayer.right - layerPadding, layerRectInLayer.bottom - layerPadding])
                text = renderText('[{layerType}] {layerName}'.format(layerType={'full': 'f', 'clip': 'c'}[layer['type']], layerName=layer['name']), parseLength(theme['aside']['>']['layerList']['>']['layer']['font-size']), theme['aside']['>']['layerList']['>']['layer']['color'])
                layerList.blit(text, [layerRectInLayer.left, layerRectInLayer.top + (layerHeight - text.get_size()[1])/2])

                if isHover(mx, my, layerRectInWindow):
                    if mLClick and not mLClickProcessed:
                        draggingLayer = layer['id']
                        mLClickProcessed = True
                    elif mRClick and not mRClickProcessed:
                        project['pages'][currentPage].pop(idList(project['pages'][currentPage]).index(layer['id']))
                        if selectedLayer == layer['id']: selectedLayer = False
                        if draggingLayer == layer['id']: draggingLayer = False
                        mRClickProcessed = True
                    elif mDBClick and not mDBClickProcessed:
                        layerRenameFlag = True
                        mDBClickProcessed = True
                if mLClick and mLClickProcessed and draggingLayer == layer['id']:
                    targetRelativeLayerIndex = math.floor((my - layerListRect.top + (layerListScrollY%layerHeight) - layerHeight/2) / layerHeight + 0.5)
                    currentIndex = idList(project['pages'][currentPage]).index(layer['id'])
                    targetIndex = max(min(currentIndex - relativeLayerIndex + targetRelativeLayerIndex, len(project['pages'][currentPage])-1), 0)
                    if targetIndex > currentIndex:
                        (project['pages'][currentPage][currentIndex : targetIndex-1])
                        project['pages'][currentPage][currentIndex : targetIndex] = project['pages'][currentPage][currentIndex+1 : targetIndex+1]
                    elif targetIndex < currentIndex:
                        project['pages'][currentPage][targetIndex+1 : currentIndex+1] = project['pages'][currentPage][targetIndex : currentIndex]
                    if targetIndex != currentIndex: project['pages'][currentPage][targetIndex] = layer
                    else:
                        # if selectedLayer != draggingLayer: layerRenameFlag = False
                        selectedLayer = draggingLayer
                if not mLClick:
                    draggingLayer = False
                if layer['id'] == selectedLayer and layerRenameFlag:
                    layer['name'] += keyboardInput
                    keyboardInput = ''
                    layer['name'] = parseInput(layer['name'])
                    if '\n' in layer['name']:
                        layer['name'] = layer['name'].split('\n')[0]
                        layerRenameFlag = False

            aside.blit(layerList, layerListRect.topleft)

workspace = createSurface(0, 0)
workspaceUpdateLastFrameFlag = False
workspaceTranslateX = 0
workspaceTranslateY = 0
workspaceBasicScale = 1; workspaceScale = 1
def renderWorkspace():
    global window, workspace, workspaceUpdateLastFrameFlag, workspaceUpdateToolbarFlag, workspaceUpdateAsideFlag
    global workspaceTranslateX, workspaceTranslateY, workspaceBasicScale, workspaceScale
    workspaceUpdateToolbarFlag = False
    workspaceUpdateAsideFlag = False
    workspaceRect = pg.Rect(0, parseLength(theme['toolbar']['height']), 100*vw - parseLength(theme['aside']['width']), 100*vh - parseLength(theme['toolbar']['height']))
    workspaceUpdateFlag = toolbarUpdateWorkspaceFlag or asideUpdateWorkspaceFlag
    if isHover(mx, my, workspaceRect):
        workspaceUpdateFlag = True
    if toolbar.get_size() != (100*vw, 100*vh):
        workspaceUpdateFlag = True
        workspace = createSurface(100*vw, 100*vh)
    if workspaceUpdateFlag or (workspaceUpdateLastFrameFlag and not workspaceUpdateFlag):
        workspaceUpdateLastFrameFlag = workspaceUpdateFlag
        workspace.fill((0, 0, 0, 0))
        pg.draw.rect(workspace, theme['workspace']['background-color'], workspaceRect)
        if project == False:
            warningText = renderText('Please create or open a project first!', parseLength(theme['workspace']['>']['warning']['font-size']), [255, 255, 255, 100])
            warningTextSize = warningText.get_size()
            workspace.blit(warningText, [workspaceRect.left + (workspaceRect.width - warningTextSize[0])/2, workspaceRect.top + (workspaceRect.height - warningTextSize[1])/2])
        else:
            # set basic scale value
            if project['settings']['pageSize'][1]/project['settings']['pageSize'][0] > workspaceRect.height/workspaceRect.width:
                workspaceBasicScale = workspaceRect.height/project['settings']['pageSize'][1]
            else:
                workspaceBasicScale = workspaceRect.width/project['settings']['pageSize'][0]

            # update translate variable value
            workspaceTranslateX += -mWheelX * 1500*deltaTime
            workspaceTranslateY += mWheelY * 1500*deltaTime
            scaleStep = 1 + 10*deltaTime
            lastWorkspaceScale = workspaceScale
            if mWheelZ != 0:
                workspaceScale *= (scaleStep if mWheelZ == 1 else 1/scaleStep)
                workspaceScale = min(max(workspaceScale, 0.1), 10)
            workspaceTranslateX += mx*(1/workspaceScale - 1/lastWorkspaceScale)/workspaceBasicScale
            workspaceTranslateY += my*(1/workspaceScale - 1/lastWorkspaceScale)/workspaceBasicScale

            # render layer
            for layer in project['pages'][currentPage]:
                image = getImage(project['settings']['accessDirectory'] + layer['imagePath'], project['settings']['proxiesImageQuality'])
                
                imageRect = pg.Rect(workspaceTranslateX*workspaceBasicScale*workspaceScale, workspaceTranslateY*workspaceBasicScale*workspaceScale, project['settings']['pageSize'][0]*workspaceBasicScale*workspaceScale, project['settings']['pageSize'][1]*workspaceBasicScale*workspaceScale)
                image = renderImage(image, imageRect, workspaceRect)

                workspace.blit(image, [workspaceRect.left, workspaceRect.top])

deltaTime = 0
editorState = 'loading'
async def main():
    async def init():
        await loadTheme()
        renderIcon()
        renderWorkspace()
        renderAside()
        renderToolbar()
    
    async def renderLoop():
        global vw, vh, mx, my, mLClick, mLClickProcessed, mMClick, mMClickProcessed, mRClick, mRClickProcessed, mDBClick, mDBClickProcessed, lastClickTime, lastClickX, lastClickY, mWheelX, mWheelY, mWheelZ, keyboardInput
        global layerRenameFlag
        global editorState, loadingProcess, totalTask
        global theme, project
        global window, toolbar, aside, workspace
        global deltaTime
        
        run = True
        lastFrameTime = time.time()
        while run:
            currentTime = time.time()
            deltaTime = currentTime - lastFrameTime
            lastFrameTime = currentTime

            # init new frame
            windowInfo = pg.display.Info()
            window.fill(BACKGROUND_COLOR)
            [currentVw, currentVh] = [windowInfo.current_w / 100, windowInfo.current_h / 100]
            
            # resize handle
            windowResize = False
            if vw != currentVw or vh != currentVh:
                [vw, vh] = [currentVw, currentVh]
                windowResize = True

            # update mouse position
            [mx, my] = pg.mouse.get_pos()
            if pg.mouse.get_focused() == 0:
                [mx, my] = [-1, -1]
            
            # draw frame
            if editorState == 'loading':
                loadingRate = loadingProcess/totalTask if totalTask != 0 else 0
                pg.draw.rect(window, (255, 255, 255), pg.Rect(25*vw, 50*vh - 10*px, 50*vw, 20*px), width=2*px)
                pg.draw.rect(window, (255, 255, 255), pg.Rect(25*vw, 50*vh - 10*px, (50*vw) * loadingRate, 20*px))
                if loadingRate == 1:
                    editorState = 'edit'  
            elif editorState == 'edit':
                renderWorkspace()
                renderAside()
                renderToolbar()
                updateAllComponentFlag = False
                window.fill(theme['window']['background-color'])
                window.blit(workspace, pg.Rect(0, 0, 100*vw, 100*vh))
                window.blit(aside, pg.Rect(0, 0, 100*vw, 100*vh))
                window.blit(toolbar, pg.Rect(0, 0, 100*vw, 100*vh))

            # update new frame
            pg.display.flip()
            
            # event listener
            [mWheelX, mWheelY, mWheelZ] = [0, 0, 0]
            keyboardInput = ''
            for event in pg.event.get(): 
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.KEYDOWN:
                    key = event.key
                    if key == pg.K_q and pg.key.get_mods() & pg.KMOD_CTRL:
                        run = False
                    if not(pg.key.get_mods() & pg.KMOD_CTRL):
                        keyName = pg.key.name(event.key)
                        if pg.key.get_mods() & pg.KMOD_SHIFT:
                            if keyName in '0123456789[]\\-=;\',./`':
                                keyboardInput += {'0': ')', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '[': '{', ']': '}', '\\': '|', '-': '_', '=': '+', ';': ':', '\'': '"', ',': '<', '.': '>', '/': '?', '`': '~'}[keyName]
                            elif keyName in 'abcdefghijklmnopqrstuvwxyz':
                                keyboardInput += keyName.upper()
                        elif keyName in '0123456789[]\\-=;\',./`abcdefghijklmnopqrstuvwxyz':
                            keyboardInput += keyName
                        elif keyName == 'backspace':
                            keyboardInput += '\b'
                        elif keyName == 'return' or keyName == 'enter':
                            keyboardInput += '\n'
                        elif keyName == 'escape':
                            layerRenameFlag = False
                        else: print(keyName)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        layerRenameFlag = False
                        mLClick = True
                        mLClickProcessed = False
                        if currentTime - lastClickTime < 0.3 and mx == lastClickX and my == lastClickY:
                            mDBClick = True
                            mDBClickProcessed = False
                        else:
                            mDBClick = False
                        lastClickTime = currentTime
                        [lastClickX, lastClickY] = [mx, my]
                    elif event.button == 2:
                        layerRenameFlag = False
                        mMClick = True
                        mMClickProcessed = False
                    elif event.button == 3:
                        layerRenameFlag = False
                        mRClick = True
                        mRClickProcessed = False
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        mLClick = False
                    elif event.button == 2:
                        mMClick = False
                    elif event.button == 3:
                        mRClick = False
                elif event.type == pg.MOUSEWHEEL:
                    if pg.key.get_mods() & pg.KMOD_CTRL:
                        mWheelZ = event.y
                    else:
                        [mWheelX, mWheelY] = [event.x, event.y]
            await asyncio.sleep(0.001)
    
    initTask = asyncio.create_task(init())
    renderTask = asyncio.create_task(renderLoop())
    await asyncio.gather(initTask, renderTask)

asyncio.run(main())