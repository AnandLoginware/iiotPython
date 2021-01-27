#import the library which reads all the cnc machine signals and stores in local database.
from signal_package import cncSignalsTracker
import configuration as config

#importing api.py and sendData.py to create parallel processes
import api as api_run
import sendData as sendData_run

#importing multiprocessing library
import multiprocessing as mp


database = config.DATABASENAME
holdMachineEndpoint = "http://" + config.LOCALSERVER_IPADDRESS + ":" + config.PORT + "/HoldMachine"
localHeaders = config.HEADERS



#create a cncSignalsTracker object
cnc = cncSignalsTracker()


#Running processes of api.py 
def process_of_api():
    #START THE SERVER AT PORT 5002 
    api_run.app.run(port=5002,threaded=True,debug=True)
        

#Running processes of main.py
def process_of_main():
    cnc.configure(
    databaseName = database,
    headers = localHeaders,
    holdMachineUrl = holdMachineEndpoint
        )
    cnc.getAndSetupPins()
    cnc.start()

#Running processes of sendData.py
def process_of_sendData():
    #continously run the loop to send data to server every 2 seconds 
    while(1):
        #Function call of 'SendLiveStatus' Function
        #sendData_run.SendLiveStatus("http://"+config.SERVER_IP+config.SERVER_ENDPOINT_START+"/PostMachineStatus")

        #Function call of 'SendProductionData' Function
        sendData_run.SendProductionData("http://"+config.SERVER_IP+config.SERVER_ENDPOINT_START+"/Production")

        #Function call of 'SendAlarmData' Function
        #sendData_run.SendAlarmData("http://"+config.SERVER_IP+config.SERVER_ENDPOINT_START+"/AlarmInfo")
        
        #wait for 5 seconds 
        #sleep(5)
    

#creating multiprocesses of functions
p1 = mp.Process(target = process_of_api)
p2 = mp.Process(target = process_of_main)
p3 = mp.Process(target = process_of_sendData)

#Start executing code inside target functions parallelly
p1.start()
p2.start()
p3.start()

#Wait untill the completion of processes
p1.join()
p2.join()
p3.join()
