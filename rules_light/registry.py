from exceptions import Denied, DoesNotExist

class RuleRegistry(dict):
    def run(self, user, name, *args, **kwargs):
        if name not in self:
            raise DoesNotExist(name)

        rule = self[name]

        if hasattr(rule, '__call__'):
            result = self[name](user, name, *args, **kwargs)
        else:
            result = rule

        if result:
            return True
        else:
            return False

    def require(self, user, name, *args, **kwargs):
        result = self.run(user, name, *args, **kwargs)

        if not result:
            raise Denied(self[name], user, name, *args, **kwargs)

registry = RuleRegistry()
