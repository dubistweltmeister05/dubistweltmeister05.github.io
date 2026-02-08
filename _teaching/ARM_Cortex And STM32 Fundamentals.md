---
title: "PICT 2026 - Lecture 01: ARM Cortex and STM32 Fundamentals"
collection: teaching
type: "Workshop Series"
permalink: /teaching/PICT-2026-lecture-01
venue: "PICT, Pune"
date: 2026-01-15
location: "Pune, India"
---

# ARM Cortex and STM32 Fundamentals

## Materials

### 📊 Slides
- [Download Slides (PPTX)](/files/PICT-2026/lecture-01/lec-1.pptx)

### 🎥 Video Recording
- [Watch on YouTube](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

---

# Content

- ## What is ARM and why is it split into **A / R / M** instead of “one CPU for everything”
    ARM is a British company that designs and licenses Architecture for a wide range of CPUs. But before we take a closer look at them, let's understand the NEED for what it is based on - the RISC arch.    
    
    RISC architecture of computing is inherently designed to simplify the individual instructions given to the computer to accomplish tasks. The goal is to offset the need to process more instructions by increasing the speed of each instruction, in particular by implementing an instruction pipeline, which may be simpler to achieve given simpler instructions.
    
    Compared to the Complex Instruction Set Computer (CISC), a RISC computer might require more machine code in order to accomplish a task because the individual instructions perform simpler operations. 
       
    The key operational concept of the RISC computer is that each instruction performs only one function (e.g., copy a value from memory to a register). The RISC computer usually has many (16 or 32) high-speed, general-purpose registers with a load–store architecture in which the instructions that perform arithmetic and tests operate only on the registers, and the instructions that access data in the main memory of the computer only load data from memory into registers or store data from registers into memory. 
    
    The design of the CPU allows RISC computers few simple addressing modes and predictable instruction times that simplify design of the system as a whole.
    
	ARM (Acorn RISC Machines / Advanced RICS Machines), is an implementation of this philosophy.
	
	Unlike Intel or AMD, ARM does not manufacture chips. Instead, it creates **CPU blueprints** that other companies license and integrate into their own silicon. This model allows ARM architectures to appear in a vast range of products, from tiny microcontrollers to high-performance application processors.
	
	Primarily, the ARM solutions are dedicated towards -
	- system-on-chips architecture-built products. Here, the core systems are integrated, and any customization is left to the end user.  
	- system-on-modules architecture-built products. Here, the customization is shifted onto the chip, converting it to a MODULE. This is done primarily to save time and is essentially - "pay, plug, and play".
	
	However, ARM’s customers needed processors with **very different guarantees**. Some systems needed virtual memory and rich operating systems. Others needed strict real-time behavior with zero tolerance for missed deadlines. Others needed ultra-low power and extreme simplicity. Trying to solve all of these with a single architecture would force unacceptable compromises. As a result, ARM split its Cortex product line into three distinct architectural profiles, each optimized for a different class of systems. And if anyone needed any more proof about the immense creativity of us engineers, the lines are named Cortex-A, Cortex-R, and Cortex-M.  
	
	---
	
   ![ARM Cortex Family Overview](/files/PICT-2026/lecture-01/images/2018-04-06-12-43-40-1024x844.jpg.webp)
    - ### Cortex-A → MMU, Linux, user/kernel space
	    **Cortex-A processors represent ARM’s application-class computing line.** These are the “big-boy” CPUs from ARM, designed to run full operating systems like Linux and Android, with clear separation between user space and kernel space. Architecturally, Cortex-A cores include everything required for application-level compute: a Memory Management Unit (MMU) for virtual memory, high-bandwidth memory subsystems with multi-level caches, out-of-order execution to maximize instruction throughput, and SIMD engines such as NEON for media and signal processing workloads. 
	    
	    This makes them suitable for compute-heavy systems ranging from smartphones and tablets to networking equipment, automotive infotainment, robotics platforms, and servers. Naturally, this level of capability comes at a higher silicon cost and power budget compared to microcontroller-class cores. 
	    
	    Within the Cortex-A family, different SKUs exist to target different power-performance trade-offs: Cortex-A5 and A7 are power-efficient, in-order cores; Cortex-A9 and A15 prioritize raw performance through out-of-order execution; Cortex-A17 improves efficiency while retaining out-of-order pipelines; and the A50-series cores such as A53, A57, and A72 introduce the 64-bit ARMv8-A architecture, enabling modern operating systems and server-class workloads.


		- #### A5
			The Cortex A5 is the smallest processor of the A-range, but it can still demonstrate multicore performance. It is the right choice for designers who have experience with ARM926EJ-S or similar, and additionally, it is compatible with A9 and A15 processors.

		- #### A7   
			In terms of power consumption, the A5 and A7 processors are nearly the same. However, the performance provided by the A7 is 20% higher. The Cortex-A7 finds its application in smartphones and tablets and is famous for its power optimization technology. This technology can potentially save up to 75% of CPU energy and in this way can greatly increase battery life. It is compatible with the A15 and A17.

		- #### A15
			The Cortex-A15 has the highest performance among the members of this set. The performance demonstrated by the A15 is 200% higher than the A9. The A15 processor finds its application in high-end devices, low-power servers, and wireless technologies. This is the first processor in the range that fits data management and virtual environment solutions.

		- #### A17
		    The effectiveness of the Cortex-A17 is impressive. This is why its main aim is satisfying the needs of premium-class devices. With considerably improved efficiency in comparison to other members of the A-team, the A17 demonstrates 60% higher performance than that of the A9. The processor can be configured with 1–4 cores with out-of-order pipelines. An A17 in combination with an A7 creates the big.little configuration mentioned above.

		- #### A50
		    The Cortex-A50 processor extends the areas of application to low-power servers. It demonstrates useful power-optimized features and creates great conditions for the migration of 64-bit operating systems to mobile solutions.
		   
			---
		    
    - ### Cortex-R → hard real-time, safety
	    **Cortex-R processors are designed for systems where timing matters more than raw throughput.** Unlike Cortex-A cores, which optimize average performance, Cortex-R cores are built to guarantee bounded and predictable execution. They target hard real-time applications such as automotive control units, storage controllers, industrial automation, and networking data-paths, where missing a deadline is a system failure.
	    
	    Architecturally, Cortex-R processors avoid features that introduce unpredictability, such as aggressive speculation or complex virtual memory systems. Instead, they rely on tightly coupled memories (TCM) for deterministic access, carefully controlled caches, fast and predictable interrupt handling, and extensive reliability features like ECC, lock-step execution, and fault detection. 
	    
	    While they resemble high-end microcontrollers in terms of real-time behavior, Cortex-R cores deliver significantly higher performance and scalability, allowing them to sit in the gap between Cortex-M microcontrollers and Cortex-A application processors. In practice, Cortex-R processors run bare-metal firmware or real-time operating systems, prioritizing worst-case execution time over peak performance.

		- #### R4
		  The Cortex-R4 microcontroller can be clocked to 600 MHz. Its main characteristics are a dual-issue 8-stage pipeline and prefetch prediction. R4 controllers can quickly handle any incoming interruptions.

		- #### R5
		    This type of processor takes care of networking and data storage. It extends the set of R4 features by adding improved efficiency and reliability. It deals with error management and enables fast peripheral reading/writing. The dual-core implementation of the Cortex-R5 allows the construction of strong systems with lightning-fast response.
		- #### R7
		    The processors from this category demonstrate very high performance. They feature an 11-stage pipeline and enable both out-of-order execution and high-level branch prediction. Tools can be implemented for lock-step, symmetric, and asymmetric multiprocessing. The generic interrupt controller is another significant feature that should be mentioned.
        
        ---
        
    - ### Cortex-M → MCU, bare-metal / RTOS
	    **Cortex-M processors are designed to make software feel as close to hardware as possible.** This family targets the microcontroller market, where simplicity, low power consumption, fast startup, and deterministic behavior are more important than high compute throughput. Cortex-M cores eliminate complex features like MMUs and deep pipelines, allowing programs to start executing immediately after reset and respond to interrupts with extremely low latency. 
	    
	    A defining feature of Cortex-M is the tight integration of the NVIC interrupt controller into the core itself, enabling fast and predictable interrupt handling that is critical for control-oriented systems. Different Cortex-M variants exist to address different segments: M0 and M0+ emphasize minimal silicon area and ultra-low power, M3 provides a general-purpose 32-bit MCU platform, M4 adds DSP extensions for signal-processing workloads, and higher-end variants trade some simplicity for performance while remaining deterministic. 
	    
	    Cortex-M processors commonly run bare-metal code or lightweight RTOSes and dominate applications such as sensors, motor control, wearables, power systems, medical devices, and embedded control logic. In essence, Cortex-M cores are CPUs designed to disappear into the product, doing their job quietly, efficiently, and predictably.
		
		- #### M0+
		    This kind of processor shows rather low performance. It uses the Thumb-2 instruction set and has a 2-stage pipeline. Significant features are the bus for single-cycle GPIO and the micro trace buffer. The Cortex-M0+ is a level up from an 8-bit MCU. With this processor, bug fixing gets easier.
		- #### M3 & M4
		    They both provide 1.25 DMIPS/MHz performance, 32-bit bus, increased clock speed, and efficient debugging options. The architectures are the same, as well as the instruction sets. What is the difference between them? Well, the difference is that the core of M4 is capable of DSP.
---

## ARM CORTEX-M4 Features
![Cortex-M4 Features](/files/PICT-2026/lecture-01/images/Pasted image 20260106134812.png)

The **Cortex-M4** is a high-performance 32-bit processor specifically designed for the **microcontroller market**. It sits at a sweet spot where deterministic real-time behavior meets enough computational capability to handle modern embedded workloads such as motor control, digital power, and signal processing. The goal of the Cortex-M4 is not to compete with application processors, but to deliver **maximum useful performance per milliwatt** while keeping the system simple and predictable.

At its core, the Cortex-M4 uses a **3-stage pipelined (fetch, decode, execute) Harvard architecture**, separating instruction and data paths to improve throughput without introducing the unpredictability of deep pipelines or speculative execution. This design allows the processor to achieve strong real-time performance while remaining easy to reason about from a timing perspective. Combined with a highly optimized instruction set, this enables the Cortex-M4 to deliver excellent performance even at relatively modest clock speeds.

A defining strength of the Cortex-M4 is its ability to handle **compute-intensive embedded tasks** efficiently. In addition to standard 32-bit integer operations, the core optionally includes an **IEEE-754 compliant single-precision Floating-Point Unit (FPU)**, making it well suited for control algorithms, filtering, and sensor fusion. The M4 also includes **DSP extensions**, such as single-cycle multiply, multiply-accumulate (MAC), SIMD instructions, saturating arithmetic, and hardware division. These features allow operations that would otherwise require multiple instructions to be completed efficiently and deterministically.

Despite this added capability, the Cortex-M4 remains extremely **area- and power-efficient**. ARM achieves this by tightly integrating system components directly into the core, reducing external logic and minimizing latency. The processor supports multiple low-power modes, including sleep and optional deep-sleep states, allowing the system to rapidly reduce power consumption while retaining program state—an essential requirement for battery-powered and energy-constrained devices.

From a software and tooling perspective, the Cortex-M4 emphasizes **developer productivity and debuggability**. It implements the Thumb-2 instruction set, which combines the high code density of 16-bit instructions with the performance of 32-bit instructions. This results in smaller program memory requirements without sacrificing execution speed. Extensive hardware debug support, including breakpoints, watchpoints, and trace capabilities, makes it possible to debug real-time systems without intrusive instrumentation.

---

## Interrupt Handling and the NVIC

One of the most important architectural features of the Cortex-M4 is the **tight integration of the Nested Vectored Interrupt Controller (NVIC)** directly into the processor core. Unlike external interrupt controllers found in more complex CPUs, the NVIC is designed specifically to deliver **extremely low and deterministic interrupt latency**. It supports a large number of interrupt sources with programmable priority levels, including a dedicated **Non-Maskable Interrupt (NMI)** for critical fault conditions.

Interrupt performance is further improved through **hardware stacking of registers**, which removes the need for software prologue and epilogue code in Interrupt Service Routines (ISRs). The core can also suspend multi-cycle load and store operations when an interrupt occurs, ensuring fast response times. Features such as **tail-chaining** allow the processor to transition directly from one ISR to another without restoring and re-saving context, dramatically reducing overhead in interrupt-heavy systems. As a result, ISRs can be written entirely in C without sacrificing performance or determinism.

The NVIC is also tightly coupled with the processor’s low-power modes. This allows the core to enter sleep or deep-sleep states and wake up immediately in response to an interrupt, making it possible to build systems that are both responsive and energy-efficient.

---

## Cortex-M4 Core Peripherals

To support system-level control and reliability, the Cortex-M4 integrates several core peripherals that are common across all implementations.

The **System Control Block (SCB)** provides the programmer’s interface to core system configuration and status. It exposes information about the processor, manages system exceptions, and allows control over fault handling and low-power behavior.

The **SysTick system timer** is a 24-bit down-counter designed to provide a consistent time base. It is commonly used as the tick source for real-time operating systems, but can also serve as a simple periodic timer in bare-metal applications.

The optional **Memory Protection Unit (MPU)** improves system robustness by allowing memory regions to be defined with specific access permissions and attributes. While it is not a full virtual memory system, the MPU is extremely useful for isolating tasks, protecting critical regions, and catching software bugs early - especially in RTOS-based designs.

Finally, the optional **Floating-Point Unit (FPU)** enables efficient hardware execution of single-precision floating-point operations, significantly reducing execution time and power consumption compared to software-emulated floating-point arithmetic.

## ARM Programmer's Model

When we talk about the _programmer’s model_, we are answering a very specific question:  
**“What does the CPU look like from the point of view of software?”**  
Not the silicon, not the block diagram — but the state the processor exposes to a programmer while code is running.

On Cortex-M, this model is deliberately kept **small, visible, and predictable**, which is one of the biggest reasons it is so popular in embedded systems.

---
### Modes of Operation
There are 2 modes of operation for the MCU - Thread and Handler modes. 
#### Thread Mode
Thread mode is primary mode of operation of the Cortex M4 processor during the normal execution and controller by default will always run in thread mode. In this mode, the processor executes instructions from the programs main thread sequentially advancing through the program flow. This thread of programs can be preempted by higher-priority exception, such as interrupts. To handle the interrupt the controller saves the context that is registers and program counter and transfer the control to the appropriate exception handler.
#### Handler Mode
Handler Mode is a specialized mode of operation invoked when the processor encounters an interrupt or an exception that requires immediate attention. Unlike Thread Mode, which handles regular program execution, Handler Mode focuses on servicing interrupts and exceptions effectively. Basically Handler mode is used to execute exception and ISRs (Interrupt Service Routines). When an exception or interrupt occurs the processor transits from user to handler mode to execute the corresponding exception handler or ISR. Once the ISR or Exception handler has completed its execution the processor again returns to the normal mode that is thread mode to resume the normal program execution.

The transition between these modes is entirely hardware-controlled. When an interrupt occurs, the processor automatically saves the required context, switches modes, selects the correct stack, and jumps to the appropriate handler. When the handler completes, the processor restores the previous context and resumes Thread mode execution.

This design removes a large amount of low-level bookkeeping from software and is a major reason why **interrupt service routines on Cortex-M do not require hand-written assembly wrappers**.

---
### Registers

At the heart of the Cortex-M programmer’s model is a set of **general-purpose and special-purpose registers**. The core provides sixteen architectural registers, named R0 through R15. Of these, R0 to R12 are general-purpose registers used for holding data and intermediate results. These are the registers your compiler primarily works with when translating C code into machine instructions.

R13 is the **Stack Pointer (SP)**, R14 is the **Link Register (LR)**, and R15 is the **Program Counter (PC)**. These three registers are special because they directly control execution flow. The Program Counter always points to the next instruction to be executed. The Link Register holds return addresses during function calls, and the Stack Pointer tracks the current top of the stack in memory.

Then come the Special Registers, namely the PSR, PRIMASK, FAULTMASK, BASEPRI and CONTROL register.

The PSR combines the Application Program Status Register (APSR), the Interrupt Program Status Register(IPSR), and the Execution Program Status Register (EPSR). The APSR contains the current state of the condition flags from previous instruction executions, the IPSR contains the exception type number of the current Interrupt Service Routine (ISR), while the EPSR contains the Thumb state bit, and the execution state bits for either the "If-Then" (IT) instruction or the "Interruptible-Continuable Instruction" (ICI) instruction.

The PRIMASK register prevents activation of all exceptions with configurable priority, the FAULTMASK register prevents activation of all exceptions except for Non-Maskable Interrupt (NMI), and finally, the BASEPRI register defines the minimum priority for exception processing. When BASEPRI is set to a nonzero value, it prevents the activation of all exceptions with the same or lower priority level as the BASEPRI value.

---

### Stack And Stack Pointer: MSP and PSP

The Processor functions on a full-descending stack, meaning that the stack stores the address of the last stacked item in memory. When the processor pushes a new item onto the stack, it decrements the stack pointer and then writes the item to the new memory location. The processor implements two stacks, the main stack and the process stack, with a pointer for each held in independent registers.

Unlike many simple processors, Cortex-M provides **two stack pointers**: the **Main Stack Pointer (MSP)** and the **Process Stack Pointer (PSP)**. At reset, the processor always starts execution using the MSP. This is intentional - the system must always have a known, reliable stack available immediately after reset.

The MSP is typically used for **exception and interrupt handling**, while the PSP is intended for **application code**, especially in RTOS-based systems. This separation allows the system to isolate application stacks from interrupt and kernel stacks, improving robustness and making context switching safer.

From a software point of view, only **one stack pointer is active at any given time**, but the processor can switch between MSP and PSP automatically based on the current operating mode. This mechanism is completely handled in hardware and is one of the reasons why interrupt latency on Cortex-M is so low.

Even in bare-metal systems, this distinction becomes important once interrupts, fault handlers, or an RTOS are introduced.

---

### Why This Model Matters

The Cortex-M programmer’s model is intentionally minimal, but every part of it exists for a reason. Registers provide fast, predictable execution. Dual stack pointers enable clean separation between system and application code. Simple operating modes allow fast and deterministic interrupt handling.

Together, these features make Cortex-M processors **easy to debug, easy to reason about, and extremely reliable in real-time systems** - exactly what is needed in microcontroller-class designs.

### Links
https://sirinsoftware.com/blog/the-arm-processor-a-r-and-m-categories-and-their-specifics
https://en.wikipedia.org/wiki/Arm_Holdings
https://en.wikipedia.org/wiki/Reduced_instruction_set_computer
https://medium.com/@raihann.eu/thread-mode-and-handler-mode-in-arm-6e3c6ff4d7ca

