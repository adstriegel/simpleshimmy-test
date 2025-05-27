# Overview / Goals Document

The focus of this initial verison is to explore the extent that we can construct well-formed timing sequences and to iterate on various encoding and security mechanisms that are part of the _simpleshimmy_ tool.

## Sub-Directories

* v0 - Base Directory that we will use for testing / various concepts
* v0 / docs
* v0 / server / python
* v0 / client / python

## Rationale

For our various sets of WiFi testing (and to some extent cellular), we need the ability to be able to inject particular timing waveforms.  Previously, we had code via ScaleBox and FMNC that would ride on top of TCP.  We needed TCP specifically because we wanted to be able to deploy to mobile nodes as well as to conduct various live demos (e.g. make a web get / operate within the web get).

Our goal is to get back there eventually but in the short term, we need ways to be able to deliver controlled packet sending whereby we can control the bursts, size, and timing of the various packets.

To that end, we will be building up a UDP solution whereby a client can send requests to generate various packet sequences (aka a packet train).  However, we do need to prototype and figure out how exactly we should format said requests, the extent to which we can accurately control the resulting sequences, and how we keep the overall system itself reasonably secure and safe from malicious usage.

The focus will be to build up the simpleshimmy prototype.  The name shimmy comes from the shimmy that a dog does to dry off and given that this is a UDP-focused version, it is dubbed simpleshimmy.  The package itself will be in a repository named simpleshimmy-test and this will be the zero version or base version.  The repository itself is fully public but the code contained within the repository will be viewed as pure prototype code.

## System Properties

The system will have the following characteristics:
* A client will connect to the server, possibly presenting some sort of credentials or authorization.
   * Options for both secure and insecure options should be provided though the insecure option should have controls limiting maximum rates or simultaneous clients.
* The client will make a request to the server for the desired packet timing sequence(s) whereby the sequence encoding length is minimized so as to afford containment within a single packet.
   * In an ideal world, authorization and the request all fit within a single packet.
   * Multiple versions of encoding may exist for the purposes of being human readable versus optimized for size.
   * Initial versions may presume that such information must be contained within a single packet.
* The packet sequence or packet train represents a set of packets that will be sent by the server to the client.
   * A packet train consists of a series of packets.  Each packet is a particular length (ideally less than MTU) with a specified time gap between each packet.  Packets may be sent in bursts (no time between packets).
   * Packet trains may be repeated and packet lengths and gaps may vary with all packets in the train.
   * A train may be set to be sent after a small delay or at a specific wall clock time (start of packets).
   * Packets when sent should contain appropriate identifiers with respect to which packet in the sequence that the packet is associated with.  Such information should occur as early in the payload as possible.
* The server will transmit the packet train as requested by the client using the  established UDP socket.
* The client should create a set of output files that adequately captures when each individual packet was received and the order that said packet was received in.
* The server should also create a set of output files that adequately captures when the packets were sent.
* New packet trains or sequences will require the establishment of a new UDP flow.
* Configuration files for the client or server should be easy to edit.
* Optional: The client should have the ability to send an ACK-like packet to the server at a ratio determined by an input parameter (e.g. ACK every 1 packet, every 2 packets, etc.).
   * In the event that a client is selected to ACK, the server should record when the ACK was received.
* Similarly, the client should also record when it logged the packets.

The initial version of the code will be written in Python.  Improved versions may continue to build on that same code or may create alternate versions.

A shell script wrapper should be created that allows for the invocation of the code allowing a default or test operation.  An ex directory may contain a set of example files for the purpose testing.

## Basic Packet Sequences

* Send a set of packets with a fixed size and gap
* Send 10 packets each of 1000 bytes with a gap of 10 milliseconds between
* Send 5 packets of 1000 bytes, 10 ms gap, 5 packets of 1100 bytes, 10 ms gap
* Allow for packets to be burst
* Send 3 packets of 1000 bytes with no gap, 30 ms gap, 3 packets of 1000 bytes with no gap

## Advanced Packet Sequences

* Send 20 packets of 1250 bytes with a gap of 100 ms, 20 packets of 1250 bytes with a gap of 90 ms, repeating until the gap is only 10 ms
* Burst for a total of 4.5k bytes staying under MTU with a gap of 25 ms

## Hardening

* Basic checks with respect to correct arguments should be added
* Checks should also be added along with appropriate error reporting as to the liveness of the server

## Initial Testing

* The server can be tested initially using localhost.  Once the client seems to be robust, ns-mn1.cse.nd.edu can be used for testing.

# Output

* An example output should be provided to the user and the console

# Confirmation

* Use tcpdump and / or Wireshark to confirm correct timing for the packets as sent by the server.
* To what extent can we have unit testing for confirmation?