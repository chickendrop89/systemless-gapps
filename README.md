![System-less GApps](.github/logo.png "System-less GApps")

 - A script that converts a **NikGApps** package into a **Magisk/KSU Module**.
 - Periodical Updates at [SourceForge](https://sourceforge.net/projects/systemless-gapps/)

## Compatibility:

 - Works on most AOSP based custom roms
 - Works on most AOSP based OEM roms (Motorolla, asus, ..etc)
 - May or may not work on bloated stock roms, like oneui, coloros ..etc
  - **DOES NOT work on MIUI**.

## Why Systemless GApps?

 - Systemless GApps can be disabled or installed temporarily 
 - It can be used to change other GApps packages previously installed, meaning a device with core gapps can be changed to stock without wiping the data partition

## Automated Builds
[![Download Systemless GApps](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/systemless-gapps/files)

## Usage
 - [Download NikGApps Package](https://nikgapps.com/downloads)
 - [Download Python3+ and pip](https://www.python.org/downloads/)

 * Install requirements using pip:
 ```shell
 $ pip install -r requirements.txt
 ```

* Run the script itself:
 ```shell
 $ python main.py <input: nikgapps package> <output directory>
 ```

## Example Usage:
 ```shell
 $ python main.py nikgapps-stock-arm64-13-20231107-signed.zip release/
 ```

## Host Requirements
 - Python 3.8+

## Android Requirements
 - Android 14+
 - 64-bit Architecture
 - Bash ([If not included in your ROM, download this](https://github.com/Magisk-Modules-Alt-Repo/mkshrc))
 - Either `Magisk 27.0+` or `KernelSU v0.9.4+`

## Credits

 * [wacko1805](https://github.com/wacko1805) for [original MagiskGApps](https://github.com/wacko1805/MagiskGapps)
 * [NikGApps](https://nikgapps.com/) by [Nikhil Menghani](https://t.me/inikhilmenghani)
 * [Zackptg5](https://github.com/Zackptg5/) for [MMT-Extended](https://github.com/Zackptg5/MMT-Extended)
