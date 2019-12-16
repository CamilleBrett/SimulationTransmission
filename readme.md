# Simulation d'une transmission avec Python

## A quoi sert ce programme ?

Ce code génère une transmission aux caractéristiques suivantes :

* Message : message de longueur nb_symboles.

* Codage canal : code convolutif. La machine à états est à quatre états.

* Modulation : modulation d'amplitude sur 4 états (ASK-4); la porteuse est à la fréquence f_porteuse, d'amplitude 1 et de phase 0. Le signal est échantillonné à la fréquence f_ech. Les symboles sont émis à la fréquence f_symnoles.

* Canal : canal à bruit blanc additif Gaussien, de rapport signal à bruit gammadB décibels.

* Décodage canal : décodage au maximum de vraissemblance avec l'algorithme de Viterbi.

## Comment simuler la transmission ?

Pour simuler la transmission, exécuter le code `main.py`.

* Les paramètres f_porteuse, f_symboles, f_ech, gammadB, nb_symboles sont modifiables.

* Dans la console, on affiche les informations suivantes sur la transmission simulée :
	* La taille du message envoyé;
	* La fréquence porteuse, la fréquence d'échantillonnage et la fréquence d'émission symboles;
	* Le nombre d'erreurs dans la transmission;
	* Le taux d'erreur symbole au RSB choisi;
	* Le taux d'erreur binaire au RSB choisi;

* Dans une fenêtre, on affiche les figures suivantes :
	* Le message à transmettre;
	* Le message encodé;
	* Le signal modulé;
	* Le signal reçu après passage dans le canal;
	* Le message codé reçu
	* L'information reçue (message décodé).