from PyQt5.QtWidgets import QStyledItemDelegate, QStyle
from PyQt5.QtGui import QPixmap, QPainter, QFontMetrics
from PyQt5.QtCore import Qt


#
#
# This is to mediate the image/status code in column 1, it has no other purpose.
# I made this under duress

class ImageAndTextDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        data = index.data(Qt.DisplayRole)
        if isinstance(data, tuple) and len(data) == 2:
            image_path, status_code = data

            # Load and Scale Image
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                # Calculate vertical center
                cell_middle = option.rect.y() + (option.rect.height() // 2)  #that + margin is missing but is just fine tuning the margin
                pixmap_top = cell_middle - (pixmap.height() // 2)

                # Draw Image
                painter.drawPixmap(option.rect.x(), pixmap_top, pixmap)

            # Draw Text
            text_offset = pixmap.width() + 5  # 5 pixels space between image and text
            painter.drawText(option.rect.adjusted(text_offset, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, str(status_code))
