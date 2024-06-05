import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu,
                               QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QTableWidget,
                               QTableWidgetItem, QLabel, QPushButton, QWidget, QHeaderView,
                               QDialog, QDialogButtonBox)
from PySide6.QtGui import QPixmap, QCursor, QAction
from PySide6.QtCore import Qt, QSize


class ImageDetailDialog(QDialog):
    def __init__(self, image_path, actors, parent=None):
        super().__init__(parent)
        self.setWindowTitle("图片详情")
        layout = QVBoxLayout()

        self.image_label = QLabel()
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        layout.addWidget(self.image_label)

        self.actors_list = QComboBox()
        self.actors_list.addItems(actors)
        layout.addWidget(self.actors_list)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)


class ImageAnnotationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图片标注界面")
        self.setGeometry(100, 100, 1200, 800)

        self.current_page = 1
        self.records_per_page = 10

        main_layout = QVBoxLayout()

        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        menu = QMenu("选择", self)
        menu_bar.addMenu(menu)
        annotate_action = QAction("图片标注", self)
        task_action = QAction("任务分配", self)
        menu.addAction(annotate_action)
        menu.addAction(task_action)

        search_layout = QHBoxLayout()
        self.image_name_search = QLineEdit()
        self.image_name_search.setPlaceholderText("根据图片名称搜索")
        self.movie_name_search = QLineEdit()
        self.movie_name_search.setPlaceholderText("根据影视名称搜索")
        self.image_type_search = QComboBox()
        self.image_type_search.addItems(["图片类型", "海报", "新闻图片", "截图", "粉丝图片"])
        search_layout.addWidget(self.image_name_search)
        search_layout.addWidget(self.movie_name_search)
        search_layout.addWidget(self.image_type_search)

        # button_layout = QHBoxLayout()
        self.search_button = QPushButton("搜索")
        self.clear_search_button = QPushButton("清空搜索")
        # button_layout.addWidget(self.search_button)
        # button_layout.addWidget(self.clear_search_button)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.clear_search_button)

        self.search_button.clicked.connect(self.perform_search)
        self.clear_search_button.clicked.connect(self.clear_search)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["影视名称", "豆瓣ID", "图片", "演员名称", "详情"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        pagination_layout = QHBoxLayout()
        self.total_label = QLabel("总数量: 100")
        self.current_page_label = QLabel("当前页: 1")
        self.first_page_button = QPushButton("第一页")
        self.previous_page_button = QPushButton("前一页")
        self.next_page_button = QPushButton("后一页")
        self.last_page_button = QPushButton("最后一页")
        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("页码")
        self.page_input.setFixedWidth(50)
        self.page_input.returnPressed.connect(self.goto_page)

        self.records_per_page_select = QComboBox()
        self.records_per_page_select.addItems(["10", "20", "50", "100"])
        self.records_per_page_select.setCurrentText("10")
        self.records_per_page_select.currentTextChanged.connect(self.update_records_per_page)

        pagination_layout.addWidget(self.total_label)
        pagination_layout.addWidget(self.current_page_label)
        pagination_layout.addWidget(self.first_page_button)
        pagination_layout.addWidget(self.previous_page_button)
        pagination_layout.addWidget(self.next_page_button)
        pagination_layout.addWidget(self.last_page_button)
        pagination_layout.addWidget(self.page_input)
        pagination_layout.addWidget(QLabel("每页显示条数:"))
        pagination_layout.addWidget(self.records_per_page_select)

        self.first_page_button.clicked.connect(lambda: self.change_page(1))
        self.previous_page_button.clicked.connect(lambda: self.change_page(self.current_page - 1))
        self.next_page_button.clicked.connect(lambda: self.change_page(self.current_page + 1))
        self.last_page_button.clicked.connect(lambda: self.change_page(self.total_pages()))

        main_layout.addLayout(search_layout)
        # main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(pagination_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.load_data()
        self.display_page(self.current_page)
        self.set_styles()

    def set_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QMenuBar {
                background-color: #f2f2f2;
                color: #333333;
            }
            QMenuBar::item {
                background-color: #f2f2f2;
                color: #333333;
            }
            QMenuBar::item:selected {
                background-color: #dcdcdc;
            }
            QMenu {
                background-color: #ffffff;
                color: #333333;
            }
            QMenu::item:selected {
                background-color: #dcdcdc;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px;
                min-width: 100px;  /* 添加最小宽度 */
            }
            QPushButton:hover {
                background-color: #45a049;
                 min-width: 100px;  /* 添加最小宽度 */
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: none;
            }
        """)

    def load_data(self):
        with open('fake_data.json', 'r') as f:
            self.data = json.load(f)
        self.total_records = len(self.data)

    def display_page(self, page_number):
        self.table.setRowCount(0)
        start_index = (page_number - 1) * self.records_per_page
        end_index = start_index + self.records_per_page
        end_index = min(end_index, self.total_records)

        for record in self.data[start_index:end_index]:
            self.add_table_row(record["movie_name"], record["douban_id"], record["image_path"], record["actors"])

        self.current_page_label.setText(f"当前页: {page_number}")

    def add_table_row(self, movie_name, douban_id, image_path, actors):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(movie_name))
        self.table.setItem(row_position, 1, QTableWidgetItem(douban_id))

        image_label = QLabel()
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        image_label.setFixedSize(QSize(100, 100))
        image_label.setCursor(QCursor(Qt.PointingHandCursor))
        image_label.mousePressEvent = lambda event, img=image_path: self.show_image_detail(img, actors)
        self.table.setCellWidget(row_position, 2, image_label)

        actor_combo = QComboBox()
        actor_combo.addItems(actors)
        self.table.setCellWidget(row_position, 3, actor_combo)

        detail_button = QPushButton("详情")
        detail_button.clicked.connect(lambda: self.show_image_detail(image_path, actors))
        self.table.setCellWidget(row_position, 4, detail_button)

    def show_image_detail(self, image_path, actors):
        dialog = ImageDetailDialog(image_path, actors, self)
        dialog.exec()

    def change_page(self, page_number):
        if page_number < 1:
            page_number = 1
        elif page_number > self.total_pages():
            page_number = self.total_pages()

        self.current_page = page_number
        self.display_page(page_number)

    def goto_page(self):
        page_number = int(self.page_input.text())
        self.change_page(page_number)

    def update_records_per_page(self):
        self.records_per_page = int(self.records_per_page_select.currentText())
        self.change_page(1)

    def total_pages(self):
        return (self.total_records + self.records_per_page - 1) // self.records_per_page

    def perform_search(self):
        print("搜索功能暂未实现")

    def clear_search(self):
        self.image_name_search.clear()
        self.movie_name_search.clear()
        self.image_type_search.setCurrentIndex(0)
        self.load_data()
        self.change_page(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageAnnotationApp()
    window.show()
    sys.exit(app.exec())
