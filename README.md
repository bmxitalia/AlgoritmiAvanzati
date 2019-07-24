# algorithms
La repository contiene i seguenti esercizi:

## Lab. 1 - Resilienza di una rete di comunicazione

In questo laboratorio analizzeremo la connettività di una rete di calcolatori sottoposta ad un attacco. In particolare, simuleremo attacchi che disabilitano un numero crescente di server della rete per comprometterne l'operatività. In termini computazionali, la rete sarà modellata con un grafo non orientato da cui verranno eliminati man mano dei nodi secondo un certo ordine. Misureremo la *resilienza* della rete come la dimensione della componente connessa più grande rimasta nel grafo dopo l'eliminazione dei nodi.

Il laboratorio va svolto a gruppi di massimo tre persone. E' sufficiente che uno solo dei componenti sottometta i risultati, specificando nel testo della risposta i nomi dei componenti del gruppo.

**Grafi da analizzare**

In questo laboratorio analizzeremo la resilienza di tre tipi di grafi diversi:

- **Una rete di calcolatori reale,** rappresentata nel file di testo allegato. La rete è composta da  6474 nodi e 13233 archi non orientati. Il file contiene l'elenco degli archi del grafo e non corrisponde esattamente alle assunzioni fatte a lezione: in particolare, include anche un certo numero di cappi (archi da un nodo verso se stesso), che vanno quindi ignorati.
- **Un grafo ER**, generato con il processo casuale ER visto a lezione, modificato per generare grafi non orientati anziché grafi orientati.
- **Un grafo UPA.** A lezione abbiamo visto la procedura DPA per generare grafi orientati (la D in DPA sta per "directed"). In questo laboratorio modificheremo il codice per generare grafi non orientati, ottenendo una procedura che chiameremo UPA. E' importante notare che in questo caso il grado dei nodi che vengono aggiunti al grafo non è più zero, e quindi che la loro probabilità di essere estratti nelle iterazioni successive diventa più alta. Il codice modificato deve tener conto di questo fatto.

**Domanda 1**

Iniziamo la nostra analisi esaminando la resilienza della rete di calcolatori rispetto ad un attacco che sceglie i server da disattivare in modo casuale, e confrontandola con quella di un grafo ER e un grafo UPA di dimensioni simili.

Come prima cosa determinate dei valori di *n, p* e *m* tali che la procedura ER e la procedura UPA generino un grafo con lo stesso numero di nodi ed un numero di archi simile a quello della rete reale. Come valore del parametro *m* per la procedura UPA potete usare il numero intero più vicino ~~al grado medio~~ *al grado medio diviso 2* dei vertici della rete reale.

Quindi, per ognuno dei tre grafi (rete reale, ER, UPA), simulate un attacco che disabiliti i nodi della rete uno alla volta seguendo un ordine casuale, fino alla disattivazione di tutti i nodi del grafo, e calcolate la resilienza del grafo dopo ogni rimozione di un nodo.

Dopo aver calcolato la resilienza dei tre grafi, mostrate il risultato in un grafico con scala lineare che combini le tre curve ottenute. Usate un grafico a punti oppure a linea per ognuna delle curve. L'asse orizzontale del grafico deve corrispondere al numero di nodi *disattivati* dall'attacco (che variano da 0 a *n*), mentre l'asse verticale alla dimensione della componente connessa più grande rimasta dopo aver rimosso un certo numero di nodi. Aggiungete una legenda al grafico che permetta di distinguere le tre curve e che specifici i valori di *p* e *m* utilizzati. Allegate il file con la figura nell'apposito spazio.

**Domanda 2.**

Considerate quello che succede quando si rimuove una frazione significativa dei nodi del grafo usando l'attacco con ordine casuale. Diremo che un grafo è *resiliente* a questo tipo di attacco quando la dimensione della componente connessa più grande è superiore al 75% del numero dei nodi ancora attivi. 



Esaminate l'andamento delle tre curve del grafico ottenuto nella Domanda 1, e dite quali dei tre grafi sono resilienti dopo che l'attacco in ordine casuale ha rimosso il 20% dei nodi della rete.

**Domanda 3.**



Consideriamo ora un attacco che sceglie i nodi da rimuovere sulla base della struttura del grafo. In particolare, una strategia di attacco che ad ogni passo disattiva un nodo tra quelli di grado massimo rimasti nella rete. 



Per ognuno dei tre grafi (rete reale, ER, UPA), simulate un attacco di questo tipo fino alla disattivazione di tutti i nodi del grafo, e calcolate la resilienza dopo ogni rimozione di un nodo.

Mostrate il risultato in un grafico che combini le tre curve come nella Domanda 1e allegate il file con la figura nell'apposito spazio.

**Domanda 4.**

Considerate quello che succede quando si rimuove una frazione significativa dei nodi del grafo usando l'attacco che sceglie i nodi con grado massimo.  Esaminate l'andamento delle tre curve del grafico ottenuto nella Domanda 3, e dite quali dei tre grafi sono resilienti dopo che l'attacco ha rimosso il 20% dei nodi della rete.

## Lab 2. La rete dei trasporti pubblici

Il dominio applicativo di questo laboratorio è quello delle reti di trasporto pubblico. Il problema che vi si chiede di affrontare è quello di fornire informazioni sugli orari dei trasporti agli utenti della rete: più precisamente, di trovare un collegamento da una stazione di partenza a una stazione di arrivo e consenta all'utente di arrivare a destinazione il prima possibile. 

Il laboratorio va svolto a gruppi di massimo tre persone. E' sufficiente che uno solo dei componenti sottometta i risultati, specificando nel testo della risposta i nomi dei componenti del gruppo.

##### **La rete dei trasporti pubblici**

In questo laboratorio la rete di trasporti pubblici da analizzare è la rete dei treni ed autobus del Lussemburgo proveniente da [European Data Portal](https://www.europeandataportal.eu/data/en/dataset/horaires-et-arrets-des-transport-publics) e che potete trovare nel file allegato. La rete è composta 515 *linee* di autobus e treni locali, regionali ed internazionali. Ogni linea è descritta in un file con estensione .LIN e comprende più *corse* che percorrono la linea ad orari diversi. Ogni corsa è descritta nel file .LIN come mostrato qui sotto:

```
*Z 01884 C82---                                             % 01884 C82---*A BH 120904002 120904002 000066  00945  00945              % 01884 C82---*A BH 120604001 120604001 000066  00950  00949              % 01884 C82---*R 1 120603002 120903018 120603002  00942  00956            % 01884 C82---*G CRB 120903018 120603002  00942  00956                    % 01884 C82---*A VE 120903018 120603002 000066  00942  00956              % 01884 C82---120903018 Wiltz, Gare                  00942                % 01884 C82---120904002 Paradiso, Gare        00945  00945                % 01884 C82---120604001 Merkholtz, Gare       00949  00950                % 01884 C82---120603002 Kautenbach, Op der G  00956                       % 01884 C82---
```

Le righe che iniziano con un asterisco formano l'intestazione. La riga che inizia con *Z riporta l'identificativo univoco della corsa, composto da un numero di corda a 5 cifre e un ID testuale della linea (nell'esempio, corsa 01884 della linea C82). Le altre righe che iniziano con un asterisco contengono informazioni aggiuntive sulla corsa che si possono ignorare. Dopo l'intestazione sono riportate in sequenza le stazioni che compongono la corsa. Ogni riga riporta il codice identificativo della stazione, il suo nome, l'orario di arrivo e l'orario di partenza dalla stazione. Gli orari sono in formato hh:mm (ore e minuti), con uno zero iniziale per portare la dimensione a 5 cifre. Orari successivi alle 24:00 si riferiscono al giorno successivo. La corsa descritta nell'esempio parte dalla stazione di Wiltz alle ore 9:42 e arriva alla stazione Kautenbach alle 9:56. Il carattere % identifica i commenti. I file sono tabulati con spaziatura fissa.

Il dataset contiene altri due file: il file **bahnof** con i nomi completi delle stazioni ed il file **bfkoor** con le coordinate geografiche delle stazioni (longitudine e latitudine).

##### **Il problema da risolvere**

Data una stazione di partenza A, un orario di partenza e una stazione di arrivo B, il problema da risolvere è quello di trovare un percorso che parta da A non prima dell'orario prestabilito e consenta all'utente di arrivare a B il prima possibile. La soluzione deve tener conto degli eventuali tempi di attesa nelle stazioni. Per semplificare il problema assumete che i trasferimenti all'interno di una stazione richiedano tempi trascurabili.

##### **Domanda 1**

Modellate il problema da risolvere usando un grafo orientato e pesato. Descrivete l'approccio che avete usato per creare il grafo, indicando cosa rappresentano i vertici del grafo, cosa rappresentano gli archi e quali pesi e valori avete associato agli archi.

##### Domanda 2

Risolvete il problema utilizzando uno degli algoritmi per il problema dei cammini minimi visti a lezione. Indicate quale algoritmo avete utilizzato e se e come è stato modificato per poter risolvere il problema.

##### **Domanda 3**

Testate la vostra implementazione con i seguenti viaggi:

- Da 200415016 a 200405005, partenza non prima delle 09:30
- Da 300000032 a 400000122, partenza non prima delle 05:30
- Da 210602003 a 300000030, partenza non prima delle 06:30
- Da 200417051 a 140701016, partenza non prima delle 12:00
- Da 200417051 a 140701016, partenza non prima delle 23:55
- Altre tre combinazioni di viaggio scelte a piacere

Per ogni viaggio, fornite l'elenco delle corse che lo compongono, le stazioni di cambio con gli orari di partenza e l'orario di arrivo a destinazione.

Per esempio, il viaggio più breve da 500000079 (CdT Trier, Hauptbahnhof) a 300000044 (CdT Namur, Gare) con partenza alle ore 13:00 è il seguente:

```
Viaggio da 500000079 a 300000044
Orario di partenza: 13:00
Orario di arrivo: 17:18
13:46 : corsa 06171 CFLBUS da 500000079 a 200405036
14:47 : corsa 06311 CFLBUS da 200405036 a 300000003
15:31 : corsa 02138 C82--- da 300000003 a 300000044
```

Le coordinate geografiche delle stazioni contenute nel file **bfkoor** possono essere utilizzate per rappresentare la soluzione in forma grafica:

![img](https://elearning.unipd.it/math/pluginfile.php/47952/mod_assign/intro/Esempio_sol.png)

##### **Domanda 4**

Commentate la qualità delle soluzioni trovate dalla vostra implementazione: rappresentano soluzioni di viaggio ragionevoli oppure no? In caso negativo, quali sono i motivi che portano la vostra implementazione a generare soluzioni di viaggio irragionevoli? Ci sono dei modi per evitare che lo faccia?

## Lab. 3 - Il Commesso Viaggiatore

**Descrizione del problema**

In questo laboratorio risolveremo un problema intrattabile confrontando i tempi di calcolo e la qualità delle soluzioni che si possono ottenere con algoritmi esatti e con algoritmi di approssimazione. Il problema da affrontare è il cosiddetto "Problema del Commesso Viaggiatore" (TSP), definito come segue: date le coordinate x,yx,y di NN punti nel piano (i vertici), e una funzione di peso w(u,v)w(u,v)definita per tutte le coppie di punti (gli archi), trovare il ciclo semplice di peso minimo che visita tutto gli NN punti. La funzione peso w(u,v)w(u,v) è definita come la distanza Euclidea o Geografica tra i punti uu e vv (potete trovare i dettagli su come calcolare la distanza nella descrizione del dataset). La funzione peso è simmetrica e rispetta la disuguaglianza triangolare.

**Algoritmi**

Gli algoritmi da implementare per risolvere il problema rientrano in tre categorie: (1) algoritmi esatti; (2) euristiche costruttive; e (3) algoritmi 2-approssimati.

- **Algoritmi esatti:** implementate l'algoritmo esatto di Held e Karp. Poiché questo algoritmo è di complessità esponenziale, l'implementazione deve interrompere l'esecuzione se non trova la soluzione ottima entro TT minuti, restituendo la soluzione migliore trovata fino a quel momento, se esiste. Molto probabilmente l'algoritmo riuscirà a trovare la soluzione ottima solo per le istanze più piccole (circa 10 nodi), e fornirà una soluzione parziale per quelle più grandi.
- **Euristiche costruttive:** scegliete *una* fra le euristiche costruttive viste a lezione ed implementatela: Nearest Neighbour, Closest Insertion, Farthest Insertion, Random Insertion, Cheapest Insertion.
- **Algoritmi 2-approssimati:** implementate l'algoritmo 2-approssimato basato sull'albero di copertura minimo.

**Dataset**

Il dataset contiene 7 grafi di esempio, sia reali che generati casualmente. Proviene da TSPLIB e si trova nel file tsp-dataset.zip allegato.Le prime righe di ogni file contengono alcune informazioni sull'istanza, come il numero di punti NN (che varia da 14 a 1000) e il tipo di coordinate: Eculidee (EUC_2D) o Geografiche (GEO). Le righe poste dopo NODE_COORD_SECTION descrivono i vertici del grafo: ogni riga comprende un ID del vertice (intero univoco) seguito dalle coordinate x e y che possono essere valori reali. I tre valori sono separati da spazi. 

Gestione dell'input e calcolo corretto delle distanze:

- **File in formato GEO:** la coordinata x è la latitudine, la coordinata y la longitudine
  - convertire le coordinate x,y in radianti usando il codice specificato nelle [TSPLIB FAQ (Q: I get wrong distances for problems of type GEO.)](https://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/TSPFAQ.html). La formula considera la parte intera di x e y (NON ARROTONDA ALL'INTERO PIU' VICINO).
  - calcolare la distanza geografica tra i punti i e j usando il codice presente nelle FAQ per "dij". Anche in questo caso il codice considera la parte intera delle distanze.
- **File in formato EUC_2D:** In questo caso non occorre fare conversioni di coordinate. Calcolare la distanza Eculidea e arrotondate il valore all'intero più vicino.

**Domanda 1.**

Eseguite i tre algoritmi che avete implementato (Held-Karp, euristica costruttiva e 2-approssimato) sui 7 grafi del dataset. Mostrate i risultati che avete ottenuto in una tabella come quella sottostante. Le righe della tabella corrispondono alle istanze del problema. Le colonne mostrano, per ogni algoritmo, il peso della soluzione trovata, il tempo di esecuzione e l'errore relativo calcolato come (SoluzioneTrovata−SoluzioneOttima)/SoluzioneOttima(SoluzioneTrovata−SoluzioneOttima)/SoluzioneOttima. Potete aggiungere altra informazione alla tabella che ritenete interessanti. La tabella può essere inserita online nello spazio di testo o allegata in un file separato.

**Domanda 2.**

Commentate i risultati che avete ottenuto: come si comportano gli algoritmi rispetti alle varie istanze? C'è un algoritmo che riesce sempre a fare meglio degli altri rispetto all'errore di approssimazione? Quale dei tre algoritmi che avete implementato è più efficiente? 

## Lab. 4 - Clustering di dati medici

In questo laboratorio analizzeremo le prestazioni dei due metodi di clustering visti a lezione su vari set di dati che rappresentano rischio di cancro negli Stati Uniti. In particolare, confronteremo i due metodi di clustering rispetto a tre parametri:

- **Efficienza:** quale metodo impiega meno tempo per calcolare il clustering?
- **Automazione:** quale metodo richiede meno supervisione umana per generare raggruppamenti ragionevoli? 
- **Qualità:** quale metodo genera cluster con meno errori?

**Dataset**

I metodi di clustering verranno applicati a diversi gruppi di dati 2D che includono informazioni sul rischio di contrarre il cancro causato da inquinanti atmosferici. La versione originale di questi dati è disponibile [in questo sito Web](https://www.epa.gov/national-air-toxics-assessment/2014-nata-assessment-results). Ogni voce nel set di dati corrisponde a una contea degli Uniti e include informazioni sulla popolazione totale della contea e il rischio di cancro pro capite.
Per facilitare la visualizzazione, i dati includono la posizione (x,y)(x,y) di ogni contea [in questa mappa degli Stati Uniti.](https://elearning.unipd.it/math/pluginfile.php/48589/mod_assign/intro/USA_Counties.png) Le coordinate sono specificate come pixel dell'immagine, con l'origine nell'angolo in alto a sinistra. [Questa immagine](https://elearning.unipd.it/math/pluginfile.php/48589/mod_assign/intro/full_bubbleplot.png) mostra un esempio di sovrapposizione dei dati alla mappa con un grafico a bolle il cui raggio e colore rappresentano la popolazione totale e il rischio di cancro della contea corrispondente.Il dataset completo include 3108 contee. Usando le soglie 3.0⋅10−53.0⋅10−5, 3.5⋅10−53.5⋅10−5 e 4.0⋅10−54.0⋅10−5 per eliminare le contee con basso rischio di cancro si ottengono dataset più piccoli con 1041, 562 e 212 contee, rispettivamente. Questi quattro dataset saranno i nostri dati di test per i metodi di clustering e sono allegati alla pagina in formato CSV. Ogni riga dei file corrisponde ad una contea ed è composta da cinque campi in quest'ordine: codice della contea, coordinata x, coordinata y, popolazione e rischio di cancro.

**Efficienza**

Le prime tre domande considerano l'efficienza degli algoritmi di Clustering Gerarchico e Clustering k-means.

**Domanda 1**

Create un'immagine dei 15 cluster generati applicando l'algoritmo di Clustering Gerarchico al set di dati completo con 3108 contee. Utilizzate un colore diverso per identificare ogni cluster. È possibile allegare un'immagine con le 3108 contee colorate per cluster o una visualizzazione ottimizzata con le contee colorate per cluster e collegate al centro dei relativi cluster con delle linee. Non è necessario includere assi, etichette degli assi o un titolo per questa immagine. 

**Domanda 2**

Create un'immagine dei 15 cluster generati applicando 5 iterazioni dell'algoritmo k-means al set di dati completo con 3108 contee. I cluster iniziali devono corrispondere alle 15 contee con la popolazione maggiore.
Utilizzate un colore diverso per identificare ogni cluster. È possibile allegare un'immagine con le 3108 contee colorate per cluster o una visualizzazione ottimizzata con le contee colorate per cluster e collegate al centro dei relativi cluster con delle linee. Non è necessario includere assi, etichette degli assi o un titolo per questa immagine.

**Domanda 3**

Quale metodo di clustering è più veloce quando il numero di cluster di output è un numero piccolo o una piccola frazione del numero di punti del dataset? Fornite una breve spiegazione in termini dei tempi di esecuzione asintotici di entrambi i metodi. Assumete che HierarchicalClustering usi FastClosestPair e che k-means usi sempre un piccolo numero di iterazioni.

**Automazione**

Nelle prossime domande, confronteremo il livello di supervisione umana richiesto da ciascun metodo.

**Domanda 4**

Create un'immagine dei 9 cluster generati applicando l'algoritmo di Clustering Gerarchico al set di dati con 212 contee. Utilizzate un colore diverso per identificare ogni cluster. È possibile allegare un'immagine con le 212 contee colorate per cluster o una visualizzazione ottimizzata con le contee colorate per cluster e collegate al centro dei relativi cluster con delle linee. Non è necessario includere assi, etichette degli assi o un titolo per questa immagine.

**Domanda 5**

Create un'immagine dei 9 cluster generati applicando 5 iterazioni dell'algoritmo k-means al set di dati con 212 contee. I cluster iniziali devono corrispondere alle 9 contee con la popolazione maggiore. Utilizzate un colore diverso per identificare ogni cluster. È possibile allegare un'immagine con le 212 contee colorate per cluster o una visualizzazione ottimizzata con le contee colorate per cluster e collegate al centro dei relativi cluster con delle linee. Non è necessario includere assi, etichette degli assi o un titolo per questa immagine.

**Domanda 6**

I clustering calcolati nelle domande 4 e 5 mostrano che non tutti i risultati sono uguali. In particolare, alcuni clustering sono migliori di altri. Un modo per rendere questo concetto più preciso è formulare una misura matematica dell'errore associato a un cluster. Dato un cluster CC, il suo errore è la somma dei quadrati delle distanze di ciascuna contea nel cluster dal centro del cluster, pesata per la popolazione di ciascuna contea. Se pipi è la posizione della contea e wiwi è la sua popolazione, l'errore del cluster è: error(C)=∑pi∈Cwi⋅δ(pi,center(C))2error(C)=∑pi∈Cwi⋅δ(pi,center(C))2

Data una lista di cluster LL, la distorsione del clustering è la somma degli errori associati ai cluster:
distortion(L)=∑C∈Lerror(C)distortion(L)=∑C∈Lerror(C)
Calcolate la distorsione dei clustering che avete ottenuto per le domande 4 e 5. Specificate i valori di distorsione (con almeno quattro cifre significative) dei due clustering nella casella di testo sottostante, indicando a quale dei due algoritmi si riferisce ogni valore. 
Come verifica della correttezza del codice, le distorsioni associate ai 16 cluster di output prodotti da Clustering Gerarchico e k-means clustering (con 5 iterazioni) sul set di dati con 562 contee sono approssimativamente 2.26×10112.26×1011 e 3.86×10113.86×1011, rispettivamente.

**Domanda 7**

Esaminate i clustering generati nelle domande 4 e 5. In particolare, concentrate la vostra attenzione sul numero e sulla forma dei cluster situati nella costa occidentale degli Stati Uniti. Descrivete la differenza tra le forme dei cluster prodotti da questi due metodi sulla costa occidentale degli Stati Uniti. Per quale motivo un metodo produce un clustering con una distorsione molto più alta dell'altro? Per aiutarvi a rispondere a questa domanda, dovreste considerare in che modo k-means clustering genera il clustering iniziale in questo caso. Nello spiegare la vostra risposta, rivedete la geografia della costa occidentale degli Stati Uniti.

**Domanda 8**

In base alla risposta alla domanda 7, quale metodo (clustering gerarchico o k-means clustering) richiede meno supervisione umana per produrre clustering con distorsione relativamente bassa?

**Qualità**

Nelle prossime due domande, analizzerete la qualità dei clustering prodotti da ciascun metodo come misurata dalla loro distorsione.

**Domanda 9**

Calcolare la distorsione dei clustering prodotti da Clustering Gerarchico e k-means clustering (utilizzando 5 iterazioni) sui set di dati con 212, 562 e 1041 contee, rispettivamente, variando il numero di cluster di output da 6 a 20 (estremi inclusi) 
**Nota importante:** per calcolare la distorsione dei clustering prodotti da HierarchicalClustering, è bene ricordare che è possibile utilizzare il cluster gerarchico di dimensione 20 per calcolare il clustering gerarchico di dimensione 19 e così via. Altrimenti, introdurrete un fattore 15 non necessario nel tempo di calcolo dei 15 raggruppamenti gerarchici.Dopo aver calcolato queste distorsioni per entrambi i metodi di clustering, create tre grafici separati (uno per ciascun set di dati) che confrontino la distorsione dei clustering prodotti da entrambi i metodi. Ogni figura dovrebbe includere due curve disegnate come grafici a linee. L'asse orizzontale per ciascun grafico indica il numero di cluster di output mentre l'asse verticale indica la distorsione associata a ciascun clustering. Per ogni figura, includere un titolo che indica il set di dati utilizzato nella creazione dei grafici e una legenda che distingue le due curve.

**Domanda 10**

Per ciascun set di dati (212, 562 e 1041 contee), c'è un metodo di clustering che produce sempre risultati con distorsione inferiore quando il numero di cluster di output è compreso tra 6 e 20? Se è così, indicare per quali insiemi di dati un metodo è superiore all'altro.

## Lab. 5 - Clustering k-means parallelo

In questo laboratorio confronteremo l'algoritmo di clustering k-means seriale sviluppato per il laboratorio 4 con la sua versione parallela. In particolare, analizzeremo come variano i tempi di calcolo dei due algoritmi rispetto a quattro parametri:

- Numero di punti 
- Numero di cluster
- Numero di iterazioni 
- Granularità del parallelismo

##### Dataset

I metodi di clustering verranno applicati ad un dataset comprende [città e paesi degli Stati Uniti](https://public.opendatasoft.com/explore/dataset/cities-and-towns-of-the-united-states/table/). Ogni voce nel set di dati corrisponde a una città o paese include informazioni sulla popolazione e sulle coordinate geografiche (latitudine e logitudine).

Il dataset completo include 38183 città e paesi, ed è allegato alla pagina in formato CSV. Ogni riga dei file corrisponde ad una città o paese ed è composta da cinque campi in quest'ordine: codice, nome, popolazione, latitudine e longitudine. 

##### Algoritmi

Implementate la versione seriale e la versione parallela dell'algoritmo di clustering k-means. Usate le k città con popolazione più alta come centroidi iniziali per l'algoritmo. Per calcolare la distanza tra i punti usate lo stesso modo che avete usato nel Laboratorio 3 per calcolare la distanza tra i punti di tipo GEO.

##### Domanda 1

Confrontate i tempi di calcolo dell'algoritmo seriale e dell'algoritmo parallelo per il clustering k-means, al variare del **numero di punti.** 

Usate le soglie di popolazione minima 250, 2.000, 5.000, 15.000, 50.000, e 100.000 per eliminare città e paesi con bassa popolazione e ottenere dataset più piccoli con meno punti. 

Misurate i tempi di calcolo dell'algoritmo seriale e di quello parallelo sul dataset complessivo con 38183 punti e su quelli ridotti. Per tutti i dataset, fissate il numero di cluster a 50 ed il numero di iterazioni a 100.

Dopo aver misurato i tempi, create un grafico che mostri la variazione dei tempi di calcolo dei due algoritmi al variare del numero di punti. La figura dovrebbe includere due curve disegnate, una per l'algoritmo seriale e una per l'algoritmo parallelo. L'asse orizzontale indica il numero di punti mentre l'asse verticale indica la il tempo di calcolo. 

Calcolate lo speedup ottenuto dall'algoritmo parallelo. Come varia rispetto al numero dei punti?

##### Domanda 2

Confrontate i tempi di calcolo dell'algoritmo seriale e dell'algoritmo parallelo per il clustering k-means, al variare del **numero di cluster.** 

Usando il dataset complessivo con 38183 punti, misurate i tempi di calcolo dell'algoritmo seriale e di quello parallelo variando il numero di cluster da 10 a 100. Mantenete costante il numero di iterazioni a 100.

Dopo aver misurato i tempi, create un grafico che mostri la variazione dei tempi di calcolo dei due algoritmi al variare del numero di cluster. In questo caso l'asse orizzontale indica il numero di cluster mentre l'asse verticale indica la il tempo di calcolo.

Calcolate lo speedup ottenuto dall'algoritmo parallelo. Come varia rispetto al numero dei cluster?

##### Domanda 3

Confrontate i tempi di calcolo dell'algoritmo seriale e dell'algoritmo parallelo per il clustering k-means, al variare del **numero di iterazioni.** 

Usando il dataset complessivo con 38183 punti, misurate i tempi di calcolo dell'algoritmo seriale e di quello parallelo variando il numero di iterazioni da 10 a 1000. Mantenete costate il numero di cluster a 50.

Dopo aver misurato i tempi, create un grafico che mostri la variazione dei tempi di calcolo dei due algoritmi al variare del numero di iterazioni. In questo caso l'asse orizzontale indica il numero di iterazioni mentre l'asse verticale indica la il tempo di calcolo.

Calcolate lo speedup ottenuto dall'algoritmo parallelo. Come varia rispetto al numero di iterazioni?

##### Domanda 4

Per migliorare i tempi di calcolo di un algoritmo risulta spesso utile limitare il parallelismo, passando ad una procedura seriale quando la dimensione dell'input scende sotto una certa soglia. Per esempio, in un algoritmo divide-et-impera si può stabilire una soglia di *cutoff* al di sotto della quale si utilizza un algoritmo seriale iterativo, invece di dividere ulteriormente l'input e procedere in parallelo.

Usando il dataset complessivo con 38183 punti, misurate i tempi di calcolo dell'algoritmo di clustering k-means parallelo utilizzando diverse soglie di cutoff per controllare la granularità del parallelismo.

Dopo aver misurato i tempi, create un grafico che mostri la variazione dei tempi di calcolo al variare del cutoff. Quale valore di cutoff vi permette di ottenere le prestazioni migliori?

##### Domanda 5

Specificare le caratteristiche hardware del computer dove sono stati eseguiti i test, in particolare processore e numero di core disponibili.