# Config Manager

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
python script.py --host hostname --username username --keyfile /path/to/keyfile --playbook /path/to/playbook.yml
```

Replace 'hostname', 'username', '/path/to/keyfile', and '/path/to/playbook.yml' with your actual values.

The playbook should be in YAML format and look something like this (a sample_playbook.yml file is provided):

```
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

Note: for idempotency to work in the command module you will have to set up a flag like it is shown in the sample tasks.
