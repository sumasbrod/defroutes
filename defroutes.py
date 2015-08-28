#!/usr/local/bin/python
import sys
import os
import re
import time

"""
Default routes module for FreeBSD systems
"""

new_def_route = "192.168.100.1"
def_route_get_command = "netstat -rn | grep default"
def_route_set_command = "route change default {0}"
def_route_add_command = "route add default {0}"
regex_string = "(?P<match>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})"
def_route_file = "/var/tmp/defroute.old"
log_file = "/var/log/defroutes.log"

def get_current_def_route():
    try:
        log_activity("Getting current default route")
        res = os.popen(def_route_get_command)
        line = res.readline()
        res.close()
        if len(line) > 0:
            regex = re.compile(regex_string)
            matches = regex.search(line).groupdict()
            log_activity("Current route is {0}".format(matches['match']))
            return matches['match']
        else:
            log_activity("Current route is nothing!")
            return None
    except IOError as err:
        log_activity("I/O error({0}): {1}".format(err.errno, err.strerror))

def get_old_def_route():
    try:
        log_activity("Getting old route")
        _in = open(def_route_file)
        line = _in.readline()
        _in.close()
        if len(line) > 0:
            log_activity("Old route is {0}".format(line))
            return line
        else:
            log_activity("There is no old route in {0} file".format(def_route_file))
            return None
    except IOError as err:
        log_activity("I/O error({0}): {1}".format(err.errno, err.strerror))

def log_activity(message):
    try:
        log = open(log_file, "a")
        logstring = "{0} - {1}".format(time.strftime("%d.%m.%y %H:%M:%S"), message)
        log.write(logstring + '\n')
        log.close()
    except IOError as err:
        print("I/O error({0}): {1}".format(err.errno, err.strerror))
    
def set_default_route(route):
    try:
        log_activity("Setting default route to {0}".format(route))
        command = def_route_set_command.format(route)
        res = os.popen(command)
        line = res.readline()
        if len(line) > 0:
            #need to process change add cases
            log_activity("Result of setting route is: {0}".format(line))
        else:
            log_activity("There are errors in setting route.")
    except IOError as err:
        log_activity("I/O error({0}): {1}".format(err.errno, err.strerror))

def save_def_route(route):
    try:
        log_activity("Saving route to {0}".format(def_route_file))
        _out = open(def_route_file, "w")
        _out.write(route)
    except IOError as err:
        log_activity("I/O error({0}): {1}".format(err.errno, err.strerror))
    finally:
        _out.close()

def set_new_default_route():
    log_activity("Set new default route call...")
    old_def_route = get_current_def_route()
    save_def_route(old_def_route)
    set_default_route(new_def_route)

def set_old_default_route():
    log_activity("Set old default route call...")
    old_def_route = get_old_def_route()
    set_default_route(old_def_route)

