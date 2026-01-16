# EpiTrello

La référence pour une organisation sereine.

## Introduction

### Contexte

EpiTrello vise à améliorer l'organisation des équipes et la visibilité des
tâches à réaliser. L'outil sera utilisable par une interface web simple et
intuitive. L'objectif n'est pas de faire un produit plus complet que d'autre
tableau, mais de réaliser un produit pouvant être utilisé pour une tâche
simple: s'organiser en découpant une mission en tâche et les placer sur un
tableau séparer en plusieurs catégories.

### Objectifs

1. Découper une mission en plusieurs tâches sur un tableaux numérique.
2. Personnaliser le tableau (catégories, tâches).
4. Sauvegarde des tableaux dans une base de donnée.
5. Partage du tableau a plusieurs membres, et gestion des membres.
6. Developper le back-end, le front-end, et la documentation pour le déployer sur un serveur.
7. Respecter le temps imparti décrit plus bas.

### Périmètre

- deux developpeurs à raison de trois jours par semaine.
- Commencant le 19 octobre 2025
- Finissant le 28 janvier 2026.

### Eléments existants

- Un Github Project listant les tâches et etape à suivre. A completer suivant l'evolution du projet.
- Le framework Django pour le back-end.
- Le framework Nuxt pour le front-end.

## Cibles

- Les travailleurs seuls sur un projet, recherchant un outil d'organisation.
- Les equipe voulant se repartir des tâches.
- Les chefs de projet voulant un historique des tâches réalise.

## Concurrences

1. Trello. Application de référence.
2. Jira. Complet, mais très difficile à prendre en mains.
3. Github Project, plus specialisé sur le developpement informatique.

Notre force: une interface simple, sans prise de tête, et facile à prendre en main.

## Charte graphique

1. Logo:
2. Couleurs:
3. Typographie:

## Délais de réalisation

1. version 1.0: 28 février.

## Spécifications fonctionnelles

1. Accueil (Liste des tableaux)

> Afficher la liste des tableaux de l'utilisateur.
> Afficher les tableaux mis en favoris.

2. Page de Connexion

> Connexion avec le SSO de Google.
> Redirection vers la page d'accueil.

3. Création de tableaux

> Dans le menu d'accueil, créer un tableau.
> Possibilité de changer la couleur de fond d'écran par défaut.

4. Création de catégorie

> Sur la Page Tableau, créer des catégories.
> Ces catégories permettent de visualiser l'état des tâches.

5. Création de tâche

> Sur la Page Tableau, créer une tâche.

6. Collaboration sur un tableaux

> Deux utilisateurs sur le même tableau, peuvent le modifier en même temps.
> Quand une modification est faites par un utilisateur, elle est répercutée chez l'autre utilisateur.

7. Modification de tâche

> Sur la Page Tableau, sélectionner une tâche et modifier ses informations.
> Renseigner un titre, une description, une date de début, une date de fin, une personne assignée.

8. Organisation de tâche

> Sur la Page Tableau, déplacer des tâches dans des catégories, les ordonner dans un ordre spécifique.

9. Personnalisation des tâches

> Sur la Page Tableau, seléctionner une tâche. Modifier la couleur de la tâche

10. Personnalisation des tableaux

> Sur la Page Tableau, Modifier la couleur du tableau.

## Spécifications fonctionnelles (detaillees)

1. Accueil (Liste des tableaux)

__Objectif__: Lister les tableaux disponibles.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé des tableaux.
__Etape a suivre__:
    1. Ouvrir la Page d'Accueil.
__Resultat__: Voir les tableaux créer.

2. Page de Connexion

__Objectif__: Connecter l'utilisateur.
__Preconditions__:
    1. L'utilisateur a un compte Google.
__Etape a suivre__:
    1. Ouvrire la Page de Connexion.
    2. Cliquer sur le bouton de connexion a Google.
__Resultat__: être redirige vers la page d'accueil.

3. création de tableaux

__Objectif__: créer un tableau.
__Preconditions__:
    1. L'utilisateur est connecte.
__Etape a suivre__:
    1. Ouvrir la Page d'Accueil.
    2. Cliquer sur le bouton de création de tableau.
    3. Renseigner le formulaire.
    4. Valider la création
__Resultat__: Voir le tableau créer.

4. création de catégorie

__Objectif__: créer des tâches.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur le bouton de création de catégorie.
    3. Renseigner le titre de la catégorie.
    4. Valider la création de la catégorie.
__Resultat__: Voir la catégorie.

5. création de tâche

__Objectif__: créer des tâches.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
    3. L'utilisateur a créé une catégorie.
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur le bouton de création de tâche.
    3. Renseigner le titre de la tâche.
    4. Valider la création de tâche.
__Resultat__: Voir la tâche.

6. Collaboration sur un tableaux

__Objectif__: Collaboration en temps réel entre plusieurs utilisateurs.
__Preconditions__:
    1. Les utilisateurs sont connectes.
    2. Un tableau a été créé.
    3. Le crrateur du tableau a invité l'autre sur son tableau.
    4. Un utilisateur a créer une catégorie
__Etape a suivre__:
    1. Les deux utilisateurs doivent ouvrir la Page du même tableau.
    2. Un utilisateur crée une tâche.
__Resultat__: L'autre utilisateur constate la création de la tâche sur son écran.

7. Modification de tâche

__Objectif__: Modifier une tâche.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
    3. L'utilisateur a créé une tâche.
    4. L'utilisateur a créé une catégorie.
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur la tâche déjà créer.
    3. Modifier les informations de la tâche.
    4. Valider la modification.
__Resultat__: Voir les changements d'informations de la tâche.

8. Organisation de tâche

__Objectif__: Déplacer la tâche dans une autre catégorie.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
    4. L'utilisateur a créé 2 catégories.
    3. L'utilisateur a créé une tâche.
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur la tâche déjà créer.
    3. Modifier les informations de la tâche.
    4. Valider la modification.
__Resultat__: Voir le changement de catégorie de la tâche.

9. Personnalisation des tâches

__Objectif__: Changer la couleur de fond de la tâche.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
    4. L'utilisateur a créé une catégories.
    3. L'utilisateur a créé une tâche.
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur la tâche déjà créer.
    3. Modifier la couleur de la tâche.
    4. Valider la modification.
__Resultat__: Voir le changement de couleur.

10. Personnalisation des tableaux

__Objectif__: Changer la couleur de fond du tableau.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur les paramètre du tableau.
    3. Modifier la couleur de fond du tableau.
    4. Valider la modification.
__Resultat__: Voir le changement de couleur.

## Spécifications techniques

- Authentification utilisant le SSO de Google.
- Le back-end doit être developpé en utilisant le framework Django.
- L'API du back-end doit utiliser la librairie Django-Ninja.
- Le front-end doit être developpé en utilisant le framework Nuxt.

## Annexes

### Back-end

- [Documentation Framework Django](https://www.djangoproject.com/)
- [Documentation Django Ninja](https://django-ninja.dev/)

### Front-end

- [Documentation Framework Nuxt](https://nuxt.com/)
