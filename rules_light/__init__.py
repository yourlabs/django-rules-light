from .registry import RuleRegistry, registry, run, require, autodiscover
from .class_decorator import class_decorator
from .decorators import make_decorator
from .exceptions import Denied, DoesNotExist, RulesLightException
from .middleware import Middleware
from .shortcuts import is_authenticated, is_staff

default_app_config = 'rules_light.apps.RulesLightConfig'

__version__ = (0, 2, 0)
