![System-less GApps](.github/logo.png "System-less GApps")

 - A script that converts a **NikGApps** package into a **Magisk/KSU Module**.
 - ~~Periodical Updates at [SourceForge](https://sourceforge.net/projects/systemless-gapps/)~~

## ~~Automated Builds~~
 - I will not be publishing a release until the bugs listed in **[KNOWN-BUGS.MD](https://github.com/chickendrop89/systemless-gapps/blob/master/KNOWN-BUGS.MD)** will be fixed

## Usage
 - [Download NikGApps Package](https://nikgapps.com/downloads)
 - [Download Python3+ and pip](https://www.python.org/downloads/)

 * Install requirements using pip:
 ```shell
 $ pip install -r requirements.txt
 ```

 -----

 ```
  usage: main.py [-h] -i INPUT -o OUTPUT_DIR [-dr] [-fw]

   ___ _ _  ___ _|⎻|_ ___ ._ _ _ |⎻| ___  ___ ___ ___  ___  ___  ___  ___  ___
  <_-<| | |<_-<  | | / ._>| ' ' || |/ ._><_-<<_-<|___|/ . |<_> || . \| . \<_-<
  /__/`_. |/__/  |_| \___.|_|_|_||_|\___./__//__/     \_. |<___||  _/|  _//__/
      <___'                                           <___'     |_|  |_|          

  required arguments:
    -i INPUT, --input INPUT   
                          Input NikGApps package archive (Zip format)
    -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                          Output directory for the final archive

  optional arguments:
    -dr, --dont-replace-aosp-apps
                          Don't replace conflicting AOSP apps with the Module
    -dt, --dont-trigger-setup-wizard
                          Don't trigger setup wizard after reboot
    -fw, --force-setup-wizard
                          Force setup wizard (don't check for installation)

  example: main.py -i package.zip -o out
 ```

## Notice
 - Please disable `playintegrityfix` or similar modules affecting GMS before installing, [they can sometimes cause unexpected issues such as this](https://github.com/chickendrop89/systemless-gapps/issues/1).
They can be installed again after the setup is complete.

## Android Requirements
 - Android 14+
 - 64-bit Architecture
 - Bash ([If not included in your ROM, download this](https://github.com/Magisk-Modules-Alt-Repo/mkshrc))
 - Either `Magisk 27.0+` or `KernelSU v0.9.4+`

## ROM Compatibility:
 - Confirmed to work on most AOSP ROMs
 - Most likely won't work on MIUI 

## Host Requirements
 - Python 3.8+

## Credits
 * [wacko1805](https://github.com/wacko1805) for [original MagiskGApps](https://github.com/wacko1805/MagiskGapps)
