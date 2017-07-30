import requests
import logging
import time
import subprocess

import json
import os

import re # regex in get_selector_type_as_str()

from urlparse import urlparse

import traceback
import argparse

import socket

import binascii

'''

!!! NOTE: only edit the copy in the "shared" directory !!!

'''

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

__author__ = '@TweekFawkes'
sScriptName = os.path.basename(__file__)

'''

- getToLogging()
- lineSplit(sLine, sStart, sEnd)
- getCurrentIpAddy()
- splunkTime(sProject, sSourceTool, sCmdToExecute, sCmdOut, sSeverity)
- splunkEvent(jEvent, sSourceTool)
- sortUniqList(lMyList)

'''

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def getTimeMillSec():
    millis = int(round(time.time() * 1000))
    return str(millis)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def sortUniqList(lMyList):
    lMyList = sorted(set(lMyList))
    return lMyList

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def getToLogging():
    #logging.basicConfig()
    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename="logs/"+str(int(time.time()))+'-'+sScriptName+'.log',
                        filemode='w')
    logger = logging.getLogger(__name__)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def lineSplit(sLine, sStart, sEnd):
    iStart = sLine.find(sStart)
    sLine = sLine[iStart + len(sStart):]
    iEnd = sLine.find(sEnd)
    sLine = sLine[:iEnd]
    sResult = sLine.strip()
    return sResult

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def getCurrentIpAddy():
    process = subprocess.Popen(['/usr/bin/curl', 'https://ipcurl.net'], stdout=subprocess.PIPE)
    sIpOut, sCmdErr = process.communicate()
    sIpOut = sIpOut.strip()
    logging.debug("sIpOut: " + str(sIpOut))
    return sIpOut

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def splunkTime(sProject, sSourceTool, sCmdToExecute, sCmdOut, sSeverity, objSplunk):
    sResult = "error"
    logging.debug("Start splunkTime()")
    try:
        sTimeNow = str(int(time.time()))
        logging.debug("sTimeNow: " + str(sTimeNow))
        sIpOut = getCurrentIpAddy()

        jDataToSplunk = {
            "time": sTimeNow,
            "host": sIpOut,
            "source": sSourceTool,
            "sourcetype": "darktools:" + sSourceTool,
            "event": {
                "project": sProject,
                "command": sCmdToExecute,
                "message": sCmdOut,
                "severity": sSeverity
            }
        }

        sApiSendToSplunkUrl = objSplunk.get_sHecUrl()
        sApiKey = objSplunk.get_sApiKey()

        jHeaders = {'Authorization': 'Splunk ' + sApiKey, 'Content-Type': 'application/json'}

        logging.debug("sApiSendToSplunkUrl: " + str(sApiSendToSplunkUrl))
        logging.debug("sApiKey: " + str(sApiKey))
        logging.debug("jHeaders: " + str(jHeaders))
        logging.debug("jData: " + str(jDataToSplunk))

        r = requests.post(sApiSendToSplunkUrl, headers=jHeaders, data=json.dumps(jDataToSplunk), verify=False)
        logging.debug("r.text: " + str(r.text))
        sResult = "yas!"
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        raise

    return sResult

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def splunkEvent(jEvent, sSourceTool):
    sResult = "error"
    logging.debug("Start splunkEvent()")
    try:
        sTimeNow = str(int(time.time()))
        logging.debug("sTimeNow: " + str(sTimeNow))
        sIpOut = getCurrentIpAddy()

        jDataToSplunk = {
            "time": sTimeNow,
            "host": sIpOut,
            "source": sSourceTool,
            "sourcetype": "darktools:"+sSourceTool,
            "event": jEvent
        }

        import yaml

        with open("config.yaml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        sApiSendToSplunkUrl = cfg['HEC_URL']
        sApiKey = cfg['HEC_KEY']

        jHeaders = {'Authorization': 'Splunk ' + sApiKey, 'Content-Type': 'application/json'}

        logging.debug("sApiSendToSplunkUrl: " + str(sApiSendToSplunkUrl))
        logging.debug("sApiKey: " + str(sApiKey))
        logging.debug("jHeaders: " + str(jHeaders))
        logging.debug("jData: " + str(jDataToSplunk))

        r = requests.post(sApiSendToSplunkUrl, headers=jHeaders, data=json.dumps(jDataToSplunk), verify=False)
        logging.debug("r.text: " + str(r.text))
        result = "yas!"
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        raise

    return result

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #
