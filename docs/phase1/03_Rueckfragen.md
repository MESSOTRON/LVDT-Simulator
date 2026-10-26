# Phase 1 – Rückfragen an MESSOTRON

Stand: 24.10.2026 · gehört zu [01_Machbarkeitsanalyse.md](01_Machbarkeitsanalyse.md)

> **Update 26.10.2026:** Die öffentlichen MESSOTRON-Unterlagen beantworten einen Teil der
> Fragen. Stand je Frage: [../phase2/01_Webrecherche_messotron.md](../phase2/01_Webrecherche_messotron.md),
> Abschnitt 6.

Die Fragen sind nach Wichtigkeit sortiert. Block A entscheidet, ob und wie gut wir mit
der vorhandenen Messdatenbank kalibrieren können. Stichworte als Antwort genügen.

## A. Messdaten und Messbedingungen (entscheidend)

1. **Messkette:** Ist der gespeicherte Ausgangswert die rohe Sekundärspannung (Effektivwert)
   oder das Ausgangssignal einer Auswerteelektronik (demoduliert, verstärkt)? Falls
   Elektronik: Typ, Verstärkung, Demodulation (phasenempfindlich oder gleichrichtend),
   wird die Referenzphase abgeglichen, Filter?
   → *Ohne diese Information lassen sich weder absolute Empfindlichkeiten noch Linearitäten
   vergleichen. Im Demo-Modell ergibt derselbe Sensor je nach Auswertung 0,22 %, 0,33 % oder
   12,5 % Linearitätsabweichung (Analyse, Abschnitt 2.6).*
2. **Speisung:** Spannung (eff.), Frequenz, Konstantspannung oder Konstantstrom,
   Innenwiderstand der Quelle. Für alle Messungen eines Typs gleich?
3. **Last:** Eingangswiderstand der Messung bzw. Elektronik am Sekundärausgang, Kabellänge.
4. **Welche Größen enthält ein Datensatz?** Nur Position und Ausgangssignal, oder auch
   Phase, Primärstrom, Einzelspannungen S1/S2, Nullspannung, Temperatur?
   → *Phase oder Primärstrom machen die Werkstoffidentifikation eindeutig.*
5. **Linearitätsdefinition:** Ausgleichsgerade nach kleinsten Quadraten, Minimax oder
   Endpunktgerade? Bezug: % vom Endwert (einseitig) oder % der Spanne?
6. **Datenbank:** System (SQL Server, Access, CSV, …), ungefähre Anzahl Messungen und
   Sensortypen. Ist jede Messung eindeutig einem Artikel, einer Wickelprogramm-Version und
   einem Kern (Werkstoff, Länge) zugeordnet, oder geht die Zuordnung nur über Artikelnummer
   und Zeichnung?

## B. Bauform und Werkstoffe

7. **Kernwerkstoffe:** Welche Stahlsorten (Werkstoffnummern) setzen Sie ein, in welchem
   Zustand (gezogen, geschliffen, geglüht)? Wie wird der Kern angebunden (Gewindestange,
   Stößel), und ist dieses Teil magnetisch?
8. **Gehäuse/Käfig:** Werkstoff, Wandstärke, Endscheiben/Deckel (Werkstoff, Bohrung).
   Gibt es Schlitze, eine zusätzliche Abschirmung (z. B. Mu-Metall) oder einen
   nicht rotationssymmetrischen Kabelabgang?
9. **Wickelkörper:** Edelstahlrohr (Sorte, Wandstärke, kaltverformt?) bzw. Kunststoff/GFK
   (Material, Kammerstege).
10. **Rotationssymmetrie:** Gibt es Bauformen mit deutlich nicht rotationssymmetrischen
    Elementen? Diese würden wir zunächst zurückstellen.

## C. Wicklung und CNC-Programme

11. **Wickelmaschine und Steuerung:** Hersteller/Typ und Programmformat. Bitte ein
    Beispielprogramm mit der zugehörigen Wickelanweisung schicken. Daran erstelle ich den
    Import (Parser).
12. **Inhalt der Programme:** Ist jede Lage mit Wendepunkten und Steigung je Abschnitt
    enthalten, oder werden Lagen über Wiederholschleifen/Parameter erzeugt?
13. **Anordnung:** Liegt die Primärspule unter, über oder neben den Sekundärspulen? Gibt es
    Kammerwicklungen, durchgehende Lagenwicklungen, progressive bzw. abgestufte
    Verlegeformeln, gegenläufige Lagen?
14. **Draht und Wickelbild:** Drahtsorten (blank-Ø, Lackgrad), Wickelbild (orthozyklisch,
    wild, Lage für Lage), Isolationsfolien zwischen den Spulen?
15. Liegen **gemessene Gleichstromwiderstände** je Spule vor (Prüfprotokoll)?

## D. Ziele und Rahmenbedingungen

16. **Prioritäten der Ausgabegrößen** (bitte reihen): Kennlinie/Linearität,
    Empfindlichkeit, Phase, optimale Frequenz, Primärimpedanz/Stromaufnahme,
    Temperaturverhalten, Nullspannung.
17. **Genauigkeitsziel:** Welche Abweichung Modell ↔ Messung wäre für Sie „gut genug“,
    z. B. Empfindlichkeit ±5 %, Phase ±3°, Linearitätsverlauf ±0,1 % der Spanne?
18. **Nutzer und Plattform:** Wer arbeitet mit dem Werkzeug (Entwicklung, Fertigung,
    Vertrieb)? Windows-Desktopanwendung, Browseroberfläche oder Python-Werkzeug für die
    Entwicklung? Sind Lizenzen für FEM-Software (COMSOL, Ansys Maxwell, FEMM) vorhanden?
    Sie würden nur zum Gegenrechnen dienen.
19. **Datenübergabe und Vertraulichkeit:** Dürfen Wickelprogramme und Zeichnungen in dieses
    private GitHub-Repository? Soll die Messdatenbank lieber über SharePoint/OneDrive
    bereitgestellt werden?
20. **Zusatzmessungen:** Sind ein LCR-Meter oder Impedanzanalysator und ein Messplatz für
    Frequenzsweeps verfügbar? Können wir 3–5 Referenzsensoren gezielt nachmessen (siehe
    Datenanforderungen, Abschnitt 5)?
21. **Umfang:** Nur LVDTs (Differenzialtransformator mit drei Spulen) oder auch induktive
    Halbbrücken bzw. LVITs? Das Modell deckt beides ab, nur die Beschaltung ist anders.
22. **Referenzsensoren:** Welche 3–5 Typen schlagen Sie vor (Profil siehe
    Datenanforderungen, Abschnitt 6)?
