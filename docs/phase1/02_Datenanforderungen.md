# Phase 1 – Datenanforderungen für den digitalen Zwilling

Stand: 24.10.2026 · gehört zu [01_Machbarkeitsanalyse.md](01_Machbarkeitsanalyse.md)

Diese Liste beschreibt, welche Daten das Modell braucht, wofür und in welcher Form. Wir
starten nicht mit allen Produkten, sondern mit **3 bis 5 Referenzsensoren** (Vorschlag in
Abschnitt 6). Für diese Typen sollte das Datenpaket möglichst vollständig sein.

Prioritäten:
- **A**: zwingend für die Nachrechnung
- **B**: macht die Kalibrierung deutlich sicherer
- **C**: nützlich für spätere Ausbaustufen

---

## 1. Geometrie (je Sensortyp)

| Prio | Angabe | Wofür | Form |
|---|---|---|---|
| A | Wickelkörper: Innen-/Außendurchmesser, Wandstärke des Edelstahlrohres bzw. Kunststoffkörpers, Länge | Windungsradien, Wirbelströme im Rohr | Zeichnung (PDF) oder 3D-Modell (STEP) |
| A | Kammerteilung: Lage und Breite der Kammern und Stege (z-Koordinaten) | Lage der Spulen | Zeichnung |
| A | Gehäuse: Innen-/Außendurchmesser, Länge, Deckel/Endscheiben (Dicke, Bohrung), Lage relativ zum Wickelkörper | magnetischer Rückschluss, Wirbelströme | Zeichnung / STEP |
| A | Kern: Durchmesser, Länge, ggf. Bohrung/Fase; Kernanbindung (Stößel, Gewindestange: Durchmesser, Länge, Werkstoff) | flussführendes Element; ein magnetischer Stößel verändert die Kennlinie | Zeichnung |
| A | Definition des Nullpunkts und des Messbereichs (Kernposition ↔ Gehäuse) | Bezug der Kennlinie | Zeichnung / Prüfanweisung |
| B | Abweichungen von der Rotationssymmetrie: Schlitze im Gehäuse, Kabelabgang, Abflachungen | Bewertung, ob 2D ausreicht | Foto / Zeichnung |
| C | Toleranzen der o.g. Maße | Toleranzanalyse | Zeichnung |

## 2. Werkstoffe

| Prio | Angabe | Wofür |
|---|---|---|
| A | Werkstoffnummer bzw. Handelsname für Kern, Gehäuse, Deckel, Wickelrohr, Stößel | Ausgangswerte und Zuordnung zu Werkstoffklassen |
| A | Lieferzustand / Wärmebehandlung (gezogen, geschält, geglüht, magnetisch schlussgeglüht?) | Permeabilität hängt stark davon ab |
| B | vorhandene Kennwerte: elektrischer Widerstand, Permeabilität, Koerzitivfeldstärke (Werkszeugnis, Datenblatt) | Startwerte der Kalibrierung |
| B | **Probestäbe** jedes Kernwerkstoffs (je ca. 100 mm) | Leitfähigkeit per 4-Leiter-Messung; optional Permeabilität |
| C | Chargeninformation der Kernstäbe | Chargenstreuung |

## 3. Wicklung (je Spule P, S1, S2)

| Prio | Angabe | Wofür | Form |
|---|---|---|---|
| A | **CNC-Wickelprogramm** (Originaldatei) plus Bezeichnung von Maschine und Steuerung | windungsgenaue Verteilung n(z) je Lage | Textdatei(en) |
| A | **Wickelanweisung** (PDF): Drahtsorte, Windungszahl, Lagen, Wickelrichtung, Start/Ende, Isolationsfolien, Verschaltung | Ergänzung und Kontrolle des Programms | PDF |
| A | Draht: Nenndurchmesser blank, Lackgrad (Grad 1/2/3), Hersteller | Lagenhöhe, Gleichstromwiderstand | Angabe |
| A | Verschaltung der Sekundärspulen (Gegenreihe, Anschlussbelegung, 4-/5-/6-Draht) | Vorzeichen, Ausgangsschaltung | Schaltbild |
| B | **gemessener Gleichstromwiderstand** je Spule (Soll und Ist) | Plausibilisierung von Windungszahl und Lagenaufbau | Tabelle |
| B | gemessener Außendurchmesser je Wicklung | tatsächliche Lagenhöhe (Wickelbild) | Tabelle |
| C | Wickelbild (orthozyklisch, wild, Lage für Lage), Drahtzug | Feinmodell der Windungsradien | Angabe |

## 4. Messdaten (Messdatenbank)

| Prio | Angabe | Wofür |
|---|---|---|
| A | Kennlinie: Kernposition und Ausgangssignal je Messpunkt, je Seriennummer | Kalibrierung und Validierung |
| A | Zuordnung jeder Messung zu Artikel, Wickelprogramm (Version), Kern (Werkstoff, Länge) und Prüfdatum | ohne Zuordnung keine Kalibrierung |
| A | Messbedingungen: Speisespannung (eff.), Frequenz, Quellimpedanz, Lastwiderstand am Ausgang, Kabel | Absolutwerte von Empfindlichkeit und Phase |
| A | Messkette: wird das AC-Signal direkt gemessen (Effektivwert, mit oder ohne Phase) oder ein demoduliertes Signal einer Elektronik? Typ, Verstärkung, Demodulationsart und Phasenabgleich der Elektronik | Rückrechnung auf die Sekundärspannung; die Auswertung beeinflusst auch die gemessene Linearität |
| A | Definition der ausgewiesenen Linearität (Ausgleichsgerade, Bezugsgröße) | identische Auswertung im Modell |
| B | Phase Ausgang ↔ Speisung, Primärstrom, Einzelspannungen S1 und S2, Nullspannung | trennt Permeabilität von Leitfähigkeit (siehe Analyse, Abschnitt 5) |
| B | Messungen bei mehreren Frequenzen oder Speisespannungen (falls vorhanden) | Frequenzgang, Aussteuerungseinfluss |
| C | Temperatur bei der Messung, Temperaturgangmessungen | Temperaturmodell |

**Format:** Export als CSV/Excel genügt (eine Zeile je Messpunkt oder je Messung mit
Positions-/Wertespalten), dazu eine kurze Beschreibung der Spalten. Bei direktem
Datenbankzugriff: Schema (Tabellen/Felder) und Typ (SQL Server, Access, …).

## 5. Gezielte Zusatzmessungen (Empfehlung, Prio B)

Diese Messungen kosten wenig Zeit, machen die Kalibrierung aber eindeutig:

1. **Frequenzgang** an 3–5 Referenzsensoren: 500 Hz … 20 kHz (ca. 10 Frequenzen), bei Kern
   in Nullstellung und bei ± Messbereichsende: Sekundärspannung mit Phase und Primärstrom
   (Betrag und Phase) oder Primärimpedanz.
2. **Impedanzen mit LCR-Meter**: L und R von P, S1, S2 jeweils ohne Kern und mit Kern in
   Nullstellung, bei 1, 2,5, 5 und 10 kHz.
3. **Pegelabhängigkeit**: Kennlinie oder Endwert bei zwei Speisespannungen (z. B. 1 V und 5 V),
   um nichtlineares Werkstoffverhalten (Rayleigh-Bereich) zu erkennen.
4. **Leitfähigkeit der Kernstäbe** (4-Leiter-Widerstandsmessung, ca. 100 mm Stab).
5. Optional: **Eigenresonanz** der Sekundärspulen (Impedanzanalysator), um kapazitive
   Effekte auszuschließen.

## 6. Vorschlag Referenzsensoren

| Nr. | Profil | Zweck |
|---|---|---|
| R1 | Edelstahlrohr, kurzer Hub, gängigster Kernwerkstoff, viele Messungen | Basiskalibrierung |
| R2 | wie R1, aber anderer Kernwerkstoff oder andere Kernlänge | trennt Kern- von Spuleneinfluss |
| R3 | Kunststoff- oder GFK-Wickelkörper | Wirbelstromeinfluss des Rohres |
| R4 | langer Hub mit progressiver/abgestufter Wicklung | Prüft die Umsetzung der Verlegeformel |
| R5 | ein Typ mit vorhandenen Phasen- oder Frequenzdaten | Identifikation Permeabilität ↔ Leitfähigkeit |

Für die Validierung brauchen wir zusätzlich 1–2 Typen, deren Daten **nicht** in die
Kalibrierung eingehen. An ihnen zeigt sich, ob das Modell wirklich vorhersagt.

## 7. Datenübergabe

- **Kleine Dateien** (Wickelprogramme, PDFs, Zeichnungen) können in dieses Repository unter
  `data/` (privates Repository, bitte bestätigen) oder in einen SharePoint-Ordner.
- **Messdatenbank**: nicht in Git. Besser ein Export in einen SharePoint/OneDrive-Ordner; die
  Microsoft-365-Verbindung dieser Sitzung kann dort lesen, wenn Sie es freigeben.
- Vertrauliche Kundendaten (Kundennamen, Auftragsnummern) können vor der Übergabe entfernt
  werden. Das Modell braucht nur Artikel/Design-Kennungen.
