import platform
import mysql.connector
import logging, os, json
from logging.config import dictConfig
from typing import Any, List
from win32com.client import Dispatch
from PyQt5 import QtCore, QtGui, QtWidgets

from mainwindow import Ui_MainWindow

__version__ = "1.0.0"

MAX_LOG_SIZE_MB = 10
MAX_LOG_COUNT = 2

if not os.path.exists("Logs"):
    os.mkdir("Logs")


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
            "filename": "Logs/backend.log",
            "maxBytes": MAX_LOG_SIZE_MB * 1024 * 1024,
            "backupCount": MAX_LOG_COUNT,
            "formatter": "default"
        },
        "frontend_log_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "Logs/frontend.log",
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
            "level": logging.DEBUG,
            "handlers": ["backend_log_file", "frontend_log_file", "console"]
        },
        "backend": {
            "level": logging.DEBUG,
            "handlers": ["backend_log_file", "console"]
        },
        "frontend": {
            "level": logging.DEBUG,
            "handlers": ["frontend_log_file", "console"]
        }
    }
})

# Create the loggers
root_logger = logging.getLogger("root")
backend_logger = logging.getLogger("backend")
frontend_logger = logging.getLogger("frontend")
root_logger.info('=' * 50)


class DymoLabelPrinter:
    def __init__(self) -> object:
        self.printer_name = None
        self.label_file_path = None
        self.is_open = False
        self.printer_engine = Dispatch('Dymo.DymoAddIn')
        self.label_engine = Dispatch('Dymo.DymoLabels')
        printers = self.printer_engine.GetDymoPrinters()
        self.PRINTERS = [printer for printer in printers.split('|') if printer]
        backend_logger.info(f'Printers: {self.PRINTERS}')

    def __enter__(self):
        self.printer_engine.StartPrintJob()
        backend_logger.debug(f"Starting new print job. Selected printer: {self.printer_name}")
        return self.printer_engine

    def __exit__(self, exc_type, exc_val, exc_tb):
        backend_logger.debug("Ending print job.")
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
            backend_logger.error(f"Could not open label file: {label_file_path}")
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


class FishbowlLabelGenerator(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self) -> object:
        super().__init__()
        self.printer = DymoLabelPrinter()
        self.setupUi(self)
        self.setWindowTitle(f'Fishbowl Label Generator v{__version__}')
        self.selectedPrinterComboBox.addItems(self.printer.PRINTERS)
        self.connect_signals()
        self.printPushButton.setEnabled(False)
        self.settings = QtCore.QSettings('Fishbowl Label Generator', 'Fishbowl Label Generator')

        self.settings.beginGroup('MainWindow')
        try:
            self.restoreGeometry(self.settings.value('geometry'))
            self.labelFileLineEdit.setText(self.settings.value('label_file_path'))
            self.printer.register_label_file(self.settings.value('label_file_path'))
            self.selectedPrinterComboBox.setCurrentText(self.settings.value('selected_printer_name'))
            self.printPushButton.setEnabled(True)
        except Exception:
            pass
        self.settings.endGroup()

        self.settings.beginGroup('MySQL')
        self.mysql_host = self.settings.value('host', "localhost")
        self.mysql_port = self.settings.value('port', "3306")
        self.mysql_user = self.settings.value('user', "gone")
        self.mysql_password = self.settings.value('password', "fishing")
        self.mysql_database = self.settings.value('database', "none")
        self.settings.endGroup()
        self.centralwidget.setEnabled(False)

        self.total_label.setText(f"Total Labels: 0")
        self.selected_label_total.setText(f"Selected Labels: 0")

        self.connect_to_mysql()

    def on_table_row_double_clicked(self):
        selected_row = self.tableWidget.selectedItems()
        self.print_selected_row(selected_row)

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
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.show_mysql_error)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.loadingDialog.close)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def show_mysql_error(self, error):
        backend_logger.exception(f"Error connecting to database: {error}")
        self.mysql_connection = None
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText(
            "Could not connect to MySQL database. Make sure the connection settings are correct then close and reopen the program.")
        msg.setInformativeText(str(error))
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        self.on_mysql_settings_triggered()

    def on_worker_result(self, connection):
        self.mysql_connection = connection
        backend_logger.info(f"Successfully connected to server at: {self.mysql_host}.")
        self.loadingDialog.close()

    def closeEvent(self, event: QtGui.QCloseEvent):
        root_logger.info("Closing application.")

        backend_logger.debug("Saving window settings.")
        self.settings.beginGroup('MainWindow')
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('label_file_path', self.labelFileLineEdit.text())
        self.settings.setValue('selected_printer_name', self.selectedPrinterComboBox.currentText())
        self.settings.endGroup()

        backend_logger.debug("Saving MySQL settings.")
        self.settings.beginGroup('MySQL')
        self.settings.setValue('host', self.mysql_host)
        self.settings.setValue('port', self.mysql_port)
        self.settings.setValue('user', self.mysql_user)
        self.settings.setValue('password', self.mysql_password)
        self.settings.setValue('database', self.mysql_database)
        self.settings.endGroup()

        event.accept()

    def connect_signals(self):
        backend_logger.info("Connecting signals.")

        self.selectedPrinterComboBox.currentIndexChanged.connect(self.on_current_printer_index_changed)
        self.browsePushButton.clicked.connect(self.on_browse_button_clicked)
        self.printPushButton.clicked.connect(self.on_print_button_clicked)
        self.actionMySQL_Settings.triggered.connect(self.on_mysql_settings_triggered)
        self.searchPushButton.clicked.connect(self.on_search_button_clicked)
        self.tableWidget.doubleClicked.connect(self.on_table_row_double_clicked)
        self.tableWidget.itemSelectionChanged.connect(self.on_table_selection_changed)
        self.printSelectedPushButton.clicked.connect(self.on_print_selected_button_clicked)
    
    def on_table_selection_changed(self):
        selected_row = self.tableWidget.selectedItems()
        selected_total = selected_row[6].text()

        values = {}
        for item in self.tableWidget.selectedItems():
            column_name = self.tableWidget.horizontalHeaderItem(item.column()).text()
            values[column_name] = item.text()
        
        frontend_logger.debug(f"Selection changed. Values:\n[{json.dumps(values, indent=4)}]")
        self.selected_label_total.setText(f"Selected Labels: {selected_total}")

    def on_print_selected_button_clicked(self):
        selected_row = self.tableWidget.selectedItems()
        if len(selected_row) == 0:
            return

        self.print_selected_row(selected_row)

    def print_selected_row(self, row):
        data = [{
            "BARCODE": row[0].text(),
            "part_number": row[1].text(),
            "part_description": row[2].text(),
            "quantity": row[6].text(),
            "MATERIAL_THICKNESS": row[7].text()
        }]
        frontend_logger.info(f"Printing selected row: {data}")
        self.print_data(data)

    def on_search_button_clicked(self):
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
        askRetryConnect.setText("Would you like to reconnect to the server using these settings?")
        askRetryConnect.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        askRetryConnect.setDefaultButton(QtWidgets.QMessageBox.Yes)
        retryConnect = askRetryConnect.exec_()
        if retryConnect == QtWidgets.QMessageBox.Yes:
            self.mysql_host = dialog.layout().itemAt(1).widget().text()
            self.mysql_port = dialog.layout().itemAt(3).widget().text()
            self.mysql_user = dialog.layout().itemAt(5).widget().text()
            self.mysql_password = dialog.layout().itemAt(7).widget().text()
            self.mysql_database = dialog.layout().itemAt(9).widget().text()
            backend_logger.info(f"User requested to reconnect to MySQL server: {self.mysql_host}:{self.mysql_port}")
            self.connect_to_mysql()
        self.centralwidget.setEnabled(True)

        self.mysql_host = dialog.layout().itemAt(1).widget().text()
        self.mysql_port = dialog.layout().itemAt(3).widget().text()
        self.mysql_user = dialog.layout().itemAt(5).widget().text()
        self.mysql_password = dialog.layout().itemAt(7).widget().text()
        self.mysql_database = dialog.layout().itemAt(9).widget().text()

    def on_current_printer_index_changed(self, index: int):
        self.printer.set_printer(self.selectedPrinterComboBox.currentText())

    def on_browse_button_clicked(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Label File', '', '*.label')
        if file_path:
            self.printer.register_label_file(file_path)
            self.labelFileLineEdit.setText(file_path)
            self.printPushButton.setEnabled(True)

    def on_print_button_clicked(self):
        data = self.get_label_data()
        if not data:
            return
        label_data = []
        frontend_logger.info(f"Printing all labels in table {len(data)}.")
        for row in data:
            label_data.append({
                "BARCODE": row["woNumber"],
                "part_number": row["partNumber"],
                "part_description": row["partDescription"],
                "quantity": row["labelQty"],
                "MATERIAL_THICKNESS": row[7].text()
            })
        self.print_data(label_data)

    def print_data(self, data: List[dict]):
        with self.printer as printer:
            for label in data:
                quantity = label.pop('quantity')
                log_data = []
                for field_name, field_value in label.items():
                    self.printer.set_field(field_name, field_value)
                    log_data.append({field_name: field_value})
                printer.Print(quantity, False)
                frontend_logger.debug(f"Printing {quantity} labels:\n{json.dumps(log_data, indent=4)}")

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
        cursor.execute(query, values)
        result = cursor.fetchall()
        total_labels = 0
        for row in result:
            row["MATERIAL_THICKNESS"] = self.find_material_thickness(cursor, row['partNumber'])
            total_labels += row["labelQty"]
            
            if row["labelQty"] != 0:
                continue
            row["labelQty"] = 1

        cursor.close()
        self.total_label.setText(f"Total Labels: {total_labels}")
        return result

    def find_material_thickness(self, cursor, part_number: str):
        cursor.execute("SELECT num FROM bom WHERE id = (SELECT defaultBomId FROM part WHERE num = %(part_number)s)", {"part_number": part_number})
        bom_number = cursor.fetchall()
        
        if len(bom_number) <= 0:
            return "N/A"
        return bom_number[0]["num"][-4:-1]
        
    def populate_table(self, data: List[dict]):
        frontend_logger.debug(f"Populating table with {len(data)} rows.")
        self.tableWidget.setRowCount(0)
        for row, row_data in enumerate(data):
            self.tableWidget.insertRow(row)
            for column, column_data in enumerate(row_data.values()):
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(column_data)))
        self.resize_all_columns(self.tableWidget)

    def resize_all_columns(self, tableWidget: QtWidgets.QTableWidget):
        frontend_logger.debug("Resizing all columns in table.")
        for column in range(tableWidget.columnCount()):
            tableWidget.resizeColumnToContents(column)

def main():
    app = QtWidgets.QApplication([])
    window = FishbowlLabelGenerator()
    window.show()
    app.exec_()

if __name__ == '__main__':
    root_logger.info(f"Starting application... Version: {__version__}")

    # Log the os platform, version and architecture
    bits, linkage = platform.architecture()
    root_logger.info(f'{platform.system()} OS detected. Version: "{platform.version()}" Architecture: [Bits: "{bits}", Linkage: "{linkage}"]')

    try:
        main()
    except Exception as error:
        root_logger.error("Application failed to start.")
        root_logger.exception(f"Exception: {error}")
        raise error