import paho.mqtt.client as mqtt #import the client1
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSize, QObject , QCoreApplication, QSettings ,QTimer , QThreadPool ,  QThread , QRunnable ,pyqtSignal
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
       
    
    def __del__(self):    
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


    def run(self):        
        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.
  
        broker_address="localhost"
        client = mqtt.Client("P1 " + self.topic) #create new instance
        client.on_message=self.on_message #attach function to callback

        client.connect(broker_address) #connect to broker
        client.loop_start() #start the loop

        client.subscribe(self.topic)
        while 1 :
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

        self.recvMesages = []

        settings = QSettings("test.ini", QSettings.IniFormat)
        print(settings.value("port"))
        self.sendMessageText.setText("your mensaage")
        self.sendRoomText.setText("test/2")
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

    def newMsg_fun(self , message  ) :
        result =  "topic : " + message[0].topic  + "\r\npayload  : " +  str(message[0].payload.decode("utf-8"))
        print( result )
        self.payloadList.addItem(result)
    
    def subscribe_fun(self) :
        self.thread = Worker(self.newTopicText.text())
        self.thread.signal.connect(self.newMsg_fun)
        self.thread.start()



    def test_fun(self ,result) :
        self.payloadList.addItem(result)
        print("test : " + result)
    
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



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()