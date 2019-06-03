# Origami Grid Patterns
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
To simplify editing, ungrouping it you get three distinct groups of objects: the mountain creases, the valley creases and enclosure. These groups can also be divided into smaller groups. Magic ball example:

```
magic-ball
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
    │   ├── bottom
    │   └── top
    ├── line 2
    │   ├── bottom
    │   └── top
    ├── line 3
    │   ├── bottom
    │   └── top
    └── line ...
        ├── bottom
        └── top
```

## Patterns implemented until now:
- Magic ball

## Todo:
- Add more patterns if necessary
- Add option to draw points
- Finish implementing unit selector (everything is drawn in milimeters, the selector does not do anything yet)

