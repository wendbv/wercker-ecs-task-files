# Wercker step for inserting configuration into AWS ECS task files

This tool will insert all ENV variables with the prefix `ECS_` into the environment section of an amazon task file, stripping the `ECS_` prefix. It will also replace any occurance of `$VARIABLE` in a task file with the value of the corresponding ENV variable (if there is one).

## Usage

Put the this in your `wercker.yml`.

```yml
- wendbv/aws-task-files:
  - task-file: 'task-file.json'
```

Given the following ENV variables, for instance set throught the Wercker interface.

```bash
export ECS_SETTING_1='setting 1'
export ECS_SETTING_2='setting 2'
export RELEASE_VERSION='0.1'
```

And the following ECS task file (`task-file.json`).

```json
[
    {
        "volumesFrom": [],
        "memory": 1000,
        "portMappings": [
            {
                "hostPort": 80,
                "containerPort": 80,
                "protocol": "tcp"
            }
        ],
        "essential": true,
        "entryPoint": [
            "./run.py"
        ],
        "mountPoints": [],
        "name": "my-app",
        "environment": [],
        "image": "username/my_app:$RELEASE_VERSION",
        "command": [],
        "cpu": 1000
    }
]
```

The Wercker step will change the `task-file.json` into the following:

```json
[
    {
        "volumesFrom": [],
        "memory": 1000,
        "portMappings": [
            {
                "hostPort": 80,
                "containerPort": 80,
                "protocol": "tcp"
            }
        ],
        "essential": true,
        "entryPoint": [
            "./run.py"
        ],
        "mountPoints": [],
        "name": "my-app",
        "environment": [
            {
                "name": "SETTING_1",
                "value": "setting 1"
            },
           {
                "name": "SETTING_2",
                "value": "setting 2"
            }
        ],
        "image": "username/my_app:0.1",
        "command": [],
        "cpu": 1000
    }
]
```

## Options

- task-file:
    The base task file that should be used to insert settings in (required).
- prefix:
    The prefix that is used to find the variables to insert in to the `environment` section (default `ECS_`).
- json-format:
    If set to `terse`, the JSON will not contain newlines.
- target-file:
    File to write the new JSON content to (default: same as `task-file`).
