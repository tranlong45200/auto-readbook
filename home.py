import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton

from main import swipe_read_until_100


class MyApplication(QWidget):
    def __init__(self):
        super().__init__()

        # Tạo widget và layout
        self.init_ui()

    def init_ui(self):
        # Tạo các thành phần giao diện
        self.edit_text = QLineEdit(self)
        self.button = QPushButton('Click me', self)

        # Tạo layout và thêm các thành phần vào layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.edit_text)
        layout.addWidget(self.button)

        # Đặt layout cho widget chính
        self.setLayout(layout)

        # Kết nối sự kiện nhấn nút với hàm xử lý
        self.button.clicked.connect(self.on_button_click)

        # Cài đặt kích thước cửa sổ và hiển thị
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('auto read book')
        self.show()

    def on_button_click(self):
        # Xử lý sự kiện khi nút được nhấn
        user_input = self.edit_text.text()
        print(f'User input: {user_input}')
        swipe_read_until_100()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApplication()
    sys.exit(app.exec_())
