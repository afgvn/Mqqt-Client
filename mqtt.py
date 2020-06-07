import paho.mqtt.client as mqtt #import the client1
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys , time

ORGANIZATION_NAME = '3Dimesiones App'
ORGANIZATION_DOMAIN = 'example.com'
APPLICATION_NAME = 'Mqtt-client'


class Worker(QThread):

    signal = pyqtSignal(object )
    
    def __init__(self , topic):
        QThread.__init__(self)
        print("subscribe new topic ")
        self.topic = topic
        self.flagRun = True
       
    
    def __del__(self):  
        self.flagRun = False  
        print("delete  task")
    
    def on_message(self , client, userdata, message ):
        
        '''
        print("message received " ,tempStr )
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)
        '''
        messageTemp = [ message ]
        self.signal.emit( messageTemp )

    def stop(self):
        self.flagRun = False


    def run(self):        
        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.
  
        broker_address="localhost"
        client = mqtt.Client("P1 " + self.topic) #create new instance
        client.on_message=self.on_message #attach function to callback

        client.connect(broker_address) #connect to broker
        client.loop_start() #start the loop

        client.subscribe(self.topic)
        while (self.flagRun) :
            time.sleep(1) # wait
        client.loop_stop() #stop the loop


class Ui(QtWidgets.QMainWindow):


    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('mqqt2.ui', self) # Load the .ui file
        self.show() # Show the GUI
        # Conectamos los eventos con sus acciones
        self.sendButton.clicked.connect(self.send_fun)
        self.saveConfigBtn.clicked.connect(self.saveCn_fun)
        self.subscribeButton.clicked.connect(self.subscribe_fun)
        self.deleteTopicBtn.clicked.connect(self.unsubscribe_fun)
        self.configButton.clicked.connect(self.confW_fun)
        self.connectButton.clicked.connect(self.conect_fun)
        self.disconnectButton.clicked.connect(self.disconect_fun)

        self.configButton.setEnabled(True)



        self.topics = []
        self.counter = 0
        self.flagActive=False

        settings = QSettings("test.ini", QSettings.IniFormat)
        print(settings.value("port"))
        self.sendMessageText.setText("your mensaage")
        self.sendRoomText.setText("test/1")
        self.newTopicText.setText("test/#")
        #self.subscribe_fun()
        self.hostText.setText(settings.value("Host" , "localhost" ))
        self.portText.setText(settings.value("port", "1883"))

        '''
        settings = QSettings("testA.ini", QSettings.IniFormat)
        size = settings.beginReadArray("logins")
        for i  in range(size):
            settings.setArrayIndex(i)
            print(settings.value("login" ))
        settings.endArray()


        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.counter = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        '''
    def conect_fun( self ) :
        print("conect!!!")
        self.configButton.setEnabled(False)
        self.flagActive=True
        self.subscribe_fun()

    def disconect_fun( self ) :
        print("disconect++++++")
        self.configButton.setEnabled(True)
        #self.topics[i].stop()
        for i in  self.topics :
           i.stop()
        self.topics.clear()
        self.topicsList.clear()
        self.flagActive=False

    def newMsg_fun(self , message  ) :
        result =  "topic : " + message[0].topic  + "\r\npayload  : " +  str(message[0].payload.decode("utf-8"))
        print( result )
        self.payloadList.addItem(result)
    
    def subscribe_fun(self) :
        self.thread = Worker(self.newTopicText.text())
        self.topics.append(self.thread)
        self.topicsList.addItem(self.newTopicText.text())
        '''
        self.thread.signal.connect(self.newMsg_fun)
        self.thread.start()'''
        pos = len(self.topics) -  1
        self.topics[pos].signal.connect(self.newMsg_fun)
        self.topics[pos].start()
        

    def unsubscribe_fun(self) :
        self.topics[self.topicsList.currentRow()].stop()
        self.topics.pop(self.topicsList.currentRow())
        self.topicsList.takeItem(self.topicsList.currentRow())


    def recurring_timer(self):
        self.counter +=1
        print("Counter: %d" % self.counter)

    #send mesage to topic 
    def send_fun(self):
        client = mqtt.Client("P2") #create new instance
        client.connect(self.hostText.text(),int(self.portText.text())) #connect to broker roomsendText
        client.publish(self.sendRoomText.text(),self.sendMessageText.text())#publish


    #save configuration of broker 

    def saveCn_fun(self):
        
        settings = QSettings("test.ini", QSettings.IniFormat)
        settings.setValue("Host", self.hostText.text())
        settings.setValue("port", self.portText.text())
        settings.sync()

        settings = QSettings("testA.ini", QSettings.IniFormat)
        size = settings.beginReadArray("logins")
        settings.endArray()
        settings.beginWriteArray("logins")
        settings.setArrayIndex(size)
        settings.setValue("login", "prueba # " + str(size))
        settings.endArray()

    def confW_fun (self):
        #self.close()
        '''
        next=Dialog_TempIP(self)
        next.__init__()'''
        dlg = CustomDialog(self)
        dlg.show()
        '''
        if dlg.exec_():
            print("Success!")
        else:
            print("Cancel!")'''


 
class CustomDialog(QDialog):

    signal = pyqtSignal(object )

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)
        uic.loadUi('mqqt_conf.ui', self) # Load the .ui file

    def accept(self):
        print("test accpet")
        self.close()

        




	

        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()