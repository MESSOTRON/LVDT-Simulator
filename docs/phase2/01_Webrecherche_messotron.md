# Phase 2 – Öffentliche MESSOTRON-Daten: was sie für den digitalen Zwilling liefern

Stand: 26.10.2026 · gehört zu [../phase1/02_Datenanforderungen.md](../phase1/02_Datenanforderungen.md)
und [../phase1/03_Rueckfragen.md](../phase1/03_Rueckfragen.md)
Daten: [messotron_web_daten.json](messotron_web_daten.json) (23 Sensortypen bzw. Baureihen, 5 Messverstärker, je mit
Quelle und Belastbarkeit) · Rechnung: [phase_check_results.json](phase_check_results.json)

---

## 0. Ergebnis in Kürze

Die Website (messotron.com / messotron.de: Produktseiten, Datenblätter, Betriebsanleitungen,
Technische Hinweise, Wissensdatenbank) beantwortet einen Teil der Rückfragen. Den Innenaufbau
der Sensoren beschreibt sie erwartungsgemäß nicht.

**Was die Website liefert:**

- **Messkette der MESSOTRON-Elektronik** (Rückfragen A.1–A.3): Die TF-Messverstärker MBI 46.x
  speisen mit **ca. 2 V eff Sinus bei 5 kHz** (max. 12 mA eff), haben **ca. 200 kΩ
  Eingangswiderstand** und demodulieren **phasenempfindlich mit Phasenabgleich**. Die Phase
  wird so eingestellt, dass der Ausgang bei **ca. 3/4 des Nennhubs maximal** ist.
- **Definitionen** (A.5): Empfindlichkeit und Nennausgang in den Datenblättern werden
  **phasenunabhängig** (Betrag) ermittelt und haben bei nicht kalibrierten Sensoren **±10 %
  Toleranz**. Die Linearitätsabweichung ist die größte Abweichung von der Sollgeraden,
  **bezogen auf den gesamten Messbereich** (FSO).
- **Werkstoffe** (B.7, B.8): Gehäuse aus **rostfreiem Stahl**, Kern aus **magnetischem
  Edelstahl**, Kernverlängerungen **unmagnetisch**. Einige Kerne sind **PTFE-beschichtet**.
- **Kennwerte von 23 Typen**: Gehäuse-Ø 5–25 mm, Kern-Ø 2–5,6 mm, Hübe von 8 mm bis 1000 mm,
  Standardfrequenz 5 kHz (Option 10 kHz, einzelne Typen 3 kHz oder 10 kHz Standard),
  Nennausgang langer Typen 80–175 mV/V, Primärimpedanzen 50 Ω bis > 400 Ω.
- **Kern und Spule sind gepaart**: Tauchanker sind nicht beliebig tauschbar, zu jedem Sensor
  gehört ein Prüfprotokoll.

**Wichtigster Befund für das Modell:** MESSOTRON nennt für seine LVDTs eine Phase zwischen
Speise- und Ausgangsspannung von **typisch 1–20°**. Der Demo-LVDT aus Phase 1 liegt mit den
angenommenen Werkstoffwerten bei 5 kHz bei **−75°**. Eine Nachrechnung (Abschnitt 5.1) zeigt:
Der Gehäusewerkstoff allein erklärt den Unterschied nicht. Die angenommenen
Wirbelstromverluste in Wickelrohr, Kern und Gehäuse sind zusammen deutlich zu hoch, oder der
Aufbau realer Sensoren unterscheidet sich vom Demo. Die Phase ist damit ein starker Hebel für
die Kalibrierung, und die Bauart des Wickelkörpers wird zur wichtigsten offenen Frage.

**Was fehlt** (erwartungsgemäß, intern): Wickelkörper, Wandstärken, Kammerteilung,
Windungszahlen, Drahtsorten, Werkstoffnummern, Wickelprogramme, Prüfstandsbeschreibung und
die Messdatenbank. Block A der Rückfragen bleibt für die **Prüfstandsmessungen** offen, denn
die Website beschreibt nur die Verstärker, nicht den Prüfplatz.

## 1. Vorgehen und Belastbarkeit

- Der direkte Abruf von www.messotron.de und www.messotron.com war aus der Arbeitsumgebung
  durch die Netzwerkrichtlinie gesperrt. Die Daten stammen deshalb aus **Auszügen einer
  Websuche** über diese Seiten und PDFs. Gesucht wurde nur auf den MESSOTRON-Domains.
- Jeder Wert in [messotron_web_daten.json](messotron_web_daten.json) trägt Quelle und
  Belastbarkeit: **hoch** (mehrfach gleich oder wörtlich zitiert), **mittel** (ein Auszug,
  plausibel), **niedrig** (Tabelle im Auszug verschoben oder widersprüchlich).
- Bekannte Widersprüche: DTU (5 mm oder 16 mm Gehäuse), DGO (Kern 3/5 mm in einer
  Variante), DPF (320 bar oder < 50 bar), DFI (320 oder 450 bar), DU (Zuordnung der
  Nennausgänge zu den Baulängen).
- **Vor einer Verwendung in der Kalibrierung** sind die Werte gegen die Original-PDFs zu
  prüfen. Dafür reicht es, die Domains messotron.com und messotron.de in den
  Netzwerkeinstellungen der Umgebung freizugeben oder die PDFs unter `data/` abzulegen.

## 2. Messkette und Definitionen laut MESSOTRON

| Thema | Aussage MESSOTRON | Quelle | Bedeutung für das Modell |
|---|---|---|---|
| Speisung | MBI 46.31 / 46.12 / 46.13 / 46.51: ca. 2 V eff, Sinus, 5 kHz ±5 % (Option 1–20 kHz), max. 12 mA eff. Sensordatenblätter: 1–5 V eff | Betriebsanleitungen MBI 46.31, 46.13; Datenblatt MBI 46.51 | Standardfall U₀ = 2 V, f = 5 kHz. Auslegungsgrenze \|Z_P\| ≳ 2 V / 12 mA ≈ 170 Ω |
| Last | Eingangswiderstand sekundär ca. 200 kΩ | MBI 46.12, 46.13, 46.31 | R_load = 200 kΩ statt 100 kΩ im Demo (Einfluss gering, Abschnitt 5.1) |
| Sensorbereich der Elektronik | Eingangsimpedanz 100–1000 Ω; Nennausgang 20–600 mV/V (46.31) bzw. 130–600 mV/V (46.12/46.13, Option /V6 für < 130 mV/V) | dto. | Zielbereich für Auslegungen |
| Demodulation | Oszillator speist und liefert die Referenz, Auswertung ratiometrisch. Der Phasentrimmer „verschiebt die Auswertung der Messspannung auf der Zeitachse“ | Wissensdatenbank TF-Messverstärker; MBI 46.13 | **phasenempfindliche (synchrone) Demodulation** mit einstellbarer Referenzphase |
| Phasenabgleich | Kern auf ca. 3/4 des Nennhubs (46.31: „kurz vor Messbereichsende“), mit P_Ph den Ausgang auf Maximum stellen, danach Nullpunkt prüfen. Grobstufe über Kondensatoren C1/C2 | Technische Hinweise; MBI 46.31 | Referenzphase = Phase von U_out bei 0,75·x_nenn. Das entspricht etwa Zeile 2 der Tabelle in Analyse 2.6 |
| Nullpunkt | Symmetrische Sensoren: Mitte. Abgleich mit **herausgenommenem Tauchanker** auf 0 V, dann Anker so fixieren, dass 0 V bleibt. Alternativ: Stellung, in der normale und vertauschte Speiseleitungen denselben Wert liefern | Technische Hinweise | x = 0 ist elektrisch definiert (Ausgangsnull), nicht geometrisch |
| Phasenverschiebung | LVDT typisch **1–20°**, abhängig von Spulentyp und Frequenz; Kabelkapazität trägt bei. LVIT (Differentialdrossel) praktisch keine Phase | Technische Hinweise (DE/EN) | Plausibilitätsgrenze für die Kalibrierung (Abschnitt 5.1) |
| Empfindlichkeit, Nennausgang | U_out/U_Speise je mm bzw. am Ende des Nennhubs. **Phasenunabhängig** ermittelt, **±10 %** bei nicht kalibrierten Sensoren; kalibrierte Sensoren z. B. 80 mV/V unabhängig vom Hub. Abhängig von der Frequenz, üblich 3, 5 oder 10 kHz | Technische Hinweise; Wissensdatenbank | Vergleich mit Datenblatt über \|U_out(x_nenn)\|/U₀ bei 5 kHz; ±10 % reicht nur zur Plausibilisierung |
| Linearität | Größte Abweichung zwischen Sollkennlinie (Gerade) und realer Kennlinie, bezogen auf den gesamten Messbereich (FSO). Optimaler Abgleich berücksichtigt den Linearitätsfehler über Nullpunkt und Verstärkung (Beispiel: Fehler auf 0,32 % gesenkt) | MBI 46.51.39, MBI 46.32 | Bezug = Spanne, wie `nonlinearity_pct_span` im Modell. **Offen:** Ausgleichsgerade oder Gerade aus Null- und Endpunktabgleich? |
| Anschluss | LVDT standardmäßig 4-Leiter, mehrere Serien optional 5-Leiter (Mittelanzapfung) oder 6-Leiter (getrennte Sekundärspulen); LVIT 3-Leiter | Technical Guidelines; MBI 46.31 | Einzelspannungen S1/S2 sind nur bei 5-/6-Leiter-Typen messbar |
| Paarung | Wegaufnehmer und Tauchanker sind gepaart, nicht beliebig tauschbar. Bei Ersatz neu kalibrieren und neues **Prüfprotokoll** | Technische Hinweise | Jede Messung braucht die Zuordnung zum konkreten Kern |
| Abgleichbedingungen | Im eingebauten Zustand, bei Betriebstemperatur, mit betriebswarmem Verstärker | Technische Hinweise | Messbedingungen in der Datenbank mitführen |

## 3. Bauformen und Kennwerte

Auszug der LVDT-Typen mit verwertbaren Zahlen (vollständig in der JSON-Datei):

| Typ | Gehäuse-Ø | Kern-Ø | Hub | f | Nennausgang / Empfindlichkeit | Z_P | Belastbarkeit |
|---|---|---|---|---|---|---|---|
| DM | 20 mm, Einbaulänge 35 mm | – (Kern 3 g) | ±8 mm (erweitert ±10) | 5 kHz | 40 mV/V/mm | > 400 Ω | hoch |
| DTU | 5 mm, Länge 42 mm | – | 8 mm | 5 kHz | 24 mV/V | ≈ 50 Ω | mittel |
| DTL | 12 mm h9 | 3 mm | 50 / 100 / 200 mm | 5 kHz | 133 / 135 / 125 mV/V | – | hoch |
| DUH | 16 mm | 5,6 mm inkl. PTFE | ±25 … ±250 mm | 5 kHz | 107 / 140 / 163 / 175 / 160 / 162 mV/V | – | mittel |
| DUR | – | – | ±12,5 … ±500 mm | 5 kHz | 100 … 175 mV/V | – | mittel |
| DU | 14 mm | 2 / 3 mm (vermutlich Kern) | 15 … 1000 mm | 5 / 10 kHz | ca. 80–175 mV/V (5 kHz), ca. 100–250 mV/V (10 kHz) | – | niedrig |
| DLH | 12 mm | 3,6 mm inkl. PTFE | bis 500 mm | – | – | – | mittel |
| DGO | 20 mm | – | ±12,5 … ±150 mm | 5 kHz (10) | – | – | hoch |
| DPL | 12 mm | – | ±25 … ±200 mm | **10 kHz** (5) | – | – | mittel |

LVIT-Typen (Halbbrücke): WLG (12 mm, Nennausgang 80 mV/V, 5–10 kHz), WLH (60 … 1,4 mV/V/mm),
WLR (12 mm), **WLU** (16 mm Edelstahl, Spulenimpedanz 600 ±100 Ω mit Kern, **3 kHz**,
Nennausgang ca. 314–340 mV/V). Die Serie **WP** (Langweg bis 1000 mm) arbeitet mit einem
Mantelanker nach dem Wirbelstromprinzip; die zweite Halbbrückenspule ist elektronisch
nachgebildet.

Auffällig:

- Die **Nennausgänge langer Typen bei 5 kHz liegen eng beieinander** (DTL, DUH, DUR, DU:
  etwa 100–175 mV/V). Das ist eine erste, grobe Kontrolle für Längenreihen im Modell.
- Beim DU nennt das Datenblatt **bei 10 kHz höhere Nennausgänge als bei 5 kHz** (Auszug
  unsicher). Das passt zu einer verlustarmen Bauform mit widerstandsbestimmter Primärspule.
  Im Demo-LVDT fällt die Empfindlichkeit oberhalb von etwa 200–300 Hz dagegen ab
  (Analyse 4.3). Auch das spricht dafür, dass die Demo-Verluste zu hoch angesetzt sind.
- Kern-Ø in den Datenblättern enthalten teils die **PTFE-Beschichtung** (DUH 5,6 mm,
  DLH 3,6 mm). Für das Modell zählt der Stahldurchmesser.

## 4. Werkstoffe

| Teil | Aussage | Quelle |
|---|---|---|
| Gehäuse | „hochwertiger rostfreier Stahl“; für den elektrischen Anschluss auch Aluminium | Technische Hinweise; DAA, DPF, DFI, WLU |
| Kern | „magnetischer Edelstahl“ (DM). Allgemein: magnetisierbares, wechselmagnetisches Material (Mu-Metall, Ferrit, Weicheisen genannt) | Datenblatt DM; Wissensdatenbank |
| Kernverlängerung | unmagnetischer Werkstoff | Datenblatt DM |
| Kernoberfläche | PTFE-Beschichtung (DUH, DLH) | Datenblätter DUH, DLH |
| Fertigung | spitzenloses Rundschleifen, Drehen, CNC-Drehen und -Fräsen im Haus | Services / Fertigung |

Folge für das Modell: Phase 1 hat für das Gehäuse Automatenstahl (1.0718, σ = 5 MS/m)
angenommen. Laut Website ist das Gehäuse aus rostfreiem Stahl. Offen ist, ob **ferritisch**
(magnetischer Rückschluss, σ ≈ 1,4–1,7 MS/m) oder **austenitisch** (unmagnetisch, kein
Rückschluss). Das ändert Empfindlichkeit, Primärimpedanz und Phase deutlich (Abschnitt 5.1).
Die Werkstoffbibliothek in `lvdt_sim/materials.py` bleibt unverändert, bis das geklärt ist.

## 5. Folgen für Modell und Phase 2

### 5.1 Plausibilitätsprüfung der Phase

Rechnung mit [examples/phase2_phase_check.py](../../examples/phase2_phase_check.py): Demo-LVDT
aus Phase 1 (Kern 50 mm) unter MBI-Bedingungen (2 V, 5 kHz, 200 kΩ). Die Werkstoffwerte sind
weiterhin **Annahmen**; der ferritische Edelstahl ist mit µr = 300, σ = 1,6 MS/m angesetzt.

| Variante (5 kHz, ±5 mm) | Empfindlichkeit | Phase | \|Z_P\| in Null | I_P bei 2 V |
|---|---|---|---|---|
| Basis Phase 1 (Automatenstahl-Gehäuse, Edelstahlrohr) | 54,9 mV/V/mm | −75,0° | 164 Ω | 12,2 mA |
| Basis mit Kunststoffkörper | 71,4 mV/V/mm | −47,0° | 210 Ω | 9,5 mA |
| Gehäuse ferritischer Edelstahl, Edelstahlrohr | 69,5 mV/V/mm | −71,2° | 189 Ω | 10,6 mA |
| Gehäuse austenitisch (unmagnetisch), Edelstahlrohr | 97,9 mV/V/mm | −70,1° | 113 Ω | 17,8 mA |
| Gehäuse ferritischer Edelstahl, Kunststoffkörper | 92,1 mV/V/mm | −40,0° | 258 Ω | 7,8 mA |
| … dito, Kern ohne Wirbelströme | 145,1 mV/V/mm | −21,9° | 422 Ω | 4,7 mA |
| … dito, Gehäuse ohne Wirbelströme | 124,1 mV/V/mm | −26,7° | 347 Ω | 5,8 mA |
| … dito, Kern und Gehäuse ohne Wirbelströme | 200,0 mV/V/mm | −2,4° | 680 Ω | 2,9 mA |

Befund:

- Der **Gehäusewerkstoff allein** ändert die Phase nur von −75° auf −70° bis −71°. Den
  größten Einzelbeitrag liefert im Demo das **Edelstahl-Wickelrohr** (rund 30°), danach Kern
  und Gehäuse (je etwa 13–18°).
- In den Bereich 1–20° kommt der Demo-Aufbau erst, wenn die Verluste in Rohr, Kern **und**
  Gehäuse zusammen deutlich kleiner sind als angenommen. Mögliche Ursachen in realen
  Sensoren: Kunststoff- oder dünnwandiger Wickelkörper, kleinere Kerndurchmesser
  (2–5 mm statt 6 mm im Demo), andere Werkstoffwerte, andere Proportionen.
- Konsequenz: Die Absolutwerte der Phase aus Phase 1 (−39° bis −75°) sind **nicht** auf
  MESSOTRON-Sensoren übertragbar. Die reale Phase ist dafür ein **empfindlicher
  Kalibrierwert**, und die Bauart des Wickelkörpers (Rückfrage B.9) wird zur wichtigsten
  offenen Konstruktionsfrage.

### 5.2 Messbedingungen und Auswertung im Modell

1. **Standardbedingungen** für Nachrechnungen: U₀ = 2 V eff, f = 5 kHz, R_load = 200 kΩ,
   solange die Prüfstandsdaten nichts anderes sagen.
2. **Auslegungsgrenze**: \|Z_P\| bei Speisefrequenz mindestens ≈ 170 Ω (2 V / 12 mA), Ziel
   100–1000 Ω und Nennausgang 20–600 mV/V (Bereich der MBI-Verstärker). Der Demo-LVDT liegt
   mit 164 Ω knapp darunter.
3. **Aussteuerung**: Bei 2 V statt 3 V sinkt die Feldstärke im Kern auf etwa 2/3, also auf
   rund 75–80 A/m eff (Analyse 2.5). Das liegt weiter im Rayleigh-Bereich; die Messung bei
   zwei Speisespannungen bleibt sinnvoll.
4. **Auswertung wie MBI-Verstärker** (noch nicht umgesetzt): Referenzphase = Phase von U_out
   bei 0,75·x_nenn, Nullpunkt aus der Ausgangsnull. `lvdt_sim.analysis.evaluate` bestimmt die
   Referenzphase bisher aus der komplexen Ausgleichsgeraden. Eine Variante mit fester
   Referenzphase ist eine kleine Erweiterung.
5. **Datenblattvergleich** über den Betrag \|U_out(x_nenn)\|/U₀ (phasenunabhängig, ±10 %).
6. **LVIT-Halbbrücke** ergänzen: Die W-Serie ist ein großer Teil des Programms.
   `lvdt_sim/circuit.py` kennt bisher nur die LVDT-Beschaltung. Die Feldrechnung bleibt
   gleich. Die Serie WP (Mantelanker, elektronische Halbbrücke) stellen wir zurück.

### 5.3 Folgen für die Datenübernahme

- **Kern-Spulen-Paarung**: Die Datenbank muss jede Messung dem konkreten Kern zuordnen
  (Werkstoff, Länge, Durchmesser ohne Beschichtung).
- **Prüfprotokoll**: Zu jedem Sensor existiert eines. Sein Inhalt (Punkte, Phase,
  Bedingungen) ist der wahrscheinlichste Weg zu Block A der Rückfragen.
- **Zwei Frequenzen**: Mehrere Typen gibt es für 5 und 10 kHz. Messungen desselben Designs
  bei beiden Frequenzen helfen bei der Trennung von µr und σ etwas. Beide liegen aber im
  Bereich starken Skin-Effekts; die direkte σ-Messung am Kernstab bleibt der robuste Weg.

## 6. Stand der Rückfragen nach der Webrecherche

Legende: ✔ beantwortet · ◐ teilweise · ○ offen (intern)

| Nr. | Thema | Stand | Was die Website sagt / was offen bleibt |
|---|---|---|---|
| A.1 | Messkette | ◐ | MBI-Verstärker: phasenempfindlich, Phase auf Maximum bei 3/4 Hub; Datenblattwerte = Betrag. **Offen:** Womit misst der Prüfplatz für die Datenbank? |
| A.2 | Speisung | ◐ | Elektronik 2 V eff / 5 kHz Sinus; Sensoren 1–5 V eff, 5 kHz Standard, 10 kHz Option. **Offen:** Prüfplatzwerte, Quellimpedanz |
| A.3 | Last | ◐ | MBI ≈ 200 kΩ. **Offen:** Prüfplatz, Kabel |
| A.4 | Inhalt eines Datensatzes | ◐ | Prüfprotokoll je Sensor; 4-Leiter Standard (S1/S2 einzeln nur bei 5/6-Leiter). **Offen:** Felder des Protokolls |
| A.5 | Linearitätsdefinition | ◐ | Bezug = gesamter Messbereich. **Offen:** Ausgleichsgerade oder Null-/Endpunktgerade |
| A.6 | Datenbank | ○ | – |
| B.7 | Kernwerkstoffe | ◐ | magnetischer Edelstahl, Verlängerung unmagnetisch, PTFE-Beschichtung, Kern-Ø 2–5,6 mm. **Offen:** Werkstoffnummern, Zustand |
| B.8 | Gehäuse | ◐ | rostfreier Stahl, Ø 5–25 mm. **Offen:** ferritisch oder austenitisch, Wandstärke, Endscheiben |
| B.9 | Wickelkörper | ○ | nichts öffentlich; nach 5.1 die wichtigste offene Frage |
| B.10 | Rotationssymmetrie | ○ | – |
| C.11–15 | Wicklung, CNC-Programme | ○ | nichts öffentlich (erwartet) |
| D.16 | Prioritäten | ○ | – |
| D.17 | Genauigkeitsziel | ◐ | Bezug: Datenblatt ±10 % Empfindlichkeit, Linearitätsklassen 0,5 / 0,25 / 0,1 % FSO. Das Modellziel ±3–5 % liegt deutlich darunter |
| D.18–20 | Nutzer, Datenübergabe, Zusatzmessungen | ○ | – |
| D.21 | Umfang LVDT / LVIT | ◐ | Programm umfasst LVDT (D-Serien), LVIT-Halbbrücken (W-Serien) und WP-Langweg. **Offen:** gewünschter Umfang |
| D.22 | Referenzsensoren | ◐ | Kandidaten nach öffentlicher Datenlage: **DM** (viele Kennwerte, kompakt), **DUH** oder **DTL** (Längenreihe mit Nennausgängen), **WLU** oder **WLG** für LVIT. Endgültig entscheidet die interne Datenlage |

## 7. Nächste Schritte

1. Werte gegen die Original-PDFs prüfen: Domains messotron.com/.de in der Umgebung
   freigeben oder PDFs unter `data/` ablegen. Vorrang haben die als „niedrig“ markierten
   Werte und die Typen, die Referenzsensoren werden könnten.
2. Restfragen beantworten, vor allem: **Prüfplatz-Messkette** (A.1–A.3), **Wickelkörper**
   (B.9), **Gehäusestahl ferritisch oder austenitisch** (B.8), **Linearitätsgerade** (A.5),
   **Inhalt des Prüfprotokolls** (A.4).
3. Optional schon jetzt im Code: Auswertung mit fester Referenzphase (MBI-Verfahren) und
   Standardlast 200 kΩ; Beschaltung für LVIT-Halbbrücken.
