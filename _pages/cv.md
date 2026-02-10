---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
======
* **Bachelor of Technology in Electronics and Telecommunication**
  * P. Impri Chinchwad College of Engineering (PCCOE), Pune
  * 2021-2025
  * CGPA: 8.12

Work Experience
======
* **Firmware Engineer** | Tor.ai, Pune (2024-2025)
  * **Networking Stack Development (Qualcomm SoC - Arch Linux)**: Brought up the complete networking stack for an Arch Linux image. Developed configuration scripts and automation services for LAN/WAN Ethernet ports, LTE modem, and Wi-Fi interfaces. Implemented user-configurable network interfaces with intelligent fallback system based on user-defined priority, ensuring seamless network continuity during disconnections.
  * **Network Protocols & Services**: Set up DHCP client and server on Ethernet ports, configured Wi-Fi Client and AP modes, developed SMS reception and transmission utility for LTE interface, and implemented EtherNet/IP over MQTT protocols.
  * **Embedded Graphics (TouchGFX)**: Designed and implemented real-time GUI for a Smart Industrial 3-Phase Energy Meter. Developed complete visual interface using TouchGFX Designer, implemented data pipeline from firmware to graphics codebase, coded screen interactions and transitions, optimized memory usage, and ensured visual smoothness and system stability.
  * **System Firmware (FreeRTOS)**: Explored and maintained FreeRTOS-based system architecture with dedicated threads for 3-phase AC voltage measurement, frequency analysis, MODBUS data publishing, and other real-time tasks. Gained deep understanding of industrial energy metering systems and embedded systems engineering.
  * **Secure Communication (TLS over MQTT via BLE)**: Currently implementing user-configurable static TLS over MQTT with BLE data reception. Developed data chunking algorithm (33-byte packets) for BLE transmission, implemented chunk reconstruction on receiver side, and integrated with TLS implementation for secure communication.

* **Linux Kernel Developer** | Vicharak Computers, Surat (2025-Present)
  * Led and successfully completed migration efforts on support for Linux Kernel v5.10 to Linux Kernel v6.1.75 on the YOCTO build for the Product "Vaaman". Added application support for USB 2.0/3.0, MIPI-CSI, Audio Codec (Rockchip ES-8316), RTC, and Wi-Fi/Bluetooth Chip (RTL8822CS) in the YOCTO build Image.
  * Worked on adding Kernel Driver support for Audio Codec within the Private Linux Kernel Source.
  * Implemented complete board bring-up procedure for a custom All-Winner A20 based development board. Automated the process via scripting, leading to a reduction of time taken for bring-up by 50%.

* **Embedded Software Intern – R&D** | Knorr-Bremse Technology Center India – Kiepe Electric, Pune (12 Months, 2024-2025)
  * Spearheaded integration testing for the Base Software of CSM and CSE controllers, ensuring seamless functionality and enhancing overall system reliability by identifying critical performance gaps.
  * Researched the CI/CT pipeline for Embedded Testing at the base software level for the complete product development process. Working with build-automation tools like Jenkins and Docker.
  * Conducted architectural analysis of tri-core DSP processors from Texas Instruments for performance enhancements and applicability, presenting findings to Dortmund headquarters to guide the design of a Traction Control Unit for railways.
  * Led a code review and requirement verification activity for the base software of a product called Modular System Controller, which handles diagnostics and sensor communication for a wagon in railways.
  * Worked on Unit testing for various software components across many projects at the company. Gained hands-on experience with software tools like Tessy.

Technical Skills
======
* **Core Competencies**
  * Embedded C
  * YOCTO Project
  * Embedded Linux
  * Real-Time Operating Systems (FreeRTOS, RTOS)
  * Data Structures and Algorithms
  * Analog/Digital Electronics

* **Microcontrollers & Processors**
  * STM32 (ARM Cortex-M4)
  * Qualcomm SoC
  * Arduino
  * Texas Instruments DSP Processors
  * All-Winner A20

* **Embedded Systems Development**
  * Linux Kernel Development
  * Bare-metal library development
  * Peripheral Drivers: GPIO, RCC, NVIC, EXTI, I2C, SPI, UART, USART
  * Motor Control (BLDC Motors)
  * Sensor Integration
  * Embedded Graphics (TouchGFX)

* **Networking & Communication Protocols**
  * MQTT, TLS/SSL
  * EtherNet/IP
  * MODBUS
  * Bluetooth Low Energy (BLE)
  * DHCP Client/Server
  * LTE/4G (SMS, Data)
  * Wi-Fi (Client & AP modes)

* **Tools & Technologies**
  * Jenkins & Docker (CI/CD)
  * Git & GitHub
  * Tessy (Unit Testing)
  * TouchGFX Designer
  * USB 2.0/3.0, MIPI-CSI
  * Audio Codecs (Rockchip ES-8316)
  * Wi-Fi/Bluetooth (RTL8822CS)

Projects
======
* **Ronin Virtual Machine**
  * A stack-based virtual machine (VM) coded in C, capable of interpreting and executing a set of basic instructions including arithmetic operations, conditional jumps, and stack manipulations.
  * Designed to simulate a minimal computing environment with features like program reading and writing to files.

* **Fully Autonomous Pick-And-Place Robot** (Team Lead)
  * Led a team of 3 engineers and oversaw microcontroller application development for the backup navigation system of a 3-wheeled mobile robot.
  * Developed control algorithms and sensor integration for autonomous operation.

* **Semi-Autonomous BLDC Mobile Robot**
  * Responsible for operation and maintenance of BLDC Motors and motor drivers used for mobile navigation.
  * Developed and operated a double-flywheel ring throwing mechanism.
  * Prototyped mechanisms and electronic PCBs for power delivery and voltage regulation applications.

Collegiate Club Contributions
======
* **Team Automatons** | Embedded Software Lead (2022-2024)
  * Responsible for reviving the usage of 32-bit microcontrollers at the team. Delivered a wireless navigation control system for manual control of 4 and 3-wheeled robots, written using self-written bare metal libraries. This led to a 25% improvement in control system performance.
  * Conceived a custom Programmer's Model and libraries for GPIOs, RCC, NVIC&EXTI, and communication protocols like I2C, SPI, UART, and USART for Cortex M-4-based microcontrollers from ST Microelectronics.
  * Developed backup navigation and application codes for a double-flywheel mechanism for the ROBOCON challenge's ball-passing task.
  * Led a sub-team for the documentation round of ROBOCON 2024, securing a score of 97 out of 100.
  * Wrote custom libraries for Arduino interfacing of commonly used sensors such as TF Mini (ToF Sensor), TCS230 (Color Detection Sensor), and Motor Drivers like BTS7960 and Cytron MD10C/MD30C.
  * Created and maintained the GitHub organization for Team Automatons, establishing a centralized repository for the team's legacy codebase.
  * **Participated in DD ROBOCON 2024, stood AIR 2.**

* **Team Automatons** | Junior Engineer (2021-2022)
  * Handled BLDC Motors and motor drivers; designed, developed, and debugged modular scripts for integration of motor control with Arduino and wireless control devices.
  * Prototyped various application mechanisms including double flywheel mechanism, arm throwing mechanism, pinch-gripper mechanism, and claw-picking mechanism.
  * Worked with electronic sensors and actuators for custom robotic application systems.
  * **Participated in DD ROBOCON 2023, stood at AIR 14.**

Volunteering
======
* Conducted workshops on "Electronics in Robotics" at various schools through the IEEE SPS PCCOE Chapter under the IEEE Try Engineering Initiative.

Achievements & Activities
======
* **Martial Arts**: First Dan Black Belt in Karate
* **Sports**: Former club-level cricketer and active table tennis player
* **Music**: Guitarist
* **Football**: Passionate Manchester United supporter

Teaching & Workshops
======
  <ul>{% for post in site.teaching reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
