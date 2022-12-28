# Universal Rig Adapter for Maya
Fit rigged joint skeleton to mesh that has been modified, or scaled, with the weights transferred to new one.

![image](https://user-images.githubusercontent.com/88772846/209735789-54982a17-dadb-4728-8a8e-82f2c36ee474.png)

## Commercial / Non Commercial Use
For non commercial use, use this file here. If you make money out of this project, or you use it in a project that makes money for you or a third party, please buy the commercial license from Artstation. There is no funcional changes in both the versions, just that one helps me pay the bills.



## Uses
1. If you keep the topology same you can use a program like wrap 3D to use the same rig over and over again with a different shape of geometry.
2. In case you have sculpted the mesh in Zbrush you can use this to fit your skeleton to fit the new shape.
3. In case you wanna scale your current model in the scene.

## Video Demo and Tutorial
https://youtu.be/VRcPe2P-hlk

## Instructions on how to use.
1. Run from script editor or save to shelf. You can save the py script anywhere, it's not path dependant.
2. Click on the corresponding buttons after having selected the objects in the scene, the currently rigged object is Original Mesh, the scaled or modified model is New Mesh, and the root joint is the primary joint of the skeleton.
3. Once the skeleton is in position, use either the UV method or the Dictionary method to reskin the modified mesh.

## Note
1. Written in Python 3. Will not work in older Maya version.
2. Works on hierarchal joint based skeleton system.
3. Will ignore if something like a mesh, or helper is part of the hierarchal chain.
