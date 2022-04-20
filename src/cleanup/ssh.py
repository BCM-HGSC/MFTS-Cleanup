from logging import Logger
import paramiko

def ssh_run_remote_command(self, cmd):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.host,
                           username=self.config['ssh_user'],
                           password=self.config['ssh_password'])
        stdin, stdout, stderr = ssh_client.exec_command(cmd)

        out = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if self.log_level:
            Logger.info(out)
        if error:
            raise Exception('There was an error pulling the runtime: {}'.format(error))
        ssh_client.close()

        return out 





