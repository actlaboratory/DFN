# coding: UTF-8

from __future__ import unicode_literals
import addonHandler
import globalVars
import gui
import hashlib
import json
import os
import sys
import tempfile
import threading
import time
import versionInfo
import winreg
import wx
from logHandler import log
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from .constants import *
from .translate import *

try:
    import addonHandler
    addonHandler.initTranslation()
except BaseException:
    def _(x): return x

try:
    import updateCheck
    if (globalVars.appArgs.install and globalVars.appArgs.minimal):
        updatable = False
    elif globalVars.appArgs.secure or config.isAppX:
        updatable = False
    else:
        updatable = True
except RuntimeError:
    updatable = False

AUTO=0
MANUAL=1

class AutoUpdateChecker:
    def __init__(self):
        self.updater = None
        if not updatable:
            log.warning("Update check not supported.")

    def autoUpdateCheck(self, mode=AUTO):
        """
        Call this method to check for updates. mode=AUTO means automatic update check, and MANUAL means manual triggering like "check for updates" menu invocation.
        When set to AUTO mode, some dialogs are not displayed (latest and error).
        """

        if not updatable:
            return
        self.updater = NVDAAddOnUpdater(mode)

class NVDAAddOnUpdater ():
    def __init__(self, mode, version=addonVersion):
        self.mode = mode
        self.version = version
        if updatable:
            t = threading.Thread(target=self.check_update)
            t.daemon = True
            t.start()

    def check_update(self):
        post_params = {
            "name": addonKeyword,
            "version": addonVersion,
            "updater_version": "1.0.0",
        }
        req = Request("%s?%s" % (updateURL, urlencode(post_params)))
        try:
            f = urlopen(req)
        except BaseException:
            if self.mode == MANUAL:
                gui.messageBox(_("アップデートサーバに接続できません。\nインターネット接続を確認してください。"),
                               _("エラー"), style=wx.CENTER | wx.ICON_WARNING)
            return False

        if f.getcode() != 200:
            if self.mode == MANUAL:
                gui.messageBox(_("アップデートサーバに接続できません。"), _("エラー"), style=wx.CENTER | wx.ICON_WARNING)
            return False

        try:
            update_dict = f.read().decode("utf-8")
            f.close()
            update_dict = json.loads(update_dict)
        except BaseException:
            if self.mode == MANUAL:
                gui.messageBox(
                    _("不正なデータが送信されました。\nこの問題が継続する場合、ACT Laboratoryにお問い合わせください。"),
                    _("エラー"),
                    style=wx.CENTER | wx.ICON_WARNING)
            return False

        code = update_dict["code"]
        if code == UPDATER_LATEST:
            if self.mode == MANUAL:
                gui.messageBox(_("お使いのアドオンは最新です。"), _("アップデート確認"), style=wx.CENTER | wx.ICON_INFORMATION)
            return False
        elif code == UPDATER_BAD_PARAM:
            if self.mode == MANUAL:
                gui.messageBox(_("不正なデータが送信されました。\nこの問題が継続する場合、ACT Laboratoryにお問い合わせください。"),
                               _("アップデート確認"), style=wx.CENTER | wx.ICON_INFORMATION)
            return False
        elif code == UPDATER_NOT_FOUND:
            if self.mode == MANUAL:
                gui.messageBox(_("このアドオンのアップデータは登録されていません。\nこの問題が継続する場合、ACT Laboratoryまでお問い合わせください。"),
                               _("アップデート確認"), style=wx.CENTER | wx.ICON_INFORMATION)
            return False
        elif code == UPDATER_VISIT_SITE:
            if self.mode == MANUAL:
                gui.messageBox(_("アップデートが見つかりましたが、このままアップデートを継続することができません。\nアドオンのウェブサイトを確認してください。"),
                               _("アップデート確認"), style=wx.CENTER | wx.ICON_INFORMATION)
            return False

        new_version = update_dict["update_version"]
        url = update_dict["updater_url"]
        if "updater_hash" not in update_dict or update_dict["updater_hash"] is None or update_dict["updater_hash"] == "":
            hash = None
        else:
            hash = update_dict["updater_hash"]
        # end set hash

        caption = _("アップデート確認")
        question = _("{summary} Ver.{newVersion}が利用できます。\nアップデートしますか？\n現在のバージョン: {currentVersion}\n最新バージョン: {newVersion}").format(
            summary=addonSummary, newVersion=new_version, currentVersion=addonVersion)
        answer = gui.messageBox(question, caption, style=wx.CENTER | wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_INFORMATION)
        if answer == wx.OK:
            downloader = UpdateDownloader(addonName, [url], hash)
            wx.CallAfter(downloader.start)
            return
        else:
            return True


class UpdateDownloader(updateCheck.UpdateDownloader):
    def __init__(self, addonCode, urls, fileHash=None):
        try:
            super(UpdateDownloader, self).__init__(urls, fileHash)
        except BaseException:
            pass
        self.urls = urls
        self.fp = tempfile.NamedTemporaryFile(prefix="%s_update_" % addonCode, suffix=".nvda-addon", mode="wb", delete=False)
        self.destPath = self.fp.name
        self.fileHash = fileHash

    def start(self):
        self._shouldCancel = False
        self._guiExecTimer = wx.PyTimer(self._guiExecNotify)
        gui.mainFrame.prePopup()
        self._progressDialog = wx.ProgressDialog(_("アップデートをダウンロード中"),
                                                 _("接続中..."),
                                                 style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE,
                                                 parent=gui.mainFrame)
        self._progressDialog.Raise()
        t = threading.Thread(target=self._bg)
        t.daemon = True
        t.start()

    def _error(self):
        self._stopped()
        self.cleanup_tempfile()
        gui.messageBox(
            _("アップデートのダウンロードに失敗しました。"),
            _("エラー"),
            wx.OK | wx.ICON_ERROR)

    def _download(self, url):
        headers = {}
        if updaterUserAgent:
            headers["User-Agent"] = updaterUserAgent
        req = Request(url, headers=headers)
        try:
            remote = urlopen(req, timeout=120)
        except BaseException:
            raise RuntimeError("Download failed")
            return
        if remote.code != 200:
            raise RuntimeError("Download failed with code %d" % remote.code)
        size = int(remote.headers["content-length"])
        if self.fileHash:
            hasher = hashlib.sha1()
        self._guiExec(self._downloadReport, 0, size)
        read = 0
        chunk = 8192
        while True:
            if self._shouldCancel:
                self.fp.close()
                self.cleanup_tempfile()
                return
            if size - read < chunk:
                chunk = size - read
            block = remote.read(chunk)
            if not block:
                break
            read += len(block)
            if self._shouldCancel:
                self.fp.close()
                self.cleanup_tempfile()
                return
            self.fp.write(block)
            if self.fileHash:
                hasher.update(block)
            self._guiExec(self._downloadReport, read, size)
        if read < size:
            raise RuntimeError("Content too short")
        if self.fileHash and hasher.hexdigest().lower() != self.fileHash.lower():
            raise RuntimeError("Content has incorrect file hash")
        self.fp.close()
        self._guiExec(self._downloadReport, read, size)

    def _downloadSuccess(self):
        self._stopped()
        from gui import addonGui
        addonGui.promptUserForRestart()
        try:
            try:
                bundle = addonHandler.AddonBundle(self.destPath.decode("mbcs"))
            except AttributeError:
                bundle = addonHandler.AddonBundle(self.destPath)
            except BaseException:
                log.error("Error opening addon bundle from %s" % self.destPath, exc_info=True)
                gui.messageBox(translate("Failed to open add-on package file at %s - missing file or invalid file format") % self.destPath,
                               translate("Error"),
                               wx.OK | wx.ICON_ERROR)
                return
            bundleName = bundle.manifest['name']
            for addon in addonHandler.getAvailableAddons():
                if not addon.isPendingRemove and bundleName == addon.manifest['name']:
                    addon.requestRemove()
                    break
            progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame,
                                                             _("アップデートをダウンロード中"),
                                                             _("アドオンがアップデートされるまでお待ちください。"))
            try:
                gui.ExecAndPump(addonHandler.installAddonBundle, bundle)
            except BaseException:
                log.error("Error installing  addon bundle from %s" % self.destPath, exc_info=True)
                progressDialog.done()
                del progressDialog
                gui.messageBox(_("アドオンのアップデートに失敗しました。"),
                               _("エラー"),
                               wx.OK | wx.ICON_ERROR)
                return
            else:
                progressDialog.done()
                del progressDialog
        finally:
            self.cleanup_tempfile()

    def cleanup_tempfile(self):
        if not os.path.isfile(self.destPath):
            return
        try:
            os.remove(self.destPath)
        except BaseException:
            pass
        return
