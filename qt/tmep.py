import sys
import os
import pandas as pd
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QLineEdit, QFileDialog, QWidget, QMessageBox, QComboBox)
from PySide6.QtGui import QDoubleValidator, QIntValidator, QFont
from PySide6.QtCore import Qt


class ExcelExtractor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel 分层抽取")
        self.setGeometry(100, 100, 500, 350)

        self.excel_file_path = ""

        main_layout = QVBoxLayout()

        # 选择Excel文件
        file_layout = QHBoxLayout()
        self.file_label = QLabel("选择Excel文件:")
        self.file_label.setFont(QFont("Arial", 12))
        self.file_path_input = QLineEdit()
        self.file_path_input.setReadOnly(True)
        self.file_button = QPushButton("浏览")
        self.file_button.clicked.connect(self.select_excel_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(self.file_button)

        # 输入列名称
        column_layout = QHBoxLayout()
        self.column_label = QLabel("输入列名称:")
        self.column_label.setFont(QFont("Arial", 12))
        self.column_input = QLineEdit()
        column_layout.addWidget(self.column_label)
        column_layout.addWidget(self.column_input)

        # 输入Sheet索引
        sheet_layout = QHBoxLayout()
        self.sheet_label = QLabel("输入Sheet索引 (默认0):")
        self.sheet_label.setFont(QFont("Arial", 12))
        self.sheet_input = QLineEdit()
        self.sheet_input.setValidator(QIntValidator())
        self.sheet_input.setText("0")
        sheet_layout.addWidget(self.sheet_label)
        sheet_layout.addWidget(self.sheet_input)

        # 选择抽取方法
        method_layout = QHBoxLayout()
        self.method_label = QLabel("选择抽取方法:")
        self.method_label.setFont(QFont("Arial", 12))
        self.method_combobox = QComboBox()
        self.method_combobox.addItems(["按百分比抽取", "按数量抽取"])
        self.method_combobox.currentTextChanged.connect(self.update_input_fields)
        method_layout.addWidget(self.method_label)
        method_layout.addWidget(self.method_combobox)

        # 动态显示输入框的布局
        self.dynamic_layout = QVBoxLayout()

        # 输入百分比
        self.percentage_layout = QHBoxLayout()
        self.percentage_label = QLabel("输入百分比 (0-1):")
        self.percentage_label.setFont(QFont("Arial", 12))
        self.percentage_input = QLineEdit()
        self.percentage_input.setValidator(QDoubleValidator(0.0, 1.0, 2))
        self.percentage_layout.addWidget(self.percentage_label)
        self.percentage_layout.addWidget(self.percentage_input)

        # 输入最小抽取数量
        self.min_count_layout = QHBoxLayout()
        self.min_count_label = QLabel("最小抽取数量:")
        self.min_count_label.setFont(QFont("Arial", 12))
        self.min_count_input = QLineEdit()
        self.min_count_input.setValidator(QIntValidator())
        self.min_count_layout.addWidget(self.min_count_label)
        self.min_count_layout.addWidget(self.min_count_input)

        # 输入抽取数量
        self.count_layout = QHBoxLayout()
        self.count_label = QLabel("输入抽取数量:")
        self.count_label.setFont(QFont("Arial", 12))
        self.count_input = QLineEdit()
        self.count_input.setValidator(QIntValidator())
        self.count_layout.addWidget(self.count_label)
        self.count_layout.addWidget(self.count_input)

        # 把输入百分比和输入数量布局加入
        self.dynamic_layout.addLayout(self.percentage_layout)
        self.dynamic_layout.addLayout(self.min_count_layout)
        self.dynamic_layout.addLayout(self.count_layout)

        # 执行和下载按钮
        button_layout = QHBoxLayout()
        self.execute_button = QPushButton("执行")
        self.execute_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px;")
        self.execute_button.clicked.connect(self.execute_extraction)
        self.download_button = QPushButton("下载")
        self.download_button.setStyleSheet("background-color: #008CBA; color: white; font-size: 14px;")
        self.download_button.clicked.connect(self.download_file)
        button_layout.addWidget(self.execute_button)
        button_layout.addWidget(self.download_button)

        main_layout.addLayout(file_layout)
        main_layout.addLayout(column_layout)
        main_layout.addLayout(sheet_layout)
        main_layout.addLayout(method_layout)
        main_layout.addLayout(self.dynamic_layout)
        main_layout.addLayout(button_layout)

        self.update_input_fields(self.method_combobox.currentText())

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def update_input_fields(self, method):
        # 清空动态布局中的所有组件
        # for i in reversed(range(self.dynamic_layout.count())):
        #     widget = self.dynamic_layout.itemAt(i).widget()
        #     if widget is not None:
        #         widget.deleteLater()

        # 根据选择的抽取方法动态添加输入框
        if method == "按百分比抽取":
            # self.dynamic_layout.addLayout(self.percentage_layout)
            # self.dynamic_layout.addLayout(self.min_count_layout)
            for i in reversed(range(self.dynamic_layout.itemAt(2).layout().count())):
                self.dynamic_layout.itemAt(2).layout().itemAt(i).widget().hide()
            for i in reversed(range(self.dynamic_layout.itemAt(0).layout().count())):
                self.dynamic_layout.itemAt(0).layout().itemAt(i).widget().show()
            for i in reversed(range(self.dynamic_layout.itemAt(1).layout().count())):
                self.dynamic_layout.itemAt(1).layout().itemAt(i).widget().show()

        elif method == "按数量抽取":
            for i in reversed(range(self.dynamic_layout.itemAt(0).layout().count())):
                self.dynamic_layout.itemAt(0).layout().itemAt(i).widget().hide()
            for i in reversed(range(self.dynamic_layout.itemAt(1).layout().count())):
                self.dynamic_layout.itemAt(1).layout().itemAt(i).widget().hide()
            for i in reversed(range(self.dynamic_layout.itemAt(2).layout().count())):
                self.dynamic_layout.itemAt(2).layout().itemAt(i).widget().show()
            # self.dynamic_layout.addLayout(self.count_layout)

    def select_excel_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.excel_file_path = file_path
            self.file_path_input.setText(file_path)

    def execute_extraction(self):
        try:
            method = self.method_combobox.currentText()
            column_name = self.column_input.text()
            sheet_index = int(self.sheet_input.text())

            if not self.excel_file_path:
                QMessageBox.warning(self, "警告", "请先选择Excel文件")
                return

            if not column_name:
                QMessageBox.warning(self, "警告", "请输入列名称")
                return

            # 生成输出文件名
            base_name = os.path.basename(self.excel_file_path)
            name, ext = os.path.splitext(base_name)
            date_str = datetime.now().strftime("%Y-%m-%d")
            self.output_file_path = f"{name}_{date_str}{ext}"

            # 读取Excel文件
            df = pd.read_excel(self.excel_file_path, sheet_name=sheet_index)

            if method == "按百分比抽取":
                percentage = float(self.percentage_input.text())
                min_count = int(self.min_count_input.text())
                # 分层抽取按百分比和最小抽取数量
                sampled_df = df.groupby(column_name, group_keys=False).apply(
                    lambda x: x.sample(n=min(len(x), max(int(len(x) * percentage), min_count))))
            elif method == "按数量抽取":
                count = int(self.count_input.text())
                # 分层抽取按数量
                sampled_df = df.groupby(column_name, group_keys=False).apply(lambda x: x.sample(n=min(len(x), count)))

            # 保存到新的Excel文件
            sampled_df.to_excel(self.output_file_path, index=False)
            QMessageBox.information(self, "成功", "抽取完成并保存到指定位置")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"执行时发生错误: {str(e)}")

    def download_file(self):
        if self.output_file_path:
            try:
                QMessageBox.information(self, "下载", f"文件已保存到: {self.output_file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"下载时发生错误: {str(e)}")
        else:
            QMessageBox.warning(self, "警告", "请先执行抽取操作")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelExtractor()
    window.show()
    sys.exit(app.exec())
