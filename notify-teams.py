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

def create_message(url, notificationType, hostAlias, hostState, hostDuration, serviceDesc, serviceState, serviceDuration, longMessage):
    message = {}
    message['@type'] = 'MessageCard'
    message['@context'] = 'https://schema.org/extensions'

    ''' Handle problems '''
    if notificationType == 'PROBLEM' :
        message['themeColor'] = 'FF0000'
        
        if hostState == 'DOWN':
            message['title'] =  'Problem detected with ' + hostAlias
            message['text'] =  '/!\\ Host (' + hostAlias + ') is down since '+ hostDuration +'!'

        elif hostState == 'UNREACHABLE': 
            message['title'] =  'Problem detected with ' + hostAlias
            message['text'] =  '/!\\ Host (' + hostAlias + ') is unreachable since '+ hostDuration +'!'

        elif serviceState == 'CRITICAL' or serviceState == 'UNKNOWN' or serviceState == 'WARNING':
            message['title'] =  '/!\\ Service (' + hostAlias + '/' + serviceDesc + ') is '+ serviceState.lower() + ' since ' + serviceDuration + '!'
            message['text'] = longMessage

    ''' Handle recoveries '''
    if notificationType == 'RECOVERY' :
        message['themeColor'] = '00FF00'
        message['summary'] =  'Problem is now solved with ' + hostAlias + '/' + serviceDesc
        
        if hostState == 'UP' and serviceState == 'OK': 
            message['text'] =  'Host/Service (' + hostAlias + '/' + serviceDesc +') are now OK'


    ''' Add Action Card '''
    actions = []
    viewInShinkenAction = {}
    viewInShinkenAction['@type'] = 'OpenUri'
    viewInShinkenAction['name'] = 'View in Shinken'
    
    target = {}
    target['os'] = 'default'
    target['uri'] = 'http://monitoring.omega-cap.local/'+hostAlias
    
    targets = []
    targets.append(target)
    viewInShinkenAction['targets'] = targets
    
    actions.append(viewInShinkenAction)
    message['potentialAction'] = actions
    
    return message

def send_to_teams(url, message_json):
    """ posts the message to the O365 Teams webhook url """
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=message_json, headers=headers)
    if r.status_code == requests.codes.ok:
        print('success')
        return True
    else:
        print('Enable to send to O365 Teams')
        print(r.reason + '('+str(r.status_code)+')')
        print(r.content)
        return False

def main(args):

    # verify url
    url = args.get('url')
    if url is None:
        # error no url
        print('error no url')
        exit(2)

    notificationType = args.get('notificationType')
    hostAlias = args.get('hostAlias')
    hostState = args.get('hostState')
    hostDuration = args.get('hostDuration')
    serviceDesc = args.get('serviceDesc')
    serviceState = args.get('serviceState')
    serviceDuration = args.get('serviceDuration')
    longMessage = args.get('msg')
    
    message_dict = create_message(url, notificationType, hostAlias, hostState, hostDuration, serviceDesc, serviceState, serviceDuration, longMessage)
    message_json = json.dumps(message_dict)
    
    send_to_teams(url, message_json)

if __name__=='__main__':
    args = {}
    
    parser = argparse.ArgumentParser()

    # Positional arguments
    parser.add_argument('url', action='store', help='O365 Teams connector Webhook URL')
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

    #if not sys.__stdin__.isatty():
    #    args['long_message'] = sys.__stdin__.read()
    #    pass
    
    main(args)