UVIC_SCHEMA = {
    "type": "object",
    "properties": {
        "institution": {
            "type": "string"
        }
    }
}

UVIC_PROGRAM_SCHEMA = {
    "type": "object",
    "properties": {
        "academic_writing_requirement": {
            "type": "object"
        },
        "minimum_coursework_units": {
            "type": "object"
        }
    },
    "required": ["academic_writing_requirement", "minimum_coursework_units"]
}


UVIC_ENGINEERING_PROGRAM_SCHEMA = {
    "type": "object",
    "properties": {
        "Name": {
            "type": "string"
        },
        "Degree": {
            "type": "string"
        },
        "Honours": {
            "anyOf": [
                {
                    "type": "null"
                },
                {
                    "type": "array",
                    "items": {
                        "type": "object"
                    }
                }
            ]
        },
        "Options": {
            "anyOf": [
                {
                    "type": "null"
                },
                {
                    "type": "object",
                }
            ]
        },
        "General Requirements": {
            "type": "array",
            "items": {
                "type": "object"
            }
        },
        "Specializations": {
            "anyOf": [
                {
                    "type": "null"
                },
                {
                    "type": "object",
                }
            ]
        },
        "Co-op": {
            "anyOf": [
                {
                    "type": "null"
                },
                {
                    "type": "object",
                    "properties": {
                        "required": {
                            "type": "boolean"
                        },
                        "expression": {
                            "type": "object"
                        }
                    }
                }
            ]            
        },
        "Combined": {
            "anyOf": [
                {
                    "type": "null"
                },
                {
                    "type": "object",
                }
            ]
        }
    }
}