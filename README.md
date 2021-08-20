# This package contains the python classes for controlling and sampling with the Swiss Quantum ID900-MASTER Time Controller. 
 The IQ900 master provides the time-correlated single-photon counting (TCSPC), give you posibility of time tagging, counting and histrogram. The hardware platform also contains a fast speed Field-Programable Gating Array (FPGA), which is progammed using the Python package.
 
 Here we mainly define four classes that correspond to four different logical blocks inside the FPGA hardware namely, Input, Generator, Combiner, Histogram. Inside every class are defined the various properties. The first line asks for the output from the device and the second line it sets the inout for the input device. 
 
 # Input() - 
 Simplified Object class for Time Controller's INPUt unit.
	
	Class properties:
	  - ENABle (on/off) enable/disable Input Port
	  - COUPLing (AC/DC): set AC/DC coupling of input
	  - EDGE (RISing/ FALLing): set discriminator edges
	  - THREshold (V): Discriminator threshold (-2V to 2V)
	  - DELAY (ps): select the input delay
	  - SELEct (unshaped/ Shaped/ Optput/LOOP ) not implemented in this class/ refer to the original manual
	  - MODE (HIRES|LOWERS) select whether high resolution or high speed mode
	  - STATe state of the block
 # Generator() - 
 # Combiner() - 
 Simplified Object class for Time Controller's TSCOmbiners. (Provides only minimal feature for Coincidence filtering)
	
	Class properties:
	  - first : abstract of First Input Port
	  - trigger : abstract of Begin and End window Input Ports
	  - start_delay : time in ps which the start of the window is to be delayed
	  - end_delay : time in ps which the end of the window is to be delayed
	  - window : tupple defining both start_ and end_ delays
 # Statistics() - 
 Simplified Object class for Time Controller's HISTogram
	
	Class properties :
	- ref : set the blocks which timestamps are from  as reference
	- stop: set the blocks which timestamps are from as stop
	- enab: set the block which timestamps are from as enable
	- data: return all histgram data
 

The communication are based on ZeroMQ package, the official website of ZMQ is https://zeromq.org/.   
