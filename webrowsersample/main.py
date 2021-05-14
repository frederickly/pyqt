import sys
import os
import json

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QTabBar, QTabWidget, QFrame, QStackedLayout)
from PyQt5.QtGui import QIcon, QWindow, QImage
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *  # it has own package PyQtWebEngine now run pip3 install PyQtWebEngine

class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e
                        ):
        self.selectAll()

class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser")

        print("call init")
        self.create_app()
        self.setBaseSize(1366, 768)

    def create_app(self):
        print("create app")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        # Create Tabs
        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.tabbar.tabCloseRequested.connect(self.close_tab)
        self.tabbar.tabBarClicked.connect(self.SwitchTab)

        self.tabbar.setCurrentIndex(0)

        # Keep track of tabs
        self.tabCount = 0
        self.tabs =[]


        # Create AddressBar
        self.Toolbar = QWidget()
        self.ToolbarLayout = QHBoxLayout()
        self.addressbar = AddressBar()
        self.AddTabButton = QPushButton("+")

        self.addressbar.returnPressed.connect(self.BrowseTo)
        self.AddTabButton.clicked.connect(self.AddTab)

        self.Toolbar.setLayout(self.ToolbarLayout)
        self.ToolbarLayout.addWidget(self.addressbar)
        self.ToolbarLayout.addWidget(self.AddTabButton)

        # set main view
        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)


        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.Toolbar)
        self.layout.addWidget(self.container)
        self.setLayout(self.layout)

        print("run show")

        self.AddTab()
        self.show()

    def close_tab(self, i):
        self.tabbar.removeTab(i)


    def AddTab(self):
        i = self.tabCount
        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].setObjectName("tab" + str(i))

        # open webview
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("http://google.com"))

        self.tabs[i].content.titleChanged.connect(lambda: self.SetTabText(i))

        # Add webview to tabs layout
        self.tabs[i].layout.addWidget(self.tabs[i].content)

        # set top level tab from [] to layout
        self.tabs[i].setLayout(self.tabs[i].layout)

        # add tab to the top level stacked widget
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])

        # set the tab at top of screen
        self.tabbar.addTab("New Tab")
        self.tabbar.setTabData(i, {"object": 'tab' + str(i), "initial": i})


        self.tabbar.setCurrentIndex(i)

        self.tabCount += 1

    def SwitchTab(self, i):
        tab_data = self.tabbar.tabData(i)
        print("tab: ", tab_data)
        tab_content = self.findChild(QWidget, tab_data)
        self.container.layout.setCurrentWidget(tab_content)

    def BrowseTo(self):
        text = self.addressbar.text()
        print("text")
        i = self.tabbar.currentIndex()
        tab = self.tabbar.tabData(i)["object"]
        wv = self.findChild(QWidget, tab).content

        if "http" not in text:
            if "." not in text:
                url = "https://www.google.com/search?q=" + text
            else:
                url ="http://" + text
        else:
            url = text
        wv.load(QUrl.fromUserInput(url))

    def SetTabText(self, i):
        '''
            self.tabs[i].objectName = tab1
            self.tabbar.tabData(i)["object"] = tab1
        '''
        tab_name = self.tabs[i].objectName()
        # tab1
        count = 0
        running = True

        while running:
            tab_data_name = self.tabbar.tabData(count)
            if count > 99:
                running = False
            if tab_name == tab_data_name["object"]:
                newTitle = self.findChild(QWidget, tab_name).content.title()
                self.tabbar.setTabText(count, newTitle)
                running = False
            else:
                count +=1

if __name__ == "__main__":
    print("started")
    app = QApplication(sys.argv)

    window = App()

    sys.exit(app.exec_())