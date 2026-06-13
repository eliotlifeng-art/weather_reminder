[app]

title = Weather Reminder
package.name = weather_reminder
package.domain = com.weatherreminder

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 0.1.0

requirements = python3,cython==0.29.37,kivy==2.2.1,kivymd==1.1.1,requests,plyer

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,RECEIVE_BOOT_COMPLETED,VIBRATE,POST_NOTIFICATIONS

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.gradle_dependencies = androidx.work:work-runtime:2.8.1

[buildozer]
log_level = 2
warn_on_root = 0
