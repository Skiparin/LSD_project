# LSD report

Final report for Large System Development

Hand-in date: 21/12/2018

## Authors
Gruppe G:
- Laura Hartig
- Michael Daugbjerg
- Nicolai Mikkelsen
- Tim Hemmingsen
- Ørvur Guttesen

## Introduction
Dette er vores afsluttende rapport for vores LSD projekt. Under dette forløb har vi fokuseret på at opbygge en form af Reddit helt fra bunden af. Vi gik fra en beskrivelse af vores projekt, til implementation af diverse features og i mellemtiden til maintenance som operators til en anden gruppes projekt under udvikling.

Vores projekt består af Continuous Integration i form a weekly releases og vores givet opgaver igennem forløbet. Vores mål var at kunne dække disse opgaver og implementere de nødvendige funktioner lige så vel som at kunne overholde vores Service-level Agreement (SLA), som er vores agreement med vores observer gruppe. Derudover er det også vores pligt, at holde øje med den gruppe, som vi skulle operate på. Dette gjorde vi igennem deres monitoring system, hvor vi skulle notificere gruppen, hvis noget gik galt i deres projekt.

Alt dette vil blive uddybet, forklaret og analyseret igennem denne rapport.

## Requirements, architecture, design and process

### System requirements
Vi satte os ned og gennemgik hvordan Hacker News var opbygget og hvilke funktionaliteter det havde og hvordan vi forventede det var bygget. Derefter kiggede vi på [opgavebeskrivelsen](https://github.com/datsoftlyngby/soft2018fall-lsd-teaching-material/blob/master/assignments/01-HN%20Clone%20Task%20Description.ipynb) for at få idéer til hvad vi skulle have og hvilke ting vi følte ville være fede at få med ind over. I forhold til opgavebeskrivelsen, mente vi at funktionaliteten var vigtigst, og ikke de visuelle dele af hjemmesiden. Vi valgte derfor at prioritere alle de endpoints som skulle laves og den simulation som var givet til os. Dette var det vigtigste og første vi valgte at lave i vores projekt. Derefter fokuserede vi på vores database og hvordan den kunne bygges op til at være effektiv. Dette indebar at vi skulle gøre det muligt at få svartider der var lave nok til ikke at få "timed out" på vores requests. Vi ville også gøre vi ikke havde redundant data i vores database. Til sidst ville vi lave en hjemmeside som stadig kunne vise de forskellige posts som var blevet lagt i ned i databasen på vores forside. Vi ville gerne have vi havde noget visuelt på vores side som varierede i forhold til den data som var blevet givet til os.

Vi valgte ikke at prioritere det mere visuelle på vores side, når man gik længere ind på vores hjemmeside. Vi følte ikke dette requirement var lige så stort som de andre og det ikke havde lige så stort fokus i projektet som de andre requirements.
Vores system requirement endte dermed at være fuld support af endpoints. Svartider som ikke overskrider hvad normalt kan forventes af hjemmesider, hvilket vi valgte at være omkring 1 sekund. En frontpage som gav mulighed for at vise nyt information som var givet til websitet, hvilket vi valgte skulle være posts.
Resterende ting ville ikke være på vores requirement liste, men vil kunne blive implementeret i løbet af systems levetid.

### Development process
Til vores projekt valgte vi at arbejde agilt. Her ville vi gøre brug af Continuous Integration i form af weekly releases. Dette gjorde at hele projektet ikke blev deployet på én gang, men derimod blev delt op i de forskellige releases. Her gjorde vi brug af noget fra Scrum, da det passede rigtig godt til at kunne lave disse weekly releases. Vi brugte GitHub’s “Projects” tool til at lave en product backlog med User Stories. Her brudte vi vores User Stories ned til forskellige tasks, for at specificere de forskellige features, vi ville udvikle under projektet. Vi opdaterede vores backlog dashboard løbende, så vi havde et overblik over, hvor langt vi var kommet med hver task og feature. Som nævnt, valgte vi kun at bruge dele af Scrum og gjorde derfor ikke brug af daglige møder og sprint reviews. Vi holdte dog stadig møder omkring projektet et par gange om ugen, da det passede med vores skolegang. Vi havde som sådan heller ikke nogen Scrum Master eller Product Owner, men blev derimod enige som gruppe, om hvad der skulle specifikt skulle laves og prioriteres i de forskellige releases. Derudover gjorde vi også brug af Pair Programming, da vi ofte sad to mand og arbejdede på den samme task eller feature.

### Software architecture
Vi havde planer om at lave en arkitektur, der kunne understøtte trafikken som vi ville få fra Hackernews simulationen. Til at starte med, ville vi se, hvilke af de værktøjer som vi normalt bruger, der kunne blive brugt til projektet. Vi startede med at have brug for et sted at gemme informationen, og vi havde i over et år brugt PostgreSQL som database, og ud fra anbefalinger fra forskellige kilder fandt vi også ud af, at PostgreSQL var mere end hurtig nok til vores behov. 
 
Bagefter havde vi brug for frameworks til både frontend og backend delen af vores system, og her havde at vi mest brugt Flask som et API framework, men også en smule til frontend. Vi begyndte at undersøge, om det var muligt at bruge Flask til vores system. Problemet med Flask “out of the box” er, at det er single threaded og ikke kan holde på så mange requests af gangen som så mange andre frameworks. Men efter nærmere undersøgelse, fandt vi ud af, at ved at bruge uWSGI, kunne vi godt bruge Flask. uWSGI er en måde at hoste flere Python applikationer til NGINX, lighttpd, and cherokee mellem andre. Ved brug af uWSGI laver vi så et socket, som NGINX kan bruge.

### Software design
