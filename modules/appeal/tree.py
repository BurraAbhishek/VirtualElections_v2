appeal_menu = {
    "cleanMenu": {
        "status": "clean",
        "title": "Your account is not marked or restricted. You're all good!",
        "description": "You can safely exit to the main menu.",
        "options": [
            {
                "type": "return",
                "body": "Return to the main menu"
            }
        ]
    },
    "cheatMenu": {
        "status": "cheat",
        "title": ("Your account is banned from contesting in the elections "
            + "because you were caught cheating."),
        "description": ("We define this as violating the Election Code of "
            + "Conduct in any way."),
        "options": [
            {
                "type": "accept",
                "body": (
                    "I accept that I violated the Election Code of Conduct"
                )
            },
            {
                "type": "deny",
                "body": "I deny violating the Election Code of Conduct"
            },
            {
                "type": "query",
                "body": "I would like to know more about my sanction"
            },
            {
                "type": "return",
                "body": "Return to the main menu"
            }
        ]
    },
    "AltMenu": {
        "status": "alt",
        "title": ("Your account is banned from contesting in the elections "
            + "due to multi-accounting."),
        "description": ("We define this as violating the Election Code of "
            + "Conduct by creating multiple accounts"
            + "for the same contestant."),
        "options": [
            {
                "type": "accept",
                "body": (
                    "I accept that I violated the Election Code of Conduct"
                )
            },
            {
                "type": "deny",
                "body": "I deny violating the Election Code of Conduct"
            },
            {
                "type": "query",
                "body": "I would like to know more about my sanction"
            },
            {
                "type": "return",
                "body": "Return to the main menu"
            }
        ]
    },
    "illegalAccessMenu": {
        "status": "unauthorized",
        "title": (
            "You were caught trying to access the admin pages" 
            + " without authorization."
        ),
        "description": (
            "Read the Terms of Service. "
            + "This mark does not appear by accident."
        ),
        "options": [
            {
                "type": "deny",
                "body": "I accidentally tried to log in as admin"
            },
            {
                "type": "deny",
                "body": (
                    "I accidentally typed incorrect credentials. "
                    + "I can prove that I have admin permissions."
                )
            },
            {
                "type": "return",
                "body": "Return to the main menu"
            }
        ]
    },
}