import signal
import sys
import json
import feedparser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QSplitter,
    QTreeView, QTableView, QTextEdit, QProgressBar, QStatusBar, QTextBrowser, 
    QVBoxLayout, QWidget, QMenu, QInputDialog, QLineEdit, QMessageBox, QHeaderView
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QDesktopServices
from PyQt5.QtCore import Qt, QPoint, QUrl, pyqtSignal, QModelIndex

import feedparser

from modules.feed  import parse_url
from modules.dates import normalizar_data
from modules.files import detect_formats

TREE_FILE = "tree_data.json"
LIST_DATA = []

class MyTableView(QTableView):
    doubleLeftClicked = pyqtSignal(QModelIndex)
    doubleRightClicked = pyqtSignal(QModelIndex)

    def mouseDoubleClickEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            if event.button() == Qt.LeftButton:
                self.doubleLeftClicked.emit(index)
            elif event.button() == Qt.RightButton:
                self.doubleRightClicked.emit(index)
        super().mouseDoubleClickEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Exemplo com Qt5")

        self._create_toolbar()
        self._create_central_widget()
        self._create_statusbar()

        self.load_tree_structure()

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
        self.tree_view.doubleClicked.connect(self.handle_tree_double_click)
        
        main_splitter.addWidget(self.tree_view)

        # Right splitter (TableView + TextEdit)
        right_splitter = QSplitter(Qt.Vertical)
        
        self.table_model = QStandardItemModel()
        self.table_model.setHorizontalHeaderLabels(["ID","Title", "Data", "Author"])
        self.table_view = MyTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.setSortingEnabled(True)
        self.table_view.setColumnHidden(0, True)
        self.table_view.doubleLeftClicked.connect(self.on_table_left_double_click)
        self.table_view.doubleRightClicked.connect(self.on_table_right_double_click)
        self.table_view.clicked.connect(self.on_table_click)
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        #header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.resizeSection(1, 500)
        header.resizeSection(2, 200)
        header.resizeSection(3, 200)
        
        self.markdown_widget = QTextBrowser()
        self.markdown_widget.setMarkdown("")
        self.markdown_widget.setMinimumHeight(50)
        fonte = QFont("Courier New")  # Ou "Monospace", "Courier", etc.
        fonte.setStyleHint(QFont.Monospace)
        self.markdown_widget.setFont(fonte)

        right_splitter.addWidget(self.table_view)
        right_splitter.addWidget(self.markdown_widget)
        right_splitter.setStretchFactor(0, 1)
 
        main_splitter.addWidget(right_splitter)
        main_splitter.setStretchFactor(1, 1)
        

        layout = QVBoxLayout()
        layout.addWidget(main_splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        


    def on_table_right_double_click(self, index):
        pass

    def on_table_left_double_click(self, index):
        row = index.row()
        model = self.table_view.model()

        data_row = []
        for col in range(model.columnCount()):
            index_item = model.index(row, col)
            data_row.append(model.data(index_item))
        
        mydat = LIST_DATA[int(data_row[0])]
        QDesktopServices.openUrl(QUrl(mydat["link"]))
    
    def on_table_click(self, index):
        row = index.row()
        model = self.table_view.model()

        data_row = []
        for col in range(model.columnCount()):
            index_item = model.index(row, col)
            data_row.append(model.data(index_item))

        #print(f"Linha clicada: {row}")
        #print(f"Dados da linha: {data_row}")
        mydat = LIST_DATA[int(data_row[0])]
        
        D = detect_formats(mydat['summary'])
        
        maior_chave = max(D, key=D.get)
        
        if 'HTML'==maior_chave:
            description =   "<h1>"+ \
                            mydat['title']+ \
                            "</h1>\n"+ \
                            mydat['summary']
            self.markdown_widget.setHtml(description)
            
        elif 'Markdown'==maior_chave:
            description =   "# "+ \
                            mydat['title']+ \
                            "\n"+ \
                            mydat['summary']
            self.markdown_widget.setMarkdown(description)
            
        else:
            description =   mydat['title']+ \
                            "\n"+ \
                            "="*len(mydat['title'])+ \
                            "\n\n"+ \
                            mydat['summary']
            self.markdown_widget.setPlainText(description)
        

    def update_table_with_leaf_data(self, list_data):
        # 1. Limpar
        self.table_model.removeRows(0, self.table_model.rowCount())

        # Se o modelo ainda não foi definido, cria e aplica uma vez
        if not hasattr(self, 'table_model') or self.table_view.model() is None:
            self.table_model = QStandardItemModel()
            self.table_model.setHorizontalHeaderLabels(["ID","Title", "Data", "Author"])
            self.table_view.setModel(self.table_model)
            self.table_view.setSortingEnabled(True)
            self.table_view.setColumnHidden(0, True)
            self.table_view.doubleLeftClicked.connect(self.on_table_left_double_click)
            self.table_view.doubleRightClicked.connect(self.on_table_right_double_click)
            self.table_view.clicked.connect(self.on_table_click)
            self.table_view.setEditTriggers(QTableView.NoEditTriggers)
            header = self.table_view.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Interactive)
            #header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.resizeSection(1, 500)
            header.resizeSection(2, 200)
            header.resizeSection(3, 200)

        # Adicionar os dados (esperando lista de dicionários com "title" e "url")
        L = len(list_data)
        self.progress.setRange(0,L)
        for i, data in enumerate(list_data):
            id_item = QStandardItem(str(i))
            title_item = QStandardItem(data.title)
            data_item = QStandardItem(normalizar_data(data.published)) 
            author_item = QStandardItem(data.author)
            self.table_model.appendRow([id_item, title_item, data_item, author_item])
            self.progress.setValue(i+1)
        self.progress.setValue(0)

    def set_list_leaf_data_in_table_view(self,leaf_data_list):
        global LIST_DATA
        LIST_DATA=[]
        
        for item in leaf_data_list:
            feed = feedparser.parse(item['url'])
            
            L = len(feed.entries)
            self.progress.setRange(0,L)
            for j, entry in enumerate(feed.entries):
                LIST_DATA.append(entry)
                self.progress.setValue(j+1)
            self.progress.setValue(0)
            
        self.update_table_with_leaf_data(LIST_DATA)

    def handle_tree_double_click(self, index):
        item = self.tree_model.itemFromIndex(index)
        leaf_data_list = []

        def collect_leaf_data(node):
            if isinstance(node.data(), dict):
                leaf_data_list.append(node.data())
            for i in range(node.rowCount()):
                collect_leaf_data(node.child(i))

        collect_leaf_data(item)
        
        self.set_list_leaf_data_in_table_view(leaf_data_list)


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
                self.save_tree_structure()

        elif action == add_leaf_action:
            url, ok2 = QInputDialog.getText(self, "URL", "Digite a URL:")
            url = parse_url(url)
       
            if ok2 and url is not None:
                feed = feedparser.parse(url)
                
                leaf_data = {
                    "title": feed.feed.get("title", "Title"),
                    "url": url,
                    "description": feed.feed.get("subtitle", "Description")
                }
                leaf_text = f"{leaf_data['title']} ({leaf_data['url']})"
                new_leaf = QStandardItem(leaf_text)
                new_leaf.setData(leaf_data)

                if selected_item:
                    selected_item.appendRow(new_leaf)
                else:
                    self.tree_model.appendRow(new_leaf)
                self.save_tree_structure()

        elif action == remove_node_action or action == remove_leaf_action:
            if selected_item:
                parent = selected_item.parent()
                if parent:
                    parent.removeRow(selected_item.row())
                else:
                    self.tree_model.removeRow(selected_item.row())
                self.save_tree_structure()

    def show_about(self):
        QMessageBox.information(self, "Sobre", "Exemplo criado com PyQt5.\n(c) Fernando")

    # SERIALIZAÇÃO DO TREEVIEW
    def save_tree_structure(self):
        def serialize_item(item):
            data = {
                'text': item.text(),
                'user_data': item.data(),
                'children': [serialize_item(item.child(i)) for i in range(item.rowCount())]
            }
            return data

        root_items = [self.tree_model.item(i) for i in range(self.tree_model.rowCount())]
        data = [serialize_item(item) for item in root_items]

        with open(TREE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_tree_structure(self):
        import os
        if not os.path.exists(TREE_FILE):
            root_item = QStandardItem("Root")
            self.tree_model.appendRow(root_item)
            return

        def deserialize_item(data):
            item = QStandardItem(data['text'])
            item.setData(data.get('user_data'))
            for child_data in data['children']:
                item.appendRow(deserialize_item(child_data))
            return item

        with open(TREE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item_data in data:
            self.tree_model.appendRow(deserialize_item(item_data))

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()

