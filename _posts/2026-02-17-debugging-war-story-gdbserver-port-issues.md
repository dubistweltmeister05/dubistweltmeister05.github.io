---
title: 'Debugging War Story - GDBServer and Port Issues'
date: 2026-02-17
permalink: /posts/2026/02/debugging-war-story-gdbserver-port-issues/
tags:
  - debugging
  - gdbserver
  - embedded-systems
---

So, I was working at my office early in the morning. We work on STM32 boards, and while I was trying to flash my code to the board that we have, I got hit by the following error - 

```
Failed to bind to port 61235, error code -1: No such file or directory 
Failure starting SWV server on TCP port: 61235 
Failed to bind to port 61234, error code -1: No such file or directory 
Failure starting GDB server: TCP port 61234 not available. 
Shutting down... Exit.
```

The IDE's error log declared the following -
```
Error in final launch sequence: 

Failed to start GDB server 
Failed to start GDB server 
Error in initializing ST-LINK device. 
Reason: (0) Unknown. Please check power and cabling to target.
```

Now, I thought that my MCU was cooked. I am a firmware engineer after all, we have a very bad habit of assuming the fucking worst in all situations where things don't go as planned. But before I lamented my fate any more, I decided to try and give it another go, but this time via the STM32CubeProgrammer. 

I hit connect on the debugger, navigated to my elf file, and pressed start programming....and voila! Everything works just fucking fine. My MCU was indeed NOT cooked after all.

Now, this got me thinking -  why the hell did it not flash when I hit the run button on my IDE??

ChatGPT turned out to be useless as usual. It tried telling me that I have an issue with a pending task on my laptop, but little did it know - I booted the thing barely 7 mins ago and this upload was the first thing I tried to do at work!

So, we went the old fashioned way - googling things for real and diving into blogs and stack overflow. One of the fixes was that I could simply change the port at which my GDB server was running at, which seemed plausible. Plus, it looked to be quite simple to do, and I was starting to get anxious. "Well, there's no harm in trying" I said to myself, and 30 seconds later, I opened my DEBUG config on the STM32CUBEIDE, and under the debugger settings, I reconfigured the `GDBserver` to run on the port 41234. I hit apply and close, anddd.........BOOM, it ran like nothing ever happened! 

This got me thinking tho, what the hell is a `GDBServer` and why does it need to run on a port? Also, that sounds awfully like a network connection, could it be UDP, TCP, or something of similar nature? I was extremely confused, but interested to read more. And as the internet often does - my curiosity was rewarded with more and more blogs! Like the one you are reading now!

So, here is what I have learnt about `GDBServer` on the UNIX machines (Thank ). 

`gdbserver` is a control program for Unix-like systems, which allows you to connect your program with a remote GDB via `target remote`---but without linking in the usual debugging stub.

`gdbserver` is not a complete replacement for the debugging stubs, because it requires essentially the same operating-system facilities that GDB itself does. In fact, a system that can run `gdbserver` to connect to a remote GDB could also run GDB locally! `gdbserver` is sometimes useful nevertheless, because it is a much smaller program than GDB itself. It is also easier to port than all of GDB, so you may be able to get started more quickly on a new system by using `gdbserver`. Finally, if you develop code for real-time systems, you may find that the tradeoffs involved in real-time operation make it more convenient to do as much development work as possible on another system, for example by cross-compiling. You can use `gdbserver` to make a similar choice for debugging.

GDB and `gdbserver` communicate via either a serial line or a TCP connection, using the standard GDB remote serial protocol. 

On the target machine, we run the `gdbserver` with the program that we wish to debug. We do this with a specification of the way that we wish to connect to the host machine - that would be the port on which we are connecting to the host machine. The `GDBServer` starts the **process** that we've loaded onto the target machine, and then simply waits for the connection with `GDB`.

On the host, we need to have GDB with an unstripped copy of the same program. This basically means that the C program retains the debug info and the symbol tables - things like, source file paths, number mappings, etc. These things are what helps GDB when we debug. Ever wondered how does gcc help us out with the exact line number of the code that we have fucked up at? That's how. `GDBserver` has a `target remote` command, which specifies the port for connecting to the remote. 

Everything described above applies to Unix/Linux systems. In embedded systems like STM32, the MCU cannot run `gdbserver` itself, so this role is implemented by a host-side debug proxy such as `ST-LINK_gdbserver`.

In that case, here is what happens. The thing is a middleman, okay? It interacts with the `GDB` on the host PC, and the actual MCU's firmware. It listens to the `GDB` connections on a TCP port, and speaks the Remote Serial Protocol. It'll convert these commands and signals into signals that are compatible with the SWD or the JTAG interface, which is the hardware that connects with the MCU. 

So, the conclusion of the war story of mine - GDB and GDB server is something that runs on the host machine itself. They speak to each other via TCP, and for that, we need to connect via a common port. Most likely, a stale or crashed GDB server process was still holding onto the default port, which led to me not being able to flash code and debug the MCU. My initial assumption of the MCU being fried, was so far from the truth! 

Anyway, this is something that I wanted to share and put out in the world. Do let me know if my understanding is flawed or flat-out wrong! Thank you for reading this far.

