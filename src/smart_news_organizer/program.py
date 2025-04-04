import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QSplitter,
    QTreeView, QTableView, QTextEdit, QProgressBar, QStatusBar,
    QVBoxLayout, QWidget, QMenu, QInputDialog, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QPoint


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Exemplo com Qt5")

        self._create_toolbar()
        self._create_central_widget()
        self._create_statusbar()

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        refresh_action = QAction("Refresh", self)
        about_action = QAction("About", self)
        config_action = QAction("Configurate", self)

        refresh_action.triggered.connect(lambda: self.statusBar().showMessage("Refresh pressed"))
        about_action.triggered.connect(self.show_about)
        config_action.triggered.connect(lambda: self.statusBar().showMessage("Open Config"))

        toolbar.addAction(refresh_action)
        toolbar.addAction(about_action)
        toolbar.addAction(config_action)

    def _create_central_widget(self):
        main_splitter = QSplitter(Qt.Horizontal)

        # Tree View (Left)
        self.tree_view = QTreeView()
        self.tree_model = QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["Nodes"])
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.open_tree_context_menu)

        root_item = QStandardItem("Root")
        self.tree_model.appendRow(root_item)

        # Right splitter (TableView + TextEdit)
        right_splitter = QSplitter(Qt.Vertical)
        self.table_view = QTableView()
        self.text_view = QTextEdit()

        right_splitter.addWidget(self.table_view)
        right_splitter.addWidget(self.text_view)
        right_splitter.setStretchFactor(1, 1)

        main_splitter.addWidget(self.tree_view)
        main_splitter.addWidget(right_splitter)
        main_splitter.setStretchFactor(1, 1)

        layout = QVBoxLayout()
        layout.addWidget(main_splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _create_statusbar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.status.addPermanentWidget(self.progress)

    def open_tree_context_menu(self, position: QPoint):
        index = self.tree_view.indexAt(position)
        selected_item = self.tree_model.itemFromIndex(index) if index.isValid() else None

        menu = QMenu()
        add_node_action = menu.addAction("Adicionar novo nodo")
        add_leaf_action = menu.addAction("Adicionar folha final (com URL)")
        menu.addSeparator()
        remove_node_action = menu.addAction("Remover nodo")
        remove_leaf_action = menu.addAction("Remover folha")

        action = menu.exec_(self.tree_view.viewport().mapToGlobal(position))

        if action == add_node_action:
            name, ok = QInputDialog.getText(self, "Nome do novo nodo", "Digite o nome:")
            if ok and name:
                new_item = QStandardItem(name)
                if selected_item:
                    selected_item.appendRow(new_item)
                else:
                    self.tree_model.appendRow(new_item)

        elif action == add_leaf_action:
            label, ok1 = QInputDialog.getText(self, "Nome", "Digite o nome:")
            url, ok2 = QInputDialog.getText(self, "URL", "Digite a URL:")
            desc, ok3 = QInputDialog.getText(self, "Descrição", "Digite a descrição:")

            if ok1 and ok2 and ok3:
                leaf_data = {
                    "label": label,
                    "url": url,
                    "description": desc
                }
                leaf_text = f"{leaf_data['label']} ({leaf_data['url']})"
                new_leaf = QStandardItem(leaf_text)
                new_leaf.setData(leaf_data)

                if selected_item:
                    selected_item.appendRow(new_leaf)
                else:
                    self.tree_model.appendRow(new_leaf)

        elif action == remove_node_action:
            if selected_item:
                parent = selected_item.parent()
                if parent:
                    parent.removeRow(selected_item.row())
                else:
                    self.tree_model.removeRow(selected_item.row())

        elif action == remove_leaf_action:
            if selected_item and selected_item.rowCount() == 0:
                parent = selected_item.parent()
                if parent:
                    parent.removeRow(selected_item.row())
                else:
                    self.tree_model.removeRow(selected_item.row())

    def show_about(self):
        QMessageBox.information(self, "Sobre", "Exemplo criado com PyQt5.\n(c) Fernando")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec_())

