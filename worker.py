import paramiko
import os

class config(object):
    hostname = "localhost"
    port = 22
    
    username = "pdani"
    privatekey = "~/.ssh/id_rsa"
    #password = "testpass"
    
    directory = "/home/pdani/TmpPool/testdir/innen"
    save_path = "/home/pdani/TmpPool/testdir/ide"

    
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
    
    for subdir, dirs, files in os.walk(config.directory):
        for dirent in dirs:
            sftp.mkdir(os.path.join(config.save_path, dirent))
        for fil in files:
            sftp.put(os.path.join(subdir, fil), os.path.join(config.save_path, os.path.relpath(subdir, start=config.directory), fil))
            print os.path.join(config.save_path, os.path.relpath(subdir, start=config.directory), fil)
    
    ssh.close()

if __name__ == "__main__":
    main()