import argparse
import paramiko
import yaml

class ConfigManager:
    def __init__(self, host, username, key_file):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=host, username=username, key_filename=key_file)
        self.host = host       

    def run_command(self, command, sudo=False, check_command=None, check_expected_output=None):
        if sudo:
            command = 'sudo ' + command
        if check_command and check_expected_output:
            check_output = self.run_command(check_command)
            if check_output.strip() == check_expected_output:                
                return f'Check OK: no need to run command "{command}"'
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            error = stderr.read().decode('utf-8')
            if error:                
                return f"There was an error while running the command: {error}"
            else:                
                return stdout.read().decode('utf-8')
        except Exception as e:            
            return str(e)

    def manage_package(self, name, action):
        if action == 'install':
            if f'package {name} is not installed' not in self.run_command(f'rpm -q {name}'):
                return f'Package {name} is already installed'
            return self.run_command(f'sudo yum install -y {name}')
        elif action == 'remove':
            if 'package is not installed' in self.run_command(f'rpm -q {name}'):
                return f'Package {name} is already removed'
            return self.run_command(f'sudo yum remove -y {name}')

    def manage_file(self, path, action, local_path=None):
        sftp = self.client.open_sftp()
        if action == 'create' or action == 'upload':
            sftp.put(local_path, path)
        elif action == 'delete':
            sftp.remove(path)
        sftp.close()

    def manage_service(self, name, action):
        return self.run_command(f'sudo systemctl {action} {name}')

    def update(self):
        return self.run_command('sudo yum update -y')

    def manage_directory(self, path, action):
        if action == 'create':
            return self.run_command(f'mkdir -p {path}')
        elif action == 'delete':
            return self.run_command(f'rm -r {path}')

    def load_playbook(self, playbook_path):
        with open(playbook_path, 'r') as file:
            playbook = yaml.safe_load(file)
        for task in playbook['tasks']:
            print(f"TASK [{task['name']}] - {self.host}")
            sudo = task['action'].get('sudo', False)
            if task['action']['module'] == 'command':
                output = self.run_command(task['action']['command'], sudo, task['action'].get('check_command'), task['action'].get('check_expected_output'))
            elif task['action']['module'] == 'package':
                output = self.manage_package(task['action']['name'], task['action']['state'])
            elif task['action']['module'] == 'file':
                output = self.manage_file(task['action']['path'], task['action']['state'], task['action'].get('local_path'))
            elif task['action']['module'] == 'service':
                output = self.manage_service(task['action']['name'], task['action']['state'])
            elif task['action']['module'] == 'update':
                output = self.update()
            elif task['action']['module'] == 'directory':
                output = self.manage_directory(task['action']['path'], task['action']['state'])
            print(f"{output}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple Ansible-like tool.')
    parser.add_argument('--host', required=True, help='Hostname of the target machine.')
    parser.add_argument('--username', required=True, help='Username for the SSH connection.')
    parser.add_argument('--keyfile', required=True, help='Path to the SSH key file.')
    parser.add_argument('--playbook', required=True, help='Path to the playbook file.')
    args = parser.parse_args()

    config_manager = ConfigManager(args.host, args.username, args.keyfile)
    config_manager.load_playbook(args.playbook)

