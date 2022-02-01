from __future__ import annotations
import platform
import mysql.connector
import logging
import os
import json
import ctypes
import sys
import subprocess
from logging.config import dictConfig
from typing import Any, List
from win32com.client import Dispatch
from PyQt5 import QtCore, QtGui, QtWidgets

from mainwindow import Ui_MainWindow
from utilities import DefaultSetting, LabelData

__version__ = "1.0.6"

COMPANY_NAME = 'DF-Software'
PROGRAM_NAME = "Fishbowl Label Generator"
USER_HOME_FOLDER = os.path.expanduser('~')
COMPANY_FOLDER = os.path.join(USER_HOME_FOLDER, "Documents", COMPANY_NAME)
PROGRAM_FOLDER = os.path.join(COMPANY_FOLDER, PROGRAM_NAME)

settings = QtCore.QSettings(COMPANY_NAME, PROGRAM_NAME)

# Default log settings
LOG_FOLDER = os.path.join(PROGRAM_FOLDER, 'Logs')
MAX_LOG_SIZE_MB = DefaultSetting(settings=settings, group_name="Logging",
                                 name="max_log_size_mb", value=5).initialize_setting().value
MAX_LOG_COUNT = DefaultSetting(settings=settings, group_name="Logging",
                               name="max_log_count", value=3).initialize_setting().value
ROOT_LOG_LEVEL = DefaultSetting(settings=settings, group_name="Logging",
                                name="root_log_level", value=logging.INFO).initialize_setting().value
FRONT_END_LOG_LEVEL = DefaultSetting(settings=settings, group_name="Logging",
                                     name="front_end_log_level", value=logging.INFO).initialize_setting().value
BACK_END_LOG_LEVEL = DefaultSetting(settings=settings, group_name="Logging",
                                    name="back_end_log_level", value=logging.INFO).initialize_setting().value
FRONT_END_LOG_FILE = "frontend.log"
BACK_END_LOG_FILE = "backend.log"

# Default program settings
MAX_LABEL_COUNT = DefaultSetting(settings=settings, group_name="Program",
                                 name="max_label_count", value=100).initialize_setting().value
REMOVE_PRINTED_LABELS = DefaultSetting(
    settings=settings, group_name="Program", name="remove_printed_labels", value=True).initialize_setting().value
DEBUG = DefaultSetting(settings=settings, group_name="Program",
                       name="debug", value=False).initialize_setting().value
if DEBUG == "true":
    DEBUG = True
else:
    DEBUG = False

DISSABLE_LABEL_PRINTING = DefaultSetting(
    settings=settings, group_name="Program", name="disable_label_printing", value=False).initialize_setting().value
if DISSABLE_LABEL_PRINTING == "true":
    DISSABLE_LABEL_PRINTING = True
else:
    DISSABLE_LABEL_PRINTING = False


if not os.path.exists(COMPANY_FOLDER):
    os.makedirs(COMPANY_FOLDER)

if not os.path.exists(PROGRAM_FOLDER):
    os.makedirs(PROGRAM_FOLDER)

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)


dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "%(asctime)s [%(levelname)s] in %(module)s: %(message)s",
        },
        "console": {
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "[%(name)s] %(asctime)s [%(levelname)s] in %(module)s: %(message)s",
        }
    },
    "handlers": {
        "backend_log_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_FOLDER, BACK_END_LOG_FILE),
            "maxBytes": MAX_LOG_SIZE_MB * 1024 * 1024,
            "backupCount": MAX_LOG_COUNT,
            "formatter": "default"
        },
        "frontend_log_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_FOLDER, FRONT_END_LOG_FILE),
            "maxBytes": MAX_LOG_SIZE_MB * 1024 * 1024,
            "backupCount": MAX_LOG_COUNT,
            "formatter": "default"
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console"
        }
    },
    "loggers": {
        "root": {
            "level": ROOT_LOG_LEVEL,
            "handlers": ["backend_log_file", "frontend_log_file", "console"]
        },
        "backend": {
            "level": BACK_END_LOG_LEVEL,
            "handlers": ["backend_log_file", "console"]
        },
        "frontend": {
            "level": FRONT_END_LOG_LEVEL,
            "handlers": ["frontend_log_file", "console"]
        }
    }
})

# Create the loggers
root_logger = logging.getLogger("root")
backend_logger = logging.getLogger("backend")
frontend_logger = logging.getLogger("frontend")
root_logger.info('=' * 80)


class MissingRequiredSoftwareError(Exception):
    """Raised when a missing software package is missing or not found."""
    pass


class DymoLabelPrinter:
    def __init__(self) -> object:
        self.printer_name = None
        self.label_file_path = None
        self.is_open = False
        try:
            self.printer_engine = Dispatch('Dymo.DymoAddIn')
            self.label_engine = Dispatch('Dymo.DymoLabels')
        except Exception as error:
            if error.strerror == "Invalid class string":
                raise MissingRequiredSoftwareError(
                    "Missing required software program. Please install DLS8Setup.8.7.exe.")

        printers = self.printer_engine.GetDymoPrinters()
        self.PRINTERS = [printer for printer in printers.split('|') if printer]
        backend_logger.info(f'Printers: {self.PRINTERS}')

    def __enter__(self):
        self.printer_engine.StartPrintJob()
        backend_logger.debug(
            f"Starting new print job. Selected printer: {self.printer_name}")
        return self.printer_engine

    def __exit__(self, exc_type, exc_val, exc_tb):
        backend_logger.debug("Ending print job.")
        # Log the exception if one was raised
        if exc_type is not None:
            backend_logger.exception(
                f"Exception occurred during print job. Exception: {exc_tb}")
        self.printer_engine.EndPrintJob()

    def set_printer(self, printer_name: str):
        if printer_name not in self.PRINTERS:
            backend_logger.warning(f'Printer {printer_name} not found.')
            raise Exception('Printer not found')
        self.printer_engine.SelectPrinter(printer_name)
        backend_logger.info(f"Printer set to: {printer_name}")

    def print_labels(self, copies: int = 1):
        backend_logger.info(f"Printing {copies} copies.")
        with self as label_engine:
            label_engine.Print(copies, False)

    def set_field(self, field_name: str, field_value: Any):
        self.label_engine.SetField(field_name, field_value)

    def register_label_file(self, label_file_path: str) -> object:
        self.label_file_path = label_file_path
        self.is_open = self.printer_engine.Open(label_file_path)
        if not self.is_open:
            backend_logger.error(
                f"Could not open label file: {label_file_path}")
            raise Exception('Could not open label file.')
        backend_logger.info(f"Label file set to: {label_file_path}")


class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(Exception)
    result = QtCore.pyqtSignal(object)

    def __init__(self, mysql_host: str, mysql_port: int, mysql_user: str, mysql_password: str, mysql_database: str):
        super().__init__()
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database

    def run(self):
        try:
            self.result.emit(self.work())
        except Exception as e:
            self.error.emit(e)
        finally:
            self.finished.emit()

    def work(self):
        return mysql.connector.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_password,
            database=self.mysql_database
        )


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


class FishbowlLabelGenerator(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self) -> object:
        super().__init__()
        try:
            self.printer = DymoLabelPrinter()
        except MissingRequiredSoftwareError as error:
            root_logger.error(
                f"There is a missing software program required to run: {error}")

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowTitle('Missing Required Software')
            msg.setText(str(error))
            msg.setInformativeText(
                "After clicking OK, the correct software will attempt to install.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            try:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", os.path.realpath(
                    os.path.join(os.path.dirname(__file__), 'Dymo Software', 'DLS8Setup.8.7.exe')))
            except Exception as error:
                root_logger.error("Could not find DLS8Setup.8.7.exe")
                root_logger.exception(error)
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setWindowTitle('Missing Required Software')
                msg.setText(
                    "There was an issue running the software. Please try again.")
                msg.setDetailedText(str(error))
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()
            sys.exit(1)

        self.setupUi(self)

        columns = [
            "WO Number",
            "Part Number",
            "Description",
            "Total Qty Used",
            "BOM Qty",
            "UOM",
            "Label Quantity",
            "Material Thickness"
        ]
        self.tableWidget.set_table_headers(columns)

        self.setWindowTitle(f'Fishbowl Label Generator v{__version__}')
        if DEBUG:
            self.setWindowTitle(
                f'Fishbowl Label Generator v{__version__} - DEBUG MODE')
        self.selectedPrinterComboBox.addItems(self.printer.PRINTERS)
        self.connect_signals()
        self.searchPushButton.setEnabled(False)

        settings.beginGroup('MainWindow')
        try:
            self.restoreGeometry(settings.value('geometry'))
            self.labelFileLineEdit.setText(settings.value('label_file_path'))
            self.printer.register_label_file(settings.value('label_file_path'))
            self.selectedPrinterComboBox.setCurrentText(
                settings.value('selected_printer_name'))
        except Exception:
            pass
        settings.endGroup()

        settings.beginGroup('MySQL')
        self.mysql_host = settings.value('host', "localhost")
        self.mysql_port = settings.value('port', "3306")
        self.mysql_user = settings.value('user', "gone")
        self.mysql_password = settings.value('password', "fishing")
        self.mysql_database = settings.value('database', "none")
        settings.endGroup()
        self.centralwidget.setEnabled(False)

        self.total_label.setText(f"Total Labels: 0")
        self.selected_label_total.setText(f"Selected Labels: 0")

        self.connect_to_mysql()

    def on_table_row_double_clicked(self):
        self.print_selected()

    def connect_to_mysql(self):
        backend_logger.info("Connecting to Server database.")
        values = {
            "Host": self.mysql_host,
            "Port": self.mysql_port,
            "User": self.mysql_user,
            "Password": self.mysql_password,
            "Database": self.mysql_database
        }

        backend_logger.debug(f"Connection properties: {values}")
        self.centralwidget.setEnabled(False)
        self.loadingDialog = QtWidgets.QProgressDialog(self)
        self.loadingDialog.setWindowTitle('Connecting')
        self.loadingDialog.setLabelText('Connecting to Server...')
        self.loadingDialog.setCancelButton(None)
        self.loadingDialog.setModal(True)
        self.loadingDialog.setRange(0, 0)
        self.loadingDialog.setValue(0)
        self.loadingDialog.show()

        self.thread = QtCore.QThread()
        self.worker = Worker(self.mysql_host, self.mysql_port, self.mysql_user, self.mysql_password,
                             self.mysql_database)
        self.worker.moveToThread(self.thread)
        self.worker.result.connect(self.on_worker_result)
        self.worker.result.connect(lambda: self.centralwidget.setEnabled(True))
        self.worker.result.connect(
            lambda: self.searchPushButton.setEnabled(True))
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.show_mysql_error)
        self.worker.error.connect(
            lambda: self.searchPushButton.setEnabled(False))
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.loadingDialog.close)
        self.thread.finished.connect(self.thread.deleteLater)
        backend_logger.debug("Starting thread.")
        self.thread.start()

    def show_mysql_error(self, error):
        backend_logger.error(f"Error connecting to database: {error}")
        self.mysql_connection = None
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText(
            "Could not connect to MySQL database. Make sure the connection settings are correct.")
        msg.setInformativeText(str(error))
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        self.on_mysql_settings_triggered()

    def on_worker_result(self, connection):
        self.mysql_connection = connection
        backend_logger.info(
            f"Successfully connected to server at: {self.mysql_host}.")
        self.loadingDialog.close()

    def closeEvent(self, event: QtGui.QCloseEvent):
        root_logger.info("Closing application.")

        backend_logger.debug("Saving window settings.")
        settings.beginGroup('MainWindow')
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('label_file_path', self.labelFileLineEdit.text())
        settings.setValue('selected_printer_name',
                          self.selectedPrinterComboBox.currentText())
        settings.endGroup()

        backend_logger.debug("Saving MySQL settings.")
        settings.beginGroup('MySQL')
        settings.setValue('host', self.mysql_host)
        settings.setValue('port', self.mysql_port)
        settings.setValue('user', self.mysql_user)
        settings.setValue('password', self.mysql_password)
        settings.setValue('database', self.mysql_database)
        settings.endGroup()

        event.accept()

    def connect_signals(self):
        backend_logger.debug("Connecting signals.")

        self.selectedPrinterComboBox.currentIndexChanged.connect(
            self.on_current_printer_index_changed)
        self.browsePushButton.clicked.connect(self.on_browse_button_clicked)
        self.actionMySQL_Settings.triggered.connect(
            self.on_mysql_settings_triggered)
        self.searchPushButton.clicked.connect(self.on_search_button_clicked)
        self.tableWidget.doubleClicked.connect(
            self.on_table_row_double_clicked)
        self.tableWidget.itemSelectionChanged.connect(
            self.on_table_selection_changed)
        self.printSelectedPushButton.clicked.connect(
            self.on_print_selected_button_clicked)

    def on_table_selection_changed(self):
        values = {}
        selected_total = 0
        for index, item in enumerate(self.tableWidget.selectedItems()):
            column_name = self.tableWidget.horizontalHeaderItem(
                item.column()).text()
            values[index] = {column_name: item.text()}
            if column_name == "Label Quantity":
                selected_total += int(item.text())

        self.selected_label_total.setText(f"Selected Labels: {selected_total}")

    def on_print_selected_button_clicked(self) -> None:
        backend_logger.debug("Selected print button clicked.")
        selected_total = int(
            self.selected_label_total.text().split(':')[1].strip())
        if selected_total > MAX_LABEL_COUNT:
            message_box = QtWidgets.QMessageBox()
            message_box.setIcon(QtWidgets.QMessageBox.Warning)
            message_box.setWindowTitle('Warning')
            message_box.setText(
                f"You have selected {selected_total} labels. The maximum number of labels is {MAX_LABEL_COUNT}.")
            message_box.setInformativeText(f"Please select fewer labels.")
            message_box.setDetailedText(
                f"You can select up to {MAX_LABEL_COUNT} labels. If you would like to print more labels, open the registry editor, navigate to 'Computer\HKEY_CURRENT_USER\SOFTWARE\{COMPANY_NAME}\{PROGRAM_NAME}\Program' and change the value of 'max_label_count' to the desired number. Make sure Base is set to 'Decimal'. Then reopen the application.")
            message_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message_box.exec_()
            return
        self.print_selected()

    def print_selected(self) -> None:
        row_items = self.tableWidget.selectedItems()
        column_count = self.tableWidget.columnCount()
        row_count = len(row_items) // column_count
        label_data = []
        total_labels = int(self.total_label.text().split(':')[1].strip())
        # row_items is a flat list of all the selected items.
        # We need to group them by row.
        for row in range(row_count):
            row_data = {}
            for column in range(column_count):
                column_heder = self.tableWidget.horizontalHeaderItem(
                    column).text()
                row_data[column_heder] = row_items[row *
                                                   column_count + column].text()
            label = LabelData(barcode=row_data["WO Number"],
                              part_number=row_data["Part Number"],
                              part_description=row_data["Description"],
                              quantity=int(row_data["Label Quantity"]),
                              material_thickness=row_data["Material Thickness"])
            total_labels -= label.quantity
            label_data.append(label)
        self.print_data(label_data)

        if REMOVE_PRINTED_LABELS == "true":
            self.total_label.setText(f"Total Labels: {total_labels}")
            selected_rows = [row for row in range(row_count)]
            frontend_logger.info(
                f"Removing {len(selected_rows)} label(s) from table.")
            for row in sorted(selected_rows):
                backend_logger.debug(f"Removing row {row} from table.")
                self.tableWidget.removeRow(row)

    def on_search_button_clicked(self):
        backend_logger.debug("Search button clicked.")
        self.populate_table(self.get_label_data())

    def on_mysql_settings_triggered(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle('MySQL Settings')
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.resize(400, 200)
        dialog.setLayout(QtWidgets.QVBoxLayout())
        dialog.layout().addWidget(QtWidgets.QLabel('Host:'))
        dialog.layout().addWidget(QtWidgets.QLineEdit(self.mysql_host))
        dialog.layout().addWidget(QtWidgets.QLabel('Port:'))
        dialog.layout().addWidget(QtWidgets.QLineEdit(str(self.mysql_port)))
        dialog.layout().addWidget(QtWidgets.QLabel('User:'))
        dialog.layout().addWidget(QtWidgets.QLineEdit(self.mysql_user))
        dialog.layout().addWidget(QtWidgets.QLabel('Password:'))
        dialog.layout().addWidget(QtWidgets.QLineEdit(self.mysql_password))
        dialog.layout().addWidget(QtWidgets.QLabel('Database:'))
        dialog.layout().addWidget(QtWidgets.QLineEdit(self.mysql_database))
        dialog.layout().addWidget(QtWidgets.QPushButton('Save'))
        dialog.layout().itemAt(10).widget().clicked.connect(dialog.close)
        dialog.exec_()

        askRetryConnect = QtWidgets.QMessageBox()
        askRetryConnect.setIcon(QtWidgets.QMessageBox.Question)
        askRetryConnect.setWindowTitle('MySQL')
        askRetryConnect.setText(
            "Would you like to reconnect to the server using these settings?")
        askRetryConnect.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        askRetryConnect.setDefaultButton(QtWidgets.QMessageBox.Yes)
        retryConnect = askRetryConnect.exec_()
        if retryConnect == QtWidgets.QMessageBox.Yes:
            self.mysql_host = dialog.layout().itemAt(1).widget().text()
            self.mysql_port = dialog.layout().itemAt(3).widget().text()
            self.mysql_user = dialog.layout().itemAt(5).widget().text()
            self.mysql_password = dialog.layout().itemAt(7).widget().text()
            self.mysql_database = dialog.layout().itemAt(9).widget().text()
            backend_logger.info(
                f"User requested to reconnect to MySQL server: {self.mysql_host}:{self.mysql_port}")
            self.connect_to_mysql()
        self.centralwidget.setEnabled(True)

        self.mysql_host = dialog.layout().itemAt(1).widget().text()
        self.mysql_port = dialog.layout().itemAt(3).widget().text()
        self.mysql_user = dialog.layout().itemAt(5).widget().text()
        self.mysql_password = dialog.layout().itemAt(7).widget().text()
        self.mysql_database = dialog.layout().itemAt(9).widget().text()

    def on_current_printer_index_changed(self, index: int):
        backend_logger.debug(f"Current printer index changed to {index}.")
        self.printer.set_printer(self.selectedPrinterComboBox.currentText())

    def on_browse_button_clicked(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open Label File', '', '*.label')
        if file_path:
            self.printer.register_label_file(file_path)
            self.labelFileLineEdit.setText(file_path)

    def print_data(self, labels: list[LabelData]) -> None:
        backend_logger.info(f"Printing {len(labels)} label(s).")
        with self.printer as printer:
            for label in labels:
                if DISSABLE_LABEL_PRINTING:
                    frontend_logger.info(f"Printing label: {label}")
                    continue
                self.printer.set_field("barcode", label.barcode)
                self.printer.set_field("part_number", label.part_number)
                self.printer.set_field(
                    "part_description", label.part_description)
                self.printer.set_field("quantity", label.quantity)
                self.printer.set_field(
                    "material_thickness", label.material_thickness)
                printer.Print(label.quantity, False)
                backend_logger.debug(f"Printed label: {label}")

    def get_label_data(self):
        wo_number = self.lineEdit.text()
        if not wo_number:
            wo_number = "%"
        values = {"wo_number": wo_number}
        cursor = self.mysql_connection.cursor(dictionary=True)
        query = """SELECT wo.num AS woNumber,
                        part.num as partNumber,
                        part.description AS partDescription,
                        TRIM(woitem.qtyTarget)+0 AS qtyTarget,
                        TRIM(bomitem.quantity)+0 AS bomQty,
                        uom.code AS uomCode,
                        ROUND(woitem.qtyTarget) AS labelQty
                    FROM wo
                    JOIN woitem ON wo.id = woitem.woId
                    JOIN moitem ON woitem.moItemId = moitem.id
                    JOIN bomitem ON moitem.bomItemId = bomitem.id
                    JOIN part ON moitem.partId = part.id
                    JOIN uom ON woitem.uomId = uom.id

                    WHERE moitem.statusId < 50 -- Fulfilled
                    AND woitem.typeId = 20 -- Raw Good
                    AND wo.statusId < 40 -- Fulfilled
                    AND wo.num LIKE %(wo_number)s
                    AND part.typeId != 21 -- Labor
                    """
        if DEBUG:
            root_logger.warning("Limmiting query to first 100 records.")
            query += " LIMIT 100"

        cursor.execute(query, values)
        result = cursor.fetchall()
        total_labels = 0
        for row in result:
            row["MATERIAL_THICKNESS"] = self.find_material_thickness(
                cursor, row['partNumber'])
            total_labels += row["labelQty"]

            if row["labelQty"] != 0:
                continue
            row["labelQty"] = 1

        cursor.close()
        self.total_label.setText(f"Total Labels: {total_labels}")
        return result

    def find_material_thickness(self, cursor, part_number: str):
        cursor.execute("SELECT num FROM bom WHERE id = (SELECT defaultBomId FROM part WHERE num = %(part_number)s)", {
                       "part_number": part_number})
        bom_number = cursor.fetchall()

        if len(bom_number) <= 0:
            return "N/A"
        return bom_number[0]["num"][-4:-1]

    def populate_table(self, data: List[dict]):
        frontend_logger.debug(f"Populating table with {len(data)} rows.")
        self.tableWidget.setRowCount(0)
        for row in data:
            self.tableWidget.insert_row_data(
                [str(data) for data in row.values()])

        self.tableWidget.resizeColumnsToContents()


def main():
    app = QtWidgets.QApplication([])
    window = FishbowlLabelGenerator()
    window.show()
    app.exec_()


if __name__ == '__main__':
    root_logger.info(f"Starting application... Version: {__version__}")

    if DEBUG:
        root_logger.setLevel(logging.DEBUG)
        backend_logger.setLevel(logging.DEBUG)
        frontend_logger.setLevel(logging.DEBUG)
        root_logger.debug("Debug mode enabled.")

    if DISSABLE_LABEL_PRINTING:
        root_logger.warning(
            "Label printing is disabled. Labels will not be printed. However, each label will be logged.")

    # Log the os platform, version and architecture
    bits, linkage = platform.architecture()
    root_logger.info(
        f'{platform.system()} OS detected. Version: "{platform.version()}" Architecture: [Bits: "{bits}", Linkage: "{linkage}"]')

    try:
        main()
    except Exception as error:
        root_logger.error("Application failed to start.")
        root_logger.exception(f"Exception: {error}")
        raise error
