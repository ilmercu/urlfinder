# urlfinder

urlfinder is an enumeration tool which allows to find recursively all the URLs starting from a base one. URLs are taken from:
+ href attribute from `<a>` tags
+ action attribute from `<form>` tags

The tool can retrieve only URLs coming from the same domain of the base URL or retrieve the entire set of URLs based on domains in scope

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

#### Execution without scope domains

```bash
python urlfinder -u <BASE-URL>
```

#### Execution with scope domains (separated with comma)

```bash
python urlfinder -u <BASE-URL> -d <SUBDOMAIN-1>.<DOMAIN-1>,<DOMAIN-2>,*.<DOMAIN-3>
```

## Improvements

+ Retrieve URLs inside <script> tags
+ Add option to encode the URL
+ Add option to check status code from response
  + print the URL and change the color based on the status code

## Disclaimer

This tool is only for testing and academic purposes and can only be used where strict consent has been given. Do not use it for illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this tool and software in general.
