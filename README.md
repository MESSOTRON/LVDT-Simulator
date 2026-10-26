# MESSOTRON R&D – LVDT-Simulation und Auslegung

> **English:** start with [docs/HANDOVER.md](docs/HANDOVER.md) (project history, status, next steps). English translations of all documents are in [docs/en/](docs/en/).

Ziel ist ein **digitaler Zwilling für LVDTs**: Aus Bauform, Werkstoffen, Wickelanweisung
und CNC-Wickelprogramm sollen Kennlinie, Linearität, Empfindlichkeit, Phasengang,
Primärimpedanz und eine günstige Speisefrequenz vorhergesagt werden. Kalibriert und
validiert wird das Modell an der MESSOTRON-Messdatenbank. Danach soll es Varianten
rechnen (anderer Kern, Werkstoff, Frequenz, Wicklung) und neue Sensoren auslegen.

## Stand: Phase 1 – Machbarkeit (abgeschlossen, Rückfragen offen)

| Dokument | Inhalt |
|---|---|
| [docs/phase1/01_Machbarkeitsanalyse.md](docs/phase1/01_Machbarkeitsanalyse.md) | Ergebnis, Physik, Modellansatz, Proof of Concept, Genauigkeit, Vorgehen |
| [docs/phase1/02_Datenanforderungen.md](docs/phase1/02_Datenanforderungen.md) | Welche Daten in welcher Form gebraucht werden |
| [docs/phase1/03_Rueckfragen.md](docs/phase1/03_Rueckfragen.md) | Offene Fragen an MESSOTRON |

## Stand: Phase 2 – Daten & Import (begonnen)

| Dokument | Inhalt |
|---|---|
| [docs/phase2/01_Webrecherche_messotron.md](docs/phase2/01_Webrecherche_messotron.md) | Öffentliche MESSOTRON-Daten: Messkette der MBI-Verstärker, Definitionen, Werkstoffe, Kennwerte; Stand der Rückfragen; Plausibilitätsprüfung der Phase |
| [docs/phase2/messotron_web_daten.json](docs/phase2/messotron_web_daten.json) | Kennwerte von 23 Sensortypen und 5 Messverstärkern mit Quelle und Belastbarkeit |

## Proof-of-Concept-Rechenkern `lvdt_sim/`

2D-axialsymmetrische, zeitharmonische Finite-Elemente-Rechnung (Flussfunktion r·A_φ)
mit Wirbelströmen in Kern, Wickelrohr und Gehäuse. Die Wicklung wird windungsgenau aus
Lagen/Verfahrwegen verteilt. Das Ergebnis ist die vollständige Impedanzmatrix
P/S1/S2 je Kernposition und Frequenz. Daraus folgt die Beschaltung (Speisung,
Gegenreihenschaltung, Last).

| Modul | Aufgabe |
|---|---|
| `materials.py` | Werkstoffe (komplexe Permeabilität, Leitfähigkeit), Annahmen-Bibliothek |
| `geometry.py` | Regionen, Wicklungslagen, Spulen; Umsetzung von Verfahrwegen (CNC) in Lagen |
| `mesh.py`, `fem.py` | strukturiertes, an Eindringtiefe angepasstes Netz; Assemblierung und Lösung |
| `model.py` | digitaler Zwilling: Design → Impedanzmatrix Z(x, f) |
| `circuit.py` | Speisung, Gegenreihenschaltung der Sekundärspulen, Last |
| `analysis.py` | Kennlinie, phasenrichtige Auswertung, Linearität, Frequenzgang |
| `designs.py` | generisches Beispiel (fiktiv, kein MESSOTRON-Produkt) |

```bash
pip install -r requirements.txt
python tests/test_validation.py          # Validierung gegen analytische Lösungen (~2 s)
python examples/demo_generic_lvdt.py     # Demo inkl. Diagramme in docs/phase1/img (~10 min)
python examples/phase2_phase_check.py    # Phasen-Plausibilität unter MBI-Bedingungen (~15 s)
```

Die Werkstoffwerte im Prototyp sind **Annahmen**. Quantitative Aussagen über reale
MESSOTRON-Sensoren gibt es erst nach der Kalibrierung (Phase 3).
