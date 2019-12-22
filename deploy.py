import paramiko
import os.path

from utilities import error


class PluginDeployer:
    def __init__(self, remote_connect_details):
        self.ssh = SshClient(
            remote_connect_details['url'],
            remote_connect_details['ssh_username'],
            remote_connect_details['ssh_password'],
            remote_connect_details['ssh_plugin_dir']
        )

        self.sftp = SftpClient(
            remote_connect_details['url'],
            remote_connect_details['sftp_username'],
            remote_connect_details['sftp_password'],
            remote_connect_details['sftp_plugin_dir']
        )

    def deploy(self, filepaths):
        self.sftp.connect()
        self.ssh.connect()

        self.sftp.transfer(filepaths)
        self.ssh.install(filepaths)
        self.sftp.remove_transfered_files()

        self.sftp.destroy()
        self.ssh.destroy()


class SftpClient:
    def __init__(self, url, username, password, remote_dir):
        self.url = url
        self.username = username
        self.password = password
        self.remote_dir = remote_dir
        self.transfered = []

    def connect(self):
        try:
            self.connection = paramiko.SSHClient()
            self.connection.load_system_host_keys()
            self.connection.connect(
                self.url,
                username=self.username,
                password=self.password
            )
            self.client = self.connection.open_sftp()
        except:
            error("SFTP client couldn't connect.")

    def destroy(self):
        if self.client:
            self.client.close()
        if self.connection:
            self.connection.close()

    def transfer(self, filepaths):
        print("Transfering...")
        for repo_name, local_filepath in filepaths.items():
            # print("Transfering " + repo_name + "...")
            try:
                remote_filepath = self.remote_dir + '/' + \
                    os.path.basename(local_filepath)
                self.client.put(local_filepath, remote_filepath)
                self.transfered.append(remote_filepath)
            except Exception:
                self.destroy()

    def remove_transfered_files(self):
        for remote_filepath in self.transfered:
            try:
                self.client.remove(remote_filepath)
            except Exception:
                error("Couldn't remove zip file.")
                self.destroy()


class SshClient:
    def __init__(self, url, username, password, remote_dir):
        self.url = url
        self.username = username
        self.password = password
        self.remote_dir = remote_dir

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.connect(
                self.url,
                username=self.username,
                password=self.password
            )
        except:
            error("SSH client couldn't connect.")
            self.destroy()

    def destroy(self):
        if self.client:
            self.client.close()

    def install(self, filepaths):
        print("Installing...")
        plugins_str = ''
        for repo_name, local_filepath in filepaths.items():
            # print("Installing " + repo_name + "...")

            filename = os.path.basename(local_filepath)
            remote_filepath = f"{self.remote_dir}/{filename}"
            plugins_str += ' ' + remote_filepath

        stdin, stdout, stderr = self.client.exec_command(
            f"wp plugin install {plugins_str} --force"
        )
        print(stderr.read().decode())
        print(stdout.read().decode())
