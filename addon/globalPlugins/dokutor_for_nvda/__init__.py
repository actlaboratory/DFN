from __future__ import unicode_literals
import os
import globalPluginHandler
import gui
import wx
import addonHandler
import speechDictHandler
try:
    import _pickle
except:
    import cPickle as _pickle
import tones
import time
import ui
import globalVars
try:
    import buildVersion as _versionInfo
except ImportError:
    import versionInfo as _versionInfo

import config
from logHandler import log
from .constants import *
from . import updater
from .compat import messageBox


try:
    addonHandler.initTranslation()
except BaseException:
    def _(x): return x


confspec = {
    "checkForUpdatesOnStartup": "boolean(default=True)",
    "enableOnStartup": "boolean(default=False)", # 2026.1以下
    "onStartup": "string(default=disable)", # 2026.2以上
}
config.conf.spec["DFN_global"] = confspec


def isCompatibleWith20262():
    return (_versionInfo.version_year == 2026 and _versionInfo.version_major >= 2) or _versionInfo.version_year >= 2027


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("読ター For NVDA")

    def __init__(self, *args, **kwargs):
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        
        if not isCompatibleWith20262():
            # dokutor dic file path
            self.dictPickle = os.path.join(os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "riryou_dict.dat")
            self.dictFile = os.path.join(os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "riryou_dict.dict")
            self.dictFileSource = os.path.join(os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "dokutor_dev.csv")
        
        if globalVars.appArgs.secure:
            return
        # end secure screen
        
        # setup updater
        if self.getUpdateCheckSetting() is True:
            self.autoUpdateChecker = updater.AutoUpdateChecker()
            self.autoUpdateChecker.autoUpdateCheck(mode=updater.AUTO)
        # end update check
        
        self._setupMenu()

        startupConf = self.getEnableOnStartupSetting()
        if startupConf == True or startupConf == "enable":
            if isCompatibleWith20262():
                self.load(True)
            else:
                self.load()
        elif startupConf == False or startupConf == "disable":
            self.clear(True)

    def terminate(self):
        super(GlobalPlugin, self).terminate()
        try:
            gui.mainFrame.sysTrayIcon.menu.Remove(self.rootMenuItem)
        except BaseException:
            pass

    def _setupMenu(self):
        self.rootMenu = wx.Menu()
        
        self.dictStateToggleItem = self.rootMenu.Append(wx.ID_ANY, self.dictStateToggleString(),
            _("理療科用読み辞書の適用状態を切り替えます。")
        )
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.toggleDictState, self.dictStateToggleItem)
        
        self.enableOnStartupToggleMenu = wx.Menu()
        self.StartupEnable = self.enableOnStartupToggleMenu.AppendRadioItem(
            wx.ID_ANY,
            _("有効"),
            _("起動時に常に有効にします。")
        )
        self.StartupDisable = self.enableOnStartupToggleMenu.AppendRadioItem(
            wx.ID_ANY,
            _("無効"),
            _("起動時に常に無効にします。")
        )
        if isCompatibleWith20262():
            self.StartupSame = self.enableOnStartupToggleMenu.AppendRadioItem(
                wx.ID_ANY,
                _("前回と同じ"),
                _("前回の状態を保持して起動します。")
            )
        self.enableOnStartupToggleItem = self.rootMenu.AppendSubMenu(
            self.enableOnStartupToggleMenu,
            _("起動時の理療科用読み辞書の状態"),
            _("起動時の理療科用読み辞書の適用状態を設定します。")
        )
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.toggleEnableOnStartupEnable, self.StartupEnable)
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.toggleEnableOnStartupDisable, self.StartupDisable)
        if isCompatibleWith20262():
            gui.mainFrame.sysTrayIcon.Bind(
                wx.EVT_MENU, self.toggleEnableOnStartupSame, self.StartupSame)
        self.updateCheckToggleItem = self.rootMenu.Append(
            wx.ID_ANY,
            self.updateCheckToggleString(),
            _("起動時にアップデートを確認するかどうかを設定します。")
        )
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.toggleUpdateCheck, self.updateCheckToggleItem)

        self.updateCheckPerformItem = self.rootMenu.Append(
            wx.ID_ANY,
            _("アップデートを確認(&C)"),
            _("直ちにアップデートの確認を行います。")
        )
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.performUpdateCheck, self.updateCheckPerformItem)
        
        self.rootMenuItem = gui.mainFrame.sysTrayIcon.menu.Insert(
            2, wx.ID_ANY, _("読ター For NVDA"), self.rootMenu)

        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU_OPEN, self.onRootMenuOpen)

    def onRootMenuOpen(self, evt):
        try:
            self.updateCheckToggleItem.SetItemLabel(self.updateCheckToggleString())
            self.dictStateToggleItem.SetItemLabel(self.dictStateToggleString())
            startupConf = self.getEnableOnStartupSetting()
            if startupConf == True or startupConf == "enable":
                self.StartupEnable.Check(True)
            elif startupConf == False or startupConf == "disable":
                self.StartupDisable.Check(True)
            else:
                self.StartupSame.Check(True)
        except Exception:
            pass
        evt.Skip()

    def dictStateToggleString(self):
        if isCompatibleWith20262():
            return _("理療科用読み辞書を解除する(&A)") if self._isEnableDictionaryInConfig() else _("理療科用読み辞書を適用する(&A)")
        else:
            return _("理療科用読み辞書を解除する(&A)") if "riryou" in speechDictHandler.dictTypes else _("理療科用読み辞書を適用する(&A)")
    
    def updateCheckToggleString(self):
        return _("起動時のアップデートの確認を無効化") if self.getUpdateCheckSetting() is True else _("起動時のアップデートの確認を有効化")
    

    def toggleEnableOnStartupEnable(self, evt):
        if isCompatibleWith20262():
            self.setEnableOnStartupSetting("enable")
        else:
            self.setEnableOnStartupSetting(True)
        msg = _("NVDA起動時に、自動で理療科用読み辞書を適用します。")
        messageBox(msg, _("設定変更完了"))

    def toggleEnableOnStartupDisable(self, evt):
        if isCompatibleWith20262():
            self.setEnableOnStartupSetting("disable")
        else:
            self.setEnableOnStartupSetting(False)
        msg = _("NVDA起動時は、通常の読み辞書を利用します。")
        messageBox(msg, _("設定変更完了"))

    def toggleEnableOnStartupSame(self, evt):
        self.setEnableOnStartupSetting("same")
        msg = _("NVDA起動時は、前回の設定を適用します。")
        messageBox(msg, _("設定変更完了"))
    
    def toggleUpdateCheck(self, evt):
        changed = not self.getUpdateCheckSetting()
        self.setUpdateCheckSetting(changed)
        msg = _("NVDA起動時に、自動でDFNのアップデートを確認します。") if changed is True else _("NVDA起動時に、DFNのアップデートを確認しません。")
        messageBox(msg, _("設定変更完了"))

    def performUpdateCheck(self, evt):
        updater.AutoUpdateChecker().autoUpdateCheck(mode=updater.MANUAL)

    def getEnableOnStartupSetting(self):
        if isCompatibleWith20262():
            return config.conf["DFN_global"]["onStartup"]
        else:
            return config.conf["DFN_global"]["enableOnStartup"]
    
    def setEnableOnStartupSetting(self, val):
        if isCompatibleWith20262():
            config.conf["DFN_global"]["onStartup"] = val
        else:
            config.conf["DFN_global"]["enableOnStartup"] = val
    
    def getUpdateCheckSetting(self):
        return config.conf["DFN_global"]["checkForUpdatesOnStartup"]

    def setUpdateCheckSetting(self, val):
        config.conf["DFN_global"]["checkForUpdatesOnStartup"] = val

    def script_changeDict(self, gesture):
        if isCompatibleWith20262():
            if self._isEnableDictionaryInConfig():
                self.finishTone()
                self.clear()
            else:
                tones.beep(1200, 80)
                self.load()
            return
        if "riryou" in speechDictHandler.dictTypes:
            self.clear()
        else:
            tones.beep(1200, 80)
            self.load()
    #Translators: Input help mode message for change dict command.
    script_changeDict.__doc__ = _("理療科用読み辞書の適用状態を切り替える")

    def toggleDictState(self, evt=None):
        if isCompatibleWith20262():
            if self._isEnableDictionaryInConfig():
               self.clear()
            else:
                self.load()
            return
        if "riryou" in speechDictHandler.dictTypes:
            self.clear()
        else:
            tones.beep(1200, 80)
            self.load()
    
    def _isEnableDictionaryInConfig(self):
        speechDicts = list(config.conf["speech"]["speechDictionaries"])
        return addonName in speechDicts

    def _enableDictionaryInConf(self):
        speechDicts = list(config.conf["speech"]["speechDictionaries"])
        if addonName not in speechDicts:
            speechDicts.append(addonName)
            config.conf["speech"]["speechDictionaries"] = speechDicts

    def _disableDictionaryInConf(self):
        speechDicts = list(config.conf["speech"]["speechDictionaries"])
        if addonName in speechDicts:
            speechDicts.remove(addonName)
            config.conf["speech"]["speechDictionaries"] = speechDicts

    def load(self, silent=False):
        # 2026.2以降、辞書の有効化
        if isCompatibleWith20262():
            self._enableDictionaryInConf()
            if silent:
                ui.message(_("理療科用読み辞書使用中。"))
            return
        # 2026.1以下、辞書ファイル読み込みモードのときはファイルを変換
        if os.path.isfile(self.dictFile) and (not os.path.isfile(self.dictPickle)) and (not isCompatibleWith20262()):
            dic = speechDictHandler.SpeechDict()
            dic.load(self.dictFile)
            with open(self.dictPickle, "wb") as f:
                _pickle.dump(dic, f)
        # 理療科辞書オブジェクト読み込み
        with open(self.dictPickle, "rb") as f:
            speechDictHandler.dictionaries["riryou"] = _pickle.load(f)
        # 理療科辞書タイプを追加
        ls = list(speechDictHandler.dictTypes)
        ls.insert(ls.index("default") + 1, "riryou")
        speechDictHandler.dictTypes = tuple(ls)
        if silent:
            self.finishTone()
            ui.message(_("理療科用読み辞書使用中。"))

    def clear(self, silent=False):
        # 2026.2以降、辞書の無効化
        if isCompatibleWith20262():
            self._disableDictionaryInConf()
            if silent:
                ui.message(_("理療科用読み辞書解除。"))
            return
        if "riryou" in speechDictHandler.dictTypes:
            # 理療科辞書タイプを削除
            ls = list(speechDictHandler.dictTypes)
            del ls[ls.index("riryou")]
            speechDictHandler.dictTypes = tuple(ls)
        if "riryou" in speechDictHandler.dictionaries:
            del speechDictHandler.dictionaries["riryou"]
        if silent:
            self.finishTone()
            ui.message(_("理療科用読み辞書解除。"))

    def finishTone(self):
        tones.beep(1200, 80)
        time.sleep(0.1)
        tones.beep(1200, 80)

    __gestures = {
        "kb:control+shift+NVDA+D": "changeDict"
    }
