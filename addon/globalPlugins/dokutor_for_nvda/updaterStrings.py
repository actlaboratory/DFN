try:
    import addonHandler
    addonHandler.initTranslation()
except BaseException:
    def _(x): return x

ERROR = _("エラー")
ERROR_UNABLE_TO_CONNECT = _("アップデートサーバに接続できません。\nインターネット接続を確認してください。")
ERROR_UNABLE_TO_CONNECT_SERVERSIDE = _("アップデートサーバに接続できません。")
ERROR_UPDATE_INFO_INVALID = _("アップデート情報が誤っています。\n詳しくは、ACT Laboratory までお問い合わせください。")
ERROR_REQUEST_PARAMETERS_INVALID = _("リクエストパラメータが誤っています。開発者にお問い合わせください。")
ERROR_DOWNLOADING = _("アドオンのアップデートのダウンロード中にエラーが発生しました")
ERROR_OPENING = _("アドオンパッケージファイル %s を開けませんでした。ファイルの形式が誤っているか、ファイルが壊れています。")
ERROR_FAILED_TO_UPDATE = _("%sのアップデートに失敗しました。")
NO_UPDATES = _("アップデートが見つかりませんでした。\nこのバージョンは、最新です。")
UPDATER_NOT_REGISTERED = _("このアップデータは、登録されていません。開発者にお問い合わせください。")
UPDATE_NOT_POSSIBLE = _("アップデートが見つかりましたが、このバージョンからのアップデートができません。ソフトウェアのWebサイトを確認してください。")
UPDATE_CHECK_TITLE = _("アップデートの確認")
UPDATE_CONFIRMATION_TITLE = _("アップデート確認")
UPDATE_CONFIRMATION_MESSAGE = _("{summary} Ver.{newVersion} が利用可能です。\nアップデートしますか？\n現在のバージョン: {currentVersion}\n新しいバージョン: {newVersion}")
DOWNLOADING = _("アドオンのアップデートをダウンロードしています")
CONNECTING = _("接続中")
UPDATING = _("アドオンをアップデートしています")
UPDATING_PLEASE_WAIT = _("アドオンがアップデートされるまでお待ちください")
