---
date: '2026-06-05'
layout: single
permalink: /posts/2026/06/the-3-major-ways-of-reading-data-on-a-chip/
tags:
- embedded
title: The 3 Major Ways Of Reading Data On A Chip
tags:
  - embedded-systems
  - hardware
---


Let’s get straight to the damn point. When it comes to MCUs, there are three major ways of reading data from peripherals: Polling, Interrupts, and DMA. Every embedded system you’ll ever touch will rely on one or more of these mechanisms. The difference between them fundamentally comes down to one thing: who is responsible for noticing that data is ready?

Depending on the answer, your system’s CPU usage, latency, determinism, power consumption, and overall complexity change dramatically.

For this article, let’s use a simple example throughout: an IR sensor connected to an MCU via ADC, continuously producing readings that the firmware needs to process.

---

# Polling

Polling is the simplest possible approach. The CPU repeatedly checks whether a peripheral has data ready. Nothing happens automatically here. No hardware-driven notifications exist. The processor simply keeps asking the peripheral if data is available until eventually the answer becomes yes, at which point the CPU manually reads the data.

In practice, polling usually looks like a tight infinite loop where the MCU continuously checks hardware status flags. In the case of an IR sensor, the MCU starts an ADC conversion, repeatedly checks whether the conversion has completed, reads the ADC value once the conversion is done, processes the sensor output, and then repeats the entire process forever.

The biggest characteristic of polling is its CPU usage. The processor remains occupied checking flags even when nothing useful is happening. This makes polling extremely wasteful in terms of computational efficiency and power consumption, since the CPU cannot sleep while it continuously monitors peripherals.

That said, polling is also extremely simple. The execution flow is linear, predictable, and easy to debug. There is no asynchronous behavior, no interrupt context switching, and no complicated synchronization concerns. This is why polling is often the very first mechanism beginners learn in embedded systems.

Polling can actually be fairly deterministic in small bare-metal systems because the control flow is entirely under software control. However, it scales poorly. As the number of peripherals increases, the CPU spends more and more time simply checking whether something happened.

For an IR sensor, a polling-based implementation would involve manually starting ADC conversions and spinning in a loop until the ADC completion flag is set. During this waiting period, the CPU performs no useful work. It simply burns cycles waiting for hardware.

---

# Interrupts

Interrupts fundamentally change the control flow of the system. Instead of the CPU constantly asking whether data is ready, the peripheral itself notifies the CPU when something important happens.

In simple terms, the hardware effectively taps the processor on the shoulder and says: “Stop what you’re doing for a second. I have something for you.”

When this happens, the CPU temporarily pauses normal execution and jumps into a special function called an Interrupt Service Routine, or ISR. Once the ISR completes, the processor resumes whatever it was doing before the interrupt occurred.

In an IR sensor scenario, the ADC would complete its conversion and automatically raise an interrupt. The CPU would then briefly enter the ISR, read the ADC value, store or process the data, and return to normal execution. Unlike polling, the CPU does not waste time continuously checking status flags.

On ARM Cortex-M systems, much of this process is handled automatically by hardware. The NVIC receives the interrupt request, the processor automatically saves its execution context, executes the ISR, and restores the previous state afterward. This hardware support is one of the reasons Cortex-M microcontrollers are so effective for real-time embedded systems.

Interrupts drastically reduce CPU usage compared to polling because the processor only reacts when necessary. They also provide significantly lower latency, often allowing responses within microseconds depending on system configuration and interrupt priorities.

However, interrupts introduce complexity. Firmware execution is no longer purely linear. Asynchronous behavior enters the system, which means developers now need to think about shared resources, volatile variables, synchronization, race conditions, and interrupt priorities.

ISR design itself becomes extremely important. Good ISRs are meant to execute quickly and return immediately. Heavy computation, blocking operations, dynamic memory allocation, and functions like printf are generally avoided inside interrupt handlers. In most well-designed systems, the ISR simply captures the data, sets a flag, and exits, leaving heavier processing for the main loop or RTOS tasks.

For the IR sensor example, the ADC interrupt handler would simply read the sensor value and notify the main application that fresh data is available. The CPU remains free the rest of the time to execute other tasks or enter low-power states.

---

# DMA

DMA, or Direct Memory Access, takes things a step further. With DMA, the CPU is removed from the actual data transfer process almost entirely.

Instead of the processor manually moving data between peripherals and memory, a dedicated DMA controller performs the transfers independently. The CPU simply configures the DMA engine and lets it operate autonomously.

Without DMA, the typical data path looks like this:
Peripheral → CPU → Memory

With DMA, the CPU is bypassed:
Peripheral → Memory

This distinction becomes incredibly important in systems handling large or continuous streams of data.

In the case of an IR sensor being sampled continuously at high speed, manually servicing every ADC conversion through interrupts would eventually become inefficient. Instead, the ADC can be configured to work alongside DMA so that every sensor sample is automatically transferred into a memory buffer without CPU involvement.

The processor only wakes up occasionally, such as when an entire buffer has been filled and is ready for processing. This massively reduces CPU overhead and interrupt frequency.

DMA is therefore extremely efficient in terms of CPU usage, throughput, and power consumption. It is heavily used in high-speed embedded applications such as ADC sampling, UART reception, SPI communication, audio streaming, networking, and camera interfaces.

However, DMA also introduces the highest level of complexity among the three approaches. Developers now need to manage memory buffers, synchronization between software and hardware, circular buffering modes, cache coherency concerns on advanced systems, and transfer completion events.

Many DMA systems support operating modes such as normal mode, where transfers stop after completion, and circular mode, where the DMA continuously wraps around the same buffer indefinitely. Circular mode is especially common in sensor sampling and streaming applications because it enables uninterrupted continuous acquisition.

For the IR sensor example, DMA allows ADC samples to stream directly into RAM continuously while the CPU remains almost completely uninvolved. The processor simply processes batches of samples whenever required instead of handling each individual conversion.

---

# Comparing the Three

Polling is simple but inefficient. The CPU remains constantly involved, continuously checking peripherals even when nothing happens. It works well for tiny systems and quick prototypes, but becomes wasteful and un-scalable as system complexity grows.

Interrupts improve efficiency dramatically by making peripherals event-driven. The CPU only reacts when necessary, which reduces wasted cycles and improves responsiveness. However, interrupts introduce asynchronous execution and synchronization complexity.

DMA pushes efficiency even further by removing the CPU from the transfer path itself. This allows high-throughput and continuous data movement with minimal processor involvement, making DMA ideal for real-time streaming applications. The tradeoff is significantly higher implementation complexity.

---

# Final Thought

Polling, Interrupts, and DMA are not competing ideas. They are progressively more sophisticated mechanisms for handling peripheral communication.

Most real embedded systems use all three simultaneously. A firmware stack might poll simple GPIO states, use interrupts for UART events or button presses, and rely on DMA for ADC streams, networking, or audio pipelines.

The real skill in embedded engineering is not just knowing how these mechanisms work, but understanding when the added complexity is actually justified.