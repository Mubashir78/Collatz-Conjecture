import sys, re
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication
from PyQt5.QtGui import QIntValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Ui(QMainWindow):
	num_list, win_exist = [], None
	def __init__(self, width=800, height=620):
		super(Ui, self).__init__()
		uic.loadUi('collture.ui', self)
		self.setFixedSize(width, height)

		self.button.clicked.connect(self.get_input)
		self.button_graph.setDisabled(True)
		self.button_graph.clicked.connect(self.send_graph_data)
		self.txt_box.setValidator(QIntValidator())

		self.show()

	def get_input(self):
		text = self.txt_box.text()
		self.txt_box.clear()
		self.out_text.clear()

		self.out_text.append(f"--{text}--\n")

		bold_format = '<span style="text-decoration:underline;font-weight:bold;">{}</span>'

		for num in collatz_conjecture(int(text)):
			if num in {4,2,1}:
				__class__.num_list.append(bold_format.format(str(num)))
			else: __class__.num_list.append(str(num))

		self.out_text.append(", ".join(__class__.num_list))
		self.out_text.insertPlainText('.')
		self.out_text.append(f"\nNumber of steps taken: {len(__class__.num_list)}")

		self.button_graph.setDisabled(False)

	def send_graph_data(self):
		try:
			__class__.win_exist

		except AttributeError:
			__class__.win_exist = None

		if __class__.win_exist is None:
			__class__.win_exist = Graph()
			__class__.win_exist.update(__class__.num_list)
			__class__.win_exist.show()

	@classmethod
	def on_graph_close(cls):
		del __class__.win_exist

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()

	def closeEvent(self, event):
		try:
			if __class__.win_exist is not None:
				__class__.win_exist.close()

		except AttributeError:
			pass

		event.accept()


class Graph(QDialog):
	def __init__(self, width=630, height=540):
		super(Graph, self).__init__()
		uic.loadUi('graph.ui', self)

		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.setFixedSize(width, height)

		self.label.setText(f"Graphical Representation of: {Ui.num_list[0]}")

		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)

		self.toolbar = NavigationToolbar(self.canvas, self)

		self.layout.addWidget(self.toolbar)
		self.layout.addWidget(self.canvas)

	def update(self, num_list):
		self.label.setText(f"Graphical Representation of: {Ui.num_list[0]}")
		self.plot_graph(Ui.num_list)

	def plot_graph(self, num_list):
		ax = self.figure.add_subplot(111)
		ax.clear()

		ax.set_xlabel("Number of Steps Taken")
		ax.set_ylabel("Current Value")

		num_list = [int(i) for num in num_list for i in re.findall(r'\d+', num)]
		ax.plot(range(1, len(num_list)+1), num_list, 'bo-')
		ax.grid()

		self.canvas.draw()

	def closeEvent(self, event):
		Ui.on_graph_close()
		self.hide()

def collatz_conjecture(num):
	while num > 1:
		yield num
		if num % 2:
			# num is odd
			num = 3*num + 1
		else:
			# num is even
			num = num//2

	yield 1


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = Ui()
	app.exec_()
