# urlfinder

urlfinder is an enumeration tool that allows finding recursively all the URLs starting from a base one taken as input, also jumping between different domains.

URLs are taken from:
+ `href attribute` from `<a>` tags
+ `action attribute` from `<form>` tags

urlfinder retrieves:
+ URL endpoints
+ email addresses
+ phone numbers

Once an URL is found, query parameters (if any) are substituted with keywords `FUZZ0`, `FUZZ1`, etc. This allows for easy replacement by injecting payloads using a fuzzing tool.

urlfinder produces five files:
+ `url-complete-list.txt`: stores the list of all the original URLs found
+ `fuzzable-urls.txt`: stores the list of URLs containing `FUZZX` keywords
+ `mails.txt`: stores the list of email addresses
+ `phones.txt`: stores the list of phone numbers
+ `site-map.log`: stores the site map. It can be used to reconstruct the path to get a specific URL

The tool can retrieve only URLs coming from the same domain as the URL passed as argument or retrieve the entire set of URLs based on domains in scope

**WARNING**: based on the target or scope, the execution of the tool could be endless (for example scanning a social media) 

## Setup environment

### Create environment

```bash
python -m venv env
```

### Activate environment

#### PowerShell

```bash
.\env\Scripts\activate
```

#### Bash

```bash
source env/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Setup project

```bash
pip install -e .
```

## Help

```bash
python urlfinder --help                         

Usage: urlfinder [OPTIONS]

Options:
  -u, --url TEXT       URL  [required]
  -d, --domains TEXT   List of comma separated scope domains
  -cs, --check-status  Get only URLs with status code between 200 and 400
                       [default: False]
  --help               Show this message and exit.
```

## Execute tool

### Execution without scope domains

```bash
python urlfinder -u <BASE-URL>
```

### Execution with scope domains (separated with comma)

```bash
python urlfinder -u <BASE-URL> -d <SUBDOMAIN-1>.<DOMAIN-1>,<DOMAIN-2>,*.<DOMAIN-3>
```

### Execution getting only URLs coming from a non-error HTTP response code

```bash
python urlfinder -u <BASE-URL> -d <SUBDOMAIN-1>.<DOMAIN-1>,<DOMAIN-2>,*.<DOMAIN-3> -cs
```

## Improvements

+ Retrieve URLs inside `<script>` tags
+ Retrieve endpoints inside an URL, e.g. https://jkljkl.jkl/test/?continue=https://jkljkl.jkl/test-2/?id=111
+ Generate and parse URLs coming from `<form>` tags with GET `action` and inputs as query parameters
+ Add a proxy to allow the user to interact with the page catching possible missing URLs
+ Add an option to make path fuzzable
+ Add an option to make fragment fuzzable
+ Use wordlist to enumerate directories and find other fuzzable endpoints
+ Create different URLs coming from a single one containing also original values. From `?id=5&action=create&token=111`:
  + ?id=5&action=create&token=FUZZ0
  + ?id=5&action=FUZZ0&token=111
  + ?id=FUZZ0&action=create&token=111
  + ?id=5&action=FUZZ0&token=FUZZ1
  + ?id=FUZZ0&action=create&token=FUZZ1
  + ?id=FUZZ0&action=FUZZ1&token=111
  + ?id=FUZZ0&action=FUZZ1&token=FUZZ2

## Disclaimer

This tool is only for testing and academic purposes and can only be used where strict consent has been given. Do not use it for illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this tool and software in general.
