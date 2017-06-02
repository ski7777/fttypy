#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import threading
from .tx_serial import *
from .CommandCodes import *


class ftTX():

    def __init__(self, dev):
        self.data_lock = threading.Lock()
        self.data = {}

        self.connection = TXSerial(dev)

    def createTA(self, ta):
        new_ta = {}
        new_ta["io_config"] = {}
        new_ta["input_data"] = []
        for _ in range(8):
            new_ta["input_data"].append(0)
        new_ta["output_data"] = []
        for _ in range(8):
            new_ta["output_data"].append({})

        self.data_lock.acquire()
        self.data[ta] = new_ta
        self.data_lock.release()

    def getName(self):
        """
        get name of the TX-C
        """
        # execute CMD on TX-C
        data = self.connection.executeCMD("type /flash/sys_par.ini")
        # grep specific line from data
        for line in data:
            if "hostname"in line:
                return(line.split("hostname = ")[1])
        return(None)

    def getVersion(self):
        """
        get TX-C Firmware version
        """
        # execute CMD on TX-C and grep data
        data = self.connection.executeCMD("version")
        return(data[0].split("V ")[1])

    def getPrograms(self):
        """
        get programs in flash of TX-C
        """
        # execute CMD on TX-C
        data = self.connection.executeCMD("dir /flash")
        programs = []
        # grep sepecific lines
        for line in data:
            if ".bin" in line:
                programs.append(line.split("  ")[1].split(".bin")[0])
        return(programs)

    def loadProgram(self, name):
        """
        Load a program from flsh by name
        """
        # execute CMD on TX-C
        # the load cmd does not return anything so we don´t need the serial data
        self.connection.executeCMD("load /flash/" + name + ".bin")

    def runProgram(self):
        """
        Run a loaded program
        """
        # execute CMD on TX-C
        # the run cmd does not return anything so we don´t need the serial data
        self.connection.executeCMD("run")

    def stopProgram(self):
        """
        Stop a running program
        """
        # execute CMD on TX-C
        # the stop cmd does not return anything so we don´t need the serial data
        self.connection.executeCMD("stop")
