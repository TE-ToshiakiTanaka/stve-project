import os
import sys
import imp
import time
import glob

PROFILE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "profile"))
if not PROFILE_PATH in sys.path:
    sys.path.insert(0, PROFILE_PATH)

from stve.log import Log
from stve.cmd import run
from stve.exception import *

TIMEOUT = 30
UIAUTOMATOR_TIMEOUT = 180
UIAUTOMATOR_PATH = "/data/local/tmp/"

ADB_ROOT = os.path.normpath(os.path.dirname(__file__))
ADB_APK_AURA = os.path.join(ADB_ROOT, "apk", "aura")
ADB_JAR_AUBS = os.path.join(ADB_ROOT, "jar", "aubs")

L = Log("Android.Library.STVE")

class AndroidBase(object):
    def __init__(self, profile, host=PROFILE_PATH):
        self.WIFI = False
        self._set_profile(profile, host)

    def _set_profile(self, name, host):
        self.profile = None
        class_name = "_" + name
        if not os.path.exists(host):
            L.warning("%s is not exists." % host)
            raise AndroidError("%s is not exists." % host)

        try:
            prof = None
            for fdn in os.listdir(host):
                if fdn.endswith(".py") and (name in fdn):
                    prof = fdn.replace(".py", "")
            if prof == None:
                L.warning("Not have a profile : %s " % name)
                class_name = "_0000000000000000"
                for fdn in os.listdir(PROFILE_PATH):
                    if fdn.endswith("_0000000000000000.py"):
                        prof = fdn.replace(".py", "")
            f, n, d = imp.find_module(str(prof))
            module = imp.load_module(prof, f, n, d)
            self.profile = getattr(module, class_name)
            self.profile.SERIAL = name
            self.profile.TMP_PICTURE = "%s_TMP.png" % name
        except Exception as e:
            L.debug('=== Error Exception ===')
            L.debug('type     : ' + str(type(e)))
            L.debug('args     : ' + str(e.args))
            L.debug('message  : ' + e.message)
            L.debug('e        : ' + str(e))
            raise AndroidError(str(e))

    def get_profile(self):
        return self.profile

    def __exec(self, cmd, timeout=TIMEOUT):
        L.debug(cmd)
        result = run(cmd, timeout=timeout)
        if result != None:
            try:
                if result[0] == 0:
                    result = result[1].replace("\r", "")
                else:
                    L.warning(result[2].replace("\r",""))
                    raise AndroidError("Android Execute Failed.")
            except Exception as e:
                L.warning(str(e))
                raise e
        return result

    def _target(self):
        if not self.WIFI:
            return "-s %s " % (self.profile.SERIAL)
        else:
            return "-s %s:%s " % (self.profile.IP, self.profile.PORT)

    def _adb(self, cmd, timeout=TIMEOUT):
        if "adb" in cmd:
            L.debug("command include [adb]. : %s" % cmd)
        cmd = "adb %s" % cmd
        return self.__exec(cmd, timeout)

    def _adb_dump(self, cmd, timeout=TIMEOUT):
        if "adb" in cmd:
            L.debug("command include [adb]. : %s" % cmd)
        cmd = "adb %s" % cmd
        return self.__exec_dump(cmd, timeout)


    def push(self, src, dst, timeout=TIMEOUT):
        L.debug("[push] : %s -> %s" % (src, dst))
        cmd = "%spush %s %s" % (self._target(), src, dst)
        return self._adb(cmd, timeout)

    def pull(self, src, dst, timeout=TIMEOUT):
        L.debug("[pull]. : %s -> %s" % (src, dst))
        cmd = "%spull %s %s" % (self._target(), src, dst)
        return self._adb(cmd)

    def shell(self, cmd, timeout=TIMEOUT):
        if "shell" in cmd:
            L.debug("command include [shell]. : %s" % cmd)
        cmd = "%sshell %s" % (self._target(), cmd)
        return self._adb(cmd, timeout)

    def kill(self):
        cmd = "kill-server"
        return self._adb(cmd)

    def connect(self):
        if self.WIFI:
            cmd = "connect %s:%s" % (self.profile.IP, self.profile.PORT)
            return self._adb(cmd)

    def disconnect(self):
        if self.WIFI:
            cmd = "disconnect %s:%s" % (self.profile.IP, self.profile.PORT)
            return self._adb(cmd)

    def usb(self):
        if self.WIFI:
            self.disconnect()
            self.WIFI = False
        cmd = "%susb" % (self._target())
        return self._adb(cmd)

    def tcpip(self):
        if not self.WIFI:
            self.disconnect()
            self.WIFI = True
        cmd = "tcpip %s" % (self.profile.PORT)
        return self._adb(cmd)

    def root(self):
        cmd = "%sroot " % self._target()
        L.debug(str(self._adb(cmd)))
        self.kill()
        if self.WIFI: self.tcpip()
        else: self.usb()
        self.connect()

    def remount(self):
        cmd = "%sremount " % self._target()
        L.debug(self._adb(cmd))

    def restart(self):
        cmd = "%sreboot" % self._target()
        L.debug(self._adb(cmd))

    def install(self, application, timeout=TIMEOUT):
        cmd = "%sinstall -r %s" % (self._target(), application)
        L.debug(self._adb(cmd, timeout))

    def uninstall(self, application):
        cmd = "%suninstall %s" % (self._target(), application)
        L.debug(self._adb(cmd))

    def adb(self, cmd, timeout=TIMEOUT):
        if "adb" in cmd:
            L.debug("command include [adb]. : %s" % cmd)
        cmd = "%s %s" % (self._target(), cmd)
        return self._adb(cmd, timeout)

    def wait(self, timeout=TIMEOUT):
        return self.adb("wait-for-device", timeout)

class AndroidApplication(object):
    """
        This class is not Interface of Android Module.
    """
    def __init__(self, adb):
        self._adb = adb

    def release(self):
        os.chdir(ADB_APK_AURA)
        if os.name =='nt': result = run("gradlew.bat assembleRelease")
        else: result = run("gradlew assembleRelease")

        if result[0] == 0:
            L.info(result[1].replace("\n",""))
        else:
            L.warning(result[2].replace("\n",""))
            raise AndroidError("Android Utility Re-cycle Application Build Failed.")

    def install(self):
        path = os.path.join(ADB_APK_AURA, "app", "build", "outputs", "apk", "app-release.apk")
        if os.path.exists(path):
            result = self._adb.install(path, timeout=600)
            L.info(result); return result
        else:
            raise AndroidError("Android Utility Re-cycle Application Not Exists. %s " % path)


    def uninstall(self):
        result = self._adb.uninstall(self._adb.get().AURA_PACKAGE)
        L.info(result); return result

    def execute(self, command, bundle):
        arg = ""
        for k, v in bundle.items():
            args += " -e %s %s" % (k, v)
        result = self._adb.shell("am startservice -a %s %s" % (command, arg))
        L.info(result); return result

class AndroidUiAutomator(object):
    """
        This class is not Interface of Android Module.
    """
    def __init__(self, adb):
        self._adb = adb

    def build(self):
        os.chdir(ADB_JAR_AUBS)
        if os.name =='nt': result = run("gradlew.bat uiautomatorbuild")
        else: result = run("gradlew uiautomatorbuild")

        if result[0] == 0:
            L.info(result[1].replace("\n",""))
        else:
            L.warning(result[2].replace("\n",""))
            raise AndroidError("Android UiAutomator Binary for Stve Build Failed.")

    def push(self, jar):
        result = self._adb.push(jar, UIAUTOMATOR_PATH)
        return result

    def execute(self, jar, exe, bundle, timeout=UIAUTOMATOR_TIMEOUT):
        arg = ""
        for k, v in bundle.items():
            arg += " -e %s \"%s\"" %(k, v)
        cmd = "uiautomator runtest %s -c %s %s" % (jar, exe, arg)
        result = self._adb.shell(cmd, timeout)
        L.info(result); return result

class Android(object):
    def __init__(self, profile, host=PROFILE_PATH):
        self._adb = AndroidBase(profile, host)
        self._uiautomator = AndroidUiAutomator(self._adb)
        self._application = AndroidApplication(self._adb)

        # L.info(self._uiautomator.build())
        self.push_uiautomator()

        # L.info(self._application.release())
        self.install_application()

        self.exec_uiautomator(self.get().JAR_AUBS, self.get().AUBS_SYSTEM_ALLOWAPP, {})

    def get(self):
        return self._adb.get_profile()

    def install_application(self):
        self._application.install()

    def exec_application(self, command, bundle):
        self._application.execute(command, bundle)

    def push_uiautomator(self, jar=""):
        """
            Push UiAutomator's jar file.
            :arg string jar: Local Jar File Path.
            :return string: adb result.
        """
        if jar == "":
            jar = os.path.join(ADB_JAR_AUBS, "bin", self.get().JAR_AUBS)
        return self._uiautomator.push(jar)

    def exec_uiautomator(self, jar, exe, bundle):
        """
            Execute UiAutomator's method.
            :arg string jar: Jar File Name. Before Jar File Pushed by push_uiautomator().
            :arg string exe: Execute Path. ex.) com.sony.ste.lascall.generic.PINUnLock
            :arg dict bundle: Argument Dictionary. ex.) {"IP":"192.168.2.20", "Port":"22"}
            :return string: adb result.
        """
        return self._uiautomator.execute(jar, exe, bundle)

if __name__ == '__main__':
    a = Android("YT9111NUXX")
    print a.get().SERIAL
    print a.exec_application(a.get().AURA_DEBUGON, {})
