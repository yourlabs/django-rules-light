from .registry import RuleRegistry as RuleRegistry, registry as registry, run as run, require as require, autodiscover as autodiscover
from .class_decorator import class_decorator as class_decorator
from .decorators import make_decorator as make_decorator
from .exceptions import Denied as Denied, DoesNotExist as DoesNotExist, RulesLightException as RulesLightException
from .middleware import Middleware as Middleware
from .shortcuts import is_authenticated as is_authenticated, is_staff as is_staff

default_app_config = 'rules_light.apps.RulesLightConfig'

__version__ = (0, 4, 0)
