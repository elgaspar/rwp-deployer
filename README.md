# RWP Deployer

A tool that downloads latest code of some wordpress plugins from a GitHub repository and uploads them to a WordPress server.

## Features
* One or more plugins can be deployed at a time.
* Can be used for public or private repositories.
* Option to only download the repository ZIP archives (and not deploy them).
* Option to keep locally the downloaded ZIP archives after deploying.

## How it works
1. Connects to your GitHub account using a personal access token.
2. After you specify some of your repositories, it downloads the latest code from master branch of them as ZIP archives.
3. Converts each of the downloaded archives:
    * Removes the suffix *'-master'* from the repository name of the directory
    * Removes the excluded files specified in config file. (See next section [Config File](##Config-File))
4. Uploads the ZIP archives to the specified WordPress server and installs the plugins. It uses an SFTP account for uploading files and an SSH account to install the plugins through [WP-CLI](https://github.com/wp-cli/wp-cli) interface.

## Config File
Create a file rwp-deployer.config inside the rwp-deployer directory and copy paste the following text:
```
[settings]
github_token=TODO 
tmp_dir=TODO
excluded_filenames=["TODO", "TODO"]

[remote]
url=TODO
ssh_username=TODO
ssh_password=TODO
ssh_plugin_dir=TODO
sftp_username=TODO
sftp_password=TODO
sftp_plugin_dir=TODO
```
Replace *TODO* with your options.
* **github_token**: Your GitHub personal access token. See [Creating a personal access token for the command line](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
* **tmp_dir**: The directory where the temporary files will be stored. If you use *download-only* or *keep-files* arguments, the ZIP archives will be saved in this directory.
* **excluded_filenames**: Filenames to exclude from the final ZIP archive that will be deployed. You can use as many as you want. Example: `["TODO", ".gitignore", 'foo.txt']`
* **url**: URL of the remote WordPress server.
* **ssh_username**, **ssh_password**: SSH credentials for the remote server. Used for installing the plugins.
* **ssh_plugin_dir**: Directory of the plugin directory in remote server used for the SSH connection.
* **sftp_username**, **sftp_password**: SFTP credentials for the remote server. Used for uploading ZIP archives and removing them after plugins are installed.
* **ssh_plugin_dir**, **sftp_plugin_dir**: Directory of the plugin directory in remote server used for the SSH and SFTP connection. Quite useful when, for example, SFTP account has access only to plugins directory and not entire WordPress directory. Examples: 
`./site/public_html/wp-content/plugins/` or `./plugins/`

## Usage
```
usage: rwp-deployer.py [-h] [-d] [-k] repo [repo ...]

Downloads latest code of a wordpress plugin from a GitHub repository, uploads it and install it in a WordPress server.

positional arguments:
  repo        repository name

optional arguments:
  -h, --help  show this help message and exit
  -d          download only and not deploy (default: false)
  -k          keep the local files after deploying (default: false)
```

## Requirements
See *requirements.txt* file.
Also, WP-CLI has to be installed in the remote server.

## Credits
Author: Gasparis Elias (GitHub account [elgaspar](https://github.com/elgaspar))

## License
**RWP Deployer** is licensed under the terms of the MIT License (See *LICENSE* file).


