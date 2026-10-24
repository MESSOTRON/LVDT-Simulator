# Phase 1 – Machbarkeitsanalyse: Simulations- und Auslegungswerkzeug für LVDTs

Stand: 24.10.2026 · Projekt MESSOTRON R&D · Phase 1 abgeschlossen, Rückfragen offen
Begleitdokumente: [02_Datenanforderungen.md](02_Datenanforderungen.md) ·
[03_Rueckfragen.md](03_Rueckfragen.md)

---

## 0. Ergebnis in Kürze

**Ja, ein valides elektromagnetisches Modell lässt sich aus den Wickeldaten herleiten.**
Ein LVDT ist physikalisch vollständig beschrieben: quasistatische Maxwell-Gleichungen mit
Wirbelströmen in einer nahezu rotationssymmetrischen Anordnung. Es fehlen keine Gleichungen.
Unbekannt sind **Werkstoffparameter** (Ihre Kern- und Gehäusestähle sind magnetisch nicht
spezifiziert), und es braucht eine **saubere Zuordnung** von Messdaten zu Wicklung, Kern
und Messbedingungen.

Ich habe die Machbarkeit nicht nur bewertet, sondern mit einem Rechenkern-Prototyp belegt
(`lvdt_sim/`, Abschnitt 4):

- **Physik korrekt:** Wirbelströme im massiven Kern weichen höchstens 0,14 % von der exakten
  Bessel-Lösung ab (100 Hz … 50 kHz). Gegeninduktivitäten von Luftspulen weichen unter 0,7 %
  vom analytischen Filamentmodell ab.
- **Numerisch sauber:** Bei 2,5-fach feinerem Netz ändert sich die Empfindlichkeit um
  0,006 %, die Phase um 0,03° und die Linearitätsabweichung um 0,004 % der Spanne. Für
  symmetrische Designs ist die Nullstellung numerisch exakt.
- **Schnell genug für Auslegung:** etwa 1 s pro Kernposition, eine komplette Kennlinie mit
  40 Punkten in unter einer Minute auf einem gewöhnlichen 4-Kern-Rechner.
- **Liefert die gewünschten Größen:** Kennlinie, Linearität, Empfindlichkeit, Phase,
  Frequenzgang, Primärimpedanz und Stromaufnahme. Die Wicklung wird windungsgenau aus
  Verfahrwegen (CNC-Logik) aufgebaut.
- **Ist als Auslegungswerkzeug nutzbar:** Am fiktiven Demo-LVDT (±10 mm) senkt allein die
  Optimierung der Kernlänge die Linearitätsabweichung von 3,9 % auf 0,33 % der Spanne
  (Abschnitt 4.3).
- **Deckt auf, was im Versuch schwer zu sehen ist:** Bei verlustbehaftetem Kern kann sich die
  Ausgangsphase über den Hub ändern. Derselbe simulierte Sensor zeigt dann je nach Messkette
  0,22 %, 0,33 % oder 12,5 % Linearitätsabweichung (Abschnitt 2.6). Für den Abgleich mit der
  Datenbank muss die Auswertung der Messkette deshalb genau bekannt sein.

**Bedingungen für ein validiertes Modell Ihrer realen Sensoren:**

1. **Werkstoffkalibrierung:** Anfangspermeabilität, Leitfähigkeit und Verluste der Kern- und
   Gehäusewerkstoffe werden aus Ihren Messdaten identifiziert, nicht aus Datenblättern
   übernommen. Wichtiger Befund aus Phase 1: Bei üblichen Speisefrequenzen (≥ 5 kHz) wirkt
   der Kern fast nur über das Verhältnis µr/σ. Am robustesten trennt man beide Werte, indem
   man **σ direkt am Kernstab misst** (einfache 4-Leiter-Messung) und µr dann aus Kennlinie
   und Phase bestimmt. Messungen bei einer zweiten, niedrigeren Frequenz helfen zusätzlich
   (Abschnitt 5).
2. **Bekannte Messbedingungen** der Datenbank: Speisespannung, Frequenz, Messelektronik und
   **Art der Demodulation** (gleichrichtend oder phasenempfindlich, Phasenabgleich), Last.
3. **Rotationssymmetrie** der Bauform. Schlitze und Kabelabgänge sind gesondert zu bewerten.
4. **Rekonstruierbare Wicklung** aus Wickelanweisung und CNC-Programm: Lagen, Steigungen,
   Wickelrichtung, Verschaltung. Nach Ihrer Beschreibung ist das gegeben.
5. **Prüfung der Aussteuerung:** Die Feldstärke im Kern erreicht bei 3 V Speisung etwa
   100–170 A/m (Abschnitt 2.5). Das liegt im Bereich, in dem die Permeabilität nicht
   schlussgeglühter Stähle pegelabhängig wird. Das wird mit einer Messung bei zwei
   Speisespannungen geprüft und ggf. im Modell berücksichtigt.

**Empfehlung:** Weiter mit Phase 2 (Datenübernahme und Import für 3–5 Referenzsensoren),
sobald die Rückfragen ([03_Rueckfragen.md](03_Rueckfragen.md)) geklärt sind.

---

## 1. Ausgangslage und Zielbild

MESSOTRON hat seine LVDT-Wicklungen bisher iterativ entwickelt: Muster wickeln, messen,
anpassen. Viele dieser Designs laufen seit Jahren zuverlässig. Es fehlt ein Werkzeug, das
vor dem ersten Muster vorhersagt, wie sich eine Wicklung verhält.

Das Zielbild in drei Stufen:

1. **Nachrechnen (digitaler Zwilling):** Bestehende Spulen aus Wickelprogramm, Geometrie
   und Kern berechnen: Kennlinie, Linearität, Empfindlichkeit, Phase, Primärimpedanz,
   günstige Speisefrequenz. Abgleich mit der Messdatenbank.
2. **Variantenrechnung:** Ausgehend von einem validierten Design einzelne Parameter ändern,
   etwa Kernwerkstoff, Kernlänge oder -durchmesser, Wickelkörper (Edelstahl ↔ Kunststoff),
   Frequenz, Windungszahlen oder Verlegeformel.
3. **Auslegung/Optimierung:** Aus Zielvorgaben (Hub, Empfindlichkeit, Linearität,
   Bauraum) einen Wicklungsvorschlag erzeugen und ihn optional als CNC-Programm ausgeben.

## 2. Physik Ihres Aufbaus: was Kennlinie, Empfindlichkeit und Phase bestimmt

### 2.1 Prinzip

Die Primärspule wird mit der Spannung U_P gespeist. Der Kern koppelt sie unterschiedlich
stark mit den Sekundärspulen S1 und S2. Für die Gegenreihenschaltung gilt

    U_out(x) = jω · [M₂(x) − M₁(x)] · I_P(x),     I_P(x) = U_P / Z_P(x)

M₁, M₂ sind die Gegeninduktivitäten, Z_P ist die Primärimpedanz. Alle drei hängen von der
Kernposition x ab und sind wegen der Wirbelströme **komplex**. Das Modell berechnet sie
direkt als Impedanzmatrix Z(x, f) der drei Spulen. Daraus folgt jede Beschaltung:
Quellimpedanz, Last, Kabel, später auch eine Auswerteelektronik.

### 2.2 Massiver Stahlkern: Wirbelströme und Skin-Effekt

Ihre Kerne sind aus massiven, hochpermeablen Stählen, nicht aus Ferrit oder Mu-Metall. Bei
kHz-Frequenzen dringt der Wechselfluss nur in eine dünne Randschicht ein:

| Werkstoff (angenommene Werte) | 1 kHz | 2,5 kHz | 5 kHz | 10 kHz | 20 kHz |
|---|---|---|---|---|---|
| Kern ferritischer Edelstahl (z. B. 1.4105), µr = 400, σ = 1,43 MS/m | 0,67 mm | 0,42 mm | 0,30 mm | 0,21 mm | 0,15 mm |
| derselbe mit µr = 150 | 1,09 mm | 0,69 mm | 0,49 mm | 0,34 mm | 0,24 mm |
| Gehäuse Automatenstahl (z. B. 1.0718), µr = 300, σ = 5 MS/m | 0,41 mm | 0,26 mm | 0,18 mm | 0,13 mm | 0,09 mm |
| Wickelrohr austenitischer Edelstahl, µr = 1,05, σ = 1,4 MS/m | 13 mm | 8,3 mm | 5,9 mm | 4,2 mm | 2,9 mm |

*Eindringtiefe δ = 1/√(π f µ₀ µr σ)*

Folgen:

- Ein Kern mit Ø 6 mm führt bei 5 kHz den Fluss praktisch nur in den äußeren 0,3–0,5 mm.
  Die **effektive Permeabilität ist komplex und frequenzabhängig**. Bei 5 kHz liegt sie im
  Validierungsbeispiel nur bei |µ_eff| ≈ 55 statt 400, mit −44° Phase
  (Bild [06](img/06_validierung_bessel.png)).
- Das erklärt, warum Ihre Sensoren **Phasenverschiebung und Wirbelstromverluste** haben
  und trotzdem gut linear sind. Die Linearität ist überwiegend eine Frage der Geometrie
  (Wicklungsverteilung, Kernlänge). Die Werkstoffverluste wirken vor allem auf
  Empfindlichkeit und Phase. Eine wichtige Ausnahme beschreibt Abschnitt 2.6.
- **Gleiche Wirkung, verschiedene Ursachen:** Bei starkem Skin-Effekt hängt das Verhalten
  näherungsweise nur von √(µr/σ) ab. Messungen bei einer einzigen hohen Frequenz können
  einen hochpermeablen, gut leitenden Kern nicht von einem weniger permeablen, schlechter
  leitenden unterscheiden. Das hat Konsequenzen für die Kalibrierung (Abschnitt 5).

### 2.3 Edelstahl-Wickelrohr: Kurzschlusswindung

Das dünne Edelstahlrohr ist elektrisch eine geschlossene Windung um den Kern. Eine einfache
Abschätzung ohne Kern (τ = µ₀σ·r·t/2 ≈ 0,9 µs bei r = 3,45 mm, t = 0,3 mm) ergibt nur
≈ 1,6° Phase bei 5 kHz. **Mit Kern ist die Wirkung um ein Vielfaches größer.** Das Rohr
umschließt den gesamten Kernfluss, und die Spannung in dieser Kurzschlusswindung steigt
entsprechend. Im Demo-LVDT kostet das Edelstahlrohr bei 5 kHz gegenüber einem
Kunststoffkörper **rund 23 % Empfindlichkeit und 27° Phase** (Abschnitt 4.3,
Bild [04](img/04_frequenzgang.png)). Die geringe Permeabilität des Rohres (µr 1–1,3, je nach
Kaltverformung) spielt dagegen eine Nebenrolle. Wandstärke und Werkstoff des Rohres sind
damit wichtige Auslegungsparameter. Solche Kopplungseffekte entgehen einer Handrechnung, die
FEM erfasst sie automatisch.

### 2.4 Gehäuse als magnetischer Käfig

Das Stahlgehäuse mit Endscheiben schließt den Fluss außen und schirmt ab. Bei kHz-Frequenzen
fließen aber auch dort Wirbelströme: Mit den angenommenen Werten beträgt δ ≈ 0,18 mm in
einer 1 mm dicken Wand. Im Demo-Modell kosten die Wirbelströme im Gehäuse bei 5 kHz
**rund 40 % Empfindlichkeit und 12° Phase** (Variante „Gehäuse ohne Wirbelströme“ in
Abschnitt 4.3). Ohne Wirbelströme in Kern, Rohr und Gehäuse wäre der Ausgang nahezu
phasengleich mit der Speisung (Kontrollrechnung mit σ = 0: Transferimpedanz exakt 90°).
Gehäusewerkstoff, Wandstärke und ein eventueller Längsschlitz sind damit **echte
Auslegungsparameter** für Phase und Empfindlichkeit, und das Modell erfasst sie.

### 2.5 Aussteuerung (Gültigkeit des linearen Modells)

Das Modell nimmt lineare Werkstoffe an, also eine konstante, gegebenenfalls komplexe
Permeabilität. Im Demo-LVDT (3 V, 5 kHz, 468 Primärwindungen, ≈ 18–22 mA) erreicht die
Feldstärke an der Kernoberfläche **≈ 110–120 A/m eff. (≈ 160–170 A/m Scheitel)**, die
Flussdichte ≈ 55–60 mT. Das ist weit weg von der Sättigung. Es liegt aber im Bereich der
Koerzitivfeldstärke nicht schlussgeglühter Stähle, also im **Rayleigh-Bereich**. Dort steigt
die Permeabilität mit der Aussteuerung, und es entstehen Hystereseverluste.

Folgen:
- Die Empfindlichkeit kann leicht von der Speisespannung abhängen.
- Für die Kalibrierung müssen die Werkstoffwerte **bei der tatsächlichen Speisespannung**
  bestimmt werden.
- Ist der Effekt relevant, wird er mit einer amplitudenabhängigen Permeabilität je Element
  abgebildet. Das ist eine iterative Lösung, kein neues Modell.
- Prüfung: Kennlinie oder Endwert bei zwei Speisespannungen messen
  ([02_Datenanforderungen.md](02_Datenanforderungen.md), Abschnitt 5).

### 2.6 Phase über dem Hub: Die Messkette bestimmt die gemessene Linearität

Der Kern ist verlustbehaftet. Wenn sein Ende tief in eine Sekundärspule eintaucht, kann sich
die Phase der Ausgangsspannung mit der Position ändern. Beim Demo-LVDT mit 36 mm Kern bleibt
sie nahezu konstant (−40° … −39°). Mit 50 mm Kern wandert sie von −81° nahe Null auf −61°
bei ±10 mm. Dann hängt die **gemessene Linearität** davon ab, wie das Signal ausgewertet wird:

| Auswertung des identischen Sensors (Kern 50 mm, ±10 mm) | Linearitätsabweichung |
|---|---|
| Gleichrichtung (Betrag, Vorzeichen aus Phasenlage) | 0,22 % der Spanne |
| Synchrondemodulation, Referenzphase optimal abgeglichen | 0,33 % |
| Synchrondemodulation, Referenz = Speisespannung ohne Phasenabgleich | 12,5 % (Signal nur 49 % des Betrags) |

Folgen:
- Für den Abgleich mit der Messdatenbank muss die Auswertung der Messkette genau bekannt
  sein (Rückfrage A.1). Das Modell kann jede dieser Auswertungen nachbilden.
- Bei der Auslegung kann das Werkzeug auf eine **über dem Hub konstante Phase** optimieren.
  Das macht den Sensor unempfindlich gegenüber der Auswerteelektronik des Kunden.

### 2.7 Nicht im Kernmodell enthalten, aber abschätzbar

- **Kapazitäten** der feindrahtigen, vielwindigen Sekundärspulen: Ihre Eigenresonanz liegt
  meist weit über der Speisefrequenz. Wir prüfen das per Messung und bilden es bei Bedarf als
  konzentrierte Kapazität im Netzwerk ab.
- **Nullspannung:** Sie entsteht durch Unsymmetrien, kapazitive Kopplung und Oberwellen. Ein
  rotationssymmetrisches Modell sagt nur den Quadraturanteil voraus. Den Rest erfassen wir
  statistisch aus der Datenbank.
- **Temperaturgang:** Er lässt sich über die Temperaturkoeffizienten von Kupfer, Stahl-σ und
  µr abbilden. Das ist eine spätere Ausbaustufe.

## 3. Modellierungsansätze im Vergleich

| Ansatz | Physikalische Vollständigkeit | Rechenzeit | Eignung |
|---|---|---|---|
| Analytisch (Filamentmodell, Bessel-Kern) | Luftspulen exakt; Kern, Gehäuse und Streufelder nur genähert | µs–ms | Vorauslegung, Plausibilisierung |
| Magnetisches Ersatzschaltbild (Reluktanznetz) | Streuung und Wirbelströme nur über Korrekturfaktoren | ms | schnell, aber erst nach Kalibrierung je Bauform |
| **2D-axialsymmetrische zeitharmonische FEM** | vollständig für lineare Werkstoffe: Wirbelströme in Kern, Rohr und Gehäuse, windungsgenaue Wicklungsverteilung | ≈ 1 s je Kernposition | **physikalischer Kern des digitalen Zwillings** |
| 3D-FEM | auch nicht rotationssymmetrische Details | Minuten bis Stunden | nur punktuell (Schlitze, Kabelabgang) |
| Rein datengetrieben (ML auf Messdaten) | keine Physik, nur Interpolation zwischen bekannten Designs | ms | ungeeignet für neue Kerne/Wicklungen außerhalb der Daten |
| **Hybrid: FEM + Kalibrierung an Messdaten + Restfehlermodell** | Physik plus Ihre Erfahrung aus zehntausenden Messungen | – | **Empfehlung** |

Für die Optimierung mit tausenden Varianten kann später ein schnelles Ersatzmodell
dazukommen, das aus FEM-Rechnungen trainiert wird.

**Eigener Rechenkern oder kommerzielle Software?** Kommerzielle Programme (COMSOL, Ansys
Maxwell) und das freie FEMM können LVDTs grundsätzlich rechnen. Ein schlanker eigener Kern
hat für dieses Ziel aber klare Vorteile: direkter Import von CNC-Programmen und Messdaten,
automatische Nachrechnung hunderter Designs, Optimierungsschleifen, keine Lizenzkosten und
volle Kontrolle über die Kalibrierung. Kommerzielle Werkzeuge bleiben zum Gegenrechnen
sinnvoll.

## 4. Proof of Concept (in Phase 1 umgesetzt)

### 4.1 Was gebaut wurde

`lvdt_sim/` ist ein Python-Paket (numpy/scipy, ca. 750 Zeilen):

- **Geometrie** als Rechteck-Regionen in der r-z-Halbebene: Wickelkörper, Kammern, Gehäuse,
  Endscheiben, bewegter Kern samt Stößel.
- **Wicklung** als Lagen mit Abschnitten konstanter Steigung. Die Funktion
  `layers_from_moves()` übersetzt Verfahrwege „von z_a nach z_b mit N Umdrehungen“ in Lagen.
  Eine Umkehr der Verfahrrichtung beginnt eine neue Lage. Das ist die Brücke zu Ihren
  CNC-Programmen; progressive Verlegeformeln sind enthalten.
- **FEM**: zeitharmonisch, axialsymmetrisch, Unbekannte ist die Flussfunktion r·A_φ.
  Das Netz wird an Materialgrenzen und an der Eindringtiefe verfeinert. Im Hubbereich ist
  es axial gleichmäßig, damit beim Verfahren des Kerns kein Umvernetzungsrauschen in der
  Kennlinie entsteht.
- **Ergebnis** je Kernposition und Frequenz ist die komplexe 3×3-Impedanzmatrix (P, S1, S2).
  Daraus berechnet das Paket Ausgangsspannung bei Last, Primärstrom, Einzelspannungen S1/S2,
  phasenrichtige (synchrone) Demodulation, Linearität und Frequenzgang.

### 4.2 Validierung

| Test | Referenz | max. Abweichung |
|---|---|---|
| Massiver Kern Ø 6 mm (µr = 400, σ = 1,43 MS/m) im axialen Wechselfeld, 100 Hz … 50 kHz | exakte Bessel-Lösung | **0,14 %** (Betrag der komplexen µ_eff) |
| Unmagnetischer Edelstahlstab (µr = 1,05, σ = 1,4 MS/m), 5 kHz | Bessel-Lösung | 0,10 % |
| Gegeninduktivitäten dreier Luftspulen | Maxwell-Formel für koaxiale Leiterschleifen, über die Wicklungsquerschnitte summiert | 0,37–0,62 % (Rest: endlicher Rechenbereich) |
| Netzkonvergenz Demo-LVDT (107 000 vs. 270 000 Unbekannte) | feineres Netz | Empfindlichkeit 0,006 %, Phase 0,03°, Linearität 0,004 % der Spanne |
| Symmetrie, Reziprozität, Lastfall | Nullspannung, U(−x) = −U(x), Z = Zᵀ, Leerlaufgrenzfall | < 10⁻⁹ relativ |

![Validierung](img/06_validierung_bessel.png)

### 4.3 Demo-LVDT (fiktiv, Werkstoffwerte angenommen)

Aufbau nach Ihrer Beschreibung: Edelstahl-Wickelrohr Ø 6,6/7,2 mm, drei Kammern
S1 | P | S2 zu je 20 mm, Primärspule 468 Windungen (Ø 0,15 mm, 4 Lagen), Sekundärspulen je
2100 Windungen (Ø 0,08 mm, 10 Lagen), Stahlgehäuse Ø 10/12 mm × 66 mm mit Endscheiben,
massiver Kern Ø 6 mm. Speisung 3 V / 5 kHz, Last 100 kΩ, Messbereich ±10 mm.

![Feldbild](img/01_feldbild.png)

**Kernlängenstudie** (eine Variantenrechnung mit 17 Kernlängen × 21 Positionen, ca. 5 Minuten):

![Kernlängenstudie](img/03_kernlaengen_studie.png)

| Kernlänge | Empfindlichkeit | Phase | Linearität ±10 mm | Linearität ±7,5 mm |
|---|---|---|---|---|
| 36 mm (Ausgangsdesign) | 98,7 mV/V/mm | −39° | 3,9 % der Spanne | 2,2 % |
| 48 mm | 60,2 mV/V/mm | – | 0,71 % | **0,06 %** |
| **50 mm (Optimum für ±10 mm)** | 53,9 mV/V/mm | −69° | **0,33 %** | 0,22 % |

*Empfindlichkeit und Phase aus der Ausgleichsgeraden über ±10 mm, Auswertung phasenrichtig
demoduliert; Linearität in % der Ausgangsspanne.*

![Kennlinie](img/02_kennlinie_linearitaet.png)

Das ist der Zielkonflikt, den Sie aus der Praxis kennen: Ein längerer Kern ist linearer,
aber weniger empfindlich. Das Werkzeug macht ihn quantitativ sichtbar und lässt die
Wicklung gegen beide Ziele optimieren, etwa mit abgestufter Sekundärwicklung statt
Kammerwicklung.

**Frequenzgang und Bauform des Wickelkörpers:**

![Frequenzgang](img/04_frequenzgang.png)

Mit den angenommenen Werkstoffwerten liegen das Empfindlichkeitsmaximum bei etwa 200–290 Hz
und der Phasennulldurchgang bei 250–370 Hz. Darüber dominieren die Wirbelstromverluste.
Bei ≈ 5 kHz ergibt sich:

| Variante | Empfindlichkeit | Phase | \|Z_P\| in Null |
|---|---|---|---|
| Edelstahl-Wickelrohr (Basis) | 55 mV/V/mm | −75° | 162 Ω |
| Kunststoff-Spulenkörper | 72 mV/V/mm | −48° | 206 Ω |
| Basis mit Gehäuse ohne Wirbelströme (z. B. längsgeschlitzt) | 93 mV/V/mm | −63° | 229 Ω |

Die Zahlen gelten nur für die angenommenen Werkstoffwerte. Sie zeigen aber, was das Werkzeug
beantwortet: welche Frequenz für ein Design günstig ist, und wie viel Empfindlichkeit und
Phase die Bauform des Wickelkörpers und das Gehäuse kosten. Die Phase hängt zudem
vom Auswertebereich ab (Abschnitt 2.6). Hier ist sie aus der Steigung zwischen ±5 mm bestimmt.

**Einfluss der unbekannten Kernwerkstoff-Parameter:**

![Werkstoffeinfluss](img/05_werkstoffeinfluss_kern.png)

Bei 5 kHz verlaufen die Linien gleicher Empfindlichkeit und gleicher Phase nahezu parallel:
Beide Messgrößen hängen dort fast nur von µr/σ ab, eine Einzelmessung trennt µr und σ nicht.
Bei 1 kHz weichen die Richtungen voneinander ab, vor allem bei niedriger Leitfähigkeit.
Betrag und Phase bei zwei Frequenzen machen die Trennung also möglich, aber nur schwach
ausgeprägt. **Der robuste Weg ist, σ direkt am Kernstab zu messen.** Dann bleibt µr als
einzige Kernunbekannte, und die ist aus Kennlinie und Phase gut bestimmbar.

### 4.4 Was der Prototyp (noch) nicht leistet

- Er ist **nicht mit realen MESSOTRON-Sensoren abgeglichen**. Alle Werkstoffwerte sind
  Annahmen, die Absolutwerte (z. B. −39° Phase) sind daher nur Größenordnungen.
- Es gibt noch keinen Import Ihrer CNC-Programme. Das Format ist unbekannt (Rückfrage C.11).
- Die pegelabhängige Permeabilität, Kapazitäten, Temperaturgang und die Auswerteelektronik
  sind noch nicht modelliert.
- Es gibt keine Bedienoberfläche, nur Python-Skripte.

## 5. Die Unbekannten und wie wir sie schließen

| Unbekannte | Wirkung | Bestimmung |
|---|---|---|
| Anfangspermeabilität µr des Kerns (je Werkstoff/Zustand) | Empfindlichkeit, Phase, Kennlinienenden | Kalibrierung an Messdaten (Betrag + Phase), nachdem σ gemessen ist |
| Leitfähigkeit σ des Kerns | Phase, Frequenzgang | 4-Leiter-Messung am Stab (einfach, ±2 %) oder Datenblatt (±10 %) |
| Hystereseverluste µ'' | Phase, Pegelabhängigkeit | Kalibrierung, Messung bei 2 Speisespannungen |
| µr, σ des Gehäuses | Empfindlichkeit, Phase, Primärimpedanz | wie Kern; Primärimpedanz ohne Kern ist dafür besonders aussagekräftig |
| Leitfähigkeit und Wandstärke des Edelstahlrohres | groß (im Demo bei 5 kHz ≈ 23 % Empfindlichkeit, 27° Phase) | σ austenitischer Stähle ist gut bekannt (Datenblatt); Wandstärke aus Zeichnung |
| µr des Edelstahlrohres (1–1,3) | gering | Kalibrierung oder Annahme |
| tatsächlicher Lagenaufbau (Lagenhöhe, Wickelbild, Lackdicke) | Windungsradien → Kopplung, Gleichstromwiderstand | Wickelanweisung + gemessener Außendurchmesser + Abgleich mit gemessenem R_dc |
| Messkette der Datenbank (Elektronik, Demodulation, Last) | Absolutwerte **und** gemessene Linearität (Abschnitt 2.6) | Dokumentation des Prüfstands (Rückfrage A.1–A.3) |
| Fertigungsstreuung (Steigungsfehler, Lagensprünge, Kerntoleranzen) | Streuung der Linearität | statistisch aus der Datenbank |

**Kalibrierstrategie:**

- Die Werkstoffe werden in **Klassen** eingeteilt, z. B. 3–6 Kernwerkstoffe und
  2–3 Gehäusewerkstoffe. Jede Klasse erhält **einen** Parametersatz für alle Designs, also
  wenige globale Parameter statt einer Anpassung je Sensortyp.
- Die Parameter werden an den Referenzsensoren identifiziert, mit allen verfügbaren
  Messgrößen (Kennlinie, Phase, Primärstrom, Frequenzpunkte).
- Der eigentliche Machbarkeitsnachweis ist die **Vorhersage für Designs, die nicht in die
  Kalibrierung eingeflossen sind**: Parameter, die an Typ A bestimmt wurden, müssen Typ B
  vorhersagen.
- Systematische Restabweichungen über viele Designs werden in einem kleinen
  Korrekturmodell erfasst und bleiben dokumentiert, nicht versteckt.

## 6. Rolle der Messdatenbank

Ihre Datenbank mit zehntausenden Messungen ist der wertvollste Baustein, aus drei Gründen:

1. **Kalibrierung und Validierung** über viele Designs, Kerne und Werkstoffe hinweg.
2. **Mittelwertkennlinie je Design:** Über viele Exemplare gemittelt fallen zufällige
   Wickelfehler heraus. Diese Mittelwertkennlinie ist die richtige Vergleichsgröße für das
   (ideale) Modell.
3. **Streuung je Design:** Daraus entsteht ein Toleranzmodell. Eine Monte-Carlo-Rechnung
   mit Steigungs- und Windungszahlfehlern sagt dann nicht nur die nominelle Linearität
   voraus, sondern auch ihre Verteilung in der Serie (Ausbeute).

Voraussetzung ist, dass jede Messung einem Design (Wickelprogramm-Version, Kern) und den
Messbedingungen zugeordnet werden kann.

## 7. Erwartete Genauigkeit

| Größe | ohne Kalibrierung (Handbuchwerte) | nach Kalibrierung (Ziel, in Phase 3 zu belegen) |
|---|---|---|
| Empfindlichkeit | ±20–40 % | ±3–5 % |
| Phase | ±10–30° | ±2–3° |
| Primärimpedanz/-strom | ±20 % | ±3–5 % |
| Kennlinienform, systematische Linearitätsabweichung | qualitativ richtig | Verlauf gut, absolut etwa ±0,05–0,1 % der Spanne |
| Linearität eines einzelnen Exemplars | – | durch Fertigungsstreuung begrenzt → statistische Aussage |
| günstigste Frequenz | Tendenz | ±10–20 % |
| Nullspannung | nicht vorhersagbar | nur statistisch |

Das sind Zielwerte, abgeschätzt aus den verbleibenden Unsicherheiten der Eingangsgrößen nach
der Kalibrierung (Werkstoffstreuung, Maßtoleranzen, Messunsicherheit). Sie sind keine
Garantie. In Phase 3 werden sie an den Referenzsensoren überprüft; das ist der zentrale
Entscheidungspunkt des Projekts.

## 8. Vorgeschlagenes Vorgehen

| Phase | Inhalt | Ergebnis / Entscheidungspunkt |
|---|---|---|
| **2 Daten & Import** | Rückfragen klären; 3–5 Referenzsensoren festlegen; CNC-Programm-Parser, Import der Wickelanweisungen, Datenbankexport; gezielte Zusatzmessungen | Referenzsensoren vollständig als Modell-Eingabe vorhanden |
| **3 Nachrechnung & Kalibrierung** | Referenzsensoren rechnen, Werkstoffklassen identifizieren, Pegelabhängigkeit prüfen | **Gate:** Werden die Genauigkeitsziele aus Abschnitt 7 erreicht, auch für nicht kalibrierte Designs? |
| **4 Validierung in der Breite** | Nachrechnung vieler Designs aus der Datenbank, Restfehler- und Streuungsmodell | belastbare Fehlerstatistik, Toleranzmodell |
| **5 Auslegungswerkzeug** | Bedienoberfläche, Variantenrechnung, Optimierung (Zielvorgaben → Wicklung/Kern), Toleranzanalyse, optional CNC-Export | einsatzfähiges Werkzeug für die Entwicklung |

## 9. Risiken und Gegenmaßnahmen

| Risiko | Wirkung | Gegenmaßnahme |
|---|---|---|
| Datenbank enthält nur demodulierte Beträge ohne Phase und Messbedingungen | µr/σ nicht trennbar, Absolutwerte unsicher | σ am Kernstab messen; kleine Zusatzmesskampagne an 3–5 Referenzsensoren |
| Auswerteverfahren der historischen Messungen unbekannt oder uneinheitlich | gemessene Linearität nicht mit dem Modell vergleichbar (Abschnitt 2.6) | Prüfstandsdokumentation; Referenzsensoren mit bekannter Messkette nachmessen |
| Chargenstreuung der Kernstäbe (Permeabilität schwankt) | Empfindlichkeit streut | Charge in der Datenbank führen; Streuung als Toleranz ausweisen |
| Pegelabhängige Permeabilität (Rayleigh) | Kalibrierung gilt nur bei einer Speisespannung | Messung bei 2 Spannungen; amplitudenabhängiges Werkstoffmodell |
| Wickelbild weicht vom Programm ab (Lagenhöhe, Wildwicklung) | Windungsradien falsch | Abgleich über R_dc und Außendurchmesser |
| Nicht rotationssymmetrische Bauelemente (Schlitze, Kabelabgang) | 2D-Fehler | Einzelvergleich mit 3D-Rechnung; Schlitz als „ohne Wirbelströme“ nähern |
| Zuordnung Messung ↔ Design lückenhaft | weniger nutzbare Daten | mit Referenzsensoren beginnen, bei denen die Zuordnung sicher ist |

## 10. Nächste Schritte

1. Rückfragen beantworten ([03_Rueckfragen.md](03_Rueckfragen.md)); Block A ist entscheidend.
2. Datenpaket für 3–5 Referenzsensoren bereitstellen
   ([02_Datenanforderungen.md](02_Datenanforderungen.md)), mindestens je ein Beispiel für
   Wickelanweisung (PDF), CNC-Programm, Zeichnung und Messdatenexport.
3. Danach Phase 2: Import und erste Nachrechnung eines realen Sensors.
