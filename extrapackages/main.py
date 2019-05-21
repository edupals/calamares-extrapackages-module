#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Copyright 2018, Raul Rodrigo Segura <raurodse@gmail.com>
#
#   GPLv3

from PythonQt.QtGui import *
from PythonQt.QtCore import *
from PythonQt.QtSvg import QSvgWidget
import PythonQt.calamares as calamares

# Set up translations.
# You may skip this if your Calamares module has no user visible strings.
# DO NOT install _ into the builtin namespace because each module loads
# its own catalog.
# DO use the gettext class-based API and manually alias _ as described in:
# https://docs.python.org/3.5/library/gettext.html#localizing-your-module
import gettext
import inspect
import os
_filename = inspect.getframeinfo(inspect.currentframe()).filename
_path = os.path.dirname(os.path.abspath(_filename))

_ = gettext.gettext

# Example Python ViewModule.
# A Python ViewModule is a Python program which defines a ViewStep class.
# One UI module ==> one ViewStep.
# This class must be marked with the @calamares_module decorator. A
# ViewModule may define other classes, but only one may be decorated with
# @calamares_module. Such a class must conform to the Calamares ViewStep
# interface and functions as the entry point of the module.
# A ViewStep manages one or more "wizard pages" through methods like
# back/next, and reports its status through isNextEnabled/isBackEnabled/
# isAtBeginning/isAtEnd. The whole UI, including all the pages, must be
# exposed as a single QWidget, returned by the widget function.
#
# For convenience, both C++ and PythonQt ViewSteps are considered to be
# implementations of ViewStep.h. Additionally, the Calamares PythonQt API
# allows Python developers to keep their identifiers more Pythonic on the
# Python side. Thus, all of the following are considered valid method
# identifiers in a ViewStep implementation: isNextEnabled, isnextenabled,
# is_next_enabled.


@calamares_module
class ExtraPackagesViewStep:
    def __init__(self):

        initial_configuration = calamares.global_storage.value('packageOperations')
        if initial_configuration is None:
            calamares.global_storage.insert('packageOperations',({'try_install':()},))
        self.main_widget = QFrame()
        self.main_widget.setLayout(QVBoxLayout())
        qsa = QScrollArea()
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        print(calamares.global_storage.keys())
        widget.layout().setAlignment(Qt.AlignCenter | Qt.AlignTop)
        qsa.setWidget(widget)
        qsa.setWidgetResizable(True)

        label = QLabel()
        self.main_widget.layout().addWidget(label)
        self.main_widget.layout().addWidget(qsa)
        label.text = _("Select extra packages to install")
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        fontlabel = QFont()
        fontlabel.setBold(True)
        fontlabel.setWeight(75)
        fontlabel.setPixelSize(20)
        label.setFont(fontlabel)
        label.setStyleSheet("QLabel{ margin:0px 0px 10px 0px}")

        #btn = QPushButton()
        count = 0
        for app in calamares.configuration['packages']:
            config = calamares.configuration['packages'][app]
            last = False
            if count+1== len(calamares.configuration['packages']):
                last = True
            widget.layout().addLayout(self.newPackageUI(config), last)
            count+=1


    def createImagePackage(self,config):
        label = QLabel()
        label.setText("")
        label.setScaledContents(True)
        label.setPixmap(QIcon.fromTheme(config['image']).pixmap(40,40))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label.setSizePolicy(sizePolicy)
        label.setMaximumSize(QSize(40, 40))
        label.setObjectName("imagePackage")
        return label

    def createNamePackage(self,config):
        label_3 = QLabel()
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label_3.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        label_3.setFont(font)
        label_3.setObjectName("label_3")
        label_3.setStyleSheet("QLabel{margin-left:5px; }")
        label_3.setText(_(config['name']))
        return label_3

    def createDescriptionPackage(self,config):
        label_2 = QLabel()
        label_2.setWordWrap(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label_2.setSizePolicy(sizePolicy)
        label_2.setObjectName("label_2")
        label_2.setStyleSheet("QLabel{margin-left:5px ; color: #666 }")
        label_2.setText(_(config['description']))
        return label_2

    def createCheckInstallPackage(self,config):
        checkBox = QCheckBox()
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        checkBox.setSizePolicy(sizePolicy)
        checkBox.setObjectName("checkBox")
        checkBox.setChecked(config['checked'])
        checkBox.connect("clicked(bool)",lambda: self.modify_package(config['package'],checkBox))
        if config['checked']:
            self.modify_package(config['package'],checkBox)
        checkBox.setText(_("Install"))
        return checkBox


    def newPackageUI(self, config, last=False):
        vLayout = QVBoxLayout()
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setObjectName("horizontalLayout")
        verticalLayout_3 = QVBoxLayout()
        verticalLayout_3.setObjectName("verticalLayout_3")
        horizontalLayout_2 = QHBoxLayout()
        horizontalLayout_2.setObjectName("horizontalLayout_2")
        verticalLayout_4 = QVBoxLayout()
        verticalLayout_4.setObjectName("verticalLayout_4")
        horizontalLayout_2.addLayout(verticalLayout_4)
        
        image_package = self.createImagePackage(config)
        name_package = self.createNamePackage(config)
        description_package = self.createDescriptionPackage(config)
        install_package = self.createCheckInstallPackage(config)

        horizontalLayout.addWidget(image_package)
        verticalLayout_4.addWidget(name_package)
        verticalLayout_4.addWidget(description_package)
        horizontalLayout_2.addWidget(install_package)

        verticalLayout_3.addLayout(horizontalLayout_2)
        horizontalLayout.addLayout(verticalLayout_3)
        vLayout.addLayout(horizontalLayout)
        if not last:
            verticalLayout_3.addWidget(self.add_line())
        return vLayout

    def add_line(self):
        line = QWidget()
        line.setFixedHeight(1)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        line.setSizePolicy(sizePolicy)
        line.setStyleSheet("QWidget{background-color: #ccc}")
        line.setObjectName("line")
        return line

    def modify_package(self, package_name, checkbox):
        all_packages = calamares.global_storage.value('packageOperations')
        if checkbox.isChecked():
            all_packages = self.install_package(all_packages, package_name)
        else:
            all_packages = self.remove_install_package(all_packages, package_name)
        calamares.global_storage.insert('packageOperations',all_packages)

    def install_package(self, list_packages, package):
        found = False
        for list_index in range(0,len(list_packages)):
            install_keys = [ x for x in ['install','try_install'] if x in list_packages[list_index] ]
            for x in install_keys:
                if package in list_packages[list_index][x]:
                    found = True
        if not found:
            if 'try_install' not in list_packages[0]:
                list_packages[0] = {'try_install':()}
            list_packages[0]['try_install'] = list_packages[0]['try_install'] + (package,)
        return list_packages

    def remove_install_package(self,list_packages, package):
        for list_index in range(0,len(list_packages)):
            if 'try_install' not in list_packages[list_index]:
                continue
            if package in list_packages[list_index]['try_install']:
                list_packages[list_index]['try_install'] = tuple(pack_elem for pack_elem in list_packages[list_index]['try_install'] if pack_elem != package)
        return list_packages

    def prettyName(self):
        return _("Extra packages")

    def isNextEnabled(self):
        return True  # The "Next" button should be clickable

    def isBackEnabled(self):
        return True  # The "Back" button should be clickable

    def isAtBeginning(self):
        # True means the currently shown UI page is the first page of this
        # module, thus a "Back" button click will not be handled by this
        # module and will cause a skip to the previous ViewStep instead
        # (if any). False means that the present ViewStep provides other UI
        # pages placed logically "before" the current one, thus a "Back" button
        # click will be handled by this module instead of skipping to another
        # ViewStep. A module (ViewStep) with only one page will always return
        # True here.
        return True

    def isAtEnd(self):
        # True means the currently shown UI page is the last page of this
        # module, thus a "Next" button click will not be handled by this
        # module and will cause a skip to the next ViewStep instead (if any).
        # False means that the present ViewStep provides other UI pages placed
        # logically "after" the current one, thus a "Next" button click will
        # be handled by this module instead of skipping to another ViewStep.
        # A module (ViewStep) with only one page will always return True here.
        return True

    def jobs(self):
        # Returns a list of objects that implement Calamares::Job.
        return []

    def widget(self):
        # Returns the base QWidget of this module's UI.
        return self.main_widget

    def retranslate(self, locale_name):
        # This is where it gets slightly weird. In most desktop applications we
        # shouldn't need this kind of mechanism, because we could assume that
        # the operating environment is configured to use a certain language.
        # Usually the user would change the system-wide language in a settings
        # UI, restart the application, done.
        # Alas, Calamares runs on an unconfigured live system, and one of the
        # core features of Calamares is to allow the user to pick a language.
        # Unfortunately, strings in the UI do not automatically react to a
        # runtime language change. To get UI strings in a new language, all
        # user-visible strings must be retranslated (by calling tr() in C++ or
        # _() in Python) and reapplied on the relevant widgets.
        # When the user picks a new UI translation language, Qt raises a QEvent
        # of type LanguageChange, which propagates through the QObject
        # hierarchy. By catching and reacting to this event, we can show
        # user-visible strings in the new language at the right time.
        # The C++ side of the Calamares PythonQt API catches the LanguageChange
        # event and calls the present method. It is then up to the module
        # developer to add here all the needed code to load the module's
        # translation catalog for the new language (which is separate from the
        # main Calamares strings catalog) and reapply any user-visible strings.
        calamares.utils.debug("PythonQt retranslation event "
                              "for locale name: {}".format(locale_name))

        # First we load the catalog file for the new language...
        try:
            global _
            _t = gettext.translation('extrapackages',
                                     localedir=os.path.join(_path, 'lang'),
                                     languages=[locale_name])
            _ = _t.gettext
        except OSError as e:
            calamares.utils.debug(e)
            pass

