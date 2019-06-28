# Origami Patterns
Inkscape extension that creates origami tesselation patterns, create for the Origabot project

## Installation:
To install a new extension, download and unpack the archive file. Copy the files into the directory listed at `Edit > Preferences > System: User extensions`

On Windows, the default directory is:
`C:\Program Files\Inkscape\share\extensions`

While on Linux, the directory is:
`/home/$USER/.config/inkscape/extensions/`

## Accessing the extention:
The extension can be found on `Extensions > Origami grid patterns`

## Input parameters:
- Number of lines
- Number of columns
- Length of each grid square
- Colors of mountain creases, valley creases and enclosure
- Dashed strokes of mountain creases, valley creases and enclosure

## Output:
Creates the pattern. 
To simplify editing, ungrouping it you get three distinct groups of objects: the mountain creases, the valley creases and enclosure. These groups can also be divided into smaller groups. Waterbomb example:

```
waterbomb
├── enclosures
│   ├── bottom
│   ├── left
│   ├── right
│   └── top
├── mountains
│   ├── horizontal lines
│   └── vertical lines
└── valleys
    ├── line 1
    │   ├── top
    │   └── bottom
    ├── line 2
    │   ├── top
    │   └── bottom
    ├── ...
    └── line N
    │   ├── top
    │   └── bottom
```

## Patterns implemented until now:
- Waterbomb tesselation (and Magic Ball)
- Kresling tower

## Todo:
- Add more patterns if necessary
- Add option to draw points
- Finish implementing unit selector (only milimiters for now)

