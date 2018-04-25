import os
import sys
import time
import math
import configparser
from random import randint
from sys import platform as _platform
import io
from PyQt5 import *
from PyQt5 import uic, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

modulelist = ["module_name_short", "MCT", "recipe", "database", "backup", "XRD", "ftir", "kp", 'grade', "iv"]
moduleavailable = ["1_is_avalable", 1, 1, 1, 1, 1, 1, 1, 1, 1]
thisversion = 0
darkthemeavailable = 1

# All modules below can be successfully imported only if you have them in your file directory
# AND ALL LIBRARIES REQUIRED FOR EACH MODULE ARE PRE_INSTALLED!
# If you are not sure what package need to be installed before running, remove the "try...except..." method for
# the specific module below, and the error message telling you what you are missing should pop up.
try:
    import MCT_calculator_class_v3
    from MCT_calculator_class_v3 import *
    thisversion += float(MCT_calculator_class_v3.__version__)
except ModuleNotFoundError:
    moduleavailable[1] = 0

try:
    import Recipe_designer
    from Recipe_designer import *
    thisversion += float(Recipe_designer.__version__)
except ModuleNotFoundError:
    moduleavailable[2] = 0

try:
    import MBEdatabase_class_v3
    from MBEdatabase_class_v3 import *

    thisversion += float(MBEdatabase_class_v3.__version__)
except ModuleNotFoundError:
    moduleavailable[3] = 0
try:
    import File_backup
    from File_backup import *

    thisversion += float(File_backup.__version__)
except ModuleNotFoundError:
    moduleavailable[4] = 0
try:
    import XRD_analyzer_class_v3
    from XRD_analyzer_class_v3 import *

    thisversion += float(XRD_analyzer_class_v3.__version__)
except ModuleNotFoundError:
    moduleavailable[5] = 0
try:
    import FTIR_fittingtool_v3
    from FTIR_fittingtool_v3 import *

    thisversion += float(FTIR_fittingtool_v3.__version__)
except ModuleNotFoundError:
    moduleavailable[6] = 0
try:
    import Kp_method_v3
    from Kp_method_v3 import *

    thisversion += float(Kp_method_v3.__version__)
except ModuleNotFoundError:
    moduleavailable[7] = 0
try:
    import Grade_Analyzer_GUI_v3
    from Grade_Analyzer_GUI_v3 import *

    thisversion += float(Grade_Analyzer_GUI_v3.__version__)
except ModuleNotFoundError:
    moduleavailable[8] = 0

try:
    import IV_controller
    from IV_controller import *

    thisversion += float(IV_controller.__version__)
except ModuleNotFoundError:
    moduleavailable[9] = 0

try:
    import qdarkstyle
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    darkthemeavailable = 0

__version__ = "3.04" + "/" + "{}".format(thisversion)
__emailaddress__ = "pman3@uic.edu"

os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))  # Change the working directory to current directory.
qtmainfile = "mainwindow.ui"  # GUI layout file.
Ui_main, QtBaseClass = uic.loadUiType(qtmainfile)
qtwelcomefile = "welcome.ui"
Ui_welcome, QtBaseClass = uic.loadUiType(qtwelcomefile)
qthelpfile = "help.ui"
Ui_help, QtBaseClass = uic.loadUiType(qthelpfile)
qtguessfile = "guessnumbers.ui"
Ui_guess, QtBaseClass = uic.loadUiType(qtguessfile)

os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
config = configparser.ConfigParser()
config.read('configuration.ini')
colortheme = int(config["Settings"]["colortheme"])
fullscreenonstart = int(config["Mainwindow"]["fullscreenonstart"])

if colortheme + darkthemeavailable == 2:
    #plt.style.use('dark_background')
    plt.rcParams.update({
        "lines.color": "white",
        "patch.edgecolor": "white",
        "text.color": "white",
        "axes.facecolor": "#31363b",
        "axes.edgecolor": "lightgray",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "grid.color": "lightgray",
        "figure.facecolor": "#31363b",
        "figure.edgecolor": "#31363b",
        "savefig.facecolor": "#31363b",
        "savefig.edgecolor": "#31363b"})


class welcome_GUI(QWidget, Ui_welcome):

    """Main FTIR fitting tool window."""

    def __init__(self):
        QWidget.__init__(self)
        Ui_welcome.__init__(self)
        self.setupUi(self)


class help_GUI(QWidget, Ui_help):

    """Main FTIR fitting tool window."""

    def __init__(self):
        QWidget.__init__(self)
        Ui_help.__init__(self)
        self.setupUi(self)


class guessnumbers_GUI(QDialog, Ui_guess):
    def __init__(self, root):
        QDialog.__init__(self, root)
        Ui_guess.__init__(self)
        self.setupUi(self)
        self.root = root
        self.listbox = self.root.listbox
        self.addlog = self.root.addlog
        self.digit = 4
        self.numberoftries = 10
        self.numberoftriesleft = self.numberoftries
        self.number = 0
        self.numberstring = ''
        self.myguess = ''
        self.As = 0
        self.Bs = 0
        self.exclude = []
        self.buttonstart.clicked.connect(self.startgame)
        self.buttonenter.clicked.connect(self.enternumber)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self)
        self.shortcut.activated.connect(self.enternumber)

    def startgame(self):
        self.digit = int(self.entry_1.text())
        self.numberoftries = int(self.entry_2.text())
        self.numberoftriesleft = self.numberoftries
        self.randomnumber()
        self.addlog('Game begins!', 'orange')
        self.countdown.display(self.numberoftriesleft)
        self.buttonstart.setText("Restart")

    def enternumber(self):
        self.myguess = str(self.entry_3.text())
        self.As = 0
        self.Bs = 0
        self.exclude = []
        if len(self.numberstring) == 0:
            self.startgame()

        if len(self.myguess) != self.digit:
            self.addlog('Invalid input.')
            return
        for i in range(0, self.digit):
            if self.myguess[i] == self.numberstring[i]:
                self.As += 1
        if self.As == self.digit:
            self.numberoftriesleft -= 1
            self.countdown.display(self.numberoftriesleft)
            self.addlog('Bingo! The number is {}.'.format(self.numberstring), 'red')
            self.buttonstart.setText("Start")
            self.entry_3.setText("")
            self.numberstring = ''
            return
        for i in range(0, self.digit):
            for j in range(0, self.digit):
                if j not in self.exclude:
                    if self.myguess[j] == self.numberstring[i]:
                        self.Bs += 1
                        self.exclude.append(j)
                        break
        self.Bs -= self.As
        self.addlog('{}    {}A{}B'.format(self.myguess, self.As, self.Bs))
        self.numberoftriesleft -= 1
        self.countdown.display(self.numberoftriesleft)
        if self.numberoftriesleft <= 0:
            self.addlog('Game over! The number is {}'.format(self.numberstring), 'orange')
            self.numberstring = ''
            self.buttonstart.setText("Start")
        self.entry_3.setText("")

    def randomnumber(self):
        while True:
            oknumber = 1
            self.number = randint(0, math.pow(10, self.digit)-1)
            self.numberstring = "%0{}d".format(self.digit) % self.number
            for i in range(0, self.digit):
                for j in range(0, self.digit):
                    if j != i:
                        if self.numberstring[j] == self.numberstring[i]:
                            oknumber = 0
            if oknumber == 1:
                break


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)


class mainwindow(QMainWindow, Ui_main):

    """Optinal settings for customized result."""

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_main.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.icns'))
        self.splitter.setSizes([800, 100])
        self.setStatusBar(self.statusbar)
        self.subwindowlist = []
        self.clipboard = QLabel()   #In order to transfer info between subwindows, create a null label as clipboard.
        self.clipboard.setParent(self)
        self.clipboard.hide()

        for i in range(0, 30):      # Set 30 subwindows max.
            sub = QMdiSubWindow()
            sub.setAttribute(Qt.WA_DeleteOnClose)       # Important for closing tabs properly.
            sub.setWindowIcon(QIcon())      # Remove the icon for each sub window.
            self.subwindowlist.append(sub)

        self.gui0 = welcome_GUI()
        self.subwindowlist[0].setWidget(self.gui0)
        self.subwindowlist[0].setWindowTitle("Welcome.")
        self.subwindowlist[0].aboutToActivate.connect(self.Normalstatus)
        self.mdi.addSubWindow(self.subwindowlist[0])
        self.subwindowlist[0].showMaximized()
        self.subwindowlist[0].show()

        self.numberofgui = 0

        self.initialmenuitems("help", 1)
        for i in range(1, len(modulelist)):
            self.initialmenuitems(modulelist[i], moduleavailable[i])

        if _platform == "darwin":
            self.status1.setText("﻿Welcome to the Toolbox. Press ⌘+M to see document/help.")
        self.status2.setText('v{}'.format(__version__))
        self.statusbar.addWidget(self.authorLabel)

        self.statusbar.addWidget(self.progressbar)
        self.progressbar.hide()
        self.statusbar.addWidget(self.status1)
        self.statusbar.addPermanentWidget(self.status2)

        self.authorLabel.mousePressEvent = self.addguess

        # System Tray
        self.trayIcon = QSystemTrayIcon(QIcon('icon.icns'), self)
        self.menu = QMenu()
        self.exitAction = self.menu.addAction("Exit")

        def quitmainwindow():
            self.close()

        self.exitAction.triggered.connect(quitmainwindow)
        self.trayIcon.setContextMenu(self.menu)

        if _platform != "darwin":
            def __icon_activated(reason):
                if reason == QSystemTrayIcon.DoubleClick:
                    self.showFullScreen()   # Currently not working.
                    self.show()
            self.trayIcon.activated.connect(__icon_activated)

        self.trayIcon.show()

    def initialmenuitems(self, item, available):
        if available == 1:
            try:
                getattr(self, "open{}".format(item)).triggered.connect(getattr(self, "add{}".format(item)))
            except AttributeError:
                getattr(self, "open{}".format(item)).setDisabled(True)
        else:
            getattr(self, "open{}".format(item)).setDisabled(True)

    def addhelp(self):
        self.numberofgui += 1
        gui = help_GUI()
        self.subwindowlist[self.numberofgui].setWidget(gui)
        self.subwindowlist[self.numberofgui].setWindowTitle("Document")
        self.subwindowlist[self.numberofgui].aboutToActivate.connect(self.Normalstatus)
        self.mdi.addSubWindow(self.subwindowlist[self.numberofgui])
        self.subwindowlist[self.numberofgui].showMaximized()
        self.subwindowlist[self.numberofgui].show()

    def addguess(self, event):
        window = guessnumbers_GUI(self)
        window.show()
        window.exec_()

    def addMCT(self):
        self.numberofgui += 1
        gui = MCT_calculator_GUI(self.subwindowlist[self.numberofgui], self)
        self.setupsubwindow(gui, "MCT Calculator", MCT_calculator_class_v3.__version__)

    def addrecipe(self):
        self.numberofgui += 1
        gui = Recipe_designer_GUI(self.subwindowlist[self.numberofgui], self)
        self.setupsubwindow(gui, "Recipe Designer", Recipe_designer.__version__)

    def adddatabase(self):
        self.numberofgui += 1
        gui = MBEdatabase_GUI(self.subwindowlist[self.numberofgui], self)
        self.setupsubwindow(gui, "MBE database updater", MBEdatabase_class_v3.__version__)

    def addbackup(self):
        self.numberofgui += 1
        gui = File_backup_GUI(self.subwindowlist[self.numberofgui], self)
        self.setupsubwindow(gui, "File backup / LN2 order generator", File_backup.__version__)

    def addXRD(self):
        self.numberofgui += 1
        gui = XRD_analyzer_GUI(self.subwindowlist[self.numberofgui], self)
        self.setupsubwindow(gui, "XRD data analyzer", XRD_analyzer_class_v3.__version__)

    def addftir(self):
        self.numberofgui += 1
        gui = FTIR_fittingtool_GUI_v3(self.subwindowlist[self.numberofgui], self)
        self.setupsubwindow(gui, "FTIR Fitting Tool", FTIR_fittingtool_v3.__version__)

    def addkp(self):
        self.numberofgui += 1
        gui = Kp_method_GUI_v3(self.subwindowlist[self.numberofgui], self)
        self.setupsubwindow(gui, "Kp method", Kp_method_v3.__version__)

    def addgrade(self):
        self.numberofgui += 1
        gui = GradeAnalyer(self.subwindowlist[self.numberofgui], self)
        self.setupsubwindow(gui, "Grade Analyzer", Grade_Analyzer_GUI_v3.__version__)

    def addiv(self):
        self.numberofgui += 1
        gui = IV_controller_GUI(self.subwindowlist[self.numberofgui], self)
        self.setupsubwindow(gui, "IV controller", IV_controller.__version__)

    def setupsubwindow(self, gui, name, version):
        self.subwindowlist[self.numberofgui].setWidget(gui)
        self.subwindowlist[self.numberofgui].setWindowTitle("{} v{}".format(name, version))

        if name == "FTIR Fitting Tool":
            self.subwindowlist[self.numberofgui].aboutToActivate.connect(self.FTIRstatus)
        else:
            self.subwindowlist[self.numberofgui].aboutToActivate.connect(self.Normalstatus)

        self.mdi.addSubWindow(self.subwindowlist[self.numberofgui])
        self.subwindowlist[self.numberofgui].showMaximized()
        self.subwindowlist[self.numberofgui].show()

        self.addinitiallog(name)

    def Normalstatus(self):
        if _platform == "darwin":
            self.status1.setText("﻿Welcome to the Toolbox. Press ⌘+M to see document/help.")
        else:
            self.status1.setText("﻿Welcome to the Toolbox. Press Ctrl+M to see document/help.")

    def FTIRstatus(self):
        if _platform == "darwin":
            self.status1.setText("Welcome to FTIR Fitting Tool. Press ⌘+P for help.")
        else:
            self.status1.setText("Welcome to FTIR Fitting Tool. Press Ctrl+P for help.")

    def addinitiallog(self, name):
        self.addlog('-' * 160, "blue")
        self.addlog('Welcome to {}.'.format(name), "blue")
        self.addlog("This is the log file.", "blue")
        self.addlog('-' * 160, "blue")

    def addlog(self, string, fg="default", bg="default"):
            item = QListWidgetItem(string)
            if fg is not "default":
                item.setForeground(QColor(fg))
            if bg is not "default":
                item.setBackground(QColor(bg))
            self.listbox.addItem(item)
            self.listbox.scrollToItem(item)
            self.listbox.show()


def main():
    app = QApplication(sys.argv)
    splash_pix = QPixmap('bg.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Simulate something that takes time
    time.sleep(2)

    window = mainwindow()
    window.setWindowTitle("Toolbox v{}".format(__version__))
    if fullscreenonstart == 1:
        window.showFullScreen()
    if colortheme + darkthemeavailable == 2:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window.show()
    splash.finish(window)

    # Override excepthook to prevent program crashing and create feekback log.

    def excepthook(excType, excValue, tracebackobj):
        """
        Global function to catch unhandled exceptions in mainthread ONLY.

        @param excType exception type
        @param excValue exception value
        @param tracebackobj traceback object
        """
        separator = '-' * 80
        logFile = time.strftime("%m_%d_%Y_%H_%M_%S") + ".log"
        notice = \
            """An unhandled exception occurred. \n""" \
            """Please report the problem via email to <%s>.\n""" \
            """A log has been written to "%s".\n\nError information:\n""" % \
            (__emailaddress__, logFile)
        timeString = time.strftime("%m/%d/%Y, %H:%M:%S")

        tbinfofile = io.StringIO()
        traceback.print_tb(tracebackobj, None, tbinfofile)
        tbinfofile.seek(0)
        tbinfo = tbinfofile.read()
        errmsg = '%s: \n%s' % (str(excType), str(excValue))
        sections = [separator, timeString, separator, errmsg, separator, tbinfo]
        msg = '\n'.join(sections)
        try:
            f = open(logFile, "w")
            f.write(msg)
            f.write("Version: {}".format(__version__))
            f.close()
        except IOError:
            pass
        errorbox = QMessageBox()
        errorbox.setText(str(notice) + str(msg) + "Version: " + __version__)
        errorbox.exec_()

    sys.excepthook = excepthook

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()