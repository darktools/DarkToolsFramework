import argparse
import logging
import os
import time
import traceback
import random
import subprocess
import random  # getUniqId()
import string  # getUniqId()
import yaml

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

__author__ = '@TweekFawkes'
sScriptName = os.path.basename(__file__)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

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

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #


parser = argparse.ArgumentParser()
parser.add_argument("-e") # dev or stage or prod
parser.add_argument("-r")
args = parser.parse_args()

logging.debug("args.e: " + str(args.e))
logging.debug("args.r: " + str(args.r))

sEnv = args.e
sEnv = sEnv.strip()

sArgR = args.r
sArgR = sArgR.strip()

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def os_popen(sCmdToExecute):
    sVar = "unknown runCommand()"
    try:
        logging.debug("runCommand() -> sCmdToExecute: " + str(sCmdToExecute))
        sVar = os.popen(sCmdToExecute).read()
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error("subprocess.Popen failed :\ ")
    return sVar

def subprocess_popen(sCmdToExecute):
    sVar = "unknown runCommand()"
    try:
        logging.debug("runCommand() -> sCmdToExecute: " + str(sCmdToExecute))
        sts = subprocess.Popen(sCmdToExecute, shell=True).wait()
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error("subprocess.Popen failed :\ ")
    return sVar

def executeCommand(sCmdToExecute, sChangeDir=None):
    sCmdOut = "unknown sCmdOut"
    try:
        logging.debug("sCmdToExecute: " + str(sCmdToExecute))
        logging.debug("sChangeDir: " + str(sChangeDir))
        sCwd = os.getcwd()
        logging.debug("sCwd: " + str(sCwd))
        if sChangeDir is not None:
            os.chdir(sChangeDir)
            sNewCwd = os.getcwd()
            logging.debug("sNewCwd: " + str(sNewCwd))
        lCmdToExecute = sCmdToExecute.split(" ")
        logging.debug("lCmdToExecute: " + str(lCmdToExecute))
        process = subprocess.Popen(lCmdToExecute, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
        sCmdOut, sCmdErr = process.communicate()
        logging.info("executeCommand(sCmdToExecute, sChangeDir) sCmdOut: " + str(sCmdOut))
        logging.info("executeCommand(sCmdToExecute, sChangeDir) sCmdErr: " + str(sCmdErr))
        os.chdir(sCwd)
        sCwdNewNew = os.getcwd()
        logging.debug("sCwdNewNew: " + str(sCwdNewNew))
    except Exception as e:
        logging.error("traceback.format_exc(): " + traceback.format_exc())
        logging.error("str(Exception): " + str(e))
        logging.error("subprocess.Popen failed :\ ")
    return sCmdOut

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

lDeliverances = ['find_subs', 'find_ips', 'find_open_tcp_ports', 'find_tcp_service', 'validate_ip']
lBandits = ['smokey', 'target_dispatcher', 'gobuster_dirb', 'udp_protoscan', 'whois_ip', 'whois_domain', 'traceroute_icmp', 'traceroute_tcp', 'traceroute_udp', 'testssl_sh', 'hydra_ftp', 'hydra_ssh', 'nikto_webapp', 'theharvester_email', 'anon_ftp', 'http_options']
lGators = ['console_gator']

sDockerHubName = sArgR
sPyCharmsDir = str(os.getcwd()) + '/'
sGatorSensorDir = sPyCharmsDir
sSharedDir = sPyCharmsDir + 'shared/'
sBuildDir = sPyCharmsDir + 'yyy_builds/'
sScriptsDeployDir = sPyCharmsDir + 'ag_scripts_deploy/'
sScriptsAioDir = sPyCharmsDir + 'ag_scripts_aio/'
sScriptsAioFFP = sScriptsAioDir + 'run_all_with_console.sh'
sConfigFileName = "config.yaml"

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

def createBashScriptFile(sFFP):
    subprocess_popen('rm -rf ' + sFFP)
    sLine = '#!/bin/bash'
    fh = open(sFFP, "w")
    fh.write(sLine + os.linesep)
    fh.close()
    print(sLine)

def appendIntoBashScriptFile(sFFP, sLine):
    with open(sFFP, 'a') as f1:
        f1.write(sLine + os.linesep)
    with open(sScriptsAioFFP, 'a') as f1:
        f1.write(sLine + os.linesep)
    print(sLine)

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def generateAmqpUri(sSharedConfigFFP, sAmqpUsername, sAmqpPassword):
    with open(sSharedConfigFFP, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    sAmqpProto = cfg['AMQP_PROTO']
    sAmqpServer = cfg['AMQP_SERVER']
    sAmqpPort = cfg['AMQP_PORT']

    sAmqpUri = sAmqpProto + sAmqpUsername + ':' + sAmqpPassword + '@' + sAmqpServer + ':' + sAmqpPort

    return sAmqpUri

def appendIntoConfigFile( sConfigToModFFP, sAmqpUri ):
    sLineAmqpUri = "AMQP_URI: '" + sAmqpUri + "'"
    with open(sConfigToModFFP, 'a') as f1:
        f1.write(sLineAmqpUri + os.linesep)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

subprocess_popen('rm -rf ' + sBuildDir)
subprocess_popen('mkdir -p ' + sBuildDir)

subprocess_popen('rm -rf ' + sScriptsDeployDir)
subprocess_popen('mkdir -p ' + sScriptsDeployDir)

subprocess_popen('rm -rf ' + sScriptsAioDir)
subprocess_popen('mkdir -p ' + sScriptsAioDir)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

sContainerName = "gator_" + sEnv
logging.debug("sContainerName: " + str(sContainerName))

# Stop the old Docker Container if it is still running for some reason...
sDockerNumber = os_popen('docker ps -a -q  --filter ancestor='+sContainerName)
logging.debug("sDockerNumber: " + str(sDockerNumber))
subprocess_popen('docker stop ' + sDockerNumber)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

sSharedConfigFFP = sSharedDir + sConfigFileName
sAmqpUsername = randomword(int(8))  # TODO: make longer
sAmqpPassword = randomword(int(8))  # TODO: make longer
sAmqpUri = generateAmqpUri(sSharedConfigFFP, sAmqpUsername, sAmqpPassword)
logging.info("sAmqpUri: " + str(sAmqpUri))

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

createBashScriptFile(sScriptsAioFFP)

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

sScriptsDeployMq = sScriptsDeployDir + 'deployMq.sh'
createBashScriptFile(sScriptsDeployMq)
appendIntoBashScriptFile(sScriptsDeployMq, '# mq - deploy script for ' + sEnv + ' environment')
appendIntoBashScriptFile(sScriptsDeployMq, 'docker kill $(docker ps -q)')
appendIntoBashScriptFile(sScriptsDeployMq, 'docker pull rabbitmq:3-management')
appendIntoBashScriptFile(sScriptsDeployMq, 'docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 -e RABBITMQ_DEFAULT_USER='+sAmqpUsername+' -e RABBITMQ_DEFAULT_PASS='+sAmqpPassword+' rabbitmq:3-management')
appendIntoBashScriptFile(sScriptsDeployMq, 'sleep 9')
appendIntoBashScriptFile(sScriptsDeployMq, '#')

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

sScriptsDeployDeliverances = sScriptsDeployDir + 'deployDeliverances.sh'
createBashScriptFile(sScriptsDeployDeliverances)
appendIntoBashScriptFile(sScriptsDeployDeliverances, '# deliverance - deploy script for ' + sEnv + ' environment')
appendIntoBashScriptFile(sScriptsDeployDeliverances, 'docker kill $(docker ps -q)')
appendIntoBashScriptFile(sScriptsDeployDeliverances, 'sleep 9')
appendIntoBashScriptFile(sScriptsDeployDeliverances, '#')
appendIntoBashScriptFile(sScriptsDeployDeliverances, 'docker pull ' + sDockerHubName + '/' + sContainerName)
appendIntoBashScriptFile(sScriptsDeployDeliverances, '#')

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

sScriptsDeployBandits = sScriptsDeployDir + 'deployBandits.sh'
createBashScriptFile(sScriptsDeployBandits)
appendIntoBashScriptFile(sScriptsDeployBandits, '# bandit - deploy script for ' + sEnv + ' environment')
appendIntoBashScriptFile(sScriptsDeployBandits, 'docker kill $(docker ps -q)')
appendIntoBashScriptFile(sScriptsDeployBandits, 'sleep 9')
appendIntoBashScriptFile(sScriptsDeployBandits, '#')
appendIntoBashScriptFile(sScriptsDeployBandits, 'docker pull ' + sDockerHubName + '/' + sContainerName)
appendIntoBashScriptFile(sScriptsDeployBandits, '#')

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #

sScriptsDeployConsole = sScriptsDeployDir + 'deployConsole.sh'
createBashScriptFile(sScriptsDeployConsole)
appendIntoBashScriptFile(sScriptsDeployConsole, '# console - deploy script for ' + sEnv + ' environment')
appendIntoBashScriptFile(sScriptsDeployConsole, 'docker kill $(docker ps -q)')
appendIntoBashScriptFile(sScriptsDeployConsole, 'sleep 9')
appendIntoBashScriptFile(sScriptsDeployConsole, '#')
appendIntoBashScriptFile(sScriptsDeployConsole, 'docker pull ' + sDockerHubName + '/' + sContainerName)
appendIntoBashScriptFile(sScriptsDeployConsole, '#')

# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #


# Create the directory to build the new Docker Container
sBuildGatorDir = sBuildDir + sContainerName + "/"
logging.debug("sBuildGatorDir: " + str(sBuildGatorDir))

# Make sure this directory is empty
subprocess_popen('rm -rf ' + sBuildGatorDir)
subprocess_popen('mkdir -p ' + sBuildGatorDir)

# Make a log directory for this contianer
sBuildLogDir = sBuildGatorDir + "logs/"
logging.debug("sBuildLogDir: " + str(sBuildLogDir))
subprocess_popen('mkdir -p ' + sBuildLogDir)

sDeliveranceModuleDir = sGatorSensorDir + 'deliverances/'
for sDeliveranceModule in lDeliverances:
    sCurDeliveranceModuleDir = sDeliveranceModuleDir + sDeliveranceModule + '/'
    subprocess_popen('cp ' + sCurDeliveranceModuleDir + "* " + sBuildGatorDir)
    appendIntoBashScriptFile(sScriptsDeployDeliverances, 'docker run -d ' + sDockerHubName + '/' + sContainerName + ' /bin/bash /app/' + sDeliveranceModule + '.sh')
    appendIntoBashScriptFile(sScriptsDeployDeliverances, 'sleep 3')
    appendIntoBashScriptFile(sScriptsDeployDeliverances, '#')

sBanditModuleDir = sGatorSensorDir + 'bandits/'
for sBanditModule in lBandits:
    sCurBanditModuleDir = sBanditModuleDir + sBanditModule + '/'
    subprocess_popen('cp ' + sCurBanditModuleDir + "* " + sBuildGatorDir)
    appendIntoBashScriptFile(sScriptsDeployBandits, 'docker run -d ' + sDockerHubName + '/' + sContainerName + ' /bin/bash /app/' + sBanditModule + '.sh')
    appendIntoBashScriptFile(sScriptsDeployBandits, 'sleep 3')
    appendIntoBashScriptFile(sScriptsDeployBandits, '#')

sGatorModuleDir = sGatorSensorDir + 'gators/'
for sGatorModule in lGators:
    sCurGatorModuleDir = sGatorModuleDir + sGatorModule + '/'
    subprocess_popen('cp ' + sCurGatorModuleDir + "* " + sBuildGatorDir)
    appendIntoBashScriptFile(sScriptsDeployConsole, 'docker run -t -i ' + sDockerHubName + '/' + sContainerName + ' /bin/bash /app/' + sGatorModule + '.sh')
    appendIntoBashScriptFile(sScriptsDeployConsole, 'sleep 3')
    appendIntoBashScriptFile(sScriptsDeployConsole, '#')

# copy the files from the shared directory to the continer's build directory
subprocess_popen('cp ' + sSharedDir + "* " + sBuildGatorDir)

# append into the build directory's config file the new string
appendIntoConfigFile(sBuildGatorDir + sConfigFileName, sAmqpUri)

# build the docker container
subprocess_popen('docker build -t ' + sContainerName + ' ' + sBuildGatorDir)
subprocess_popen('docker tag ' + sContainerName + ' ' + sDockerHubName + '/' + sContainerName + ':latest')
subprocess_popen('docker push ' + sDockerHubName + '/' + sContainerName + ':latest')

## #### ### #### ## ## ## #### ##### #### #
