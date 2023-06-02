import paramiko


class SftpComm():
    def __init__(self, parent=None, ipAddress='localhost', portNo=22, userName=None, password=None):
        self.ssh = None
        self.sftp = None
        self.ipAddr = ipAddress
        self.portNo = portNo
        self.username = userName
        self.password = password
        # self.setupSftp()
        self.connStatus = 0;

    def setupSftp(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect((self.ipAddr), port=(self.portNo), username=(self.username), password=(self.password), timeout=1)
            if self.ssh != None:
                self.sftp = self.ssh.open_sftp()
                self.connStatus = 1;
        except Exception as e:
            print(e)
            try:
                print(-1)
                self.connStatus = 0;
                return -1
            finally:
                e = None
                del e

    def sendFile(self,src,dest):
        try:
            if self.sftp != None:
                self.sftp.put(src, dest)
        except Exception as e:
            print(e);
            try:
                print(-2)
            finally:
                e = None
                del e

    def executeCommand(self,cmd):
        try:
            (stdin, stdout, stderr) = self.ssh.exec_command(cmd);
            # print("Connected");
            return (stdin, stdout, stderr);
        except Exception as e:
            # print("Connection lost : %s" %e)
            print(e);
            return -1;

    def check_connection(self):
        try:
            self.ssh.exec_command('ls', timeout=5)
            # print("Connected");
            self.connStatus = 1;
        except Exception as e:
            # print("Connection lost : %s" %e)
            self.connStatus = 0;