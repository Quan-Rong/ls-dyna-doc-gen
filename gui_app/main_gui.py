"""
GUI Application Entry Point

Main entry point for the GUI application.
"""

import sys
import os
import warnings

# Suppress libpng warning about incorrect sRGB profile
# This warning is harmless but comes from Qt's underlying C library
warnings.filterwarnings("ignore")

# Add parent directory to path to import ls_dyna_md
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Filter stderr to suppress libpng warnings
class StderrFilter:
    """Filter stderr to suppress libpng warnings."""
    def __init__(self, original_stderr):
        self.original_stderr = original_stderr
    
    def write(self, message):
        # Filter out libpng warnings
        if 'libpng warning' in message.lower() or 'iccp' in message.lower():
            return
        self.original_stderr.write(message)
    
    def flush(self):
        self.original_stderr.flush()

# Redirect stderr to filter
sys.stderr = StderrFilter(sys.stderr)

# Set Qt plugin path BEFORE importing QApplication
# This fixes the "no Qt platform plugin could be initialized" error
from PyQt5 import QtCore

# Find and set Qt plugins directory
try:
    qt_dir = os.path.dirname(QtCore.__file__)
    plugin_path = os.path.join(qt_dir, 'Qt5', 'plugins')
    if os.path.exists(plugin_path):
        os.environ['QT_PLUGIN_PATH'] = plugin_path
        # Set library paths before creating QApplication
        QtCore.QCoreApplication.setLibraryPaths([plugin_path])
except Exception:
    pass  # If we can't set it, let Qt try to find it automatically

from PyQt5.QtWidgets import QApplication
from gui_app.gui.main_window import MainWindow
from gui_app import __version__


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("LS-Dyna Documentation Generator")
    app.setApplicationVersion(__version__)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
