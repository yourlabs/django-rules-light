import rules_light

rules_light.registry['auth.user.read'] = True
rules_light.registry['auth.user.update'] = lambda user, *args: user.is_staff
