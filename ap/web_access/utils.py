from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from netaddr import EUI, IPAddress, mac_unix

from .models import WebRequest
from django.conf import settings

import datetime
import re
import socket
import subprocess

"""
This module contains web-access request specific Python functions for
communicating with the firewall.
"""


def _sendRaw(eui, minutes):
    """ Allows internet access on device with MAC address for some minutes

        Sends a string over a TCP socket to the firewall. Must be run on server
        accepted by firewall.
    """
    if not isinstance(eui, EUI):
        raise ValueError("Expected eui to be of type EUI")
    if not isinstance(minutes, int):
        raise ValueError("Expected minutes to be int")
    eui.dialect = mac_unix
    eui.dialect.word_fmt = "%.2X"
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.settimeout(1.0)
    soc.connect((settings.HOST, settings.PORT))
    soc.sendall("%s %d" % (str(eui), minutes))
    soc.close()


def _getEUI(ipAddress, mac=""):
    """ Returns EUI from IPAddress """
    if not isinstance(ipAddress, IPAddress):
        raise ValueError("Expected ipAddress to be of type netaddr.IPAddress")
    if mac == "":
        proc = subprocess.Popen(["arp", "-n", str(ipAddress)], stdout=subprocess.PIPE)
        result = proc.communicate()[0]
        # Matches MAC address
        matches = re.search('\s([a-zA-Z0-9]{1,2}(?::[a-zA-Z0-9]{1,2}){5})\s', result, re.MULTILINE)
        if matches is None:
            return None
        mac = matches.group(1)
    eui = EUI(mac)
    eui.dialect = mac_unix
    eui.dialect.word_fmt = "%.2X"
    return eui


def _getIPAddress(request):
    """ Returns IPAddress """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "") or request.META.get("REMOTE_ADDR")
    return IPAddress(x_forwarded_for.split(',')[0])


def startAccess(request, minutes, id):
    ipAddress = _getIPAddress(request)
    eui = _getEUI(ipAddress)
    if not eui:
        message = "Unable to get internet access. Could not get EUI from IP Address %s." % ipAddress
        messages.add_message(request, messages.ERROR, message)
    else:
        _sendRaw(eui, int(minutes))
        message = "Web accesss granted for %s minutes." % minutes
        messages.add_message(request, messages.SUCCESS, message)
        webRequest = get_object_or_404(WebRequest, pk=id)
        webRequest.time_started = datetime.datetime.now()
        webRequest.save()
    return redirect('web_access:web_access-list')
