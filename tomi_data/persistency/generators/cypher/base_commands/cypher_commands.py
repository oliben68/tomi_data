from tomi_data.persistency.generators.base_generator import BaseGenerator
from tomi_data.persistency.generators.cypher import BooleanOperator


class CypherCommands(BaseGenerator):
    excluded_properties = []
    property_prefix = ""

    @staticmethod
    def properties_values_map(excluded=None, property_prefix=None, **properties):
        if len(properties) == 0:
            return "{}"

        property_prefix = "" if type(property_prefix) != str else property_prefix
        excluded_properties = [] if excluded is None else [property_prefix + e for e in excluded] + excluded
        keys_values = [
            "`{key}`: {value}".format(key=key.replace(property_prefix, ""), value=CypherCommands.format_value(value))
            for key, value in properties.items() if key not in excluded_properties and value is not None
        ]
        return "{{{props}}}".format(props=", ".join(keys_values))

    @staticmethod
    def properties_values_list(boolean_operator=None, excluded=None, **properties):
        if len(properties) == 0:
            return ""

        if type(boolean_operator) != BooleanOperator:
            boolean_operator = BooleanOperator.AND

        properties_values = [
            "`{k}` = {v}".format(k=key.replace(CypherCommands.property_prefix, ""),
                                 v=CypherCommands.format_value(value)) for key, value in properties.items() if
            key not in (CypherCommands.excluded_properties if excluded is None else excluded) and value is not None
        ]
        return boolean_operator.value.join(properties_values)
