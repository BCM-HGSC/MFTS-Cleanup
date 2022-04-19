import paramiko

ssh = paramiko.SSHClient()

ssh.connect('10.70.12.36', port=22, username='sug-login1')


 