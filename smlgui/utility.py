"""
Utility for pre-processing the file before sending it to ``processor``.
"""
import logging
import platform
import sys
from contextlib import contextmanager

from PyQt5 import QtWidgets, QtCore, QtGui

from smlgui.processor import check_files

logger = logging.getLogger(__name__)


def select_folder():
    """
    Open's a QT QFileDialog and returns the path of the folder
    """
    logging.info("Select folder.")
    folder_location = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")

    check_files(folder_location)

    return folder_location


def is_windows():
    """
    Check if windows os

    >>> print(is_windows())
    True or False

    Returns
    -------
    bool: bool
        True or False.

    """
    if sys.platform == 'win32':
        return True
    return False


def is_mac():
    """
    Check if mac os

    >>> print(is_mac())
    True or False

    Returns
    -------
    bool: bool
        True or False.

    """
    if sys.platform == 'darwin':
        return True
    return False


def is_linux():
    """
    Check if linux os

    >>> print(is_linux())
    True or False

    Returns
    -------
    bool: bool
        True or False.

    """
    if sys.platform == 'linux':
        return True
    return False


def load_stylesheet():
    """
    Load's the ``style.qss``.
    """
    # Smart import of the rc file
    import smlgui.gui.assets.style_rc

    f = QtCore.QFile(":darkstyle/style.qss")
    if not f.exists():
        logger.error("Unable to load stylesheet, file not found in "
                     "resources")
        return ""
    else:
        f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        ts = QtCore.QTextStream(f)
        stylesheet = ts.readAll()
        if platform.system().lower() == 'darwin':  # see issue #12 on github
            mac_fix = '''
            QDockWidget::title
            {
                background-color: #31363b;
                text-align: center;
                height: 12px;
            }
            '''
            stylesheet += mac_fix
        return stylesheet


def loading_effects_decorator(func):
    """
    Decorator for creating an loading cursor.

    >>> @loading_effects_decorator
    >>> def do_lengthy_process():
    >>>     # DO something
    >>>     pass

    Parameters
    ----------
    func: function

    Returns
    -------
    new_function: object

    """

    def new_function(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            func(self)
        except Exception as e:
            raise e
            print("Error {}".format(e.args[0]))
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    return new_function


@contextmanager
def loading_effects_context():
    """
    Using context manager to create loading cursor for snippets of code.

    >>> with loading_effects_context():
    >>>     # Do something
    >>>     pass
    """
    try:
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        yield
    finally:
        QtWidgets.QApplication.restoreOverrideCursor()
