import sys
import json

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QPen
from datetime import datetime
import time
import socket


class MainWindow(QMainWindow):

	def __init__(self, udpaddr):
		super(MainWindow, self).__init__()
		self.udpaddr = udpaddr
		self.lastPoint = QPoint()
		self.image = QPixmap("2.jpg")
		self.drawing = False
		# self.log = []
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.drawPixmap(self.rect(), self.image)

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.drawing = True
			self.lastPoint = event.pos()
			print("press")

			X = 1920 - 2 * event.y()
			Y = 2 * event.x()
			print("(%s, %s)    %s" % (X, Y, datetime.now()))
			message = json.dumps({"x": X, "y": Y, "time": time.time(), "mouse": "press"})
			self.sock.sendto(message.encode(), self.udpaddr)

	def mouseMoveEvent(self, event):
		if event.buttons() == Qt.LeftButton and self.drawing:
			X = 1920 - 2 * event.y()
			Y = 2 * event.x()
			print("(%s, %s)    %s" % (X, Y, datetime.now()))
			message = json.dumps({"x": X, "y": Y, "time": time.time(), "mouse": "down"})

			self.sock.sendto(message.encode(), self.udpaddr)
			painter = QPainter(self.image)
			painter.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
			painter.drawLine(self.lastPoint, event.pos())
			self.lastPoint = event.pos()
			self.update()

	def mouseReleaseEvent(self, event):
		X = 1920 - 2 * event.y()
		Y = 2 * event.x()
		print("(%s, %s)    %s" % (X, Y, datetime.now()))

		print("release")
		message = json.dumps({"x": X, "y": Y, "time": time.time(), "mouse": "release"})

		self.sock.sendto(message.encode(), self.udpaddr)
		painter = QPainter(self.image)
		painter.eraseRect(self.rect())
		self.drawing = False


if __name__ == '__main__':
	app = QApplication(sys.argv)
	addr = ("192.168.0.68", 9090)
	m = MainWindow(addr)
	m.move(300, 20)
	m.resize(540, 960)
	m.show()
	app.exec_()
