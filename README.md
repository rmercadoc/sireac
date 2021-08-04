# 🖥SIREAC

[SIREAC](https://sireac.rmercado.dev) is a Music Chord Sentiment Based Recommender system.

## Usage

Usage example
```
python sireac.py --joy=4 --suprise=3
```

Help message
```
sireac.py

        Chord recommender system.
        Makes recommendations of chords to continue a piece according to the given desired sentiments.

        OPTION                  DESCRIPTION
        -s <path-to-score>      specify teh path of the musicxml file to analyze and recommend to
        --anger=(1-5)           specify a value of anger in range (1-5)
        --fear=(1-5)            specify a value of fear in range (1-5)
        --joy=(1-5)             specify a value of joy in range (1-5)
        --love=(1-5)            specify a value of love in range (1-5)
        --sadness=(1-5)         specify a value of sadness in range (1-5)
        --surprise=(1-5)        specify a value of surprise in range (1-5)
        -n --n                  specify the amount of recommendations (max 10)

        -w --w                  specify the width of the verbose output (def 80)

        -v                      verbose output
        -d                      detailed output (to be used with -v option)

```


## Python MusicXML feature parser
Python music xml feature parser.

The main purpose in to identify music features from musicXML files, to further use this information 
and the results from SIREAC [survey](https://sireac.rmercado.dev) to develop a music chord
recommender system that aims to help new composers to achieve the desired sentiment on their pieces 
recommending the use of various harmonies.

I'm developing this as part of my thesis for my application for the graduate degree of software engineer.

 

