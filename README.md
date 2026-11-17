# Fishing in the Clouds (Pêcher dans les nuages)

Un petit jeu de pêche cosy en pixel art façon Minecraft : elle pêche des nuages depuis le balcon d'un immeuble de Hanoï vu de profil.
Textes du jeu en anglais, commentaires du code en français.
Pensé pour le Samsung Galaxy Z Flip 7 à moitié plié (mode Flex) : le ciel en haut, le balcon en bas.

## Jouer
- Le jeu tient dans **`index.html`** (un seul fichier, aucune dépendance) : il peut s'ouvrir tel quel dans un navigateur.
- En ligne : activer **GitHub Pages** (Settings → Pages → Branch `main`, dossier `/root`), puis ouvrir
  `https://homotopic-to-the-circle.github.io/clouds-fishing/` dans Chrome sur le téléphone.

## L'installer sur l'écran d'accueil (PWA)
1. Ouvrir l'adresse GitHub Pages dans **Chrome** sur le Flip.
2. Menu ⋮ → **Ajouter à l'écran d'accueil** → **Installer**.
3. Le jeu s'ouvre ensuite en plein écran, sans barre d'adresse, et fonctionne hors-ligne (`sw.js`).

Si `index.html` est ouvert seul (sans les autres fichiers), il génère lui-même un manifest et ses icônes.

## Comment on joue
- **Fish** sort la canne (interrupteur ON/OFF) : le bouchon s'envole dans les nuages.
- Un nuage qui passe près du bouchon peut s'y intéresser et **grignoter** (petites secousses) : ne pas taper tout de suite.
- Quand **ça mord** (« ! », vibration, bouton « REEL IN! »), taper l'écran ou le bouton.
- Le **carnet** (en bas à gauche) liste toutes les prises ; la progression est sauvegardée sur le téléphone.
- Le ciel suit l'heure réelle ; certains nuages ne passent qu'à certaines heures.

## Modifier le jeu
Tout ce qui est éditable est en haut du `<script>` de `index.html`, section **« 1. DONNÉES ÉDITABLES »** :
- `CONFIG` : chance d'objet spécial (`CHANCE_OBJET_SPECIAL: 0.11`), objet garanti à la première prise (`PREMIERE_PRISE`), délais, taille des pixels…
- `RARETES` : poids d'apparition, durée de la fenêtre de ferrage.
- `NUAGES` : noms, descriptions, heures de passage, indices du carnet.
- `OBJETS_SPECIAUX` : souvenirs du voyage. **Les emplacements `souvenir1` à `souvenir5` sont à remplir** (nom + description,
  en anglais, sprite au choix parmi `pho, eggcoffee, poisson, chat, rocher, carte, lanterne, tabouret, livre`). `actif: false` retire un objet.
- `TEXTES`, `PALETTE_HORAIRE` : messages et couleurs du ciel heure par heure.

Après une modification publiée sur GitHub Pages, incrémenter `VERSION` dans `sw.js` pour que le téléphone récupère la nouvelle version.

## Tester une heure précise
Ajouter `?h=` à l'adresse : `index.html?h=19.5` (coucher de soleil), `?h=23` (nuit), `?h=6` (aube).

## Police
La police pixel `CloudBlocks` (style blocs, dessin original) est générée par `outils/police.py` et intégrée en base64 dans `index.html`.
Pour modifier une lettre : éditer le tableau `G` du script, puis `python3 outils/police.py` (nécessite `pip install fonttools`).
