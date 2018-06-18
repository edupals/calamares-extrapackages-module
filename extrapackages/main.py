#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Copyright 2018, Raul Rodrigo Segura <raurodse@gmail.com>
#
#   GPLv3

import platform
import imghdr

from PythonQt.QtGui import *
from PythonQt.QtCore import *
from PythonQt.QtSvg import QSvgWidget
import PythonQt.calamares as calamares

import gettext
import inspect
import os
_filename = inspect.getframeinfo(inspect.currentframe()).filename
_path = os.path.dirname(os.path.abspath(_filename))

_ = gettext.gettext

@calamares_module
class ExtraPackagesViewStep:
    def __init__(self):

        self.main_widget = QFrame()
        self.main_widget.setLayout(QVBoxLayout())
        qsa = QScrollArea()
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
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

        for app in calamares.configuration['packages']:
            print(app)
            config = calamares.configuration['packages'][app]
            print(config['name'])
            print(config['description'])
            print(config['image'])
            print(config['checked'])
            print(config['package'])
            widget.layout().addLayout(self.add_package(config))


    def add_package(self, config, last=False):
        vLayout = QVBoxLayout()
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setObjectName("horizontalLayout")
        is_img = True
        if imghdr.what(config['image']) == '':
            is_img = False
        if is_img:
            label = QLabel()
            label.setText("")
            label.setScaledContents(True)
            label.setPixmap(QPixmap(config['image']))

        else:
            label = QSvgWidget()
            label.load(config['image'])
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label.setSizePolicy(sizePolicy)
        label.setMaximumSize(QSize(40, 40))
        label.setObjectName("label")


        horizontalLayout.addWidget(label)
        verticalLayout_3 = QVBoxLayout()
        verticalLayout_3.setObjectName("verticalLayout_3")
        horizontalLayout_2 = QHBoxLayout()
        horizontalLayout_2.setObjectName("horizontalLayout_2")
        verticalLayout_4 = QVBoxLayout()
        verticalLayout_4.setObjectName("verticalLayout_4")
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
        verticalLayout_4.addWidget(label_3)
        label_2 = QLabel()
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label_2.setSizePolicy(sizePolicy)
        label_2.setObjectName("label_2")
        label_2.setStyleSheet("QLabel{margin-left:5px ; color: #666 }")
        verticalLayout_4.addWidget(label_2)
        horizontalLayout_2.addLayout(verticalLayout_4)
        checkBox = QCheckBox()
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        checkBox.setSizePolicy(sizePolicy)
        checkBox.setObjectName("checkBox")
        checkBox.setChecked(config['checked'])
        checkBox.connect("clicked(bool)",lambda: self.modify_package(config['package'],checkBox))
        horizontalLayout_2.addWidget(checkBox)
        verticalLayout_3.addLayout(horizontalLayout_2)
        horizontalLayout.addLayout(verticalLayout_3)
        vLayout.addLayout(horizontalLayout)
        if not last:
            verticalLayout_3.addWidget(self.add_line())
        label_3.setText(_(config['name']))
        label_2.setText(_(config['description']))
        checkBox.setText(_("Install"))
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
        print(package_name,checkbox.isChecked())


    def prettyName(self):
        return _("Dummy PythonQt ViewStep")

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
        return [DummyPQJob("Dummy PythonQt job reporting for duty")]

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
            _t = gettext.translation('dummypythonqt',
                                     localedir=os.path.join(_path, 'lang'),
                                     languages=[locale_name])
            _ = _t.gettext
        except OSError as e:
            calamares.utils.debug(e)
            pass

        # ... and then we can call setText(_("foo")) and similar methods on
        # the relevant widgets here to reapply the strings.

# An example Job class. Implements Calamares::Job. For method identifiers, the
# same rules apply as for ViewStep. No decorators are necessary here, because
# only the ViewStep implementation is the unique entry point, and a module can
# have any number of jobs.


class DummyPQJob:
    def __init__(self, my_msg):
        self.my_msg = my_msg

    def pretty_name(self):
        return _("The Dummy PythonQt Job")

    def pretty_description(self):
        return _("This is the Dummy PythonQt Job. "
                 "The dummy job says: {}").format(self.my_msg)

    def pretty_status_message(self):
        return _("A status message for Dummy PythonQt Job.")

    def exec(self):
        # As an example, we touch a file in the target root filesystem.
        rmp = calamares.global_storage['rootMountPoint']
        os.system("touch {}/calamares_dpqt_was_here".format(rmp))
        calamares.utils.debug("the dummy job says {}".format(self.my_msg))
        return {'ok': True}
