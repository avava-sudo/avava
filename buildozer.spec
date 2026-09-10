[app]
title = Binary Calculator
package.name = binarycalc
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 21
# Раскомментируйте и укажите точную версию build-tools
android.build_tools_version = 33.0.2
# Удалите или закомментируйте явный NDK, чтобы Buildozer использовал системный
# android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
