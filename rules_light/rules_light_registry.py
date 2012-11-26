import rules_light


rules_light.registry['rules_light.rule.read'] = lambda u, n: u.is_staff
