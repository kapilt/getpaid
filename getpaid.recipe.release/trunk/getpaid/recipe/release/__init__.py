# -*- coding: utf-8 -*-
"""Recipe release"""

import re
import os.path
egg_name_re = re.compile(r'(\S+?)([=<>!].+)')

from getpaid.recipe.release.getpaidcorepackages import GETPAID_PACKAGES

import zc.recipe.egg


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        # These are passed onto zc.recipe.egg.
        options['eggs'] = self.getpaid_eggs()
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'],
            self.name
            )

    def install(self):
        """Installer"""
        options = self.options
        location = options['location']
        self.egg.install()
        return location
        
    def update(self):
        """Updater"""
        pass

    def getpaid_eggs(self):
        """Read the eggs from dist_plone
        """
        egg_spec = self.options.get('eggs', '')
        explicit_eggs = {}
        for spec in egg_spec.split():
            name = spec
            version = ''
            match = egg_name_re.match(spec)
            if match:
                name = match.groups(1)
                version = match.groups(2)
            explicit_eggs[name] = version
        
        eggs = []
        for pkg in GETPAID_PACKAGES:
            name = pkg.name
            if name in explicit_eggs:
                eggs.append(name + explicit_eggs[name])
                del explicit_eggs[name]
            else:
                if pkg.version is not None:
                    name += "==%s" % pkg.version
                eggs.append(name)
        
        for name, version in explicit_eggs.items():
            eggs.append(name + version)
        
        return '\n'.join(eggs)
