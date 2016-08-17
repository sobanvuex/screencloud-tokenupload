import ScreenCloud
import json
import urllib.request, urllib.error, urllib.parse

from PythonQt.QtCore import QSettings, QByteArray, QBuffer, QIODevice, QFile
from PythonQt.QtGui import QWidget, QDialog
from PythonQt.QtUiTools import QUiLoader

class TokenUploader():

    def __init__(self):

        self.uil = QUiLoader()
        self.loadSettings()

    def showSettingsUI(self, parentWidget):

        self.parentWidget = parentWidget
        self.settingsDialog = self.uil.load(QFile(workingDir + "/settings.ui"), parentWidget)
        
        self.settingsDialog.group_screenshot.input_name.connect("textChanged(QString)", self.nameFormatEdited)
        self.settingsDialog.connect("accepted()", self.saveSettings)
        self.loadSettings()
        
        self.settingsDialog.group_url.input_token.text = self.url_token
        self.settingsDialog.group_url.input_address.text = self.url_address
        self.settingsDialog.group_screenshot.input_name.text = self.name_format
        
        self.settingsDialog.open()

    def nameFormatEdited(self, name_format):

        self.settingsDialog.group_screenshot.label_example.setText(ScreenCloud.formatFilename(name_format))

    def loadSettings(self):

        settings = QSettings()
        
        settings.beginGroup("uploaders")
        settings.beginGroup("tokenupload")
        
        self.url_token = settings.value("url-token", "")
        self.url_address = settings.value("url-address", "")
        self.name_format = settings.value("name-format", "Screenshot (%Y-%m-%d %H-%M-%S)")
        
        settings.endGroup()
        settings.endGroup()

    def saveSettings(self):

        settings = QSettings()
        
        settings.beginGroup("uploaders")
        settings.beginGroup("tokenupload")
        
        settings.setValue("url-token", self.settingsDialog.group_url.input_token.text)
        settings.setValue("url-address", self.settingsDialog.group_url.input_address.text)
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
        data = json.dumps({'token': self.url_token, 'name': name, 'image': image.decode('utf-8')})
        binary = data.encode('utf-8')
        
        headers = {'Content-Type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.54 Safari/537.36'}
        request = urllib.request.Request(self.url_address, binary, headers)

        try:
            
            reply = urllib.request.urlopen(request)

            response = reply.read().decode('utf-8')
            data = json.loads(response)
            error = data.get('error')
            url = data.get('href')

            if error:

                ScreenCloud.setError("Could not upload to: " + self.url_address + "\nError: " + error)
                return False

            ScreenCloud.setUrl(url)
            
        except urllib.error.HTTPError as exc:
        
            ScreenCloud.setError("Error while connecting to: " + self.url_address + "\nError:\n" + exc.fp.read())
            return False
            
        return True
