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
import config
from logHandler import log
from .constants import *
from . import updater


try:
    addonHandler.initTranslation()
except BaseException:
    def _(x): return x


confspec = {
    "checkForUpdatesOnStartup": "boolean(default=True)",
    "enableOnStartup": "boolean(default=False)",
}
config.conf.spec["DFN_global"] = confspec


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("読ター For NVDA")

    def __init__(self, *args, **kwargs):
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        
        # dokutar dic file path
        self.dictPickle = os.path.join(os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "riryou_dict.dat")
        
        if globalVars.appArgs.secure:
            return
        # end secure screen
        
        # setup updater
        if self.getUpdateCheckSetting() is True:
            self.autoUpdateChecker = updater.AutoUpdateChecker()
            self.autoUpdateChecker.autoUpdateCheck(mode=updater.AUTO)
        # end update check
        
        self._setupMenu()
        
        if config.conf["DFN_global"]["enableOnStartup"]:
            self.load()

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
        
        self.enableOnStartupToggleItem = self.rootMenu.Append(
            wx.ID_ANY,
            self.enableOnStartupToggleString(),
            _("起動時の理療科用読み辞書の適用状態を切り替えます。")
        )
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.toggleEnableOnStartup, self.enableOnStartupToggleItem)
        
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
            2, wx.ID_ANY, _("DFN"), self.rootMenu)

    def dictStateToggleString(self):
        return _("理療科用読み辞書を解除する(&A)") if "riryou" in speechDictHandler.dictTypes else _("理療科用読み辞書を適用する(&A)")
    
    def enableOnStartupToggleString(self):
        return _("起動時の理療科用読み辞書の適用を無効化") if self.getEnableOnStartupSetting() is True else _("起動時の理療科用読み辞書の適用を有効化")
    
    def updateCheckToggleString(self):
        return _("起動時のアップデートの確認を無効化") if self.getUpdateCheckSetting() is True else _("起動時のアップデートの確認を有効化")
    
    def toggleEnableOnStartup(self, evt):
        changed = not self.getEnableOnStartupSetting()
        self.setEnableOnStartupSetting(changed)
        msg = _("NVDA起動時に、自動で理療科用読み辞書を適用します。") if changed is True else _("NVDA起動時は、通常の読み辞書を利用します。")
        self.enableOnStartupToggleItem.SetItemLabel(self.enableOnStartupToggleString())
        wx.MessageBox(msg, _("設定変更完了"))
    
    def toggleUpdateCheck(self, evt):
        changed = not self.getUpdateCheckSetting()
        self.setUpdateCheckSetting(changed)
        msg = _("NVDA起動時に、自動でDFNのアップデートを確認します。") if changed is True else _("NVDA起動時に、DFNのアップデートを確認しません。")
        self.updateCheckToggleItem.SetItemLabel(self.updateCheckToggleString())
        wx.MessageBox(msg, _("設定変更完了"))

    def performUpdateCheck(self, evt):
        updater.AutoUpdateChecker().autoUpdateCheck(mode=updater.MANUAL)

    def getEnableOnStartupSetting(self):
        return config.conf["DFN_global"]["enableOnStartup"]
    
    def setEnableOnStartupSetting(self, val):
        config.conf["DFN_global"]["enableOnStartup"] = val
    
    def getUpdateCheckSetting(self):
        return config.conf["DFN_global"]["checkForUpdatesOnStartup"]

    def setUpdateCheckSetting(self, val):
        config.conf["DFN_global"]["checkForUpdatesOnStartup"] = val

    def script_changeDict(self, gesture):
        if "riryou" in speechDictHandler.dictTypes:
            self.clear()
        else:
            self.load()
    #Translators: Input help mode message for change dict command.
    script_changeDict.__doc__ = _("理療科用読み辞書の適用状態を切り替える")

    def toggleDictState(self, evt=None):
        if "riryou" in speechDictHandler.dictTypes:
            self.clear()
        else:
            self.load()
    
    def load(self):
        ui.message(_("理療科用読み辞書を適用します。"))
        # 理療科辞書オブジェクト読み込み
        with open(self.dictPickle, "rb") as f:
            speechDictHandler.dictionaries["riryou"] = _pickle.load(f)
        # 理療科辞書タイプを追加
        ls = list(speechDictHandler.dictTypes)
        ls.insert(ls.index("default") + 1, "riryou")
        speechDictHandler.dictTypes = tuple(ls)
        self.dictStateToggleItem.SetItemLabel(self.dictStateToggleString())
        self.finishTone()

    def clear(self):
        ui.message(_("理療科用読み辞書を解除します。"))
        if "riryou" in speechDictHandler.dictTypes:
            # 理療科辞書タイプを削除
            ls = list(speechDictHandler.dictTypes)
            del ls[ls.index("riryou")]
            speechDictHandler.dictTypes = tuple(ls)
        if "riryou" in speechDictHandler.dictionaries:
            del speechDictHandler.dictionaries["riryou"]
        self.dictStateToggleItem.SetItemLabel(self.dictStateToggleString())
        self.finishTone()

    def finishTone(self):
        tones.beep(1200, 80)
        time.sleep(0.1)
        tones.beep(1200, 80)

    __gestures = {
        "kb:control+shift+NVDA+D": "changeDict"
    }
