import unittest
import subprocess
import sys
import notifyTeams

class TestNotifyTeamsCLI(unittest.TestCase):

    def test_no_args(self):
        proc = subprocess.Popen([sys.executable, 'notifyTeams.py'])
        proc.communicate()
        self.assertEqual(proc.returncode, 2)

    def test_allArgsButUrls(self):
        args = []
        args.append(sys.executable)
        args.append('notifyTeams.py')
        args.append('PROBLEM')
        args.append('host')
        args.append('DOWN')
        args.append('1h')
        args.append('Service A')
        args.append('OK')
        args.append('1m')
        
        proc = subprocess.Popen(args)
        proc.communicate()
        self.assertEqual(proc.returncode, 2)

    def test_allArgs(self):
        args = []
        args.append(sys.executable)
        args.append('notifyTeams.py')
        args.append('https://outlook.office.com/webhook/')
        args.append('http://localhost/')
        args.append('PROBLEM')
        args.append('host')
        args.append('DOWN')
        args.append('1h')
        args.append('Service A')
        args.append('OK')
        args.append('1m')
        
        proc = subprocess.Popen(args)
        proc.communicate()
        self.assertEqual(proc.returncode, 0)

    def test_createMessage_ProblemHost(self):
        args = {}

        # Problem Host DOWN
        args['shinkenURI'] = 'http://localhost/'
        args['notificationType'] = 'PROBLEM'
        args['hostAlias'] = 'host1'
        args['hostState'] = 'DOWN'
        args['hostDuration'] = '3h 2m 1s'
        args['serviceDesc'] = 'Service A'
        args['serviceState'] = 'OK'
        args['serviceDuration'] = '1m'
        
        msg = notifyTeams.create_message(args['shinkenURI'], args['notificationType'], 
                                   args['hostAlias'], args['hostState'], args['hostDuration'],
                                   args['serviceDesc'], args['serviceState'], args['serviceDuration'], "")
        self.assertEqual(msg['@type'], 'MessageCard')
        self.assertEqual(msg['@context'], 'https://schema.org/extensions')
        self.assertEqual(msg['themeColor'], 'FF0000')
        self.assertEqual(msg['title'], 'Problem detected with '+args['hostAlias'])
        self.assertEqual(msg['text'], '/!\\ Host ('+args['hostAlias']+') is '+args['hostState'].lower()+' since '+args['hostDuration']+'!')

        # Problem Host UNREACHABLE
        args['shinkenURI'] = 'http://localhost/'
        args['notificationType'] = 'PROBLEM'
        args['hostAlias'] = 'host1'
        args['hostState'] = 'UNREACHABLE'
        args['hostDuration'] = '3h 2m 1s'
        args['serviceDesc'] = 'Service A'
        args['serviceState'] = 'OK'
        args['serviceDuration'] = '1m'
        
        msg = notifyTeams.create_message(args['shinkenURI'], args['notificationType'], 
                                   args['hostAlias'], args['hostState'], args['hostDuration'],
                                   args['serviceDesc'], args['serviceState'], args['serviceDuration'], "")
        self.assertEqual(msg['@type'], 'MessageCard')
        self.assertEqual(msg['@context'], 'https://schema.org/extensions')
        self.assertEqual(msg['themeColor'], 'FF0000')
        self.assertEqual(msg['title'], 'Problem detected with '+args['hostAlias'])
        self.assertEqual(msg['text'], '/!\\ Host ('+args['hostAlias']+') is '+args['hostState'].lower()+' since '+args['hostDuration']+'!')

    def test_createMessage_ProblemService(self):
        args = {}
        
        # Service CRITICAL
        args['shinkenURI'] = 'http://localhost/'
        args['notificationType'] = 'PROBLEM'
        args['hostAlias'] = 'host1'
        args['hostState'] = 'UP'
        args['hostDuration'] = '3h 2m 1s'
        args['serviceDesc'] = 'Service A'
        args['serviceState'] = 'CRITICAL'
        args['serviceDuration'] = '1m'
        args['longMessage'] = 'Disk is full'
        
        msg = notifyTeams.create_message(args['shinkenURI'], args['notificationType'], 
                                   args['hostAlias'], args['hostState'], args['hostDuration'],
                                   args['serviceDesc'], args['serviceState'], args['serviceDuration'], args['longMessage'])
        self.assertEqual(msg['@type'], 'MessageCard')
        self.assertEqual(msg['@context'], 'https://schema.org/extensions')
        self.assertEqual(msg['themeColor'], 'FF0000')
        self.assertEqual(msg['title'], '/!\\ Service ('+args['hostAlias']+'/'+args['serviceDesc']+') is '+args['serviceState'].lower()+' since '+args['serviceDuration']+'!')        
        self.assertEqual(msg['text'], args['longMessage'])

        # Service WARNING
        args['shinkenURI'] = 'http://localhost/'
        args['notificationType'] = 'PROBLEM'
        args['hostAlias'] = 'host1'
        args['hostState'] = 'UP'
        args['hostDuration'] = '3h 2m 1s'
        args['serviceDesc'] = 'Service A'
        args['serviceState'] = 'WARNING'
        args['serviceDuration'] = '1m'
        args['longMessage'] = 'Disk is full'
        
        msg = notifyTeams.create_message(args['shinkenURI'], args['notificationType'], 
                                   args['hostAlias'], args['hostState'], args['hostDuration'],
                                   args['serviceDesc'], args['serviceState'], args['serviceDuration'], args['longMessage'])
        self.assertEqual(msg['@type'], 'MessageCard')
        self.assertEqual(msg['@context'], 'https://schema.org/extensions')
        self.assertEqual(msg['themeColor'], 'FF0000')
        self.assertEqual(msg['title'], '/!\\ Service ('+args['hostAlias']+'/'+args['serviceDesc']+') is '+args['serviceState'].lower()+' since '+args['serviceDuration']+'!')        
        self.assertEqual(msg['text'], args['longMessage'])

        # Service UNKNOWN
        args['shinkenURI'] = 'http://localhost/'
        args['notificationType'] = 'PROBLEM'
        args['hostAlias'] = 'host1'
        args['hostState'] = 'UP'
        args['hostDuration'] = '3h 2m 1s'
        args['serviceDesc'] = 'Service A'
        args['serviceState'] = 'UNKNOWN'
        args['serviceDuration'] = '1m'
        args['longMessage'] = 'Disk is full'
        
        msg = notifyTeams.create_message(args['shinkenURI'], args['notificationType'], 
                                   args['hostAlias'], args['hostState'], args['hostDuration'],
                                   args['serviceDesc'], args['serviceState'], args['serviceDuration'], args['longMessage'])
        self.assertEqual(msg['@type'], 'MessageCard')
        self.assertEqual(msg['@context'], 'https://schema.org/extensions')
        self.assertEqual(msg['themeColor'], 'FF0000')
        self.assertEqual(msg['title'], '/!\\ Service ('+args['hostAlias']+'/'+args['serviceDesc']+') is '+args['serviceState'].lower()+' since '+args['serviceDuration']+'!')        
        self.assertEqual(msg['text'], args['longMessage'])

    def test_createMessage_RecoveryHostService(self):
        args = {}

        # Recovery Host and Service
        args['shinkenURI'] = 'http://localhost/'
        args['notificationType'] = 'RECOVERY'
        args['hostAlias'] = 'host1'
        args['hostState'] = 'UP'
        args['hostDuration'] = '3h 2m 1s'
        args['serviceDesc'] = 'Service A'
        args['serviceState'] = 'OK'
        args['serviceDuration'] = '1m'
        
        msg = notifyTeams.create_message(args['shinkenURI'], args['notificationType'], 
                                   args['hostAlias'], args['hostState'], args['hostDuration'],
                                   args['serviceDesc'], args['serviceState'], args['serviceDuration'], "")
        self.assertEqual(msg['@type'], 'MessageCard')
        self.assertEqual(msg['@context'], 'https://schema.org/extensions')
        self.assertEqual(msg['themeColor'], '00FF00')
        self.assertEqual(msg['summary'], 'Problem is now solved with '+args['hostAlias']+'/'+args['serviceDesc'])
        self.assertEqual(msg['text'], 'Host/Service (' + args['hostAlias'] + '/' + args['serviceDesc'] +') are now OK')

        # Recovery Host
        args['shinkenURI'] = 'http://localhost/'
        args['notificationType'] = 'RECOVERY'
        args['hostAlias'] = 'host1'
        args['hostState'] = 'UP'
        args['hostDuration'] = '3h 2m 1s'
        args['serviceDesc'] = 'Service A'
        args['serviceState'] = 'CRITICAL'
        args['serviceDuration'] = '1m'
        
        msg = notifyTeams.create_message(args['shinkenURI'], args['notificationType'], 
                                   args['hostAlias'], args['hostState'], args['hostDuration'],
                                   args['serviceDesc'], args['serviceState'], args['serviceDuration'], "")
        self.assertEqual(msg['@type'], 'MessageCard')
        self.assertEqual(msg['@context'], 'https://schema.org/extensions')
        self.assertEqual(msg['themeColor'], '00FF00')
        self.assertEqual(msg['summary'], 'Problem is now solved with host '+args['hostAlias'])
        self.assertEqual(msg['text'], 'Host (' + args['hostAlias'] +') is now UP')


if __name__ == '__main__':
    unittest.main()
