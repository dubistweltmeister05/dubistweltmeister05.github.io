---
title: 'Ethernet Magnetics: Why Every Port Needs a Transformer'
date: 2026-06-05
permalink: /posts/2026/06/ethernet-magnetics/
excerpt: 'Galvanic isolation, common-mode rejection, and the engineering trade-offs between discrete magnetics modules and integrated-magnetics RJ45 jacks in PCB design.'
toc: true
toc_label: 'Contents'
tags:
  - networking
  - hardware
  - embedded-systems
  - pcb-design
---

## Introduction

Every Ethernet port - from the gigabit NIC in your laptop to the industrial switch on a factory floor - contains a small transformer between the PHY chip and the RJ45 connector. These "magnetics" are not optional. They are mandated by the IEEE 802.3 standard and serve a function so critical that omitting them risks destroying silicon, injuring users, or failing EMC certification. This post covers what Ethernet magnetics do, why they exist, and the practical PCB design decisions around implementing them.

---

## What Ethernet Magnetics Actually Are

Ethernet magnetics are small, tightly-coupled pulse transformers - typically one per differential pair, so two for 10/100BASE-T (TX and RX) and four for 1000BASE-T (which uses all four pairs bidirectionally). Each transformer consists of a primary and secondary winding on a ferrite core, with a turns ratio of 1:1 (for signal integrity) and a center-tap on each winding for bias voltage injection and common-mode termination. The component is physically small - a discrete 1000BASE-T magnetics module is typically 15×10mm or smaller in an SMD package - but its electrical role is foundational to Ethernet's reliability and safety.

The transformer's bandwidth must span the full signaling spectrum of the Ethernet variant it supports. For 100BASE-TX, this means passing clean pulses with spectral content from ~1 MHz to ~80 MHz (MLT-3 encoding at 125 Mbaud). For 1000BASE-T, the bandwidth requirement extends to ~100 MHz with tight insertion loss and return loss specifications across that range. The 802.3 standard specifies transformer performance in terms of open-circuit inductance (minimum 350 µH for GbE), leakage inductance (maximum ~0.8 µH), interwinding capacitance (typically <10 pF), and insertion loss (<1 dB at 100 MHz). These parameters are interdependent - more turns increase inductance but also raise leakage inductance and parasitic capacitance, creating a design tension that magnetics manufacturers optimize through proprietary winding geometries, low-loss ferrite materials (typically MnZn ferrites for their high permeability at Ethernet frequencies), and multi-sectional bobbin designs that minimize inter-winding coupling capacitance.

---

## Galvanic Isolation: The Primary Purpose

The most critical function of Ethernet magnetics is galvanic isolation - creating a complete electrical break between the PHY's ground plane and the cable-side ground. This isolation serves multiple purposes simultaneously, any one of which alone would justify the component's existence.

**Safety isolation** prevents hazardous voltages from reaching the user or connected equipment. Ethernet cables can run hundreds of meters through buildings, across floors, between structures with different electrical service entrances. The ground potential between two endpoints can differ by tens or even hundreds of volts due to ground loops, lightning-induced surges on cable shields, or fault conditions in building wiring. Without galvanic isolation, this potential difference would flow through the PHY's ground-referenced I/O circuits, destroying the chip and potentially creating a shock hazard at the equipment chassis. The 802.3 standard mandates a minimum isolation voltage of 1500 Vrms (for basic insulation) or 2250 Vrms (for reinforced insulation used in PoE applications), sustained for 60 seconds. This means the transformer's inter-winding insulation - typically polyester film or triple-insulated wire (TIW) - must withstand these voltages without breakdown. In practice, quality magnetics are tested to withstand 3000-4000 Vrms hipot to provide margin above the specification.

**Equipment protection from ground loops** is the day-to-day operational benefit. In any installation connecting two pieces of equipment powered from different outlets (or different phases of the same supply), a ground potential difference of 1-5V is common, and in industrial environments with heavy motor loads, 10-50V differences occur routinely. Without isolation, this differential drives current through the cable's signal conductors, saturating the PHY's input common-mode range, corrupting data, and in severe cases destroying the PHY's ESD protection diodes through sustained overcurrent. The magnetics' isolation barrier reduces this common-mode current to picoamps of leakage through the inter-winding capacitance - effectively zero from the PHY's perspective.

**Lightning and surge protection** relies on the magnetics as the first line of defense. When a nearby lightning strike induces a kilovolt-level transient on an Ethernet cable, the transformer's isolation barrier blocks the bulk of the energy from reaching the PHY. The surge instead sees the inter-winding capacitance (~10 pF) as a high-impedance path and is shunted to chassis ground through TVS diodes or gas discharge tubes placed on the cable side of the magnetics. Without the transformer, surge energy would couple directly into the PHY's ground plane, destroying not just the network interface but potentially propagating damage to the entire PCB through shared power rails.

---

## Common-Mode Rejection

Beyond isolation, Ethernet magnetics provide common-mode rejection - the ability to pass differential signals (the actual data) while blocking common-mode noise that appears identically on both conductors of a pair. This is essential because Ethernet cables act as antennas, picking up electromagnetic interference from nearby power lines (50/60 Hz hum), switch-mode power supplies (100 kHz–10 MHz harmonics), radio transmitters, and other Ethernet cables in the same bundle (alien crosstalk).

The transformer achieves common-mode rejection through its fundamental operating principle: a 1:1 transformer passes differential flux (where current flows in opposite directions on the two conductors, creating additive flux in the core) but blocks common-mode flux (where current flows in the same direction on both conductors, creating cancelling flux in the core). In an ideal transformer with perfect symmetry, common-mode rejection would be infinite. In practice, winding asymmetries, core non-uniformities, and parasitic capacitances limit the common-mode rejection ratio (CMRR) to 30-50 dB at Ethernet frequencies - still sufficient to reduce millivolt-level common-mode noise to microvolt levels that are well below the PHY's receiver sensitivity threshold.

The center-tap on each winding plays a crucial role in common-mode termination. On the line side, the center-tap is typically connected to chassis ground (or cable shield ground) through a high-voltage capacitor (typically 1-10 nF rated to 2 kV), providing a return path for common-mode currents that would otherwise find their way through parasitic paths and radiate as EMI. On the PHY side, the center-tap provides the DC bias point for the transmitter - in 1000BASE-T, the PHY drives signals referenced to a specific common-mode voltage (typically VDD/2 ≈ 1.65V for 3.3V PHYs), and the center-tap allows this bias to be injected without disturbing the differential signal path. The combination of differential-mode signal passage, common-mode rejection, and controlled center-tap termination makes the magnetics package a complete signal-conditioning front-end for the PHY.

---

## Bob Smith Termination

Nearly every Ethernet magnetics application includes a "Bob Smith termination" - a network of resistors and capacitors connected to the line-side center-taps that dramatically improves EMI performance. Named after the engineer who popularized the technique in early Ethernet designs, the Bob Smith network connects each center-tap through a 75Ω resistor to a common node, which is then AC-coupled to chassis ground through a single high-voltage capacitor (typically 1000 pF / 2 kV).

The physics behind this termination relates to the cable's characteristic impedance for common-mode signals. While Ethernet's differential impedance is 100Ω (and is terminated by the PHY's input/output impedance), the common-mode impedance of a Cat5/6 cable is approximately 75Ω per pair. Without proper common-mode termination, common-mode energy reflects back and forth along the cable, radiating at each impedance discontinuity (connectors, bends, transitions between cable and PCB trace). The Bob Smith resistors provide a matched termination for common-mode energy, absorbing it rather than allowing reflections. The AC coupling capacitor blocks DC and low-frequency ground potential differences while allowing high-frequency common-mode currents (the ones that cause radiation) to flow to chassis ground. The result is typically a 6-10 dB improvement in radiated emissions performance - often the difference between passing and failing FCC/CE EMC testing. Omitting or incorrectly implementing Bob Smith termination is one of the most common reasons Ethernet designs fail EMC certification on the first attempt.

---

## Discrete Magnetics Modules

The traditional approach to implementing Ethernet magnetics on a PCB is to use a discrete magnetics module - a standalone surface-mount or through-hole package containing all the transformers, center-tap components, and sometimes the Bob Smith termination network for one Ethernet port.

Discrete modules come in standardized footprints (commonly 24-pin SMD or 16-pin DIP for single-port GbE) and are available from manufacturers like Pulse Electronics, Bourns, Würth Elektronik, and Halo Electronics. A typical single-port GbE module contains four 1:1 pulse transformers, internal common-mode chokes (some designs integrate these), and pre-connected center-tap capacitors. The designer places the module between the PHY chip and the RJ45 connector, routing four differential pairs from the PHY to the module's primary side and four pairs from the module's secondary side to the jack.

The advantages of discrete magnetics are significant. **Flexibility** - the designer can choose magnetics independently of the connector, optimizing each for their respective requirements (e.g., selecting a magnetics module rated for extended temperature while using a standard commercial-grade jack). **Placement optimization** - the module can be positioned to minimize trace length from the PHY (critical for signal integrity at GbE speeds) while the jack is constrained to the board edge. **PoE compatibility** - discrete magnetics can be specified with reinforced isolation ratings (4 kV hipot) required for IEEE 802.3bt Type 3/4 PoE delivering up to 90W, where the voltage on the cable-side windings reaches 57V DC. **Repairability** - if magnetics are damaged by a surge event, the module can be replaced without replacing the entire connector. **Multi-port density** - for switches and routers with many ports, discrete magnetics in compact SMD packages allow tight PCB layouts that integrated jacks cannot achieve.

The disadvantages are equally real. Discrete magnetics require additional PCB area (15×10mm for a single GbE module), additional routing (four differential pairs between module and jack, plus center-tap traces), and careful layout attention to maintain impedance control on the traces between PHY, magnetics, and jack. They also add BOM cost (typically $1.50-4.00 per port for quality GbE magnetics) and assembly complexity.

---

## Integrated Magnetics Jacks

The alternative to discrete magnetics is an RJ45 connector with integrated magnetics - the transformers, common-mode chokes, and termination components are built directly into the jack housing. These "MagJack" connectors (a term popularized by BelFuse, though now used generically) combine two functions in one component: the physical RJ45 receptacle and the complete magnetics solution.

Internally, the MagJack contains miniature toroidal or planar transformers wound on ferrite cores, potted or encapsulated within the connector shell alongside the RJ45 contact springs and LED light pipes. The PCB-side pins connect directly to the PHY's differential pairs - no intermediate routing to a separate magnetics module is needed. The cable-side connections are internal to the jack, going directly from the transformer secondaries to the RJ45 contacts.

The advantages are compelling for many designs. **PCB area savings** - eliminating the discrete module saves 150-200 mm² per port, which is substantial in space-constrained designs like single-board computers, NUCs, or multi-port NICs. **Simplified routing** - the PHY's differential pairs route directly to the jack pins without an intermediate component, reducing the number of impedance-controlled trace segments and potential reflection points. **Reduced EMI risk** - shorter signal paths between magnetics and cable attachment point mean less PCB trace acting as a radiating antenna for common-mode currents. **BOM consolidation** - one part number replaces two (connector + magnetics), simplifying procurement and assembly. **Guaranteed compatibility** - the magnetics and connector are designed and tested together by the same manufacturer, eliminating integration risk.

The disadvantages matter in specific contexts. **Limited configurability** - you get whatever isolation rating, inductance, and common-mode rejection the jack manufacturer designed in; if your application needs higher isolation (e.g., medical equipment requiring 5 kV) or specific return loss characteristics, your options are constrained to what exists in catalog. **Thermal limitations** - transformers generate heat from core losses, and encapsulating them inside a plastic RJ45 shell limits thermal dissipation, which can be problematic in PoE applications where the cable-side winding carries DC current (up to 960 mA per pair for 802.3bt Type 4). **Connector lock-in** - if your preferred magnetics vendor doesn't make the jack form factor you need (e.g., right-angle, low-profile, or press-fit pin), you're forced to use discrete magnetics. **Cost at scale** - integrated MagJacks typically cost $3-8 per port, compared to $1.50-4.00 for discrete magnetics plus $0.50-2.00 for a plain RJ45 jack; for high-volume products where cents matter, discrete implementations may win. **Multi-speed validation** - some cheaper integrated jacks are characterized only for 100BASE-TX and do not meet the tighter insertion loss and return loss specifications required for 1000BASE-T or 2.5GBASE-T.

---

## Power over Ethernet (PoE) Implications

PoE adds a DC power delivery function on top of Ethernet signaling, and the magnetics are directly in the power path for "Mode A" PoE (where power is phantom-fed on the data pairs). In this configuration, the PSE (Power Sourcing Equipment) injects 48-57V DC on the center-taps of the cable-side transformer windings. The DC current flows through the transformer windings to the center-taps, through the Ethernet cable's twisted pairs, and is extracted at the PD (Powered Device) end through its magnetics' center-taps.

This means the transformer's wire gauge must handle the DC current without excessive heating or voltage drop - at 802.3bt Type 4 (90W), each pair carries up to 960 mA, flowing through the transformer winding as DC bias. The ferrite core must not saturate under this DC bias current; because the DC flows as common-mode current (same direction on both wires of each transformer), it does not create net flux in an ideal transformer, but real-world winding asymmetries create a small DC flux component that can partially saturate the core, degrading the transformer's AC signal performance. High-quality PoE magnetics use larger cores with higher saturation flux density (Bsat) or incorporate air gaps to handle the DC bias without performance degradation.

The isolation voltage requirement also increases for PoE applications. Standard Ethernet magnetics require 1500 Vrms basic insulation, but PoE adds a sustained DC voltage (up to 57V) on the cable-side windings that stress the inter-winding insulation continuously, not just during transient events. IEEE 802.3bt mandates reinforced insulation (2250 Vrms for 60 seconds) for all PoE magnetics, and safety agencies like UL/IEC require additional creepage and clearance distances on the PCB between cable-side and PHY-side traces - typically 5-8mm depending on the insulation system. This safety spacing requirement has significant PCB layout implications and is another reason some designers prefer integrated MagJacks for PoE: the required creepage/clearance is engineered into the component itself, reducing the designer's burden.

---

## PCB Layout Considerations

Proper PCB layout around Ethernet magnetics is critical for both signal integrity and EMC compliance. The magnetics sit at the boundary between two electrical domains - the PHY-referenced "clean" domain and the cable-referenced "dirty" domain - and the layout must enforce this boundary rigorously.

**Ground plane splitting** is fundamental. The PCB ground plane beneath the magnetics should be split into two zones: one continuous with the PHY's digital/analog ground, and one connected to chassis ground (the cable-side shield ground). The split aligns with the magnetics' isolation barrier - no copper pour should bridge the two domains. The only connection between the two ground planes should be through a controlled impedance path: typically a 1 MΩ resistor in parallel with a 1-10 nF high-voltage capacitor, providing a DC reference and an AC shunt for common-mode currents. Some designs use a single ground plane throughout (no split) and rely on the magnetics' CMRR alone for isolation, but this forfeits the EMI benefits of a chassis-referenced cable-side ground and often fails radiated emissions testing.

**Trace routing** between PHY and magnetics must maintain 100Ω differential impedance, be length-matched within each pair (to sub-millimeter tolerance for GbE), and be as short as physically possible. Each millimeter of unshielded differential trace between the PHY and the magnetics primary is a potential EMI antenna. Between magnetics and RJ45, the traces carry cable-referenced signals and are typically less critical for signal integrity (the cable itself is much longer and lossier than any PCB trace), but they must still maintain impedance matching and observe safety spacing from PHY-domain signals.

**Component placement** should minimize the total signal path: PHY → magnetics → RJ45 in a straight line with no unnecessary bends or vias. The magnetics module or MagJack should be as close to the board edge as possible (for the connector) while keeping the PHY-to-magnetics traces short. Decoupling capacitors for the PHY's analog supply should be placed between the PHY and the magnetics, not on the cable side of the isolation barrier. Any TVS diodes or surge protection components belong on the cable side of the magnetics, between the transformer secondary and the RJ45 contacts - placing them on the PHY side defeats the purpose of isolation.

---

## Automotive and Industrial Variants

Ethernet magnetics for automotive (100BASE-T1, 1000BASE-T1) and industrial applications face additional requirements beyond standard office Ethernet. Automotive Ethernet uses a single twisted pair (no RJ45 connector - instead using proprietary connectors like MATEnet or H-MTD), but still requires magnetics for the same reasons: galvanic isolation, common-mode rejection, and EMI control.

Automotive magnetics must survive extended temperature ranges (-40°C to +125°C or even +150°C for under-hood applications), withstand vibration and mechanical shock per standards like ISO 16750, and meet automotive-grade quality levels (AEC-Q200 for passive components). The ferrite core material must maintain its permeability and saturation characteristics across this temperature range - standard MnZn ferrites lose significant permeability above 100°C, so automotive magnetics often use specialized high-temperature ferrite compositions or NiZn ferrites that trade lower permeability for better temperature stability.

Industrial Ethernet applications (PROFINET, EtherCAT, EtherNet/IP) frequently operate in environments with extreme EMI - near variable-frequency drives, arc welders, or high-voltage switchgear - demanding magnetics with higher common-mode rejection (>40 dB at 100 MHz) and enhanced surge ratings (6 kV per IEC 61000-4-5). Some industrial magnetics modules integrate additional common-mode chokes beyond what the standard pulse transformer provides, achieving 60+ dB of common-mode attenuation at the cost of slightly higher insertion loss and larger package size.

---

## Emerging Trends

As Ethernet speeds push beyond 10GBASE-T and into 25G/50GBASE-T territory, the magnetics challenge intensifies. Higher signaling frequencies (up to 500 MHz for 25GBASE-T) demand transformers with extremely low insertion loss, flat group delay, and minimal parasitic capacitance - pushing the limits of conventional wound-transformer technology. Some vendors are exploring planar magnetics (transformers fabricated as PCB layer stackups rather than wound components) for multi-gigabit Ethernet, trading manufacturability challenges for superior high-frequency performance and thinner profiles.

The rise of Single Pair Ethernet (SPE) - standards like 10BASE-T1S and 100BASE-T1 targeting IoT, building automation, and automotive - simplifies the magnetics requirement to a single transformer per port but introduces new challenges around power delivery (PoDL - Power over Data Line, delivering up to 50W over a single twisted pair) that demand robust isolation and DC bias handling in a miniaturized package. SPE magnetics must fit in connector-sized housings for the new compact SPE connectors (IEC 63171-series), driving innovations in miniaturized ferrite cores and automated micro-winding processes.

---

## Conclusion

Ethernet magnetics are a deceptively simple component - a few windings of wire on a ferrite core - that enable the entire Ethernet ecosystem to function reliably across the enormous variety of electrical environments where networks are deployed. Without them, every Ethernet connection would be vulnerable to ground loops, surges, EMI, and safety hazards that would make reliable long-distance networking impractical. The choice between discrete magnetics modules and integrated MagJack connectors is fundamentally a PCB design trade-off between flexibility and space optimization, with neither approach being universally superior. Understanding what the magnetics actually do - and why the IEEE mandates them - equips the PCB designer to make informed decisions about component selection, layout strategy, and certification planning.

---

## Further Reading

- IEEE 802.3 Section 14.3 (MAU requirements including transformer specifications)
- AN-639: Analog Devices Ethernet Magnetics Design Guide
- Pulse Electronics: Ethernet Magnetics Selection Guide
- Würth Elektronik: Application Note - Ethernet Transformer Design
- Bob Smith Termination: "EMC and Signal Integrity Design Techniques for Ethernet"

---

*Draft created: June 5, 2026*
