import hashlib
from PyQt5 import QtCore,QtWidgets
from gui import Ui_Form
import os,sys
import datetime
### For reading ini files
import configparser

### Imported sftpcomm.py amd SftpComm is module inside sftpcomm.py
from sftpcomm import SftpComm

import paramiko

constants = 'constants.ini'
if not os.path.exists(constants):
    print("Configuration file not found")
    print("Creating New configuration file")
    ### 2 This part creates constants.ini file
    fp = open('constants.ini', 'w')
    fp.write('[server]\n')
    fp.write('server_ip = 95.179.243.248\n')
    fp.write('user_name = root\n')
    fp.write('password = 6Sz,vfn$UqWW3d5a\n')
    fp.write('rw_dir = /root/\n')
    fp.write('ro_dir = /root/\n')
    fp.write('scriptLocation = /root/update.sh\n')
    fp.write('unzipLocation = /home/automata')
    fp.close()
    print("Sucessfully created New configuration file")
else:
    print("Using Default Configuration file")
    config = configparser.ConfigParser()
    config.read('constants.ini')


class updator():
    def __init__(self,wid):

        self.gui = Ui_Form();
        self.gui.setupUi(wid);

        self.config = ('constants.ini');
        self.gui.connect.clicked.connect(self.connectController);
        self.gui.disconnect.clicked.connect(self.DisconnectController);
        self.sftpServer = SftpComm(self,ipAddress=(config.get('server', 'server_ip')),userName=(config.get('server', 'user_name')),password=(config.get('server', 'password')));

        self.connTimer = QtCore.QTimer();
        self.connTimer.setInterval(5000);
        self.connTimer.timeout.connect(self.sftpServer.check_connection);

        self.fileSysModel = QtWidgets.QFileSystemModel();
        self.fileSysModel.setRootPath(os.getcwd());

        self.gui.treeView.setModel(self.fileSysModel);
        self.gui.treeView.setRootIndex(self.fileSysModel.index(os.getcwd()));
        self.gui.treeView.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents);

        self.gui.pushButton.clicked.connect(self.selectFirmware);
        self.gui.update.clicked.connect(self.updateController);
        self.gui.treeView.clicked.connect(self.onClicked)
        self.gui.update.clicked.connect(self.flashController);
        self.currentFile = "";
        self.gui.getinfo.clicked.connect(self.getCurrenInfo);
        
        #self.pymd5sum = '';

    def getCurrenInfo(self):
        self.gui.curreninfo.append("HELLO");
        #self.sftpServer.executeCommand(r"sed -i s/\r//g %s"%(((config.get('server','scriptLocation')) + (config.get('server','scriptName')))))
        #(stdin, stdout, stderr) = self.sftpServer.executeCommand("cat /etc/os-release")
        stdin, stdout, stderr = self.sftpServer.executeCommand(r"cd /tmp/epcnc/ && md5sum *")
        for line in iter(stdout.readline, ""):
            print(line, end="")
            self.gui.curreninfo.append(line)
            print('finished.')
        


    def connectController(self):
        print("Connecting Controller");
        self.gui.logs.append("Connecting Controller")
        if(self.sftpServer.connStatus == 0):
            ret = self.sftpServer.setupSftp();
            if(ret == -1):
                print("Connection Failed");
                self.gui.logs.append("Connection Failed")
                # self.connTimer.stop();
            else:
                print(self.sftpServer.connStatus);
                self.connTimer.start();
                self.gui.connect.setText("Connected")
                self.gui.connect.setStyleSheet("background-color : green")
                print("Connection Successful");
                print(self.sftpServer.connStatus);
        else:
            print(self.sftpServer.connStatus);
            self.connTimer.start();
            self.gui.connect.setText("Connected")
            self.gui.connect.setStyleSheet("background-color : green")
            print("Connection Successful");
            print(self.sftpServer.connStatus);

    def DisconnectController(self):
        print("Disconnecting Controller");
        if(self.sftpServer.connStatus == 1):
            ret = self.sftpServer.setupSftp();
            if(ret == 1):
                print(self.sftpServer.connStatus);
                print("Connection Failed");
                self.connTimer.stop();
                print(self.sftpServer.connStatus);
            else:
                print(self.sftpServer.connStatus);
                self.connTimer.stop();
                self.gui.disconnect.setText("Disconnected")
                self.gui.connect.setText("Disconnected")
                self.gui.disconnect.setStyleSheet("background-color : red")
                self.gui.connect.setStyleSheet("background-color : red")
                print("Disconnection Successful");
                # self.scriptCheckTimer.start();
                print(self.sftpServer.connStatus);
                # self.gui.logs();

    def selectFirmware(self):
       if(self.currentFile != ""):
        
        global pymd5sum
        self.gui.infobox.append("Selected file:\n" + self.currentFile)
        self.gui.logs.append("Selected file:\n" + self.currentFile)
        # GENERATING NEW MD5SUM OF SELECTED FILE
        with open(self.currentFile, 'rb') as file_to_check:
                data = file_to_check.read()    
                pymd5sum = hashlib.md5(data).hexdigest()
                self.gui.infobox.append("md5sum:" + pymd5sum)     
                self.gui.logs.append("md5sum:" + pymd5sum)
       
        if pymd5sum == os.path.join((config.get('server', 'firmware_md'))):   
            print("Md5sum successfully verified now you can start flashing process")
            self.gui.infobox.append("Md5sum successfully verified\nNow you can start flashing process")
            self.gui.logs.append("Md5sum successfully verified\nNow you can start flashing process")
        else:
            print("Wrong firmware selected Can't be flashed")  
            self.gui.infobox.append("Wrong firmware selected Can't be flashed")
            self.gui.logs.append("Md5sum successfully verified now you can start flashing process")
            

    def updateController(self):
        if(self.sftpServer.connStatus) and ((pymd5sum) == (os.path.join((config.get('server', 'firmware_md'))))):
            #####TRANSFERING OR If Already Exist OVERWRITING SCRIPT######
            print("Updating..")
            sftpscriptfullname = ((config.get('server', 'scriptLocation')) + (config.get('server', 'scriptName')))
            print(sftpscriptfullname)

            localscriptname = (os.path.join(os.getcwd(), (config.get('server', 'scriptName'))))
            print(localscriptname)

            self.sftpServer.sendFile(localscriptname, sftpscriptfullname)
            #self.sftpServer.sendFile((os.path.join(os.getcwd(), (config.get('server', 'scriptName')))),((config.get('server','scriptLocation')) + (config.get('server','scriptName'))))
            
            print("Script Updated")
            self.gui.logs.append("Script Updated")

            # ################## DOS TO UNIX CONVERSION PART ################
            self.sftpServer.executeCommand(r"sed -i s/\r//g %s"%(((config.get('server','scriptLocation')) + (config.get('server','scriptName')))))
            # dostounix = (r"sed -i s/\r//g %s"%(ServerScriptLocation))
            # (stdin, stdout, stderr) = self.sftpServer.executeCommand(dostounix)
            print("dostounix completyed");
            self.gui.logs.append("dostounix conversation completed")
            # print(self.currentFile)
            
            self.sftpServer.sendFile((self.currentFile),(config.get('server','temp')+((self.currentFile).split('/')[-1])))
            #print((self.currentFile).split('/')[-1])
            #(stdin, stdout, stderr) = self.sftpServer.executeCommand("md5sum" + (self.currentFile) +" | awk '{print $1}'");
            #stdout.readlines();
            
            #print(os.path.join(os.getcwd(),(config.get('server','temp'))))
            #sending firmware
            #(stdin, stdout, stderr) = self.sftpServer.sendFile((self.currentFile),(os.path.join((config.get('server', 'temp')),os.path.basename(self.currentFile)).replace("\\","/")))
            #
            #self.sftpServer.executeCommand("md5sum /tmp/update.zip | awk '{print $1}'");
            # fname = self.currentFile.name
            #FirmwareName = ((config.get('server', 'temp')) + (self.currentFile))
            #print(FirmwareName)
            # (stdin, stdout, stderr) = self.sftpServer.executeCommand("md5sum %s"%(config.get('server','temp') + (self.currentFile)))
            # stdout.readlines();
            # print(stdout)
            # if(self.currentFile != ""):
            #     print("Controller updating started");
            #     self.gui.logs.append("Controller updating started")

                                
                # self.gui.infobox.append("Selected File:")     
                # self.gui.infobox.append(SelectedFirmware.rstrip())        
                
                # firm_md = os.path.join((config.get('server', 'firmware_md')))
                # print(firm_md)
                # print(firm_md)
                # ###### GENERATING NEW MD5SUM OF SELECTED FILE######
                # with open(SelectedFirmware, 'rb') as file_to_check:
                #     data = file_to_check.read()    
                #     md5_returned = hashlib.md5(data).hexdigest()
                    
                #     self.gui.infobox.append("md5sum:")     
                #     self.gui.infobox.append(md5_returned)
                #     original_md5 = (md5_returned);

                      
                # #if (controller_md5sum == md5_returned and md5_returned == firm_md):
                # if (original_md5 == firm_md):
                #     print("MD5 verified. TRANSFERING FIRMWARE TO CONTROLLER")
                        
                #     ############ FIRMWARE TRANSFER##############
                #     self.sftpServer.sendFile(SelectedFirmware, destFile);
                        
                #     #######GENERATING MD5SUM ON CONTROLLER##########
                #     (stdin, stdout, stderr) = self.sftpServer.executeCommand("md5sum /tmp/update.zip | awk '{print $1}'");
                
                #     stdOutData = stdout.readlines();
                #     controller_md5sum = ', '.join(str(item) for item in stdOutData).rstrip()
                
                #     if (original_md5 == controller_md5sum):
                #         print("MD5 verified.")
                #         self.gui.infobox.append("MD5 verified.")  
                #     else:
                #         print("MD5 verification failed! controller.")
                # else:
                #     print("MD5 verification failed! Here.")
        else:
            print("Connection Lost")    

    def flashController(self):
       ################## EXECUTING SHELL SCRIPT #####################
                    print("making backups...")
                    self.gui.logs.append("backup process started...")
                    #backlocation = (config.get('server', 'backuplocation') + str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")) + ".tgz")
                    scriptfullname = ((config.get('server', 'scriptLocation')) + (config.get('server', 'scriptName')))
                    print(scriptfullname)

                    fpwd = (config.get('server','fpwd'))
                    print(fpwd)

                    exe_unzip = (config.get('server','exe_unzip'))
                    print(exe_unzip)

                    exe_zip = (config.get('server','exe_zip'))
                    print(exe_zip)

                    backuplocation = (config.get('server','backuplocation'))
                    print(backuplocation)

                    ropath = (config.get('server', 'ro_dir'))
                    print(ropath)

                    Target_Firmware = (config.get('server','temp')+((self.currentFile).split('/')[-1]))
                    print(Target_Firmware)

                    temp = (config.get('server', 'temp'))
                    print(temp)

                    unzip_folder = (config.get('server', 'unzip_folder'))
                    print(unzip_folder)

                    (stdin, stdout, stderr) = self.sftpServer.executeCommand("sh %s %s %s %s %s %s %s %s %s"%(scriptfullname, fpwd, ropath, exe_unzip, exe_zip, backuplocation, Target_Firmware, temp, unzip_folder))
                    # stdout.readlines();
                    # print(stdout)

                    #(stdin, stdout, stderr) = self.sftpServer.executeCommand("sh %s %s %s"%((config.get('server', 'scriptFile')),"epcnc@223", "/root/bin/"))
                    #stdin, stdout, stderr) = self.sftpServer.executeCommand("sh %s %s %s %s %s"%((config.get('server','scriptLocation')) + (config.get('server','scriptName'))), (config.get('server','fpwd')), (config.get('server','exe_unzip')), (config.get('server','exe_zip')), (config.get('server','backuplocation')));
                    # stdout.readlines();
                    # print(stdout)
                    #(stdin, stdout, stderr) = self.sftpServer.executeCommand("sh %s  %s %s %s %s %s"%(((config.get('server', 'scriptLocation')) + (config.get('server', 'scriptName'))),(config.get('server', 'fpwd')), (config.get('server', 'ro_dir')), (config.get('server', 'exe_unzip')), (config.get('server', 'exe_zip')), (config.get('server', 'backuplocation'))));
                    
                    #(stdin, stdout, stderr) = self.sftpServer.executeCommand("sh %s %s %s %s %s %s"%((config.get('server', 'scriptLocation')),"epcnc@223", (config.get('server', 'scriptArgs')), (config.get('server', 'exe_unzip')), (config.get('server', 'exe_zip')), (backlocation)))
                    # binpath = self.sftpServer.executeCommand("sh %s %s %s"%((config.get('server', 'scriptLocation')),"epcnc@223", ('server', 'scriptArgs')))
                    # print(binpath)
                    # out = stdout.readlines();
                    # # print(out)
                    # self.gui.logs.append(str(out))
                    print("Flashing Controller");
        

    def onClicked(self,index):
        path = self.fileSysModel.filePath(index)
        if(os.path.isdir(path)):
            self.fileSysModel.setRootPath(path);
            self.gui.treeView.setModel(self.fileSysModel);
            self.gui.treeView.setRootIndex(self.fileSysModel.index(path));
        else:
            # do nothing
            self.currentFile = path;
            pass

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	Widget = QtWidgets.QWidget()
	rollGui = updator(Widget);
	Widget.show()
	sys.exit(app.exec_())
