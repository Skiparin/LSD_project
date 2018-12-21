# LSD report

Final report for our Large System Development project

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

## 1) Requirements, architecture, design and process
### System requirements
Vi satte os ned og gennemgik hvordan Hacker News var opbygget og hvilke funktionaliteter det havde og hvordan vi forventede det var bygget. Derefter kiggede vi på [opgavebeskrivelsen](https://github.com/datsoftlyngby/soft2018fall-lsd-teaching-material/blob/master/assignments/01-HN%20Clone%20Task%20Description.ipynb) for at få idéer til hvad vi skulle have og hvilke ting vi følte ville være fede at få med ind over. I forhold til opgavebeskrivelsen, mente vi at funktionaliteten var vigtigst, og ikke de visuelle dele af hjemmesiden. Vi valgte derfor at prioritere alle de endpoints som skulle laves og den simulation som var givet til os. Dette var det vigtigste og første vi valgte at lave i vores projekt. Derefter fokuserede vi på vores database og hvordan den kunne bygges op til at være effektiv. Dette indebar at vi skulle gøre det muligt at få svartider der var lave nok til ikke at få "timed out" på vores requests. Vi ville også gøre vi ikke havde redundant data i vores database. Til sidst ville vi lave en hjemmeside som stadig kunne vise de forskellige posts som var blevet lagt i ned i databasen på vores forside. Vi ville gerne have vi havde noget visuelt på vores side som varierede i forhold til den data som var blevet givet til os.

Vi valgte ikke at prioritere det mere visuelle på vores side, når man gik længere ind på vores hjemmeside. Vi følte ikke dette requirement var lige så stort som de andre og det ikke havde lige så stort fokus i projektet som de andre requirements.
Vores system requirement endte dermed at være fuld support af endpoints. Svartider som ikke overskrider hvad normalt kan forventes af hjemmesider, hvilket vi valgte at være omkring 1 sekund. En frontpage som gav mulighed for at vise nyt information som var givet til websitet, hvilket vi valgte skulle være posts.
Resterende ting ville ikke være på vores requirement liste, men vil kunne blive implementeret i løbet af systems levetid.
#
### Development process
Til vores projekt valgte vi at arbejde agilt. Her ville vi gøre brug af Continuous Integration i form af weekly releases. Dette gjorde at hele projektet ikke blev deployet på én gang, men derimod blev delt op i de forskellige releases. Her gjorde vi brug af noget fra Scrum, da det passede rigtig godt til at kunne lave disse weekly releases. Vi brugte GitHub’s “Projects” tool til at lave en product backlog med User Stories. Her brudte vi vores User Stories ned til forskellige tasks, for at specificere de forskellige features, vi ville udvikle under projektet. Vi opdaterede vores backlog dashboard løbende, så vi havde et overblik over, hvor langt vi var kommet med hver task og feature. Som nævnt, valgte vi kun at bruge dele af Scrum og gjorde derfor ikke brug af daglige møder og sprint reviews. Vi holdte dog stadig møder omkring projektet et par gange om ugen, da det passede med vores skolegang. Vi havde som sådan heller ikke nogen Scrum Master eller Product Owner, men blev derimod enige som gruppe, om hvad der skulle specifikt skulle laves og prioriteres i de forskellige releases. Derudover gjorde vi også brug af Pair Programming, da vi ofte sad to mand og arbejdede på den samme task eller feature.
#
### Software architecture
Vi havde planer om at lave en arkitektur, der kunne understøtte trafikken som vi ville få fra Hackernews simulationen. Til at starte med, ville vi se, hvilke af de værktøjer som vi normalt bruger, der kunne blive brugt til projektet. Vi startede med at have brug for et sted at gemme informationen, og vi havde i over et år brugt PostgreSQL som database, og ud fra anbefalinger fra forskellige kilder fandt vi også ud af, at PostgreSQL var mere end hurtig nok til vores behov. 
 
Bagefter havde vi brug for frameworks til både frontend og backend delen af vores system, og her havde at vi mest brugt Flask som et API framework, men også en smule til frontend. Vi begyndte at undersøge, om det var muligt at bruge Flask til vores system. Problemet med Flask “out of the box” er, at det er single threaded og ikke kan holde på så mange requests af gangen som så mange andre frameworks. Men efter nærmere undersøgelse, fandt vi ud af, at ved at bruge uWSGI, kunne vi godt bruge Flask. uWSGI er en måde at hoste flere Python applikationer til NGINX, lighttpd, and cherokee mellem andre. Ved brug af uWSGI laver vi så et socket, som NGINX kan bruge.
#
### Software design

#
### Software implementation
Vi vidste fra start af, at vi skulle arbejde med Flask til vores API endpoints og skrive vores kode i Python. Da vi fandt ud af at antallet af request, igennem helges api ville overstige det antal af request, som Flask kunne håndtere alene, blev vi nødt til at implementere NGINX som gjorde at vi kunne håndtere langt flere request per second. Dette skete dog meget tidligt i vores udviklingsfase så det berørte ikke noget allerede eksisterende implementering i vores projekt.
Igennem vores forløb har vi fulgt vores funktionelle og non-funktionelle krav meget godt. Vi har fået opfyldt vores SLA, som ikke var helt opfyldt i starten, da vores response time på hjemmesiden var for langsom. Dette fik vi dog rettet. Vores endpoints blev implementere løbende samt nogle af de opgave vi blev sat for i LSD faget.
Noget vi ikke havde tage hensyn til fra start af var fra de opgaver som vi fik i LSD faget. Bl.a. Prometheus blev først implementeret i vores software senere hen, og det blev implementeret med en extension til Flask.

## 2) Maintenance and SLA status
### Hand-over
I vores forløb som operators, fik vi udleveret et link til [dokumentationen](https://cphb-kepp.github.io/LSD/OperatorDocumentation) af projektet, som vi skulle monitorere. Her fik vi bl.a. adgang til deres forskellige endpoints og deres statusside. Vi brugte deres endpoints til kort at navigere rundt på hjemmesiden, mens vi på statussiden kunne se om de forskellige dele af projektet var oppe og køre. Her havde vi også adgang til alle deres logfiler, som frit kunne downloades. Vi fik dog ikke adgang til deres Grafana dashboard, da de havde problemer med at få den til at fungere, hvilket var ærgerligt, da det ville have hjulpet os meget.

I starten af forløbet, virkede deres statusside heller ikke korrekt, idet den ikke viste de rigtige statusser for systemets services. Det var derfor svært for os som operators, at se tidspunktet hvor de ville crashe deres eget system, og vi kunne på den måde ikke notificere dem, da vi i starten ikke vidste at siden viste forkert. Vi kontaktede dem derefter omkring problemet, hvor vi så fik at vide, at alt kørte, men at statussiden ikke viste det korrekt. Og da vi heller ikke havde adgang til deres Grafana, kunne vi heller ikke derigennem tjekke, om deres services faktisk var gået ned eller ej. Dette fik de dog ordnet, så vi til sidst igennem statussiden kunne se at hele systemet var oppe og køre.

Alt i alt, gav den udleveret dokumentation os nogle fine midler til kunne at monitorere den anden gruppes projekt. Dog havde det hele været en del lettere, hvis vi kunne havde haft adgang til deres Grafana dashboard.
#
### Service-level agreement
Vores SLA lød som følgende:
- 95% server uptime
- 3 seconds response time (30-50 posts at max)
- 5% or less data loss

Vi mente at disse 3 krav til deres system, var hvad vi kunne forvente i forhold til dette projekt, mens vi stadig havde i tankerne at det er et projekt som blev arbejdet på.

95% er en meget høj uptime, men eftersom der skulle udvikles på systemet i løbet af dets levetid, ville der selvfølgelig ske ting som kunne forårsage downtime. Vi håbede selvfølgelig ikke de fik 5% downtime, men hvis nu en af de nye implementering de skulle lave skabte nogle enorme problemer vil det stadig være muligt at opnå 95%.

3 sekunder response time er hvad man max kan forvente som bruger på en hjemmeside. Dette både hjemmesiden skal tage requesten, behandle det i databasen, sende dataen tilbage og giver det til slut brugeren. Selv om 3 sekunder måske er lang tid som slut bruger synes vi stadig dette er et realistisk response time at gå efter selvom dette er et arbejdsprojekt.

5% data loss er meget men eftersom det er et nyt projekt og der kan opstår problemer i starten og når nye implementeringer bliver lavet synes vi stadig dette er et vigtig ting at sætte som requirement men også noget vi mener gør man har det pusterum man skal bruge til et nyt projekt 

Selv om denne SLA er kort føler vi stadig den tager hånd om det vigtigeste ting og de ting som kunne skabe problemer igennem projektet. Med disse 3 requirements vil andre mindre og specifikke requirements også automatisk blive taget hånd om. Vi vil selvfølgelig gerne have deres database kan håndtere store mængder data og har hurtige response tider. med 5% dataloss og 3 response time vil dette blive arbejdet på for eller vil det ikke kunne opnås. 
Den anden gruppe fandt denne SLA god. Den giver dem nogle krav der er nemme at forstår og de godt kan ses som skal arbejdes på men også mulighed for dem at lave nogle fejl og få noget pusterum til at få deres implementeringer igennem ordentligt.
#
### Maintenance and reliability
Det gik godt i starten, men efterhånden som vi kom længere ind i processen, endte vores operator job desværre med at blive et punkt, som vi ikke fik gjort nok ud af. Specielt, kunne vi sagtens have lavet issues på deres GitHub eller andet dokumentation. Udover det, var det også begrænset hvor meget kommunikation, der var fra den gruppe vi skulle operate på, da deres Grafana side i store dele af projektet ikke virkede ordentligt, så det betød at vi aldrig fik et Grafana endpoint af dem. Dette betød så også, at det blev meget svært at undersøge om deres system overholdte vores SLA kriterier. Da gruppen dog endelig havde fået Grafana til at virke, fik vi det tilset på deres computer, hvor alt så helt fint ud og umiddelbart overholdte vores SLA.

Vi gik nogenlunde regulært ind på deres endpoints for at se om alt var oppe og køre og virkede, som det skulle. Under et af disse besøg fandt vi ud af, at hele deres system var nede bortset fra deres statussider, herinde kunne vi se at alle deres systemer så ikke virkede, herefter tog vi fat i dem for at sige hvad vi havde opdaget. Det tog dem ikke lang tid at få fixet deres problem, da vi et par dage efter så at alle deres systemer var oppe og køre igen, hvilket var positivt. Vi synes også at gruppen i det hele taget fik svaret godt på de problemer og andre spørgsmål, som vi havde angående deres services. Det eneste bagparti til dette, er det manglende endpoint til deres Grafana side, som vi ikke føler de fik håndteret korrekt, da vi gerne ville have haft et endpoint, om end senere hen i udviklingen af projektet. Det er også svært at ordenligt kunne konkludere på “reliabiliteten” på deres system, da vi aldrig fik et ordentligt indblik om de havde overholdt vores SLA kriterier, men hvis man ser bort fra denne synes vi, at de havde et system der fungerede godt, og deres videre håndtering var rigtig fin.

## 3) Discussion
### Technical discussion

#
### Group work reflection & lessons learned


## Conclusion
Ud fra dette projekt lærte vi meget om hvordan man kunne starte et større system fra bunden, med ikke andet end en kort beskrivelse af nogle requirements og et billede af slutresultatet. Vi har gennemgået mange faser i vores projekt hvor vi har skulle implementere noget nyt i form af weekly releases. Det var nogle gange noget, som vi ikke arbejdet med før, hvilket kunne blive til en udfordring, men ikke en stopklods. Vi har gjort brug af flere nye tools, som er blevet brugt til at forbedre vores applikation og vi skulle gå mere i dybden i de emner vi allerede kendte til, da vi havde operators på vores projekt. Derudover prøvede vi også kræfter med at være operators på en andens projekt, og lærte hvordan det var at vedligeholde uden at have adgang til source code.
Forløbet udfoldte sig rigtig godt. Alle de små og store komponenter som blev implementeret, og alle udfordringer vi er blevet stillet for, har givet os en bred erfaring indenfor projektledelse og udvikling.
