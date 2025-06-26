
### 1. `loadAllPiloti`

```sql
SELECT d.driverId,c.constructorId,d.driverId,d.driverRef,d.number,d.code,d.forename,d.surname,d.dob,d.nationality,
       pp.punteggio, COUNT(r.raceId) as gare, COUNT(r.position) as garefinite
FROM drivers AS d, constructors AS c, results AS r , races AS rs, punteggiopiloti AS pp
WHERE d.driverId=r.driverId
  && r.constructorId=c.constructorId
  && r.raceId=rs.raceId
  && YEAR(rs.date)>2019
  && d.driverId=pp.driverId
GROUP BY d.driverId
```

**Spiegazione:** Recupera tutti i piloti (`drivers`) che hanno gareggiato dopo il 2019,
unendoli con le loro scuderie (`constructors`), i risultati (`results`) e i punteggi (`punteggiopiloti`).
Calcola per ciascun pilota il numero totale di gare disputate (`gare`) e completate (`garefinite`),
includendo anche info anagrafiche.

---

### 2. `loadAllScuderie`

```sql
SELECT c.constructorId,c.constructorRef,c.name,c.nationality,s.importo
FROM constructors AS c, spesa AS s
WHERE c.constructorId=s.constructorId
```

**Spiegazione:** Seleziona tutte le scuderie (`constructors`) unite alla loro spesa (`spesa`) corrispondente. Restituisce identificativo, nome, nazionalità e importo speso.

---

### 3. `loadAllCircuiti`

```sql
SELECT c.circuitId,c.circuitRef,c.name,c.location,c.country,c.lat,c.lng
FROM circuits AS c
```

**Spiegazione:** Restituisce tutti i circuiti (`circuits`) con dettagli come nome, posizione geografica e coordinate.

---

### 4. `loadAllGara`

```sql
SELECT DISTINCT(rs.name) as nome, rs.circuitId, COUNT(rs.raceId), MAX(r.laps) as lap
FROM results AS r, races AS rs
WHERE r.raceId=rs.raceId && year(rs.date)>2018
GROUP BY rs.name
ORDER BY COUNT(rs.raceId) DESC
```

**Spiegazione:** Recupera tutte le gare (`races`) dopo il 2018 raggruppandole per nome del GP. Calcola quante volte ogni gara è stata svolta e il massimo numero di giri (`laps`) effettuati.

---

### 5. `loadAllQ1`

```sql
SELECT r.name, q.driverId, AVG(qualifica.q1) AS t1
FROM races AS r, qualifying AS q,
     (SELECT r.raceId AS gara, q.driverId AS pilota,
             CAST(SUBSTRING_INDEX(q.q1,":",1) AS INT)*60000 +
             CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(q.q1,":",-1),".",1) AS INT)*1000 +
             CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(q.q1,":",-2),".",-1)," ",1) AS INT) AS q1
      FROM races AS r, qualifying AS q
      WHERE year(r.date)>2018 && r.raceId=q.raceId) AS qualifica
WHERE r.raceId=qualifica.gara && q.driverId=qualifica.pilota && q.raceId=r.raceId
GROUP BY r.name, q.driverId
ORDER BY r.name, q.driverId
```

**Spiegazione:** Calcola la media del tempo di qualifica Q1 per ogni pilota e gara dopo il 2018, convertendo il formato `hh:mm:ss` in millisecondi.

---

### 6. `loadAllQ2`

Query simile a Q1 ma per il tempo Q2, con filtro aggiuntivo per escludere valori nulli:

```sql
...
WHERE year(r.date)>2018 && r.raceId=q.raceId && q.q2<>"NULL" && q.q2<>0
...
```

**Spiegazione:** Come sopra, ma esclude i valori nulli o zero nel campo `q2`.

---

### 7. `loadAllQ3`

Analoga alla Q2, applicata a `q3`:

```sql
...
WHERE year(r.date)>2018 && r.raceId=q.raceId && q.q3<>"NULL" && q.q3<>0
...
```

**Spiegazione:** Media del tempo in Q3, solo se disponibile e valido.

---

### 8. `loadAllGiri`

```sql
SELECT r.name, l.driverId, ROUND(CEILING(l.lap/5)), AVG(l.milliseconds) AS milli
FROM races AS r, laptimes AS l
WHERE r.raceId=l.raceId && year(r.date)>2018
GROUP BY r.name, l.driverId, ROUND(CEILING(l.lap/5))
ORDER BY ROUND(CEILING(l.lap/5))
```

**Spiegazione:** Raggruppa i tempi sul giro ogni 5 giri (`lap/5`) per pilota e gara dopo il 2018. Calcola la media dei millisecondi per ogni segmento.

---

Vuoi che ti estrapoli anche un riepilogo schematico o ti servono in questa forma discorsiva?
