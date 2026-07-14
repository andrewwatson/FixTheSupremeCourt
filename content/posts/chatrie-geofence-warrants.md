+++
title = "The Court Got One Right: Geofence Warrants Are Now a Fourth Amendment Search"
date = '2026-07-14T09:00:00-04:00'
draft = false
author = 'Editor'
description = "In Chatrie v. United States, the Supreme Court ruled that police need a real warrant before pulling everyone's location data near a crime scene. It's a genuine privacy win — and Alito's dissent shows how close it came to going the other way."

tags = ["privacy", "surveillance", "fourth-amendment", "supreme-court", "technology", "policing"]

[cover]
image = "/headers/chatrie-geofence-warrants_modern.png"
alt = "Smartphone location pin over a map, representing geofence surveillance data"
+++

Most posts on this site are about the Supreme Court taking a right away. This one isn't — mostly. On June 29, 2026, the Court ruled that "geofence warrants," the increasingly common police tactic of asking Google to hand over location data for every phone that passed near a crime scene, count as a search under the Fourth Amendment. That means police actually have to get a real warrant, based on real evidence connecting a real suspect to a real crime, before casting the net.

It's a genuine win for digital privacy. It's also a 6-3 decision, which means three sitting justices were prepared to let the practice continue unchecked — and their reasoning is worth understanding, because it's the same reasoning that could gut this protection the next time the facts are less sympathetic.

<!--more-->

## What a Geofence Warrant Actually Is

A geofence warrant doesn't name a suspect. It names a place and a time window, and orders a company — almost always Google, which retains location history for billions of Android and iPhone users through its Sensorvault database — to identify every device that was within that geographic boundary during that period. Police then narrow the list down, request more identifying information on the phones that look interesting, and build a suspect pool from people whose only "crime" was carrying a phone near where something happened.

[*Chatrie v. United States*](https://www.supremecourt.gov/opinions/25pdf/25-112_0am4.pdf) arose from a 2019 Virginia bank robbery. Police obtained a geofence warrant covering a 150-meter radius around the bank for a one-hour window, got location data on every device inside it, and eventually identified Okello Chatrie as a suspect. Chatrie argued the entire process violated the Fourth Amendment because it swept up his location data — and everyone else's — without any individualized suspicion at the outset.

## The Ruling: Location Data Is Like Location Data

Justice Kagan wrote the majority opinion, joined by Chief Justice Roberts, Sotomayor, Jackson, and Kavanaugh. The reasoning leaned heavily on [*Carpenter v. United States*](https://www.supremecourt.gov/opinions/17pdf/16-402_h315.pdf) (2018), the landmark case holding that police need a warrant to obtain historical cell-site location data from phone carriers. Kagan treated the extension to Google's geofence data as close to automatic: this location history "shares the essential characteristics of" the cell tower records at issue in *Carpenter*, and deserves the same Fourth Amendment protection. If police need a warrant to track where your phone has been over time, they need one to sweep up where everyone's phone was at a given moment too.

Justice Gorsuch concurred but on different grounds entirely — he'd have treated the location data as the user's own property held by Google, making a geofence request the digital equivalent of the government breaking into a locked filing cabinet in your home without a specific warrant naming what they're looking for. It's a narrower theory than Kagan's, but it points the same direction: this data belongs to you, and the government needs cause before it can go looking through it.

## The Dissent: A Preview of Where This Could Go Wrong

Justice Alito, joined by Thomas and in part by Barrett, dissented — and did not hold back. Alito warned the ruling would "send seismic waves through our Fourth Amendment doctrine" and "unleash upheaval" in how courts handle digital evidence going forward. His actual legal argument was narrower than the rhetoric: he'd have resolved the case on the "good faith" exception, letting the evidence stand because police reasonably relied on the warrant as written even if the warrant itself was constitutionally deficient — sidestepping the underlying privacy question entirely.

Barrett's separate dissent went further on the merits, and it's the more revealing one. She argued that under existing precedent, Chatrie had no reasonable expectation of privacy in this data at all, because he "voluntarily disclosed" his location to Google every time his phone pinged a tower or a Wi-Fi network. That's the third-party doctrine — the decades-old rule that information you hand to a company loses its constitutional protection — and it's exactly the doctrine *Carpenter* was supposed to have limited for cell-site data. Barrett's dissent shows an appetite to keep applying it broadly to everything else.

## Why This Matters Beyond One Bank Robbery

Geofence requests to Google have exploded over the past decade — from a handful of cases in 2018 to tens of thousands of requests a year at their peak, sweeping up location data on people with no connection to any crime beyond being in the wrong place at the wrong time. Civil liberties groups have flagged geofence warrants as [part of a much larger dragnet-surveillance ecosystem](/posts/flock-cameras-ice-surveillance-courts/) that courts have been slow to catch up with — license plate readers, facial recognition, and now location dumps, all operating with minimal judicial oversight because the technology outpaced the doctrine written for a world of physical searches.

*Chatrie* closes one part of that gap. It does not close all of it. Google has already begun moving location history storage to devices themselves rather than centralized servers, partly in response to litigation like this — which may make geofence warrants technically harder to execute going forward regardless of what the Court ruled. But the legal principle matters beyond this one company's engineering decisions: the next mass-surveillance tool, whatever it turns out to be, will need to clear the bar *Chatrie* just set, or fight the same battle again from scratch.

## A Real Win, With an Asterisk

Give credit where it's due: this is a case where a majority that includes Roberts and Kavanaugh sided with privacy over law enforcement convenience, using a functional, technology-aware reading of the Fourth Amendment rather than a cramped originalist one. It's worth noting when this Court gets it right, not just when it doesn't.

But a 6-3 decision with a dissent arguing that voluntarily using a smartphone forfeits your location privacy entirely is not a settled question — it's a preview of the next fight. Barrett's third-party doctrine reasoning didn't win this time. It's sitting there for the next case, the next technology, the next set of facts where three justices become five. The same lesson applies here as it does everywhere else on this Court: a right protected by one vote today is a right that depends entirely on who's sitting on the bench tomorrow.

---

### Sources

- [*Chatrie v. United States*, No. 25-112 (June 29, 2026)](https://www.supremecourt.gov/opinions/25pdf/25-112_0am4.pdf) — full opinion, concurrence, and dissents
- [*Carpenter v. United States*, 585 U.S. 296 (2018)](https://www.supremecourt.gov/opinions/17pdf/16-402_h315.pdf) — the precedent the majority extended to geofence data
- [SCOTUSblog: "Court rules that law enforcement's use of 'geofence warrant' was a 'search'"](https://www.scotusblog.com/2026/06/court-rules-that-law-enforcements-use-of-geofence-warrant-was-a-search/)
- [NPR: "Supreme Court restricts use of geofence warrants"](https://www.npr.org/2026/06/29/nx-s1-5844697/supreme-court-restricts-use-of-geofence-warrants)
- [Newsweek: "Chatrie Ruling: Alito Rips Supreme Court's 'Irresponsible Escapade' on Surveillance"](https://www.newsweek.com/alito-supreme-court-geofence-warrant-ruling-irresponsible-escapade-12135711)
- [Reason: "In big win for Fourth Amendment advocates, the Supreme Court says 'geofence warrants' count as a 'search'"](https://reason.com/2026/06/29/in-big-win-for-fourth-amendment-advocates-the-supreme-court-says-geofence-warrants-count-as-a-search/)
- [Just Security: "Unpacking the Supreme Court's Chatrie Decision"](https://www.justsecurity.org/145214/chatrie-fourth-amendment-supreme-court/)
