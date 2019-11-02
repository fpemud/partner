#!/usr/bin/python2
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import shutil
import subprocess
import time
import grp
import pwd
import socket
import re
import logging


class AssUtil:

    @staticmethod
    def stripComment(s):
        m = re.search("(.*?) *#.*", s)
        if m is not None:
            return m.group(1)
        else:
            return s

    @staticmethod
    def getGatewayInterface():
        ret = AssUtil.shell("/bin/route -n4", "stdout")
        # syntax: DestIp GatewayIp DestMask ... OutIntf
        m = re.search("^(0\\.0\\.0\\.0)\\s+([0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+)\\s+(0\\.0\\.0\\.0)\\s+.*\\s+(\\S+)$", ret, re.M)
        if m is None:
            return None
        return m.group(4)

    @staticmethod
    def getGatewayIpAddress():
        ret = AssUtil.shell("/bin/route -n4", "stdout")
        # syntax: DestIp GatewayIp DestMask ... OutIntf
        m = re.search("^(0\\.0\\.0\\.0)\\s+([0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+)\\s+(0\\.0\\.0\\.0)\\s+.*\\s+(\\S+)$", ret, re.M)
        if m is None:
            return None
        return m.group(2)

    @staticmethod
    def getLoggingLevel(logLevel):
        if logLevel == "CRITICAL":
            return logging.CRITICAL
        elif logLevel == "ERROR":
            return logging.ERROR
        elif logLevel == "WARNING":
            return logging.WARNING
        elif logLevel == "INFO":
            return logging.INFO
        elif logLevel == "DEBUG":
            return logging.DEBUG
        else:
            assert False

    @staticmethod
    def copyToDir(srcFilename, dstdir, mode=None):
        """Copy file to specified directory, and set file mode if required"""

        if not os.path.isdir(dstdir):
            os.makedirs(dstdir)
        fdst = os.path.join(dstdir, os.path.basename(srcFilename))
        shutil.copy(srcFilename, fdst)
        if mode is not None:
            AssUtil.shell("/bin/chmod " + mode + " \"" + fdst + "\"")

    @staticmethod
    def copyToFile(srcFilename, dstFilename, mode=None):
        """Copy file to specified filename, and set file mode if required"""

        if not os.path.isdir(os.path.dirname(dstFilename)):
            os.makedirs(os.path.dirname(dstFilename))
        shutil.copy(srcFilename, dstFilename)
        if mode is not None:
            AssUtil.shell("/bin/chmod " + mode + " \"" + dstFilename + "\"")

    @staticmethod
    def readFile(filename):
        """Read file, returns the whold content"""

        f = open(filename, 'r')
        buf = f.read()
        f.close()
        return buf

    @staticmethod
    def writeFile(filename, buf, mode=None):
        """Write buffer to file"""

        f = open(filename, 'w')
        f.write(buf)
        f.close()
        if mode is not None:
            AssUtil.shell("/bin/chmod " + mode + " \"" + filename + "\"")

    @staticmethod
    def mkDirAndClear(dirname):
        AssUtil.forceDelete(dirname)
        os.mkdir(dirname)

    @staticmethod
    def touchFile(filename):
        assert not os.path.exists(filename)
        f = open(filename, 'w')
        f.close()

    @staticmethod
    def forceDelete(filename):
        if os.path.islink(filename):
            os.remove(filename)
        elif os.path.isfile(filename):
            os.remove(filename)
        elif os.path.isdir(filename):
            shutil.rmtree(filename)

    @staticmethod
    def forceSymlink(source, link_name):
        if os.path.exists(link_name):
            os.remove(link_name)
        os.symlink(source, link_name)

    @staticmethod
    def getFreeSocketPort(portType, portStart, portEnd):
        if portType == "tcp":
            sType = socket.SOCK_STREAM
        elif portType == "udp":
            assert False
        else:
            assert False

        for port in range(portStart, portEnd + 1):
            s = socket.socket(socket.AF_INET, sType)
            try:
                s.bind((('', port)))
                return port
            except socket.error:
                continue
            finally:
                s.close()
        raise Exception("No valid %s port in [%d,%d]." % (portType, portStart, portEnd))

    @staticmethod
    def shell(cmd, flags=""):
        """Execute shell command"""

        assert cmd.startswith("/")

        # Execute shell command, throws exception when failed
        if flags == "":
            retcode = subprocess.Popen(cmd, shell=True).wait()
            if retcode != 0:
                raise Exception("Executing shell command \"%s\" failed, return code %d" % (cmd, retcode))
            return

        # Execute shell command, throws exception when failed, returns stdout+stderr
        if flags == "stdout":
            proc = subprocess.Popen(cmd,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate()[0]
            if proc.returncode != 0:
                raise Exception("Executing shell command \"%s\" failed, return code %d" % (cmd, proc.returncode))
            return out

        # Execute shell command, returns (returncode,stdout+stderr)
        if flags == "retcode+stdout":
            proc = subprocess.Popen(cmd,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate()[0]
            return (proc.returncode, out)

        assert False

    @staticmethod
    def shellInteractive(cmd, strInput, flags=""):
        """Execute shell command with input interaction"""

        assert cmd.startswith("/")

        # Execute shell command, throws exception when failed
        if flags == "":
            proc = subprocess.Popen(cmd,
                                    shell=True,
                                    stdin=subprocess.PIPE)
            proc.communicate(strInput)
            if proc.returncode != 0:
                raise Exception("Executing shell command \"%s\" failed, return code %d" % (cmd, proc.returncode))
            return

        # Execute shell command, throws exception when failed, returns stdout+stderr
        if flags == "stdout":
            proc = subprocess.Popen(cmd,
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate(strInput)[0]
            if proc.returncode != 0:
                raise Exception("Executing shell command \"%s\" failed, return code %d, output %s" % (cmd, proc.returncode, out))
            return out

        # Execute shell command, returns (returncode,stdout+stderr)
        if flags == "retcode+stdout":
            proc = subprocess.Popen(cmd,
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            out = proc.communicate(strInput)[0]
            return (proc.returncode, out)

        assert False

    @staticmethod
    def initLog(filename):
        AssUtil.forceDelete(filename)
        AssUtil.writeFile(filename, "")

    @staticmethod
    def printLog(filename, msg):
        f = open(filename, 'a')
        if msg != "":
            f.write(time.strftime("%Y-%m-%d %H:%M:%S  ", time.localtime()))
            f.write(msg)
            f.write("\n")
        else:
            f.write("\n")
        f.close()

    @staticmethod
    def getUsername():
        return pwd.getpwuid(os.getuid())[0]

    @staticmethod
    def getGroups():
        """Returns the group name list of the current user"""

        uname = pwd.getpwuid(os.getuid())[0]
        groups = [g.gr_name for g in grp.getgrall() if uname in g.gr_mem]
        gid = pwd.getpwnam(uname).pw_gid
        groups.append(grp.getgrgid(gid).gr_name)            # --fixme, should be prepend
        return groups


class FlexObject:
    pass
