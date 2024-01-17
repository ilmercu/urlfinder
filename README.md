# urlfinder

urlfinder is tool which allows to find recursively all the URLs starting from a base URL. URLs are taken from `<a>` tags or `<form>` action attributes.

The tool can retrieve only links coming from same domain or retrieve all the URLs in a page

## How To Execute

### Setup environment

```bash
python -m venv env
```

### Activate environment

```bash
./env/Scripts/activate
```

### Install dependencies

```bash
pip install -r .requirements.txt
```

### Setup project

```bash
pip install -e .
```

### Execute tool

```bash
python ./urlfinder/main.py -u <BASE-URL>
```

## Improvements

+ Handle protool-relative URL

## Disclaimer

This tool is only for testing and academic purposes and can only be used where strict consent has been given. Do not use it for illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this tool and software in general.
