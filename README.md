# Config Manager

[![asciicast](https://asciinema.org/a/0lo5rluSyW4OHjNNm7lksI3qe.png)](https://asciinema.org/a/0lo5rluSyW4OHjNNm7lksI3qe)

Click here to view the script in action: https://asciinema.org/a/c5SXBdevJvcAaJOuWseQ5I8rr

## Prerequisites

You need Python 3 and pip installed on your machine. The script also requires the `paramiko` and `pyyaml` Python packages.

## Installation

1. Clone this repository to your local machine.
2. Install the required Python packages using pip:

```bash
pip install paramiko pyyaml argparse
```

## Usage

You can run the script with command-line arguments like this:

```bash
python cm.py --host hostname --username username --keyfile /path/to/keyfile --playbook /path/to/playbook.yml
```

Replace 'hostname', 'username', '/path/to/keyfile', and '/path/to/playbook.yml' with your actual values.

The playbook should be in YAML format and look something like this (a sample_playbook.yml file is provided):

```yaml
  tasks:
    - name: Install package
        action:
        module: package
        name: vim
        state: install
    - name: Run command
        action:
        module: command
        command: echo "Hello, World!"
```

Notes: 

- for idempotency to work in the command module you will have to set up a flag like it is shown in the sample tasks.
- the command module allows the use of sudo:

```yaml
tasks:
  - name: Run whoami
    action:
      module: command
      command: whoami && touch /tmp/testwho.txt
      check_command: test -f /tmp/testwho.txt && echo "File exists"
      check_expected_output: "File exists"
      sudo: true
```

## Modules

### command Module
The command module takes the command you want to run on the remote machine.

Parameters:

- command: The command you want to run.
- sudo (optional): Whether to run the command with sudo. Default is false.
- check_command (optional): A command to check the current state before running the main command.
- check_expected_output (optional): The expected output of the check command. If the output of the check command matches this value, the main command will not be run.

Example:

```yaml
  - name: Run command with idempotency
    action:
      module: command
      command: echo "Hello, World!"
      check_command: test -f /tmp/test.txt && echo "File exists"
      check_expected_output: "File exists"
```

### package Module
The package module manages packages on the remote machine.

Parameters:

- name: The name of the package.
- state: The desired state of the package. Can be install or remove.

Example:

```yaml
  - name: Install package
    action:
      module: package
      name: vim
      state: install
```

### file Module
The file module manages files on the remote machine.

Parameters:

- path: The path to the file on the remote machine.
- state: The desired state of the file. Can be create, upload, or delete.
- local_path (optional): The local path to the file to be uploaded. Required if state is upload.

Example:

```yaml
  - name: Create file
    action:
      module: file
      path: /tmp/test.txt
      state: create
      local_path: test.txt
```

### directory Module
The directory module manages directories on the remote machine.

Parameters:

- path: The path to the directory on the remote machine.
- state: The desired state of the directory. Can be create or delete.

Example:

```yaml
  - name: Create directory
    action:
      module: directory
      path: /tmp/temp2dir
      state: create
```

### service Module
The service module manages services on the remote machine.

Parameters:

- name: The name of the service.
- state: The desired state of the service. Can be start, stop, restart, or reload.

Example:

```yaml
tasks:
  - name: Start service
    action:
      module: service
      name: httpd
      state: start
```

### update Module
The update module updates the system.

Example:

```yaml
tasks:
  - name: Update system
    action:
      module: update
```

