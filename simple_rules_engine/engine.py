from .fields import FIELD_NO_INPUT


def run_all(rule_list, defined_variables, defined_actions, stop_on_first_trigger=False):
    rule_was_triggered = False
    for rule in rule_list:
        result = run(rule, defined_variables, defined_actions)
        if result:
            rule_was_triggered = True
            if stop_on_first_trigger:
                return True
    return rule_was_triggered


def run(rule, defined_variables, defined_actions):
    conditions, actions = rule['conditions'], rule['actions']
    rule_triggered = check_conditions_recursively(conditions, defined_variables)
    if rule_triggered:
        do_actions(actions, defined_actions)
        return True
    return False


def check_conditions_recursively(conditions, defined_variables):
    keys = list(conditions.keys())
    if keys == ['all']:
        assert len(conditions['all']) >= 1
        for condition in conditions['all']:
            if not check_conditions_recursively(condition, defined_variables):
                return False
        return True
    elif keys == ['any']:
        assert len(conditions['any']) >= 1
        for condition in conditions['any']:
            if check_conditions_recursively(condition, defined_variables):
                return True
        return False
    elif keys == ['some']:
        assert len(conditions['some']) >= 1
        for condition in conditions['some']:
            if check_conditions_recursively(condition, defined_variables):
                return True
        return False
    else:
        assert not ('all' in keys or 'any' in keys or 'some' in keys)
        return check_condition(conditions, defined_variables)


def check_condition(condition, defined_variables):
    name, op, value = condition['name'], condition['operator'], condition['value']
    operator_type = _get_variable_value(defined_variables, name)
    return _do_operator_comparison(operator_type, op, value)


def _get_variable_value(defined_variables, name):
    def fallback(*args, **kwargs):
        raise AssertionError(
            "Variable {0} is not defined in class {1}".format(name, defined_variables.__class__.__name__))

    method = getattr(defined_variables, name, fallback)
    val = method()
    return method.field_type(val)


def _do_operator_comparison(operator_type, operator_name, comparison_value):
    def fallback(*args, **kwargs):
        raise AssertionError(
            "Operator {0} does not exist for type {1}".format(operator_name, operator_type.__class__.__name__))

    method = getattr(operator_type, operator_name, fallback)
    if getattr(method, 'input_type', '') == FIELD_NO_INPUT:
        return method()
    return method(comparison_value)


def do_actions(actions, defined_actions):
    for action in actions:
        method_name = action['name']

        def fallback(*args, **kwargs):
            raise AssertionError(
                "Action {0} is not defined in class {1}".format(method_name, defined_actions.__class__.__name__))

        params = action.get('params') or {}
        method = getattr(defined_actions, method_name, fallback)
        method(**params)
