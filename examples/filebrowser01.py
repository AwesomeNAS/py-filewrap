# coding=utf-8
#
# Copyright 2016 iXsystems, Inc.
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
#####################################################################

import sys
import getpass
from filewrap import FileProvider


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def main():
    def print_files(files):
        for i, f in enumerate(files):
            print("f.uri={0}, INDEX:{1}".format(f.uri, i))

    while True:
        i = input(">enter ftp/freenas user (optional, leave empty for 'anonymous'/'root') :")
        _user = i
        i = getpass.getpass(">enter ftp/freenas password (optional):")
        _password = i
        print("EXAMPLES:")
        print("FTP                            : 'ftp://localhost'")
        print("FTP (accepts anonymous user)   : 'ftp://ftp.funet.fi/pub/CPAN'")
        print("LOCAL                          : 'file:///Users'")
        print("REMOTE                         : 'remote://<freenas-host>/mnt/mypool/'")
        i = input(">enter path:")
        currdir = FileProvider.open(i, user=_user, password=_password)
        files = [f for f in currdir.readdir()]
        print_files(files)
        while True:
            i = input(">Select index ('k'=restart, 'm'=mkdir, 'r'=rmdir, 'enter'=navigate up):")
            if i == 'k':
                break
            elif i == 'm':
                i = input(">Dirname:")
                currdir.mkdir(i)
            elif i == 'r':
                currdir.rmdir()
                currdir = currdir.parent
            elif is_number(i) :
                if int(i) < len(files) and files[int(i)].is_dir:
                    currdir = files[int(i)]
                else:
                    continue
            else:
                currdir = currdir.parent
            files = [f for f in currdir.readdir()]
            print_files(files)


if __name__ == '__main__':
    sys.exit(main())
