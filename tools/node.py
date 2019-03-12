#! /usr/bin/env python
# -*- coding : utf-8 -*-
# vim:fenc=utf-8
# name : utils.py
# Copyright (c) 2019 / author : R.O a.k.a last_scene
# since 2019 -
# Distributed under terms of the MIT license.

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future_builtins import map
from future_builtins import filter

import pymel.core as pm
from maya import cmds

import os
import sys
import pathlib

import json

from . import utils as utils


rootpath = os.path.abspath(os.path.dirname("__file__"))


def getAttrDict(node, at, **kwargs):
    """
    """

    attrDic = {}
    attrDic["ln"] = node.attr(at).attrName(longName=1)
    if pm.attributeQuery(node.attr(at).name().split(".")[1], n=node.name(), sn=True) != None:
        attrDic["sn"] = pm.attributeQuery(node.attr(at).name().split(".")[1], n=node.name(), sn=True)
    if pm.attributeQuery(node.attr(at).name().split(".")[1], n=node.name(), nn=True) != None:
        attrDic["nn"] = pm.attributeQuery(node.attr(at).name().split(".")[1], n=node.name(), nn=True)


    attrDic["type"] = node.attr(at).type()

    if node.attr(at).isKeyable():
        attrDic["k"] = 1
    else:
        attrDic["k"] = 0
        attrDic["cb"] = pm.setAttr(node.name() + '.' + at, q=1, cb=1)

    if node.attr(at).type() == "string":
        attrDic["attrflag"] = "dt"
    else:
        attrDic["attrflag"] = "at"

    if node.attr(at).type() != "double3":
        if node.attr(at).getMin() != None:
            attrDic["min"] = node.attr(at).getMin()
        if node.attr(at).getMax() != None:
            attrDic["max"] = node.attr(at).getMax()

    if node.attr(at).type() == "enum":
        attrDic["enum"] = ":".join(node.attr(at).getEnums().keys())

    if node.attr(at).type() != "double3":
        if node.attr(at).type() != "string":
            defaultVal    = pm.attributeQuery(node.attr(at).name().split(".")[1] , n=node.attr(at).name() , listDefault=1)
            attrDic["dv"] = defaultVal[0]
            
    attrDic['value'] = cmds.getAttr(node.name()+ '.' + at)
    print(' export attribute... : ' + at)
    return attrDic


def exportUserDefineAttribute(node='', at='', **kwargs):
    if node == '':
        node = pm.selected()[0]
    if at == '':
        allUser = True

    userDefAttrDic = {}
    if allUser:
        userAttrs = pm.listAttr(node, ud=1)
        print('### ' + node + ' ###' )
        for ua in userAttrs:
            userDefAttrDic[ua] = getAttrDict(node, ua)
    print('# Done!')
    return userDefAttrDic


def exportAttrsToJson(dictonary):
    j_file = json.dumps(dictonary, sort_keys=True, indent=4)
    exportJson(j_file, f=f)


def importAttrsToJson(path):
    f = open('test.json', 'r')
    j_file = json.load(f)


def exportJson(*args, **kwargs):
    directory = utils.getFlag(kwargs, ['directory', 'd'], "")
    auto      = utils.getFlag(kwargs, ['autoName', 'auto'], False)
    filename  = utils.getFlag(kwargs, ['filename', 'f'], "")
    
    if filename == '':
        auto = True

    for j_file in args:
        if auto:
            fp = directory  + 'exportUserAttrs' + '.json'
        else:
            fp = filename
        print(fp)

        try:
            fw = open(fp,'w')
        except:
            raise
        fw.write(j_file)
        print('### > export attribute settings file : ' + os.path.join(directory, fp))
        fw.close()

'''
def importJson(**kwargs):
    inputDir     = getFlag(kwargs, ['directory', 'd'], "")
    jsonFilename = getFlag(kwargs, ['filename', 'f'], "")

    fullpath = os.path.join(inputDir, jsonFilename)

    print(" > Import json file :" + jsonFilename)
    return jsonFilename
'''

def setDictAttr(node, value, attrflag, dv, k, ln, _max, _min, _type, **kwargs):
    cb = utils.getFlag(kwargs, ['channelBox', 'cb'], True)

    if attrflag == 'at':
        pass
    elif attrflag == 'dt':
        pass


def addDictAttr(node, value, attrflag, dv, k, ln, _max, _min, _type, sn , nn, **kwargs):
    sn = utils.getFlag(kwargs, ['shortName', 'sn'], ln)
    nn = utils.getFlag(kwargs, ['niceName', 'nn'], None)
    cb = utils.getFlag(kwargs, ['channelBox', 'cb'], True)

    attrName = ln
    
    if attrflag == 'at':
        pm.addAttr(node,
                   ln  = ln,
                   at  = _type,
                   dv  = dv,
                   k   = k,
                   min = _min,
                   max = _max,
                   sn  = sn,
                   nn  = nn,
                   )
    elif attrflag == 'dt':
        pm.addAttr(node,
                   ln = ln,
                   dt = _type,
                   k  = k,
                   sn = sn,
                   nn = nn,
                   )
    if value:
        pm.setAttr(node.name() + '.' + attrName,
                   value
                  )
    if not k:
        if cb:
            pm.setAttr(node.name() + '.' + attrName,
                       cb=cb
                      )


def setAddAttrs(attributeDicts, node, _set=False, add=True, value=False):
    """this is set & add attrs from attribute dictonary member.
    """
    s = attributeDicts

    attrNames = [ an for an in s.keys() ]

    for attrName in attrNames:
        attrsDict = s[attrName]

        value     = attrsDict['value']

        attrflag  = attrsDict['attrflag']

        dv        = attrsDict['dv']

        k         = attrsDict['k']

        ln        = attrsDict['ln']

        _max      = attrsDict['max']

        _min      = attrsDict['min']

        _type     = attrsDict['type']

        try:
            nn    = attrsDict['nn']
        except:
            nn    = None

        try:
            sn    = attrsDict['sn']
        except:
            sn    = ln

        if not k:
            cb    = attrsDict['cb']


        if add:
            addDictAttr(node,
                        ln       = ln,
                        attrflag = attrflag,
                        dv       = dv,
                        k        = k,
                        _min     = _min,
                        _max     = _max,
                        _type    = _type,
                        sn       = sn,
                        nn       = nn,
                        cb       = cb,
                        )
        if _set:
            setDictAttr(node,
                        value    = value,
                        ln       = ln,
                        attrflag = attrflag,
                        dv       = dv,
                        k        = k,
                        _max     = _max,
                        _min     = _min,
                        _type    = _type,
                        cb       = cb,
                       )