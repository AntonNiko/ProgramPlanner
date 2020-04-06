EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "expressionType": {
            "type": "string"
        }
    },
    "required": ["expressionType"]
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
    "required": ["code", "requisiteType"]
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
    }
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
            "type": "array",
            "items": {
                "type": "object"
            }
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
    }
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
    }
}

RECOMMENDATION_WARNING_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "expression": {
            "type": "object"
        }
    }
}