EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "expressionType": {
            "type": "string"
        },
        "message": {
            "anyOf": [
                {
                    "type": "string"
                },
                {
                    "type": "null"
                }
            ]
        }
    },
    "required": ["expressionType", "message"]
}

REFERENCE_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "group": {
            "type": "string"
        },
        "identifier": {
            "type": "string"
        }
    },
    "required": ["group", "identifier"]
}

COURSE_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {
            "type": "string"
        },
        "requisiteType": {
            "type": "string",
            "enum": ["P","C"]
        }
    },
    "required": ["code"]
}

CONDITIONAL_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "expressionOne": {
            "type": "object"
        },
        "expressionTwo": {
            "type": "object"
        },
        "condition": {
            "type": "string",
            "enum": ["OR", "AND"]
        }
    },
    "required": ["expressionOne", "expressionTwo", "condition"]
} 

LIST_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "threshold": {
            "type": "integer"
        },
        "type": {
            "type": "string",
            "enum": ["lt", "leq", "eq", "geq", "gt"]
        },
        "expressions": {
            "anyOf": [
                {
                    "type": "array",
                    "items": {
                        "type": "object"
                    }
                },
                REFERENCE_EXPRESSION_SCHEMA
            ]    
        }
    },
    "required": ["threshold", "type", "expressions"]
}

REGISTRATION_RESTRICTION_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "expression": {
            "type": "object"
        }
    },
    "required": ["expression"]
}

YEAR_STANDING_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "enum": ["lt", "leq", "eq", "geq", "gt"]
        },
        "threshold": {
            "type": "integer"
        }
    },
    "required": ["type", "threshold"]
}

# Makes sense to have list of expressions, since the semantics of this expression define that 
# Any expression that is satisfied, "counts" towards this unit
UNITS_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "enum": ["lt", "leq", "eq", "geq", "gt"]
        },
        "threshold": {
            "type": "number"
        },
        "expressions": {
            "type": "array",
            "items": {
                "type": "object"
            }
        }                  
    },
    "required": ["type", "threshold", "expressions"]
}

AWR_SATISFIED_EXPRESSION_SCHEMA = {
    "type": "object",
}

UMBRELLA_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "level": {
            "anyOf": [
                {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    }
                },
                {
                    "type": "null"
                }
            ]
        },
        "subject": {
            "anyOf": [
                {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                {
                    "type": "null"
                }
            ]
        }
    },
    "required": ["level", "subject"]
}

NO_CREDIT_WARNING_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "expression": {
            "type": "object"
        }
    },
    "required": ["expression"]
}

RECOMMENDATION_WARNING_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "expression": {
            "type": "object"
        }
    },
    "required": ["expression"]
}