EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "expressionType": {
            "type": "string"
        }
    },
    "required": ["expressionType"]
}

REFERENCE_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "referenceFile": {
            "type": "string"
        },
        "referenceName": {
            "type": "string"
        }
    },
    "required": ["referencePointer"]
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

# Doesn't make sense to have a list as "expressions". The semantics would get wildly complicated 
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
        "expression": {
            "type": "object"
        }
    }
}

AWR_SATISFIED_EXPRESSION_SCHEMA = {
    "type": "object",
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