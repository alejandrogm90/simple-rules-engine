from unittest import TestCase

from simple_rules_engine.operators import StringType
from simple_rules_engine.variables import BaseVariables, rule_variable


class VariablesClassTests(TestCase):

    def test_base_has_no_variables(self):
        self.assertEqual(len(BaseVariables.get_all_variables()), 0)

    def test_get_all_variables(self):

        class SomeVariables(BaseVariables):

            @rule_variable(StringType)
            def this_is_rule_1(self):
                return "blah"

            def non_rule(self):
                return "baz"

        vars = SomeVariables.get_all_variables()
        self.assertEqual(len(vars), 1)
        self.assertEqual(vars[0]['name'], 'this_is_rule_1')
        self.assertEqual(vars[0]['label'], 'This Is Rule 1')
        self.assertEqual(vars[0]['field_type'], 'string')
        self.assertEqual(vars[0]['options'], [])
        self.assertEqual(len(SomeVariables().get_all_variables()), 1)
