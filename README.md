# neuronCounting
We release the code for our paper "Distinct neural networks derived from galamin-containing nociceptors and neurotensin-expressing pruriceptors" accepted by PNAS 

Using following step to run this project:

1. Download 'annotation_25.nrrd' and 'structurelite.txt' from https://help.brain-map.org/display/mousebrain/API
   
   The nuclei annotated by the 3D Allen CCFv3 were divided into two parts according to their location in the hemisphere. A total of 1014 nuclei were analyzed.
   
   Run code "dataTransfer-1.py" to transfor original data into floder "ANOnew_order".

2. Run code SingleSliceCounting_newidlist.py to get the Cell number in each nucleus. 

You need to prepare a file including the coordinates of labeled neurons. In the project, we provide a example named "pnt_correct_rotated_5-3.csv". The results are saved under folder "SSc".
