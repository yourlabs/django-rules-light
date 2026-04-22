# Plan de maintenance — django-rules-light

> Repo : https://github.com/yourlabs/django-rules-light
> Date du plan : 2026-04-20
> Auteur : contact@yourlabs.org
> Dernière inspection du code : 2026-04-20 (revue automatisée sur code réel)

---

## État actuel

| Indicateur | Valeur |
|---|---|
| Version sur PyPI (setup.py) | 0.3.2 |
| Dernier tag git | 0.3.0 |
| `__version__` dans le code | `(0, 2, 0)` — désynchronisée de 2 niveaux par rapport à PyPI |
| Dernier commit | 17 avril 2024 (merge Snyk sqlparse fix) |
| Dernier commit fonctionnel | 12 août 2022 (Fix small bug with 4.1) |
| Support Django déclaré (README) | Django 1.8+ |
| Support Python déclaré (README) | Python 2.7+ (Python 3 supporté) |
| Support Django réel (tox.ini) | Django 1.8 à 2.1 uniquement |
| Support Django ajouté ad hoc | Django 4.x (commit jan 2022, non documenté) |
| CI | Travis CI — obsolète (service dégradé depuis 2021, `.travis.yml` présent mais sans `.github/workflows/`) |
| Issues ouvertes | 1 (#13 — lien cassé dans README) |
| PRs ouvertes | 2 (#16 doc, #20 super() modernisation) |
| Mode | **Maintenance only** (description GitHub officielle) |
| Étoiles | 68 |

### Dépendances problématiques — état confirmé dans le code

| Problème | Fichier | Ligne | Confirmé |
|---|---|---|---|
| `import six` | `rules_light/class_decorator.py` | 5 | Oui — `six.string_types` ligne 67, `six.PY2` ligne 68, `six.PY3` ligne 70 |
| `from django.utils.importlib import import_module` | `rules_light/registry.py` | 140 | Oui — dans `_autodiscover()`, code mort Django >= 1.7 |
| `user.is_authenticated()` comme méthode | `rules_light/shortcuts.py` | 73 | Oui — try/except palliatif présent ; docstring `decorators.py:7,17` contient aussi `is_authenticated()` avec parenthèses |
| `smart_str as smart_text` alias | `rules_light/registry.py` | 15 | Partiellement corrigé : l'alias existe mais `smart_text` est toujours le nom utilisé aux lignes 90, 93, 94, 120 |
| `func_name` Python 2 | `rules_light/registry.py` | 109 | Oui — `hasattr(rule, 'func_name')` toujours présent |
| `from __future__ import unicode_literals` | 17 fichiers | multiple | Oui — présent dans tous les fichiers sources et tests (voir liste complète en 3.5) |
| `django-classy-tags` dans `install_requires` | `setup.py` | 55 | Réellement utilisé dans `rules_light/templatetags/rules_light_tags.py` lignes 5-8 — à garder |
| `super(ClassName, self)` ancien style | `registry.py`, `middleware.py`, `exceptions.py` | multiple | Oui — 4 occurrences (PR #20 en attente) |
| `django.VERSION >= (1, 8)` branche morte | `rules_light/class_decorator.py` | 84 | Oui — branche `else` (ligne 98) pour Django < 1.8 jamais exécutée |
| `VERSION > (1, 8)` branche morte | `rules_light/middleware.py` | 27 | Oui — branche `else` (ligne 29) pour Django <= 1.8 jamais exécutée |
| `if django.VERSION < (1, 7)` | `rules_light/tests/__init__.py` | 4 | Oui — code mort, autodiscover manuel pré-1.7 jamais exécuté |

---

## Phase 1 — Actions immédiates

Ces actions corrigent des problèmes visibles dès aujourd'hui sans toucher à la logique métier.

### 1.1 Corriger le lien cassé dans le README (issue #13)

- **Problème** : `See community guidelines <http://docs.yourlabs.org>` dans `README.rst` ligne 95 retourne 403.
- **Fichier** : `README.rst:95`
- **Code actuel** :
  ```rst
  See `community guidelines
  <http://docs.yourlabs.org>`_ for details.
  ```
- **Fix** : supprimer la mention ou remplacer par `https://github.com/yourlabs/django-rules-light/blob/master/CONTRIBUTING.rst` (si le fichier existe) ou simplement supprimer la phrase.
- **Difficulté** : triviale (1 ligne).

### 1.2 Mettre à jour les badges du README

- **Fichier** : `README.rst`, lignes 1-6.
- **Code actuel** :
  ```rst
  .. image:: https://secure.travis-ci.org/yourlabs/django-rules-light.png?branch=master
      :target: http://travis-ci.org/yourlabs/django-rules-light
  .. image:: https://img.shields.io/pypi/dm/django-rules-light.svg
      :target: https://crate.io/packages/django-rules-light
  .. image:: https://img.shields.io/pypi/v/django-rules-light.svg
      :target: https://crate.io/packages/django-rules-light
  ```
- **Problèmes** : Travis CI mort ; crate.io mort (les deux liens cibles sont invalides).
- **Fix** : remplacer par badge PyPI vers `https://pypi.org/project/django-rules-light/` et badge GitHub Actions une fois la CI migrée (Phase 3.2).
- **Difficulté** : triviale.

### 1.3 Mettre à jour les prérequis déclarés dans le README

- **Fichier** : `README.rst`, lignes 70-72.
- **Code actuel** :
  ```rst
  - Python 2.7+ (Python 3 supported)
  - Django 1.8+
  ```
- **Fix** : remplacer par les versions réelles après Phase 3.1 (ex. Python 3.10+, Django 4.2+).
- **Difficulté** : triviale.

### 1.4 Fusionner ou fermer la PR #16 (documentation RegistryView)

- PR ouverte depuis mars 2021 par spapas.
- La vue `RegistryView` est dans `rules_light/views.py` lignes 8-29 — la doc dans la docstring est incomplète.
- **Action** : review rapide, merge si correct.
- **Difficulté** : triviale.

---

## Phase 2 — Bugs à corriger

### 2.1 Supprimer la dépendance à `six`

- **Fichier** : `rules_light/class_decorator.py`
- **Lignes concernées** : 5, 67, 68-71
- **Code problématique** :
  ```python
  # ligne 5
  import six

  # ligne 67-71
  elif isinstance(args[0], six.string_types):
      if six.PY2:
          decorator_name = b'new_class_decorator'
      elif six.PY3:
          decorator_name = 'new_class_decorator'
  ```
- **Problème** : `six` est la bibliothèque de compatibilité Python 2/3. Elle n'est plus maintenue. L'import au niveau module plante à l'import si `six` n'est pas installé.
- **Fix précis** :
  1. Supprimer `import six` ligne 5.
  2. Remplacer `isinstance(args[0], six.string_types)` par `isinstance(args[0], str)` ligne 67.
  3. Remplacer les lignes 68-71 par `decorator_name = 'new_class_decorator'` (supprimer la branche `PY2`/`PY3` entièrement).
  4. Retirer `'six'` de `install_requires` dans `setup.py` ligne 54.
- **Code après correction** :
  ```python
  elif isinstance(args[0], str):
      decorator_name = 'new_class_decorator'
      new_class_decorator = type(decorator_name,
          (class_decorator,), {'rule': args[0]})
      return new_class_decorator
  ```
- **Difficulté** : faible (changement localisé, 4 lignes).

### 2.2 Corriger l'usage de `smart_text` dans `registry.py`

- **Fichier** : `rules_light/registry.py`
- **Lignes concernées** : 15, 90, 93, 94, 120
- **Code actuel** :
  ```python
  # ligne 15
  from django.utils.encoding import smart_str as smart_text

  # ligne 90
  formated_args.append(u'"%s"' % smart_text(arg))

  # lignes 93-94
  formated_args.append(u'%s="%s"' % (smart_text(key),
      smart_text(value)))

  # ligne 120
  return smart_text(rule)
  ```
- **État** : l'import est déjà migré (`smart_str as smart_text`) mais le nom `smart_text` est conservé comme alias dans tout le fichier. L'alias `smart_text` a été supprimé de Django dans Django 4.0. Importer `smart_str` sous un alias `smart_text` fonctionne en Django 4.x mais génère de la confusion.
- **Fix précis** :
  1. Ligne 15 : `from django.utils.encoding import smart_str`
  2. Remplacer tous les `smart_text(` par `smart_str(` (lignes 90, 93, 94, 120) — 4 occurrences.
- **Difficulté** : triviale (renommage pur, 5 occurrences).

### 2.3 Supprimer `_autodiscover` — code mort depuis Django 1.7

- **Fichier** : `rules_light/registry.py`
- **Lignes** : 136-195
- **Code problématique** :
  ```python
  # ligne 136-160
  def _autodiscover(registry):
      import copy
      from django.conf import settings
      from django.utils.importlib import import_module   # n'existe plus depuis Django 1.9
      from django.utils.module_loading import module_has_submodule
      ...

  # lignes 17-20 (try/except pour autodiscover_modules)
  try:
      from django.utils.module_loading import autodiscover_modules
  except ImportError:
      autodiscover_modules = None

  # ligne 192-195 (branche else jamais atteinte)
  if autodiscover_modules:
      autodiscover_modules('rules_light_registry')
  else:
      _autodiscover(registry)
  ```
- **Problème** : `django.utils.importlib` a été supprimé dans Django 1.9. `autodiscover_modules` existe depuis Django 1.7. La branche `else: _autodiscover(registry)` ligne 195 ne sera jamais exécutée avec toute version Django moderne. Si atteinte par erreur, elle lève immédiatement `ImportError`.
- **Fix précis** : supprimer `_autodiscover` (lignes 136-160), supprimer le `try/except ImportError` (lignes 17-20), simplifier `autodiscover()` :
  ```python
  from django.utils.module_loading import autodiscover_modules

  def autodiscover():
      """..."""
      autodiscover_modules('rules_light_registry')
  ```
- **Difficulté** : faible (suppression de code mort, aucun effet fonctionnel).

### 2.4 Supprimer `func_name` (attribut Python 2)

- **Fichier** : `rules_light/registry.py`
- **Lignes** : 109-110
- **Code actuel** :
  ```python
  def rule_text_name(self, rule):
      if hasattr(rule, 'func_name'):    # Python 2 uniquement — toujours False en Python 3
          return rule.func_name
      elif rule is True:
          ...
      elif hasattr(rule, '__name__'):   # couvre déjà le cas — ligne 115
          return rule.__name__
  ```
- **Problème** : `func_name` est l'attribut Python 2 des fonctions. En Python 3, l'attribut est `__name__`. La branche `hasattr(rule, '__name__')` ligne 115 couvre déjà le cas. La branche `func_name` est toujours fausse en Python 3.
- **Fix précis** : supprimer les lignes 109-110 (`if hasattr(rule, 'func_name'):` et `return rule.func_name`).
- **Difficulté** : triviale (2 lignes).

### 2.5 Corriger `user.is_authenticated()` — appel comme méthode

- **Fichier principal** : `rules_light/shortcuts.py`
- **Lignes** : 68-75
- **Code actuel** :
  ```python
  @make_decorator
  def is_authenticated(user, rulename, *args, **kwargs):
      """
      Return user.is_authenticated().     # ← docstring incorrecte
      """
      try:
          return user and user.is_authenticated()   # Django < 2.0 (méthode)
      except Exception:
          return user and user.is_authenticated     # Django 2.0+ (attribut booléen)
  ```
- **Fichier secondaire** : `rules_light/decorators.py`
- **Lignes** : 7, 17 — la docstring du module contient deux occurrences de `user.is_authenticated()` avec parenthèses (exemples de code dans la docstring).
- **Problème** : `user.is_authenticated` est un attribut booléen depuis Django 2.0 (supprimé comme méthode). Le `try/except Exception` est trop large — il masque toutes les erreurs sur la branche principale. La docstring est également incorrecte.
- **Fix précis pour `shortcuts.py`** :
  ```python
  @make_decorator
  def is_authenticated(user, rulename, *args, **kwargs):
      """
      Return True if user.is_authenticated.
      """
      return user and user.is_authenticated
  ```
- **Fix pour `decorators.py`** : lignes 7 et 17, remplacer `user.is_authenticated()` par `user.is_authenticated` dans la docstring.
- **Difficulté** : triviale (suppression du try/except + 2 corrections de docstring).

### 2.6 Supprimer les branches mortes Django < 1.8 / Django <= 1.8

- **Fichier 1** : `rules_light/class_decorator.py:84-110`
  ```python
  if django.VERSION >= (1, 8):          # ligne 84 — branche principale
      def new_get_form(self, *args, **kwargs):
          ...
  else:                                  # lignes 98-110 — JAMAIS exécuté
      def new_get_form(self, form_class, *args, **kwargs):
          ...
  ```
  **Fix** : supprimer le `if django.VERSION >= (1, 8):` et la branche `else` (lignes 98-110), garder uniquement le corps de la branche `if`.

- **Fichier 2** : `rules_light/middleware.py:27-31`
  ```python
  if VERSION > (1, 8):                  # ligne 27 — branche principale
      ctx = dict(request=request, exception=exception, settings=settings)
  else:                                  # lignes 29-31 — JAMAIS exécuté
      ctx = template.RequestContext(request, dict(exception=exception,
          settings=settings))
  ```
  **Fix** : remplacer par `ctx = dict(request=request, exception=exception, settings=settings)` (supprimer le if/else, supprimer aussi `from django import VERSION` si devenu inutile).

- **Fichier 3** : `rules_light/tests/__init__.py:1-6`
  ```python
  import django
  if django.VERSION < (1, 7):           # lignes 4-6 — JAMAIS exécuté
      import rules_light
      rules_light.autodiscover()
  ```
  **Fix** : vider entièrement ce fichier (laisser vide ou supprimer le contenu).

- **Difficulté** : triviale.

### 2.7 Confirmer l'utilisation de `django-classy-tags`

- **Résultat de l'inspection** : `django-classy-tags` EST réellement utilisé.
- **Fichier** : `rules_light/templatetags/rules_light_tags.py`, lignes 5-8 :
  ```python
  from classytags.core import Options
  from classytags.helpers import AsTag
  from classytags.arguments import (Argument, MultiKeywordArgument, MultiValueArgument)
  ```
- **Action** : NE PAS supprimer de `install_requires`. Vérifier que `django-classy-tags` est compatible avec Django 4.x/5.x — si ce n'est pas le cas, envisager de réécrire le templatetag sans cette dépendance (tag Django natif).
- **Note** : `django-classy-tags` est maintenu par divio/django-cms. Vérifier la compatibilité avant la Phase 3.

### 2.8 Fusionner la PR #20 (super() modernisation)

- PR ouverte en mars 2025 par KommuSoft.
- Les 4 occurrences de `super(ClassName, self)` dans le code (confirmées par grep) :
  - `rules_light/registry.py:41` — `super(RuleRegistry, self).__setitem__(...)`
  - `rules_light/middleware.py:36` — `super(Middleware, self).__init__()`
  - `rules_light/exceptions.py:11` — `super(Denied, self).__init__(...)`
  - `rules_light/exceptions.py:16` — `super(DoesNotExist, self).__init__(...)`
- **Action** : review et merge. Compatible Python 3 uniquement — cohérent avec l'abandon de Python 2.
- **Difficulté** : triviale (4 remplacements mécaniques).

---

## Phase 3 — Modernisation

Objectif : garder le repo utilisable avec les versions Django et Python actuelles, sans ajouter de features.

### 3.1 Déclarer la compatibilité Django 4.x et 5.x

- Le commit "Support django 4.x" (janvier 2022) et "Fix small bug with 4.1" (août 2022) existent mais ne sont pas documentés.
- Django 5.0 (décembre 2023), 5.1 (août 2024), 5.2 LTS (avril 2025) sont sortis.
- **Action** : tester manuellement sur Django 4.2 LTS, 5.0, 5.1, 5.2 et Python 3.10, 3.11, 3.12.
- Mettre à jour les classifiers dans `setup.py` (lignes 57-66) après tests.
- **Préconditions** : les bugs 2.1 à 2.6 doivent être corrigés avant le test.

### 3.2 Remplacer Travis CI par GitHub Actions

- **Fichier existant** : `.travis.yml` — présent, fonctionnel mais Travis CI est dégradé/payant depuis 2021.
- **Aucun fichier** `.github/workflows/` n'existe dans le repo.
- **Action** : créer `.github/workflows/ci.yml` avec une matrice :
  - Python : 3.10, 3.11, 3.12
  - Django : 4.2, 5.0, 5.1, 5.2
  - Commande : `pytest rules_light/tests/`
- Supprimer `.travis.yml` ou le conserver en archive.
- **Difficulté** : moyenne (rédaction du workflow YAML).

### 3.3 Mettre à jour `tox.ini`

- **Fichier** : `tox.ini`
- **État actuel** :
  ```ini
  envlist = py{27}-django{18,19,110,111}, py{36}-django{18,19,110,111,20,21}
  commands = python setup.py test   # deprecated
  ```
- **Fix** : remplacer par Python 3.10/3.11/3.12 x Django 4.2/5.x et `commands = pytest rules_light/tests/`.
- **Difficulté** : faible.

### 3.4 Migrer le packaging vers `pyproject.toml`

- **Fichiers actuels** : `setup.py` + `setup.cfg`
- `setup.py` ligne 8 contient une classe `RunTests(Command)` qui est un mécanisme deprecated.
- **Action** : créer un `pyproject.toml` avec `[build-system]` (setuptools >= 61), déplacer les métadonnées.
- Mettre à jour la version vers `0.4.0` pour marquer le passage Python 3 uniquement.
- **Synchroniser `__version__`** dans `rules_light/__init__.py:10` : actuellement `(0, 2, 0)` alors que PyPI est `0.3.2` et que la prochaine version sera `0.4.0`.
- **Difficulté** : moyenne.

### 3.5 Supprimer `from __future__ import unicode_literals`

- **Fichiers concernés** (17 au total, confirmés par grep) :
  - `rules_light/registry.py:11`
  - `rules_light/class_decorator.py:4`
  - `rules_light/shortcuts.py:25`
  - `rules_light/decorators.py:28`
  - `rules_light/middleware.py:5`
  - `rules_light/views.py:1`
  - `rules_light/urls.py:1`
  - `rules_light/exceptions.py:1`
  - `rules_light/rules_light_registry.py:1`
  - `rules_light/tests/test_autodiscover.py:1`
  - `rules_light/tests/test_class_decorator.py:1`
  - `rules_light/tests/test_decorators.py:1`
  - `rules_light/tests/test_middleware.py:1`
  - `rules_light/tests/test_registry.py:2`
  - `rules_light/tests/test_shortcuts.py:1`
  - `rules_light/tests/test_views.py:1`
  - `rules_light/tests/fixtures/class_decorator_classes.py:1`
- Sans effet en Python 3 — nettoyage de lisibilité pur.
- **Difficulté** : triviale (chercher/remplacer sur 17 fichiers).

### 3.6 Vérifier la compatibilité de `django-classy-tags`

- Utilisé dans `rules_light/templatetags/rules_light_tags.py`.
- Vérifier que `django-classy-tags` supporte Django 4.x/5.x.
- Si non compatible, réécrire le templatetag `Rule` comme un tag Django natif (simple `inclusion_tag` ou tag personnalisé) — cela permettrait également de supprimer la dépendance externe.
- **Difficulté** : faible à moyenne selon compatibilité.

### 3.7 Mettre à jour la documentation

- Le lien `django-rules-light.readthedocs.org` (ancien domaine) redirige vers `readthedocs.io`.
- Vérifier que la doc se build correctement avec Python 3 et Sphinx actuel.
- **`README.rst:80`** : `settings.MIDDLEWARE_CLASSES` est obsolète depuis Django 1.10 — remplacer par `settings.MIDDLEWARE`.
- **`rules_light/middleware.py:17`** : la docstring de la classe `Middleware` mentionne encore `settings.MIDDLEWARE_CLASSES`` — corriger en `settings.MIDDLEWARE`.
- **Difficulté** : faible.

---

## Phase 4 — Issues à fermer comme obsolètes

| # | Titre | Raison de fermeture |
|---|---|---|
| #13 | README.rst: Link to community guidelines returns 403 | Sera corrigé en Phase 1.1 — fermer après le commit |

**Note** : seulement 1 issue ouverte. Elle est légitime et sera résolue en Phase 1.
Les 2 PRs ouvertes (#16, #20) sont à traiter (voir Phases 1 et 2) avant fermeture.

---

## Résumé des actions par ordre de priorité

### Urgent — bugs bloquants à l'import sur Python 3 / Django 4+

- [ ] **2.1** Supprimer `import six` dans `rules_light/class_decorator.py:5` et `setup.py:54`
  - `isinstance(args[0], six.string_types)` → `isinstance(args[0], str)` (ligne 67)
  - Supprimer la branche `PY2`/`PY3` (lignes 68-71) → `decorator_name = 'new_class_decorator'`
- [ ] **2.2** Renommer `smart_text` → `smart_str` dans `rules_light/registry.py`
  - Ligne 15 : `from django.utils.encoding import smart_str`
  - Lignes 90, 93, 94, 120 : remplacer `smart_text(` par `smart_str(`
- [ ] **2.5** Simplifier `user.is_authenticated` dans `rules_light/shortcuts.py:68-75` (supprimer le try/except + corriger la docstring)
  - Corriger aussi la docstring de `rules_light/decorators.py:7,17`
- [ ] **2.4** Supprimer la branche `func_name` dans `rules_light/registry.py:109-110`
- [ ] **2.3** Supprimer `_autodiscover` et `django.utils.importlib` dans `rules_light/registry.py:136-160` + simplifier `autodiscover()` lignes 163-195

### Nettoyage — code mort Django < 1.8

- [ ] **2.6** Supprimer la branche `else` de `class_decorator.py:84` (Django < 1.8, lignes 98-110)
- [ ] **2.6** Supprimer la branche `else` de `middleware.py:27` (Django <= 1.8, lignes 29-31)
- [ ] **2.6** Vider `rules_light/tests/__init__.py` (autodiscover pré-1.7, lignes 4-6)

### Urgent — visibilité / confiance du repo

- [ ] **1.1** Corriger le lien cassé `http://docs.yourlabs.org` dans `README.rst:95` (issue #13)
- [ ] **1.2** Mettre à jour les badges du README (Travis CI mort, crate.io mort) — `README.rst:1-6`
- [ ] **1.3** Mettre à jour les prérequis dans le README (Python 2.7+ / Django 1.8+ obsolètes) — `README.rst:70-72`
- [ ] Corriger `settings.MIDDLEWARE_CLASSES` → `settings.MIDDLEWARE` dans `README.rst:80` et `middleware.py:17`

### PRs à traiter

- [ ] **2.8** Merger PR #20 (super() modernisation) après review — 4 occurrences dans `registry.py:41`, `middleware.py:36`, `exceptions.py:11,16`
- [ ] **1.4** Merger PR #16 (correction doc RegistryView) après review

### CI / packaging

- [ ] **3.2** Créer `.github/workflows/ci.yml` (remplacer `.travis.yml`)
- [ ] **3.3** Mettre à jour `tox.ini` (Python 3.10-3.12, Django 4.2-5.x, commande `pytest`)
- [ ] **3.4** Migrer vers `pyproject.toml`, synchroniser `__version__` (`rules_light/__init__.py:10` : `(0, 2, 0)` → `(0, 4, 0)`) et créer un tag git `0.4.0`

### Tests de compatibilité

- [ ] **3.1** Tester sur Django 4.2 LTS + Python 3.10/3.11/3.12
- [ ] Tester sur Django 5.0 + Python 3.11/3.12
- [ ] Tester sur Django 5.2 LTS + Python 3.12
- [ ] Documenter les résultats dans README et classifiers PyPI (`setup.py:57-66`)

### Documentation et nettoyage cosmétique

- [ ] **3.5** Supprimer les `from __future__ import unicode_literals` (17 fichiers — liste complète en section 3.5)
- [ ] **3.6** Vérifier la compatibilité `django-classy-tags` avec Django 4.x/5.x
- [ ] **3.7** Vérifier le build ReadTheDocs et corriger les mentions `MIDDLEWARE_CLASSES`
- [ ] Fermer issue #13 après correction du lien
