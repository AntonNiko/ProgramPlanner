SECTION_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[ABT]\\d{2}$"
        },
        "type": {
            "type": "string",
            "enum": ["lecture", "lab", "tutorial"]
        },
        "crn": {
            "type": "integer"
        },
        "meetings": {
            "type": "array",
            "items": {
                "type": "object"
            }
            
        }
    },
    "required": ["name", "type", "crn", "meetings"]
}

SECTION_MEETING_SCHEMA = {
    "type": "object",
    "properties": {
        "days": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["M","T","W","R","F"]
            }
        },
        "location": {
            "type": "string"
        },
        "date range": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "string",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "end": {
                    "type": "string",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                }
            },
            "required": ["start", "end"]
        },
        "times": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "string",
                    "pattern": "^\\d{2}:\\d{2}$"
                },
                "end": {  
                    "type": "string",
                    "pattern": "^\\d{2}:\\d{2}$"
                }
            },
            "required": ["start", "end"]
        }
    },
    "required": ["days", "location", "date range", "times"]
}