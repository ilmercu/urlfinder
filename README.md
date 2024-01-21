# urlfinder

urlfinder is an enumeration tool which allows to find recursively all the URLs starting from a base one. URLs are taken from:
+ href attribute from `<a>` tags
+ action attribute from `<form>` tags

The tool can retrieve only URLs coming from the same domain of the base URL or retrieve the entire set of URLs in a page considering infinite domains

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
+ Retrieve and save mails coming from <a> tags
+ Retrieve URLs inside <script> tags

## Disclaimer

This tool is only for testing and academic purposes and can only be used where strict consent has been given. Do not use it for illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this tool and software in general.
