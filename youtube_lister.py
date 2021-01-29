#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from datetime import datetime

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QStandardItem


class YouTubeLister(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        # Add a temporary list of items to display in the table
        self.datastore = [{"id": QStandardItem("1"), "title": QStandardItem("one"), "link": QStandardItem("one"), 
                                                    "source": QStandardItem("unknown"), "date": QStandardItem("20201006")},
                          {"id": QStandardItem("2"), "title": QStandardItem("two"), "link": QStandardItem("two"), 
                                                    "source": QStandardItem("unknown"), "date": QStandardItem("20201006")},
                          {"id": QStandardItem("3"), "title": QStandardItem("three"), "link": QStandardItem("three"), "source": QStandardItem("unknown"), "date": QStandardItem("20201006")}]
        super().__init__(parent=parent)
        self.initUI()

    def initUI(self):

        vbox_main_panel = QtWidgets.QVBoxLayout()
        widget = QtWidgets.QWidget()

        self.tableView = QtWidgets.QTableView()
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        hbox_top_panel = QtWidgets.QHBoxLayout()
        hbox_middle_panel = QtWidgets.QHBoxLayout()
        # hbox_lower_panel = QtWidgets.QHBoxLayout()

        # fboxFilters = QtWidgets.QFormLayout()
        fboxDetails = QtWidgets.QFormLayout()
        
        # CENTRE
        # set up the main details form
        self.titleDetail = QtWidgets.QLineEdit()
        self.linkDetail = QtWidgets.QLineEdit()
        self.sourceDetail = QtWidgets.QLineEdit()
        self.dateDetail = QtWidgets.QLineEdit()
        self.ratingDetail = QtWidgets.QLineEdit()
        
        # Build the form (CENTRE)
        fboxDetails.addRow("Title:", self.titleDetail)
        fboxDetails.addRow("Link:", self.linkDetail)
        fboxDetails.addRow("Source:", self.sourceDetail)
        fboxDetails.addRow("Date:", self.dateDetail)
        fboxDetails.addRow("Rating:", self.ratingDetail)

        # Add the form to the layout (CENTRE)
        hbox_top_panel.addLayout(fboxDetails)

        vbox_main_panel.addLayout(hbox_top_panel)
        vbox_main_panel.addLayout(hbox_middle_panel)
        # vbox_main_panel.addLayout(hbox_lower_panel)
        
        self.linkModel = QtGui.QStandardItemModel()
        self.linkModel.setHorizontalHeaderLabels(("ID", "Title", "Link", "Source", "Date"))
        for row in self.datastore:
            self.linkModel.appendRow(row.values())
        self.tableView.setModel(self.linkModel)
        # self.tableView.resizeColumnsToContents()

        vbox_main_panel.addWidget(self.tableView)
        vbox_main_panel.setStretchFactor(self.tableView, 1)
        
        widget.setLayout(vbox_main_panel)
        self.setCentralWidget(widget)
        self.setWindowTitle('YouTube Listings')
        self.setGeometry(160, 160, 900, 600)


def main():
    app = QtWidgets.QApplication([])

    win = YouTubeLister()
    win.show()
    win.raise_()
    app.exec_()


if __name__ == "__main__":
    main()
