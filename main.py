import ScreenCloud
import json
import urllib2

from PythonQt.QtCore import QSettings, QByteArray, QBuffer, QIODevice, QFile
from PythonQt.QtGui import QWidget, QDialog
from PythonQt.QtUiTools import QUiLoader


class UrlUploader():
	def __init__(self):
		self.uil = QUiLoader()
		self.loadSettings()

	def showSettingsUI(self, parent_widget):
		self.parentWidget = parent_widget
		self.settingsDialog = self.uil.load(QFile(workingDir + "/settings.ui"), parent_widget)
		self.settingsDialog.group_screenshot.input_name.connect("textChanged(QString)", self.nameFormatEdited)
		self.settingsDialog.connect("accepted()", self.saveSettings)
		self.loadSettings()
		self.settingsDialog.group_url.input_token.text = self.url_token
		self.settingsDialog.group_url.input_address.text = self.url_address
		self.settingsDialog.group_url.input_attribute.text = self.url_attribute
		self.settingsDialog.group_screenshot.input_name.text = self.name_format
		self.settingsDialog.open()

	def nameFormatEdited(self, name_format):
		self.settingsDialog.group_screenshot.label_example.setText(ScreenCloud.formatFilename(name_format))

	def loadSettings(self):
		settings = QSettings()
		settings.beginGroup("uploaders")
		settings.beginGroup("urluploader")
		self.url_token = settings.value("url-token", "")
		self.url_address = settings.value("url-address", "")
		self.url_attribute = settings.value("url-attribute", "href")
		self.name_format = settings.value("name-format", "Screenshot (%Y-%m-%d %H-%M-%S)")
		settings.endGroup()
		settings.endGroup()

	def saveSettings(self):
		settings = QSettings()
		settings.beginGroup("uploaders")
		settings.beginGroup("urluploader")
		settings.setValue("url-token", self.settingsDialog.group_url.input_token.text)
		settings.setValue("url-address", self.settingsDialog.group_url.input_address.text)
		settings.setValue("url-attribute", self.settingsDialog.group_url.input_attribute.text)
		settings.setValue("name-format", self.settingsDialog.group_screenshot.input_name.text)
		settings.endGroup()
		settings.endGroup()

	def isConfigured(self):
		self.loadSettings()
		return not(not self.url_token or not self.url_address)

	def getFilename(self):
		self.loadSettings()
		return ScreenCloud.formatFilename(self.name_format)

	def upload(self, screenshot, name):
		self.loadSettings()
		q_ba = QByteArray()
		q_buff = QBuffer(q_ba)
		q_buff.open(QIODevice.WriteOnly)
		screenshot.save(q_buff, ScreenCloud.getScreenshotFormat())
		q_buff.close()
		image = q_ba.toBase64().data()
		data = json.dumps({'token': self.url_token, 'name': name, 'image': image})
		headers = {"Content-Type": "application/json"}
		request = urllib2.Request(self.url_address, data, headers)
		try:
			reply = urllib2.urlopen(request)
		except Exception as e:
			ScreenCloud.setError("Could not upload to: " + self.url_address)
			return False
		try:
			response = reply.read()
			data = json.loads(response)
			url = data.get(self.url_attribute)
			ScreenCloud.setUrl(url)
		except Exception as e:
			ScreenCloud.setError("Could not upload to: " + self.url_address + "\n" + e.message)
			return False
		return True
