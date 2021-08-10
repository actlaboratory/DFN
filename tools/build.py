# -*- coding: utf-8 -*-
#app build tool
#Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
#Copyright (C) 2019-2020 guredora <contact@guredora.com>
#Copyright (C) 2021 yamahubuki <itiro.ishino@gmail.com>
#Copyright (C) 2021 Hiroki Fujii <hfujii@hisystron.com>

#constantsのimport前に必要
import os
import sys
sys.path.append(os.getcwd())

import datetime
import glob
import hashlib
import json
import math
import shutil
import subprocess
import urllib.request

import buildVars.ADDON_VERSION
from tools import bumpup

class build:
	def __init__(self):
		# appVeyorかどうかを判別し、処理をスタート
		appveyor = self.setAppVeyor()
		print("Starting build for DFN(appveyor mode=%s)" % (appveyor,))

		# パッケージのパスとファイル名を決定
		package_path = "output\\"
		if 'APPVEYOR_REPO_TAG_NAME' in os.environ:
			build_filename = os.environ['APPVEYOR_REPO_TAG_NAME']
		else:
			build_filename = 'snapshot'
		print("Will be built as %s" % build_filename)

		# addonフォルダの存在を確認
		if not os.path.exists("addon"):
			print("Error: no addon folder found. Your working directory must be the root of the project. You shouldn't cd to tools and run this script.")
			exit(-1)

		# 前のビルドをクリーンアップ
		self.creen(package_path)

		# appveyorでのスナップショットの場合はバージョン番号を一時的に書き換え
		if build_filename == "snapshot" and appveyor:
			self.makeSnapshotVersionNumber()

		# ビルド
		self.makeVersionInfo()
		self.build(package_path, build_filename)
		archive_name = "DFN-%s.zip" % (build_filename,)

		# スナップショットでなければ
		if build_filename == "snapshot" and not appveyor:
			print("Skipping batch archiving because this is a local snapshot.")
		else:
			patch_name = "DFN-%spatch.zip" % (build_filename,)
			self.makePackageInfo(archive_name, patch_name, build_filename)
		print("Build finished!")

	def runcmd(self,cmd):
		proc=subprocess.Popen(cmd.split(), shell=True, stdout=1, stderr=2)
		proc.communicate()
		return proc.poll()

	def setAppVeyor(self):
		if len(sys.argv)>=2 and sys.argv[1]=="--appveyor":
			return True
		return False

	def creen(self,package_path):
		if os.path.isdir(package_path):
			print("Clearling previous build...")
			shutil.rmtree("output\\")

	def makeSnapshotVersionNumber(self):
		#日本標準時オブジェクト
		JST = datetime.timezone(datetime.timedelta(hours=+9))
		#Pythonは世界標準時のZに対応していないので文字列処理で乗り切り、それを日本標準時に変換
		dt = datetime.datetime.fromisoformat(os.environ["APPVEYOR_REPO_COMMIT_TIMESTAMP"][0:19]+"+00:00").astimezone(JST)
		major = str(dt.year)[2:4]+str(dt.month).zfill(2)
		minor = str(dt.day)
		patch = str(int(math.floor((dt.hour*3600+dt.minute*60+dt.second)/86400*1000)))
		bumpup.bumpup(major+"."+minor+"."+patch, str(dt.date()))

	def build(self, package_path, build_filename):
		print("Building...")
		shutil.copytree("public", "output")
		ret = self.runcmd("scons")
		print("build finished with status %d" % ret)
		if ret != 0:
			sys.exit(ret)


		print("Compressing into package...")
		shutil.make_archive("DFN-%s" % (build_filename,),'zip','output')

	def makePackageInfo(self, archive_name, patch_name, build_filename):
		print("computing hash...")
		#日本標準時オブジェクト
		JST = datetime.timezone(datetime.timedelta(hours=+9))
		#Pythonは世界標準時のZに対応していないので文字列処理で乗り切り、それを日本標準時に変換
		dt = datetime.datetime.fromisoformat(os.environ["APPVEYOR_REPO_COMMIT_TIMESTAMP"][0:19]+"+00:00").astimezone(JST)
		dateStr = "%s-%s-%s" % (str(dt.year), str(dt.month).zfill(2), str(dt.day).zfill(2))
		with open(archive_name, mode = "rb") as f:
			content = f.read()
		package_hash = hashlib.sha1(content).hexdigest()
		print("creating package info...")
		info = {}
		info["package_hash"] = package_hash
		info["patch_hash"] = None
		info["version"] = buildVars.ADDON_VERSION
		info["released_date"] = dateStr
		with open("DFN-%s_info.json" % (build_filename,), mode = "w") as f:
			json.dump(info, f)


if __name__ == "__main__":
	build()
