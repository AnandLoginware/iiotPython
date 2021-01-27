#*********This script is used to send all the IIOT data from device to server**************************



#importing of required libraries
from time import sleep 
import sqlite3 
import requests as req
from datetime import datetime
import configuration as config

#making a connection with the database
conn2=sqlite3.connect(config.DATABASENAME)

#create a cursor object to exceute all sql queries
curs2=conn2.cursor()

max_var=1


#Function which sends AlarmInfo  data
#parameters :  endpoint - at which endpoint to send the data
#no return type for the fucntion
def SendAlarmData(endpoint):
   
   print("****************SENDING ALARM DATA********************")
   try:
             curs2.execute("select * from alarm ")
             result=curs2.fetchall()
             print(result)
             if result is not None: 
               data={}                   
               for colm in result:
                 Id=colm[0]
                 data["ID"]=colm[0]
                 data["MachineID"]=colm[1]
                 data["OperatorName"]=colm[2]
                 data["JobID"]=colm[3]
                 data["Shift"]=colm[4]
                 data["Component"]=colm[5]
                 data["ModelName"]=colm[6]
                 data["Operation"]=colm[7]
                 data["TimeStamp"]=colm[8]
                 data["Reason"]=colm[9]
                 response=req.post(endpoint,data=data,timeout=2)
                 if(response.status_code>=200 and response.status_code<=206):
                         curs2.execute("delete from alarm where id=(?)",(Id,))
                         conn2.commit()
                         print("{} entry send to server and deleted from local database ").format(Id)
                 else:
                    print(response.status_code) 
                    print("didnot get good response from server") 
                    return        
                            
             else:
                print("no data to send ...")
   except Exception as e:
              print("Exception occured : ",e)
              return




          

#Function which sends liveStatus data
#parameters :  endpoint - at which endpoint to send the data
#no return type for the fucntion
def SendLiveStatus(endpoint):
         print("****************SENDING LIVE SIGNALS DATA********************")
         try:
           curs2.execute("select * from live_status")
           result=curs2.fetchone()
           if result is not None: 
             Id=str(result[0])
             machineId=result[1]
             machineType=result[2]
             status=str(result[3])
             signalColor=result[4]
             signalName=result[5]
             response=req.post(endpoint+"?ID="+Id+"&MachineID="+machineId+"&MachineType="+machineType+"&Status="+status+"&SignalName="+signalName+"&SignalColor="+signalColor,timeout=2)
             if(response.status_code>=200 and response.status_code<=206):
                    print("Current Live Status : {}".format(signalName))
                    print(" Live Status data successfully sent ")
             else:
                 print("didnot get good response from server")
                 return             
           else:
               print("no data to send....")
         except Exception as e:
              print("Exception occured : ",e)
              return





#Function which sends production data
#parameters :  endpoint - at which endpoint to send the data
#no return type for the fucntion
def SendProductionData(endpoint):
   global max_var
   print("********************SENDING PRODUCTION DATA****************************")
   try:
           curs2.execute("select * from live_status")
           liveStatusResult=curs2.fetchone()
           if liveStatusResult is not None:
              
              signalName=liveStatusResult[5]
              print(signalName)
              if signalName=='Machine Idle':
                   print("****************************************")
                   curs2.execute("select * from production")
                   result=curs2.fetchall()           
                   if result is not None:
                     data={}                     
                     for colm in result:
                        Id=colm[0]
                        data["ID"]=colm[0]
                        data["OperatorName"]=colm[1]
                        data["JobID"]=colm[2]
                        data["Shift"]=colm[3]
                        data["Component"]=colm[4]
                        data["ModelName"]=colm[5]
                        data["Operation"]=colm[6]
                        data["CycleTime"]=float(colm[7])
                        data["InspectionStatus"]=colm[8]
                        data["Status"]=colm[9]
                        data["TimeStamp"]=datetime.strptime(colm[10], '%Y/%m/%d %H:%M:%S') 
                        data["MachineID"]=colm[11]
                        if(Id==max_var):
                            print("sucess")
                            max_var+=1
                        #response=req.post(endpoint,timeout=2,data=data)
                        
                        
                        '''if(response.status_code>=200 and response.status_code<=206):
                                curs2.execute("delete from production where id=(?)",(Id,))
                                conn2.commit()
                                print("{} entry sent to server and  deleted from local database..".format(Id))    
                        else:
                              print("didnot get good response from server")
                              return'''
                   else:
                       print("no data to send ...")
   except Exception as e:
            print("Exception occured : ",e)
            return
 

                              






