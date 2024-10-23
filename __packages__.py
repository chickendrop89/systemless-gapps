# Sourced from the official NikGApps project (GPLv3)
# https://github.com/nikgapps/project/blob/main/NikGapps/build/PackageConstants.py
def getPackageReplacement(package_name: str):
    """Throws a list of directories to replace if there is a conflicting GApp"""

    package_replacement = {
        "com.google.android.gms": ["PrebuiltGmsCoreQt", "PrebuiltGmsCoreRvc", "GmsCore"],
        "com.google.android.dialer": ["Dialer"],
        "com.google.android.contacts": ["Contacts"],
        "com.google.android.tts": ["PicoTts"],
        "com.google.android.inputmethod.latin": ["LatinIME"],
        "com.google.android.calendar": ["Calendar", "Etar", "SimpleCalendar"],
        "com.google.android.apps.messaging": ["RevengeMessages", "messaging", "Messaging", "QKSMS", "Mms"],
        "com.google.android.apps.photos": ["Gallery", "SimpleGallery", "Gallery2", "MotGallery", "MediaShortcuts",
                                           "SimpleGallery", "FineOSGallery", "GalleryX", "MiuiGallery",
                                           "SnapdragonGallery", "DotGallery", "Glimpse"],
        "com.google.android.keep": ["Notepad"],
        "com.google.android.apps.recorder": ["Recorder", "QtiSoundRecorder"],
        "com.google.android.gm": ["Email", "PrebuiltEmailGoogle"],
        "com.google.android.apps.wallpaper": ["Wallpapers", "ThemePicker"],
        "com.android.chrome": ["Bolt", "Browser", "Browser2", "BrowserIntl", "BrowserProviderProxy", "Chromium",
                               "DuckDuckGo", "Fluxion", "Gello", "Jelly", "PA_Browser", "PABrowser", "YuBrowser",
                               "BLUOpera", "BLUOperaPreinstall", "ViaBrowser", "Duckduckgo"],
        "com.google.android.youtube.music": ["SnapdragonMusic", "GooglePlayMusic", "Eleven", "CrDroidMusic"],
        "com.google.android.setupwizard": ["Provision", "SetupWizard", "LineageSetupWizard"],
        "com.google.android.pixel.setupwizard": ["Provision", "SetupWizard", "LineageSetupWizard"],
        "com.google.android.calculator": ["ExactCalculator", "MotoCalculator", "RevengeOSCalculator"],
        "com.google.android.apps.maps": ["Maps"],
        "com.google.android.apps.turbo": ["TurboPrebuilt"],
        "com.google.android.soundpicker": ["SoundPicker"],
        "com.google.android.storagemanager": ["StorageManager"],
        "com.google.android.documentsui": ["DocumentsUI"],
        "com.google.android.webview": ["webview"],
        "com.google.android.apps.restore": ["Seedvault"],
        "com.google.android.deskclock": ["DeskClock"],
        "org.lineageos.snap": ["GoogleCameraGo", "ScreenRecorder"],
        "com.google.android.as": ["DevicePersonalizationPrebuiltPixel4"],
        "com.google.android.apps.nexuslauncher": ["TrebuchetQuickStep", "Launcher3QuickStep", "ArrowLauncher",
                                                  "Lawnchair"],
        "com.android.systemui.plugin.globalactions.wallet": ["QuickAccessWallet"],
        "com.google.android.apps.youtube.music": ["SnapdragonMusic", "GooglePlayMusic", "Eleven", "CrDroidMusic"],
        "com.mixplorer.silver": ["MixPlorer"],
        "app.lawnchair": ["Lawnchair"]
    }

    return package_replacement.get(package_name, [])
