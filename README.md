# Chartmaker CLI
A Python CLI that converts json defined objects to charts as svg tags for html

*Currently only makes pie charts*

### Quick Guide:
1. Enter json data in a file. See format of 'input.json'
2. Override 'defaultstyles.json' properties such as 'stroke', 'stroke-width'
3. Open Command Line.
4. Type:
```
python chartr.py [inputFileName]
```
5. To specify output file:
```
python chartr.py [inputFileName] --out [outputFileName]
```
6. Press Enter and you're done!

### Example:
#### 'input.json':
```
{
    "centre": "310,310",
    "radius": "200",
    "stroke-width": 5,
    "show-percent": true,
    "items": [
        {
            "value": 570,
            "color": "#6ea4c1"
        },
        {
            "value": 140,
            "color": "#526f9d"
        },
        {
            "value": 89,
            "color": "#495fa0"
        },
        {
            "value": 53,
            "color": "#5d4b90"
        }
    ]
}
```
#### Output:

![Pie Chart]
