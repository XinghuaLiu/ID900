#!/usr/bin/env python3

import sys
import zmq
import socket
import numpy as np


class Statistics:
    """ Simplified Object class for Time Controller's HISTogram
	Class properties :
	- ref : set the blocks which timestamps are from  as reference
	- stop: set the blocks which timestamps are from as stop
	- enab: set the block which timestamps are from as enable
	- data: return all histgram data
	"""

    def __init__(self, parent, index):
        self._parent = parent
        self._id = index
        self._parent.exec("HIST{0}:MIN 0;BWID 100;BCOU 400".format(index))

    def __str__(self):
        return 'hist{0}'.format(self._id)

    @property
    def ref(self):
        return self._parent.exec("HIST{0}:INPO:REF:LINK? ".format(self._id))

    @ref.setter
    def ref(self, ref):
        self._parent.exec("HIST{0}:INPO:REF:LINK {1}".format(self._id, ref))

    @property
    def stop(self):
        return self._parent.exec("HIST{0}:INPO:STOP:LINK? ".format(self._id))

    @stop.setter
    def stop(self, stop):
        self._parent.exec("HIST{0}:INPO:STOP:LINK {1}".format(self._id, stop))

    @property
    def enab(self):
        return self._parent.exec("HIST{0}:ENAB:LINK?".format(self._id))

    @enab.setter
    def enab(self, enab):
        self._parent.exec("HIST{0}:ENAB:LINK {1}".format(self._id, enab))

    @property
    def min(self):
        return self._parent.exec("HIST{0}:MIN?".format(self._id))

    @min.setter
    def min(self, min):
        self._parent.exec("HIST{0}:MIN {1}".format(self._id, min))

    @property
    def bwid(self):
        return self._parent.exec("HIST{0}:BWID?".format(self._id))

    @bwid.setter
    def bwid(self, bwid):
        self._parent.exec("HIST{0}:BWID {1}".format(self._id, bwid))

    @property
    def bcou(self):
        return self._parent.exec("HIST{0}:BCOU?".format(self._id))

    @bcou.setter
    def bcou(self, bcou):
        self._parent.exec("HIST{0}:BCOU {1}".format(self._id, bcou))

    def data(self):
        return self._parent.exec("HIST{0}:DATA?".format(self._id))

    def flush(self):
        return self._parent.exec("HIST{0}:FLUS".format(self._id))

    @property
    def stat(self):
        return self._parent.exec("HIST{0}:STAT?".format(self.id))


class Combiner:
    """Simplified Object class for Time Controller's TSCOmbiners.
	(Provides only minimal feature for Coincidence filtering)
	Class properties:
	  - first : abstract of First Input Port
	  - trigger : abstract of Begin and End window Input Ports
	  - start_delay : time in ps which the start of the window is to be delayed
	  - end_delay : time in ps which the end of the window is to be delayed
	  - window : tupple defining both start_ and end_ delays
      - window_enab : set whether enable the window or not"""

    def __init__(self, parent, index):
        self._parent = parent
        self._id = index
        self._parent.exec(
            "TSCO{0}:WIND:ENAB ON;BEGI:EDGE RISING;:TSCO{0}:WIND:END:EDGE RISING;:TSCO{0}:INPO:SEC:LINK NONE;:TSCO{0}:OPIN ONLYFIR;OPOUt MUTE;".format(
                index))
        self._parent.exec("TSCO{0}:INPO:BEGIN:LINK NONE;:TSCO{0}:INPO:END:LINK NONE;".format(index))

    def __str__(self):
        return 'tsco{0}'.format(self._id)

    @property
    def first(self):
        return self._parent.exec("TSCO{0}:INPO:FIR:LINK?".format(self._id))

    @first.setter
    def first(self, first):
        self._parent.exec("TSCO{0}:INPO:FIR:LINK {1}".format(self._id, str(first)))

    @property
    def trigger(self):
        return self._parent.exec("TSCO{0}:INPO:BEGIN:LINK?".format(self._id))

    @trigger.setter
    def trigger(self, trigger):
        self._parent.exec("TSCO{0}:INPO:BEGIN:LINK {1};:TSCO{0}:INPO:END:LINK {1};".format(self._id, str(trigger)))

    @property
    def start_delay(self):
        return self._parent.exec("TSCO{0}:WIND:BEGIN:DELAY?".format(self._id))

    @start_delay.setter
    def start_delay(self, delay):
        self._parent.exec("TSCO{0}:WIND:BEGIN:DELAY {1}".format(self._id, delay))

    @property
    def end_delay(self):
        return self._parent.exec("TSCO{0}:WIND:END:DELAY?".format(self._id))

    @end_delay.setter
    def end_delay(self, delay):
        self._parent.exec("TSCO{0}:WIND:END:DELAY {1}".format(self._id, delay))

    @property
    def window(self):
        return (self.start_delay, self.end_delay)

    @window.setter
    def window(self, window_def):
        self.start_delay = window_def[0]
        self.end_delay = window_def[1]

    @property
    def opinionin(self):
        return self._parent.exec("TSCO{0}:OPIN?".format(self._id))

    @opinionin.setter
    def opinionin(self, opin):
        self._parent.exec("TSCO{0}:OPIN {1}".format(self._id, opin))

    @property
    def opinionout(self):
        return self._parent.exec("TSCO{0}:OPOU?".format(self._id))

    @opinionout.setter
    def opinionout(self, opout):
        self._parent.exec("TSCO{0}:OPOU {1}".format(self._id, opout))

    @property
    def window_enab(self):
        return self._parent.exec("TSCO{0}:WIND:ENAB?".format(self._id))

    @window_enab.setter
    def window_enab(self, enab):
        self._parent.exec("TSCO{0}:WIND:ENAB {1}".format(self._id, enab))


class Input:
    """Simplified Object class for Time Controller's INPUt unit.
	(Provides only minimal feature for Coincidence filtering)
	Class properties:
	  - ENABle (on/off) enable/disable Input Port
	  - COUPLing (AC/DC): set AC/DC coupling of input
	  - EDGE (RISing/ FALLing): set discriminator edges
	  - THREshold (V): Discriminator threshold (-2V to 2V)
	  - DELAY (ps): select the input delay
	  - SELEct (unshaped/ Shaped/ Optput/LOOP ) not implemented in this class/ refer to the original manual
	  - MODE (HIRES|LOWERS) select whether high resolution or high speed mode
	  - STATe state of the block
	  """

    # set the initial state of the INPU {enable, DC couple, Rising, 500mV, Delay 0, MODE: LOWERS}
    def __init__(self, parent, index):
        self._parent = parent
        self._id = index
        self._parent.exec(
            "INPU{0}:ENAB ON;COUP DC;EDGE RISI;DELAY 0;MODE LOWRES;".format(
                index))

    def __str__(self):
        return 'inpu{0}'.format(self._id)

    @property
    def enab(self):
        return self._parent.exec("INPU{0}:ENAB?".format(self._id))

    @enab.setter
    def enab(self, enab):
        self._parent.exec("INPU{0}:ENAB {1}".format(self._id, enab))

    @property
    def counter(self):
        return self._parent.exec("INPU{0}:COUN?".format(self._id))

    @property
    def coup(self):
        return self._parent.exec("INPU{0}:COUP?".format(self._id))

    @coup.setter
    def coup(self, coup):
        self._parent.exec("INPU{0}:COUP {2}".format(self._id, coup))

    @property
    def edge(self):
        return self._parent.exec("INPU{0}:EDGE?".format(self._id))

    @edge.setter
    def edge(self, edge):
        self._parent.exec("INPU{0}:EDGE:{1}".format(self._id, edge))

    @property
    def threshold(self):
        return self._parent.exec("INPU{0}:THRE?".format(self._id))

    @threshold.setter
    def threshold(self, threshold):
        self._parent.exec("INPU{0}:THRE {1}".format(self._id, threshold))

    @property
    def delay(self):
        return self._parent.exec("INPU{0}:DELAY?".format(self._id))

    @delay.setter
    def delay(self, delay):
        self._parent.exec("INPU{0}:DLEAY {1}".format(self._id, delay))

    @property
    def mode(self):
        return self._parent.exec("INPU{0}:MODE?".format(self._id))

    @mode.setter
    def mode(self, mode):
        self._parent.exec("INPU{0}:MODE {1}".format(self._id, mode))

    @property
    def state(self):
        return self._parent.exec("INPU{0}:STAT?".format(self._id))


class ScpiCommander:
    """ Helper to send SCPI commands"""

    def __init__(self, address):
        self._context = zmq.Context()
        self.zmq = self._context.socket(zmq.REQ)
        self.zmq.connect('tcp://' + address + ':' + '5555')

    def exec(self, cmd):
        self.zmq.send_string(cmd)
        ans = self.zmq.recv().decode('utf-8')
        return ans


class ID900:
    """Object class for ID900"""

    def __init__(self, ipAddr):
        # Init connection to ID900
        self.scpi = ScpiCommander(ipAddr)
        self.inpu = {}
        self.tsco = {}
        self.hist = {}
        # Configure common settings for TSCOs
        for i in range(1, 5):
            self.inpu[i] = Input(self.scpi, i)
        for i in range(1, 25):
            self.tsco[i] = Combiner(self.scpi, i)
        for i in range(1, 5):
            self.hist[i] = Statistics(self.scpi, i)

    def flushHIST(self):
        for i in range(1, 5):
            self.hist[i].flush()

    def enabSampling(self, acquisition_time):
        self.scpi.exec("TSGE8:ENAB OFF")
        self.scpi.exec("TSGE8:ONES:PWID %d" % (acquisition_time * 1e12))
        self.scpi.exec("TSGE8:ENAB ON")

    # configuration connections for two fold coincidence between inpu1 & inpu2 winthin window (ps)
    def config2foldCoincidence(self, window):
        # config connections for tsco5
        self.tsco[5].first = self.inpu[1]
        self.tsco[5].opinionin = 'ONLYFIR'
        self.tsco[5].opinionout = 'ONLYFIR'
        self.tsco[5].window_enab = 'OFF'
        # config connections for tsco6
        self.tsco[6].first = self.inpu[2]
        self.tsco[6].opinionin = 'ONLYFIR'
        self.tsco[6].opinionout = 'ONLYFIR'
        self.tsco[6].window_enab = 'OFF'

        # config HIST connection
        self.hist[1].ref = self.tsco[5]
        self.hist[1].stop = self.tsco[6]
        self.hist[1].enab = 'tsge8'

        self.hist[2].ref = self.tsco[6]
        self.hist[2].stop = self.tsco[5]
        self.hist[2].enab = 'tsge8'

    def setEventGenAsDelay(self, ev, delay):
        # Use TSGE1 for INPUt1 delay, TSGE2 for INPU2, etc...
        self.scpi.exec(
            "TSGE{0}:ENAB ON;:TSGE{0}:TRIG:INPO:LINK INPU{1};:TSGE{0}:MODE SPULSE;TRIG:MODE INPORT;DELAY {2};:TSGE{0}:SPUL:PWID 4000;".format(
                ev, ev, delay))

    def setInputDelay(self, num, delay):
        # Use for set input[num] for specific delay
        self.inpu[num].delay = delay

    def config3foldCoincidence(self, d2, w2, d3, w3):
        # configure Event Generators as delay, use t_process as delay value
        tp = max(d2 + w2, d3 + w3)  # compute t_process as the latest end of window
        w1 = 1  # window for trigger event must be non-null
        for g in range(1, 4):
            self.setEventGenAsDelay(g, tp)

        # route first level of TSCO
        self.tsco[1].first = 'inpu1'  # TSCO1.input = 1
        self.tsco[2].first = 'inpu2'  # TSCO2.input = 2
        self.tsco[3].first = 'inpu3'  # TSCO3.input = 3

        self.tsco[5].first = 'tsge1'  # TSCO5.input = 1'
        self.tsco[6].first = 'tsge2'  # TSCO6.input = 2'
        self.tsco[7].first = 'tsge3'  # TSCO7.input = 3'
        self.tsco[8].first = 'tsge1'
        # configure filtering of first level of TSCO
        self.tsco[2].trigger = 'inpu1'  # TSCO2.output = 2/1
        self.tsco[3].trigger = 'inpu1'  # TSCO3.output = 3/1
        self.tsco[5].trigger = 'inpu2'  # TSCO5.output = 1'/2
        self.tsco[6].trigger = 'inpu1'  # TSCO6.output = 2'/1
        self.tsco[7].trigger = 'inpu1'  # TSCO7.output = 3'/1
        self.tsco[8].trigger = 'inpu3'  # TSCO8.output = 1'/3
        # configure window size of first level of TSCO
        self.tsco[2].window = (d2, d2 + w2 + w1)
        self.tsco[3].window = (d3, d3 + w3 + w1)

        self.tsco[5].window = (tp - d2 - w2, tp - d2 + w1)
        self.tsco[6].window = (tp + d2, tp + d2 + w2 + w1)
        self.tsco[7].window = (tp + d3, tp + d3 + w3 + w1)
        self.tsco[8].window = (tp - d3 - w3, tp - d3 + w1)
        # route second level of TSCO
        self.tsco[9].first = self.tsco[5]  # TSCO9.input  = 1'/2
        self.tsco[10].first = self.tsco[6]  # TSCO10.input = 2'/1
        self.tsco[11].first = self.tsco[7]  # TSCO11.input = 3'/1

        # configure filtering of second level of TSCO
        self.tsco[9].trigger = self.tsco[3]  # TSCO9.trigger  = 3/1
        self.tsco[10].trigger = self.tsco[3]  # TSCO10.trigger = 3/1
        self.tsco[11].trigger = self.tsco[2]  # TSCO11.trigger = 2/1

        # configure window size of second level of TSCO
        self.tsco[9].window = (tp - d3 - w3, tp - d3 + w1)
        self.tsco[10].window = (tp - d3 - w3 + d2, tp - d3 + d2 + w2 + 1)
        self.tsco[11].window = (tp + d3 - d2 - w2, tp + d3 - d2 + w3)
        # config hist
        self.hist[1].ref = self.tsco[5]
        self.hist[1].stop = self.tsco[6]
        self.hist[1].enab = 'tsge8'
        self.hist[2].ref = self.tsco[8]
        self.hist[2].stop = self.tsco[7]
        self.hist[2].enab = 'tsge8'
        self.hist[3].ref = self.tsco[9]
        self.hist[3].stop = self.tsco[10]
        self.hist[3].enab = 'tsge8'
        self.hist[4].stop = self.tsco[2]
        self.hist[4].enab = 'tsge8'

    # get hist data from 1 to num in np array
    def histdata(self, num):

        data = {}
        for i in range(1, num + 1):
            data[i] = eval(self.hist[i].data())
        return data
