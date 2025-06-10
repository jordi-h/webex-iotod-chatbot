AuthenticationAdaptiveCard = {
    "roomId": "room_id",
    "markdown": "Authentication",
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "Authentication",
                        "wrap": True,
                        "weight": "Bolder",
                        "size": "ExtraLarge",
                        "isSubtle": True,
                        "color": "Dark",
                        "fontType": "Monospace",
                        "spacing": "None",
                        "horizontalAlignment": "Left"
                    },
                    {
                        "type": "TextBlock",
                        "text": "By using this Chatbot, you allow it to use your Secret API Key to interact with the IOT OD platform.",
                        "size": "Small",
                        "horizontalAlignment": "Left",
                        "maxLines": 0,
                        "color": "Warning",
                        "isSubtle": False,
                        "weight": "Lighter",
                        "fontType": "Default",
                        "wrap": True,
                        "spacing": "Padding"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Data submitted by a user is encrypted and stored within the Webex platform",
                        "wrap": True,
                        "color": "Warning",
                        "size": "Small",
                        "fontType": "Monospace"
                    },
                    {
                        "type": "Input.Text",
                        "placeholder": "Can be found under Access Control > API Key",
                        "isMultiline": True,
                        "id": "1",
                        "isRequired": True,
                        "label": "API Key ID",
                        "errorMessage": "Please provide a valid input"
                    },
                    {
                        "type": "Input.Text",
                        "placeholder": "Can be found under Access Control > API Key",
                        "isMultiline": True,
                        "id": "2",
                        "label": "Organization ID",
                        "isRequired": True,
                        "errorMessage": "Please provide a valid input"
                    },
                    {
                        "type": "Input.Text",
                        "placeholder": "Can be found under Access Control > API Key",
                        "isMultiline": True,
                        "id": "3",
                        "label": "API Key",
                        "isRequired": True,
                        "errorMessage": "Please provide a valid input"
                    }
                ],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Submit",
                    }
                ]
            }
        }
    ]
}