Rather than managing GitHub issue labels with the web interface, use
this script to do so from the command line. This script makes it
easier to delete default labels and add new ones from a standard
list. It's especially useful for organizations or users who want
consistent issue labels across a large number of repositories.

## Requirements

* Python 3  
* Python modules: `json`, `argparse`, and `requests`  
* [GitHub authorization
  token](https://help.github.com/articles/authorizing-a-personal-access-token-for-use-with-a-saml-single-sign-on-organization/)  

## Set up

### Get and store authorization token in file

If you don't have one already, set up an authorization token with
appropriate permissions [using these
instructions](https://help.github.com/articles/authorizing-a-personal-access-token-for-use-with-a-saml-single-sign-on-organization/). Once
created, save your token in a file on your computer. For example, you
might create `~/.gh_token` in your home directory that simply
contains:

```
<token string>
```

### Label files

New labels should be stored in a JSON file. For example:

```json
[
  {
	"name": "Priority: Critical",
	"description": "",
	"color": "e11d21"
  },
  {
	"name": "Priority: High",
	"description": "",
	"color": "eb6420"
  },
  {
	"name": "Priority: Medium",
	"description": "",
	"color": "fbca04"
  },
  {
	"name": "Priority: Low",
	"description": "",
	"color": "009800"
  }
]

```

## Usage

Use the `-h` or `--help` flags to see the scripts arguments:

```bash
[~] $ ./manage_repo_labels.py -h

usage: manage_repo_labels.py [-h] -i ID -t TOKEN -r REPO [-o ORG] [-l LABELS]
                             [-c] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -i ID, --id ID        GitHub ID
  -t TOKEN, --token TOKEN
                        GitHub authorization token in file
  -r REPO, --repo REPO  Repository name
  -o ORG, --org ORG     Organization name
  -l LABELS, --labels LABELS
                        Labels in JSON file
  -c, --check_existing  Flag to check existing labels
  -d, --drop_existing   Flag to drop existing labels
```

Users must supply their GitHub ID, path to authorization token file,
and the repository name. If the repository is owned by an
organization, then the the organization name must be included. The
script assumes the repository is owned by the user otherwise.
