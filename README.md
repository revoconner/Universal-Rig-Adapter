# Universal Rig Adapter for Maya
Fit rigged joint skeleton to mesh that has been modified, or scaled, with the weights transferred to new one.

![image](https://user-images.githubusercontent.com/88772846/209456628-9ea6c4e7-24fa-43b1-afbf-e4d3c348bcd2.png)



## Video Demo and Tutorial
https://youtu.be/z5zVzB6rCZU

## Instructions on how to use.
1. Run from script editor or save to shelf. You can save the py script anywhere, it's not path dependant.
2. Click on the corresponding buttons after having selected the objects in the scene, the currently rigged object is Original Mesh, the scaled or modified model is New Mesh, and the root joint is the primary joint of the skeleton.

## Note
1. Written in Python 3, will probably not work in older Maya version.
2. Works on heirarchal joint based skeleton system.
3. The old and new mesh needs to have same topology and UV, I am working on using just one requirement.
4. Will ignore if something like a mesh, or helper is part of the heirarchal chain.
