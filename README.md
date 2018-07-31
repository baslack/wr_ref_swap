# wr_ref_swap
## The Wrong Rock - Reference Updater and Swapper

Author: Benjamin Slack

### Abstract:
This utility was developed during my work on ["The Wrong Rock"](http://heromation.com/project/the-wrong-rock/).
During the course of working on the project, there were many updates to the various assets. Unfortunately, the
the way Artella handles published versions results in a new folder location for every updated asset. In a complicated
scene, this can mean dozens upon dozens of references that need to have their paths updated to allow the most 
recent version of the asset to be used. This tool mitigates that problem by inspecting the installed versions 
of a given asset and updating all references to that asset in the Maya scene file accordingly. It also allows for
the mapping of one asset to another, to allow for swapping out of generic character rigs with specific characters.
The updating and mapping is configured through the use of a simple JSON file.
