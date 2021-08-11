#Copyright (C) 2021 Hiroki Fujii <hfujii@hisystron.com>


import os
import globalPluginHandler
import speechDictHandler
try:
	import _pickle
except:
	import cPickle as _pickle
import tones
import time
import ui
import addonHandler
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("読ター For NVDA")

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		# ファイルの場所
		self.dictPickle = os.path.join(os.path.realpath(os.path.dirname(os.path.dirname(__file__))), "riryou_dict.dat")

	def script_changeDict(self, gesture):
		if "riryou" in speechDictHandler.dictTypes:
			self.clear()
		else:
			self.load()
	#Translators: Input help mode message for change dict command.
	script_changeDict.__doc__ = _("理療科用読み辞書の適用状態を切り替える")

	def load(self):
		ui.message(_("理療科用読み辞書を適用します。"))
		tones.beep(800, 100)
		# 理療科辞書オブジェクト読み込み
		with open(self.dictPickle, "rb") as f:
			speechDictHandler.dictionaries["riryou"] = _pickle.load(f)
		# 理療科辞書タイプを追加
		ls = list(speechDictHandler.dictTypes)
		ls.insert(ls.index("default") + 1, "riryou")
		speechDictHandler.dictTypes = tuple(ls)
		self.finishTone()

	def clear(self):
		ui.message(_("理療科用読み辞書を解除します。"))
		tones.beep(800, 100)		

		if "riryou" in speechDictHandler.dictTypes:
			# 理療科辞書タイプを削除
			ls = list(speechDictHandler.dictTypes)
			del ls[ls.index("riryou")]
			speechDictHandler.dictTypes = tuple(ls)
		if "riryou" in speechDictHandler.dictionaries:
			del speechDictHandler.dictionaries["riryou"]
		self.finishTone()

	def finishTone(self):
		tones.beep(1200, 80)
		time.sleep(0.1)
		tones.beep(1200, 80)

	__gestures = {
		"kb:control+shift+NVDA+D": "changeDict"
	}
