import sys
import time
from industries import Industries
from overview import Overview
from reviews import Reviews
from common import Common
from exception import InvalidInputError
from functools import partial
from typing import Any
from typing import Union
from typing import NoReturn
from typing import Sequence
from typing import Callable
from PySide6.QtCore import Qt
from PySide6.QtCore import QDir
from PySide6.QtCore import Slot
from PySide6.QtCore import Signal
from PySide6.QtCore import QRect
from PySide6.QtCore import QTimer
from PySide6.QtCore import QThread
from PySide6.QtCore import QObject
from PySide6.QtCore import QRunnable
from PySide6.QtCore import QThreadPool
from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QRadioButton
from PySide6.QtWidgets import QProgressBar
from PySide6.QtGui import QIcon
from PySide6.QtGui import QIntValidator
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtGui import QDesktopServices

class WorkerSignals(QObject):
    progress = Signal(tuple)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs) -> None:
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs['sgnl'] = self.signals.progress

    @Slot()
    def run(self) -> None:
        self.fn(*self.args, **self.kwargs)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setWindowTitle("Glassdoor Scraper")
        self.setFixedSize(600, 270)
        self.main_settings = QGroupBox(self)
        self.main_settings.setGeometry(10, 10, 580, 240)
        self.threadpool = QThreadPool()

        self.create_label(
            self.main_settings, 
            'Action Type: ',
            True,
            (10, 10))

        self.label_range_id = self.create_label(
            self.main_settings, 
            'Range ID: ',
            False,
            (10, 60),
            'The range of ids of the companies which overviews you want to get')

        self.label_company_id = self.create_label(
            self.main_settings, 
            'Company ID: ',
            False,
            (10, 60),
            'Id of the company which overview you want to get')

        self.label_url = self.create_label(
            self.main_settings, 
            'Url: ',
            False,
            (10, 60),
            'Page url from which you want to scrape reviews')

        self.label_page_number = self.create_label(
            self.main_settings, 
            'Page Number: ',
            False,
            (10, 110),
            'Page number from which you want to scrape reviews')

        self.label_range_separator = self.create_label(
            self.main_settings, 
            ':',
            False,
            (158, 60))

        self.operation_status = self.create_label(
            self.main_settings, 
            "",
            True,
            (150, 200))

        self.line_from = self.create_line_edit(
            self.main_settings,
            False,
            (100, 60, 40, 30),
            "^([1-9][0-9]{0,3}|[1-9])$"
        )

        self.line_to = self.create_line_edit(
            self.main_settings,
            False,
            (180, 60, 40, 30),
            "^([1-9][0-9]{0,3}|[1-9])$"
        )

        self.line_company_id = self.create_line_edit(
            self.main_settings,
            False,
            (100, 60, 120, 30),
            "^([1-9][0-9]{0,6}|[1-9])$"
        )

        self.line_url = self.create_line_edit(
            self.main_settings,
            False,
            (100, 60, 340, 30),
            "^https:\/\/www\.glassdoor\.com\/Reviews\/[A-Za-z-]+-Reviews-E[0-9]+\.htm$"
        )

        self.line_page_number = self.create_line_edit(
            self.main_settings,
            False,
            (100, 110, 40, 30),
            "^([1-9][0-9]{0,2}|[1-9])$"
        )

        self.action_type = self.create_action_type(
            self.main_settings,
            ['Get Industries', 'Get Overview', 'Get Reviews'],
            1,
            (100, 10))
        
        self.save_to_csv = self.create_radio_btn(
            self.main_settings, 
            'Save to CSV',
            False,
            (240, 10))

        self.save_to_json = self.create_radio_btn(
            self.main_settings, 
            'Save to JSON',
            False,
            (340, 10))

        self.get_data_btn = self.create_btn(
            self.main_settings,
            'Get Data',
            (10, 200),
            self.run)

        self.progress_bar = self.create_progress_bar(
            self,
            (10, 255))

    @staticmethod
    def create_label(parent: QWidget, name: str, visible: bool, pos: tuple[int, int], tip: str = None) -> QLabel:
        label = QLabel(parent)
        label.setGeometry(*pos, 340, 30)
        label.setText(f'{name}')
        label.setVisible(visible)
        label.setToolTip(tip)
        return label

    @staticmethod
    def create_radio_btn(parent: QWidget, name: str, visible: bool, pos: tuple[int, int]) -> QRadioButton:
        radio_btn = QRadioButton(parent)
        radio_btn.setGeometry(*pos, 120, 30)
        radio_btn.setText(f'{name}')
        radio_btn.setVisible(visible)
        return radio_btn

    @staticmethod
    def create_btn(parent: QWidget, name: str, pos: tuple[int, int], func: Callable[..., Any]) -> QPushButton:
        button = QPushButton(parent)
        button.setText(f'{name}')
        button.setGeometry(*pos, 120, 30)
        button.clicked.connect(func)
        return button

    @staticmethod
    def create_progress_bar(parent: QWidget, pos: tuple[int, int]) -> QProgressBar:
        progress_bar = QProgressBar(parent)
        progress_bar.setGeometry(*pos, 580, 10)
        progress_bar.setValue(0)
        progress_bar.setTextVisible(False)
        return progress_bar

    @staticmethod
    def create_line_edit(parent: QWidget, visible: bool, geometry: tuple[int, int, int, int], re: str) -> QLineEdit:
        line_edit = QLineEdit(parent)
        line_edit.setGeometry(*geometry)
        line_edit.setVisible(visible)
        line_edit.setValidator(QRegularExpressionValidator(re))
        return line_edit

    def create_action_type(self, parent: QWidget, items: Sequence[str], curent_idx: int, pos: tuple[int, int]) -> QComboBox:
        combo_box = QComboBox(parent)
        combo_box.setGeometry(*pos, 120, 30)
        combo_box.addItems(items)
        combo_box.currentIndexChanged.connect(self.on_option_selected)
        combo_box.setCurrentIndex(curent_idx)
        return combo_box

    def show_msg(self, no_data: bool, msg: str, sgnl: SignalInstance = None) -> None:
        if no_data:
            self.progress_bar.setMaximum(1)
        self.operation_status.setText(msg)
        sgnl.emit((1, 1))

    def show_widget(self) -> None:
        pass

    def on_option_selected(self, index: int) -> int:
        widget_visibility = {
            0: {
                'label_company_id': False,
                'line_company_id': False,
                'line_url': False,
                'label_url': False,
                'label_page_number': False,
                'line_page_number': False
            },
            1: {
                'label_company_id': True,
                'line_company_id': True,
                'line_url': False,
                'label_url': False,
                'label_page_number': False,
                'line_page_number': False
            },
            2: {
                'label_company_id': False,
                'line_company_id': False,
                'line_url': True,
                'label_url': True,
                'label_page_number': True,
                'line_page_number': True
            }
        }

        for widget, visibility in widget_visibility[index].items():
            getattr(self, widget).setVisible(visibility)

    def progress(self, data: tuple) -> None:
        self.progress_bar.setValue(data[0])
        if data[0] == data[1]:
            self.get_data_btn.setEnabled(True)
            self.progress_bar.setValue(0)

    def save_industries_data(self, sgnl: SignalInstance) -> None:
        industries = Industries()
        items = industries.get_industries()['industries']
        self.progress_bar.setMaximum(len(items))
        for count, item in enumerate(items, start=1):
            Common.save_to_csv(item.values(), 'industries')
            sgnl.emit((count, len(items)))

    def save_overview_data(self, sgnl: SignalInstance) -> None:
        overview = Overview()
        try:
            company_id = int(self.line_company_id.text())
        except ValueError:
            self.show_msg(True, "Index values can't be empty.", sgnl)
            return
        self.progress_bar.setMaximum(1)
        item = overview.get_overview(company_id)
        if item:
            Common.save_to_csv(item.values(), 'overview')
        sgnl.emit((1, 1))

    def save_reviews_data(self, sgnl: SignalInstance) -> None:
        reviews = Reviews()
        url = self.line_url.text()
        page_number = int(self.line_page_number.text())
        items = reviews.get_reviews(url, page_number)
        self.progress_bar.setMaximum(len(items))
        for count, item in enumerate(items, start=1):
            Common.save_to_csv(item.values(), 'reviews')
            sgnl.emit((count, len(items)))

    def run(self) -> None:
        self.get_data_btn.setEnabled(False)
        if self.action_type.currentIndex() == 0:
            worker = Worker(self.save_industries_data)
        if self.action_type.currentIndex() == 1:
            worker = Worker(self.save_overview_data)
        if self.action_type.currentIndex() == 2:
            worker = Worker(self.save_reviews_data)
        worker.signals.progress.connect(self.progress)
        self.threadpool.start(worker)
        self.operation_status.setText("")


class GUI:
    @staticmethod
    def show_ui() -> NoReturn:
        app = QApplication(sys.argv)
        window = MainWindow()
        screen_size = app.primaryScreen().geometry()
        x = screen_size.width() / 2 - window.geometry().width() / 2
        y = screen_size.height() / 2 - window.geometry().height() / 2

        window.move(x, y)
        window.show()
        sys.exit(app.exec())
