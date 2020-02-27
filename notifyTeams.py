#!/usr/bin/env python3 
#
#
# Author: Jean-Baptiste Guillois
# Date: 2020-02-17
#
# Based on work from Isaac J. Galvan, https://github.com/isaac-galvan
#

import argparse
import json
import requests
import sys

def create_message(shinkenURI, notificationType, hostAlias, hostState, hostDuration, serviceDesc, serviceState, serviceDuration, longMessage):
    message = {}
    message['@type'] = 'MessageCard'
    message['@context'] = 'https://schema.org/extensions'

    ''' Handle problems '''
    if notificationType == 'PROBLEM' :
        message['themeColor'] = 'FF0000'
        
        if hostState == 'DOWN' or hostState == 'UNREACHABLE':
            message['title'] =  'Problem detected with ' + hostAlias
            message['text'] =  '/!\\ Host (' + hostAlias + ') is '+hostState.lower()+' since '+ hostDuration +'!'

        elif serviceState == 'CRITICAL' or serviceState == 'UNKNOWN' or serviceState == 'WARNING':
            message['title'] =  '/!\\ Service (' + hostAlias + '/' + serviceDesc + ') is '+ serviceState.lower() + ' since ' + serviceDuration + '!'
            message['text'] = longMessage

    ''' Handle recoveries '''
    if notificationType == 'RECOVERY' :
        message['themeColor'] = '00FF00'
        
        if hostState == 'UP' and serviceState == 'OK': 
            message['summary'] =  'Problem is now solved with ' + hostAlias + '/' + serviceDesc
            message['text'] =  'Host/Service (' + hostAlias + '/' + serviceDesc +') are now OK'

        elif hostState == 'UP' and serviceState != 'OK': 
            message['summary'] =  'Problem is now solved with host ' + hostAlias
            message['text'] =  'Host (' + hostAlias + ') is now UP'


    ''' Add Action Card '''
    actions = []
    viewInShinkenAction = {}
    viewInShinkenAction['@type'] = 'OpenUri'
    viewInShinkenAction['name'] = 'View in Shinken'
    
    target = {}
    target['os'] = 'default'
    target['uri'] = shinkenURI+'host/'+hostAlias
    
    targets = []
    targets.append(target)
    viewInShinkenAction['targets'] = targets
    
    actions.append(viewInShinkenAction)
    message['potentialAction'] = actions
    
    return message

def send_to_teams(url, message_json):
    """ posts the message to the O365 Teams webhook url """
    headers = {'Content-Type': 'application/json'}
    print ('Sending to '+url)
    r = requests.post(url, data=message_json, headers=headers)
    if r.status_code == 200:
        print('success')
        return True
    else:
        print('Enable to send to O365 Teams')
        print(r.reason + '('+str(r.status_code)+')')
        print(r.content)
        return False

def main(args):

    # verify Teams url
    url = args.get('url')
    if url is None or not (url.startswith( 'http://' ) or url.startswith( 'https://' )):
        # error no url
        sys.exit('Invalid or missing Teams URL')

    # verify Shinken url
    shinkenURI = args.get('shinkenUri')
    if shinkenURI is None or not (shinkenURI.startswith( 'http://' ) or shinkenURI.startswith( 'https://' )):
        # error no url
        sys.exit('Invalid or missing Shinken URL')

    notificationType = args.get('notificationType')
    hostAlias = args.get('hostAlias')
    hostState = args.get('hostState')
    hostDuration = args.get('hostDuration')
    serviceDesc = args.get('serviceDesc')
    serviceState = args.get('serviceState')
    serviceDuration = args.get('serviceDuration')
    longMessage = args.get('msg')
    
    message_dict = create_message(shinkenURI, notificationType, hostAlias, hostState, hostDuration, serviceDesc, serviceState, serviceDuration, longMessage)
    message_json = json.dumps(message_dict)
    
    send_to_teams(url, message_json)
    
    exit(0)

if __name__=='__main__':
    args = {}
    
    parser = argparse.ArgumentParser()

    # Positional arguments
    parser.add_argument('url', action='store', help='O365 Teams connector Webhook URL')
    parser.add_argument('shinkenUri', action='store', help='Nagios/Shinken URL')
    parser.add_argument('notificationType', action='store', help='Notification type')
    parser.add_argument('hostAlias', action='store', help='Host alias')
    parser.add_argument('hostState', action='store', help='Host state')
    parser.add_argument('hostDuration', action='store', help='Host problem duration')
    parser.add_argument('serviceDesc', action='store', help='Service description')
    parser.add_argument('serviceState', action='store', help='Service state')
    parser.add_argument('serviceDuration', action='store', help='Service problem duration')
    
    # Optional argument
    parser.add_argument('--msg', action='store', help='Long Message')

    parsedArgs = parser.parse_args()

    args['url'] = parsedArgs.url
    args['shinkenUri'] = parsedArgs.shinkenUri
    args['notificationType'] = parsedArgs.notificationType
    args['hostAlias'] = parsedArgs.hostAlias
    args['hostState'] = parsedArgs.hostState
    args['hostDuration'] = parsedArgs.hostDuration
    args['serviceDesc'] = parsedArgs.serviceDesc
    args['serviceState'] = parsedArgs.serviceState
    args['serviceDuration'] = parsedArgs.serviceDuration
    
    args['msg'] = None
    if parsedArgs.msg:
        args['msg'] = parsedArgs.msg

    main(args)