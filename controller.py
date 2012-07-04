import paramiko
import os

class config(object):
    hostname = "localhost"
    port = 22
    
    username = "pdani"
    privatekey = "~/.ssh/id_rsa"
    #password = "testpass"
    
    worker_script_local ="./worker.py"
    worker_script_remote = "/home/pdani/TmpPool/testdir/worker.py"
    python_remote = "/usr/bin/python"


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if hasattr(config, 'privatekey'):
        privatekeyfile = os.path.expanduser(config.privatekey)
        privatekey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
        kwargs = {'pkey': privatekey}
    elif hasattr(config, 'password'):
        kwargs = {'password': config.password}
    
    ssh.connect(config.hostname, config.port, config.username, **kwargs)
    sftp = ssh.open_sftp()
    
    sftp.put(config.worker_script_local, config.worker_script_remote)
    
    _, stdout, _ = ssh.exec_command("%s %s" % (config.python_remote, config.worker_script_remote))
    
    for line in stdout:
        print "Here you can do anything with the file path: %s" % line.strip()
    
    ssh.close()

if __name__ == "__main__":
    main()