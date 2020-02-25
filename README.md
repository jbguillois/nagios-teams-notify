
# nagios-teams-notify
Send Nagios/Shinken alerts to a Microsoft O365 Teams channel.

## Overview

This script can send Nagios/Shinken alerts to a Microsoft O365 Teams channel.

By sending alerts to Teams, we can simplify addition and removal alert recipients, allow for self-service subscription and push preferences, and have conversations based around the alerts as they occur.

## Installation

You can should install python dependencies listed in `requirements.txt` (you might use `pip` to do so) and copy `notifyTeams.py` where it can be executed by the Nagios/Shinken user (`/usr/lib` could be a good option). Make sure the script is  executable with `chmod +x notifyTeams.py`.
You can test this script by running the included unit tests (`python -m unittest -v testNotifyTeams.py`) 

## Configuration

### Create the Webhook

From [Using Office 365 Connectors: Teams](https://docs.microsoft.com/en-us/microsoftteams/platform/concepts/connectors/connectors-using#setting-up-a-custom-incoming-webhook):

1. In Microsoft Teams, choose More options (⋯) next to the channel name and then choose Connectors.
2. Scroll through the list of Connectors to Incoming Webhook, and choose Add.
3. Enter a name for the webhook, upload an image to associate with data from the webhook, and choose Create.
4. Copy the webhook to the clipboard and save it. You'll need the webhook URL for sending information to Microsoft Teams.
5. Choose Done.

### Configure Nagios/Shinken

Create a command object in the Nagios/Shinken configuration and replace <yourshinkenurl> with your Shinken URL (http://shinkenhost/).

```
define command {
    command_name notify_teams
    command_line /path/to/script/notifyTeams.py $_CONTACTWEBHOOKURL$ <youshinkenurl> $NOTIFICATIONTYPE$ $HOSTALIAS$ $HOSTSTATE$ $HOSTDURATION$ $SERVICEDESC$ $SERVICESTATE$ $SERVICEDURATION$ --msg "$SERVICEOUTPUT$ - $LONGSERVICEOUTPUT$"
}
```
Create a contact object with the custom variable macro _WEBHOOK set to the URL from the Teams channel connector. This variable is used when running the command above.

```
define contact {
    contact_name    example-team
    alias           Example Team
    host_notifications_enabled  1
    service_notifications_enabled   1
    host_notification_period    24x7
    service_notification_period 24x7 
    host_notification_options   d,u,r,f,s
    service_notification_options    w,u,c,r,f
    host_notification_commands  notify_teams
    service_notification_commands   notify_teams
    _WEBHOOKURL <yourwebhookURL>
}
```

Then add the contact to an existing object or contact group and reload your configuration.

Create additional contacts with their own `_WEBHOOKURL` custom variable macro for each Teams channel needing notifications.
