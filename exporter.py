#!/bin/python3

from subprocess import Popen, PIPE, DEVNULL
import json
import collections

# necessary fields in journald entries
entries_we_need = ['MESSAGE', 'PRIORITY', '_PID', '_UID', '_GID', '_SOURCE_REALTIME_TIMESTAMP',
                   '_BOOT_ID', '_COMM', '_EXE', '_CMDLINE', 'OBJECT_PID', 'OBJECT_UID',
                   'OBJECT_GID', 'OBJECT_COMM', 'OBJECT_EXE', 'OBJECT_CMDLINE', 'COREDUMP_UNIT',
                   'COREDUMP_USER_UNIT']

# subprocess which gives us all journald entries since the last boot in json format
# (one entry per line)
out_channel = Popen('journalctl -b -f -a --no-tail --no-pager --output=json',
                    stdout=PIPE, stderr=DEVNULL, shell=True, universal_newlines=True)

while True:
    journal_jsonstring = out_channel.stdout.readline()
    if not journal_jsonstring:
        break

    # deserializing json object to a Python dict
    journal_pythonobj = json.loads(journal_jsonstring)

    # reforming journald entries and leaving only necessary fields
    journal_pythonobj_for_pass = {entry: journal_pythonobj[entry] for entry in journal_pythonobj
                                  if entry in entries_we_need}

    # passing selected fields of journald entries as simple strings (and sorted by their keys)
    # two different entries are separated by empty line
    journal_pythonobj_for_pass_sorted = collections.OrderedDict(sorted(journal_pythonobj_for_pass.items()))
    for key, entry in journal_pythonobj_for_pass_sorted.items():
        print(key, '=', entry)
    print('\n')

    # passing journald entries with selected fields as json objects
    print(json.dumps(journal_pythonobj_for_pass))
    print('\n')
    