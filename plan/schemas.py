EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "expression_type": {
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
    "required": ["expression_type"]
}

COURSE_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "subject": {
            "type": "string"
        },
        "number": {
            "type": "string"
        },
        "requisite_type": {
            "type": "string",
            "enum": ["P","C"]
        }
    },
    "required": ["subject", "number"]
}

CONDITIONAL_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "expression_one": {
            "type": "object"
        },
        "expression_two": {
            "type": "object"
        },
        "condition": {
            "type": "string",
            "enum": ["OR", "AND"]
        }
    },
    "required": ["expression_one", "expression_two", "condition"]
} 

LIST_EXPRESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "threshold_value": {
            "type": "integer"
        },
        "threshold_type": {
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
                }
            ]    
        }
    },
    "required": ["threshold_value", "threshold_type", "expressions"]
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

#YEAR_STANDING_EXPRESSION_SCHEMA = {
#    "type": "object",
#    "properties": {
#        "type": {
#            "type": "string",
#            "enum": ["lt", "leq", "eq", "geq", "gt"]
#        },
#        "threshold": {
#            "type": "integer"
#        }
#    },
#    "required": ["type", "threshold"]
#}

# Makes sense to have list of expressions, since the semantics of this expression define that 
# Any expression that is satisfied, "counts" towards this unit
#UNITS_EXPRESSION_SCHEMA = {
#    "type": "object",
#    "properties": {
#        "type": {
#            "type": "string",
#            "enum": ["lt", "leq", "eq", "geq", "gt"]
#        },
#        "threshold": {
#            "type": "number"
#        },
#        "expressions": {
#            "type": "array",
#            "items": {
#                "type": "object"
#            }
#        }                  
#    },
#    "required": ["type", "threshold", "expressions"]
#}

#AWR_SATISFIED_EXPRESSION_SCHEMA = {
#    "type": "object",
#}

#UMBRELLA_EXPRESSION_SCHEMA = {
#    "type": "object",
#    "properties": {
#        "level": {
#            "anyOf": [
#                {
#                    "type": "array",
#                    "items": {
#                        "type": "integer"
#                    }
#                },
#                {
#                    "type": "null"
#                }
#            ]
#        },
#        "subject": {
#            "anyOf": [
#                {
#                    "type": "array",
#                    "items": {
#                        "type": "string"
#                    }
#                },
#                {
#                    "type": "null"
#                }
#            ]
#        }
#    },
#    "required": ["level", "subject"]
#}

#NO_CREDIT_WARNING_EXPRESSION_SCHEMA = {
#    "type": "object",
#    "properties": {
#        "expression": {
#            "type": "object"
#        }
#    },
#    "required": ["expression"]
#}

#RECOMMENDATION_WARNING_EXPRESSION_SCHEMA = {
#    "type": "object",
#    "properties": {
#        "expression": {
#            "type": "object"
#        }
#    },
#    "required": ["expression"]
#}