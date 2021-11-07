# DiffuseAnimals: Reaction-Diffusion Models for the Generation of Biological Patterns
![Logo](Logo.png)


## Introduction
Reaction-diffusion equations can be utilized in order to describe processes of non-chemical systems as well as those containing one or more chemical substances that exhibit vast spatiotemporal patterns such as socioeconomic interactions, neutron diffusion, and biochemical reactions. Solutions to these equations can exhibit wave-like behavior as first described by Alan Turing in his 1952 article *The Chemical Basis of Morphogenesis*. Here, we explore the Gray-Scott and FitzHugh–Nagumo models in order to simulate the diversity of patterns found among species as observed on the skin, scales, and fur of animals and across the domains of life.

![RDModels](RDModels.png)


## Pattern Generation
We leverage [Flask](https://flask.palletsprojects.com/en/2.0.x/) to provide a web app with as an interface to modify the variables of reaction-diffusion equations to produce a GIF of the corresponding biological pattern such as the following zebrafish simulation:

![Zebrafish_pattern_GIF.gif](Zebrafish_pattern_GIF.gif "Zebrafish pattern")

The zebrafish pattern can be produced by using the interface with the parameters depicted below.


![Annotated_webapp.png](Annotated_webapp.png "Annotated web app") 


## [McGill Physics Hackathon](https://www.physics.mcgill.ca/hackathon/) 2021 Team Members:
* Ryan Senoune
* Austin J. Szuminsky
* Yuliya Shpunarska
* Xavier L'Heureux


## License
BSD 3-Clause License
