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
- Commencant le 29 octobre 2025
- Finissant le 28 janvier 2026.

### Eléments existants

- Un Github Project listant les tâches et etape à suivre. A completer suivant l'evolution du projet.
- Le framework Django pour le back-end.
- Le framework Nuxt pour le front-end.

## Cibles

- Les travailleurs seuls sur un projet, recherchant un outil d'organisation.
- Les equipe voulant se repartir des tâches.
- Les chefs de projet voulant un historique des tâches réalisés.

## Concurrences

1. Trello. Application de référence.
2. Jira. Complet, mais très difficile à prendre en mains.
3. Github Project, plus specialisé sur le developpement informatique.

Avantage concurrentiel d’EpiTrello :
Une interface épurée, rapide à comprendre, sans fonctionnalités superflues.

## Charte graphique

### Identité visuelle

L’identité visuelle d’EpiTrello est volontairement sobre et moderne, afin demettre l’accent sur la lisibilité et l’efficacité.Le design privilégie un thème sombre, réduisant la fatigue visuelle etrenforçant la concentration lors de l’utilisation prolongée de l’outil.

### Logo

*   Le logo utilisé est celui de Trello, choisi comme référence visuelle.

*   Il permet une identification immédiate du concept de tableau de tâches.

### Couleurs

La palette de couleurs est définie via des variables CSS afin d’assurer unecohérence globale et une maintenance simplifiée.

Palette principale :

*   **Principal** : Gris foncéUtilisé pour le fond principal de l’application.

*   **Secondaire** : Gris clairUtilisé pour les éléments secondaires (cartes, conteneurs).

*   **Texte** : Gris très clairGarantit une bonne lisibilité sur fond sombre.

*   **Tercière**: NoirUtilisé pour les contrastes forts et certains éléments spécifiques


### Typographie

La typographie choisie vise la clarté, la sobriété et la compatibilitémulti-plateforme.

Polices utilisées :

*   **Liberation Sans**

*   **Noto Sans**

    *   Noto Sans Regular

    *   Noto Sans Medium

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

11. Modification des tableaux

> Sur la Page Tableau, Modifier le nom du tableau.

12. Archivage de tâches

> Sur la Page Tableau, seléctionner une tâche. Archiver la tâche

13. Visualiser les tâches archivées

> Sur la Page Tableau, cliquer sur le bouton des archives

14. Restorer une tâche archivée

> Sur la Page Tableau, cliquer sur le bouton des archives
> Cliquer sur le bouton Restorer de la tâche associée

15. Supprimer une tâche archivée

> Sur la Page Tableau, cliquer sur le bouton des archives
> Cliquer sur le bouton Supprimer de la tâche associée

16. Inviter un collaborateur

> Sur la Page Tableau, inviter un collaborateur en inscrivant son adresse mail, possibilité de donner les droits d'administrateur

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
    3. Le créateur du tableau a invité l'autre sur son tableau.
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
    3. L'utilisateur a créé une catégorie.
    4. L'utilisateur a créé une tâche.
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
    3. L'utilisateur a créé une catégorie.
    4. L'utilisateur a créé une tâche.
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

11. Modification des tableaux

__Objectif__: Changer le nom du tableau.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur les paramètre du tableau.
    3. Modifier le nom du tableau.
    4. Valider la modification.
__Resultat__: Voir le changement du nom.

12. Archivage de tâches

__Objectif__: Archiver une tâche.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
    3. L'utilisateur a créé une catégorie.
    4. L'utilisateur a créé une tâche.
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur la tâche déjà créer.
    3. Cliquer sur le bouton "Archiver" de la tâche.
__Resultat__: La tâche a été archiver et n'est plus visible sur le tableau.

13. Visualiser les tâches archivées

__Objectif__: Visualiser les tâches archivées.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
    3. L'utilisateur a créé une catégorie.
    4. L'utilisateur a créé une tâche.
    5. L'utilisateur a archivé une tâche.
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur le bonton des archives.
__Resultat__: L'utilisateur peut visualiser toutes les tâches archivées.

14. Restorer une tâche archivée

__Objectif__: Restorer une tâche archivée.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
    3. L'utilisateur a créé une catégorie.
    4. L'utilisateur a créé une tâche.
    5. L'utilisateur a archivé une tâche.
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur le bonton des archives.
    3. Cliquer sur le bouton de restauration de la tâche associée
__Resultat__: La tâche est restaurée sur le tableau et n'est plus dans les archives.

15. Supprimer un tâche archivée

__Objectif__: Restorer une tâche archivée.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
    3. L'utilisateur a créé une catégorie.
    4. L'utilisateur a créé une tâche.
    5. L'utilisateur a archivé une tâche.
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur le bonton des archives.
    3. Cliquer sur le bouton de suppression de la tâche associée
__Resultat__: La tâche est supprimée des archives.

16. Inviter un collaborateur

__Objectif__: Inviter un collaborateur à participer à un tableau.
__Preconditions__:
    1. L'utilisateur est connecte.
    2. L'utilisateur a créé un tableau.
    3. Le collaborateur à inviter possède un compte EpiTrello
__Etape a suivre__:
    1. Ouvrir la Page du Tableau.
    2. Cliquer sur le bonton Partager.
    3. Inscrire le mail du collaborateur à inviter
    4. Choisir si le collaborateur à les permission d'administrateur du tableau
    5. Valider le formulaire
__Resultat__: Le collaborateur peut participer à l'édition du tableau selon les permissions données.


## Spécifications techniques

- Authentification utilisant le SSO de Google :
    *   Authentification rapide et sécurisée, sans création manuelle de mot de passe.
    *   Réduction des risques liés à la gestion d'identifiants.
    *   Simplification de l'expérience utilisateur
- Le back-end doit être développé en utilisant le framework Django :
    *   Framework robuste, sécurité intégrée et structure claire.
- L'API du back-end doit utiliser la librairie Django-Ninja:
    *   Développement d'API REST performante et typée sur les standards OpenAPI.
    *   Facilitation de validation de données et de génération de documentation.
- Le front-end doit être développé en utilisant le framework Nuxt:
    *   Création d'application web moderne et performante.
    *   Organisation du code claire et bonne gestion du routage.
    *   Adapté au projet de petite et moyenne taille.
- Le front-end sera complété par la librairie NuxtUI:
    *   Accélération du développement d'interface.
    *   Garantit une cohérence visuelle moderne.

## Annexes

### Back-end

- [Documentation Framework Django](https://www.djangoproject.com/)
- [Documentation Django Ninja](https://django-ninja.dev/)

### Front-end

- [Documentation Framework Nuxt](https://nuxt.com/)
