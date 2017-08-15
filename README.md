# Hurry!

**Hurry!** helps you run your routine commands and scripts faster. It transforms commands like 
```docker-compose -f docker-compose.dev.yml up --build -d``` into ```hurry up```.

Current version works with Python 3+ only.

## Install 
```pip install hurry-script```

## Usage
In the folder, where you want to use **Hurry!**, create *hurry.json* file with shortcuts:
```json
~/my_project/hurry.json

{
  "up": "docker-compose -f docker-compose.dev.yml up --build -d",
  "hello": "python -c \"print('Hello, World!')\"",
  "down": "docker-compose -f docker-compose.dev.yml down"
}
```

Now you can use created shortcuts: 
```
~/my_project$ hurry --help
Usage:
    hurry up
    hurry hello
    hurry down
/my_project$ hurry hello
Execute: python -c "print('Hello, World!')"
Hello, World!
/my_project$
```

**Hurry!** supports simple templating inside shortcuts:
```json
~/my_project/hurry.json

{
  "hello": "python -c \"print('Hello, World!')\"",
  "hello <name>": "python -c \"print('Hello, <name>!')\""
}
```

```
~/my_project$ hurry --help
Usage:
    hurry hello
    hurry hello <name>
~/my_project$ hurry hello
Execute: python -c "print('Hello, World!')"
Hello, World!
~/my_project$ hurry hello "My Lord"
Execute: python -c "print('Hello, My Lord!')"
Hello, My Lord!
~/my_project$ 
```
