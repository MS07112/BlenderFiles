bl_info = {
    "name": "Marker Utilities",
    "category": "Sequencer",
}

# bpy.data.scenes['SmokeWeed'].timeline_markers.items()

## Get Frame # for given Timeline Marker:
# bpy.data.scenes['SmokeWeed'].timeline_markers['Lacus-L'].frame

## Is this Marker Selected?
# C.scene.timeline_markers[marker].select

import bpy
import os



    

## TODO:  Integrate getPath functions into Marker functions in a better way.
def getProjectPath():
    return os.path.dirname(bpy.data.filepath)
def getCurrentScene():
    return bpy.context.scene
def getSceneName():
    return bpy.context.scene.name
def getTargetPath():
    target_path = os.path.dirname(bpy.data.filepath) + '/' + bpy.context.scene.name
    return target_path


project_path = getProjectPath()
current_scene = getCurrentScene()
scene_name = getSceneName()
target_path = getTargetPath()

#    image_format = bpy.data.scenes[scene_name].render.image_settings.file_format.lower()
image_format = "png"


def snapSelectedMarkers():
    enumDuplicateMarkers()

    project_path = getProjectPath()
    current_scene = getCurrentScene()
    scene_name = getSceneName()
    target_path = getTargetPath()
    
    
    numMarkers = len(bpy.data.scenes[scene_name].timeline_markers)
    timelineMarkerKeys = bpy.data.scenes[scene_name].timeline_markers.keys()

    # Default:
    for marker in timelineMarkerKeys:
        if(bpy.data.scenes[scene_name].timeline_markers[marker].select):
            # Change to frame of marker:
            bpy.data.scenes[scene_name].frame_current = bpy.data.scenes[scene_name].timeline_markers[marker].frame
            
            # Render Image
            bpy.ops.render.render()
            
            filenameOutput = "%s/%s.%s" % (target_path, marker, image_format)
            
            # Save Image
            bpy.data.images['Render Result'].save_render(filenameOutput)
    return


def snapshotMarkers(iterations, optionalName="None"):
    enumDuplicateMarkers()    

    project_path = getProjectPath()
    current_scene = getCurrentScene()
    scene_name = getSceneName()
    target_path = getTargetPath()

    if(optionalName == "None"):
        # For #iterations: 
        for num in range(0,iterations):
            # Render Image
            bpy.ops.render.render()
            
            bpy.data.images['Render Result'].save_render(target_path + '/' + getCurrentMarkerName() + '.' + image_format)
            
            # Go to frame of the next Marker
            bpy.ops.screen.marker_jump(next=True)
            
    # Optional Custom Name:
    else:
        # For #iterations: DO
        for num in range(0,iterations):
            # Render Image
            bpy.ops.render.render()
            filenameOutput = "%s/%s-%d.%s" % (target_path, optionalName, num, image_format)
            bpy.data.images['Render Result'].save_render(filenameOutput)
            
            # Go to frame of the next Marker
            bpy.ops.screen.marker_jump(next=True)

    return


def snapSequence(iterations, frameInterval, optionalName="None"):
    enumDuplicateMarkers()
    
    project_path = getProjectPath()
    current_scene = getCurrentScene()
    scene_name = getSceneName()
    target_path = getTargetPath()
    
    if(optionalName == "None"):
    
        # For #iterations: 
        for num in range(0,iterations):
            # Render Image
            bpy.ops.render.render()
            
            bpy.data.images['Render Result'].save_render(target_path + '/' + getCurrentMarkerName() + '.' + image_format)
            
            # Increase Frame Number
            bpy.data.scenes[scene_name].frame_current += frameInterval
            
    # Optional Custom Input
    else:
        # For #iterations: DO
        for num in range(0,iterations):
            # Render Image
            bpy.ops.render.render()
            filenameOutput = "%s/%s-%d.%s" % (target_path, optionalName, num, image_format)
            bpy.data.images['Render Result'].save_render(filenameOutput)
            
            # Increase Frame Number
            bpy.data.scenes[scene_name].frame_current += frameInterval
    return


    

# Navigate to proper folder
def nav2TargetFolder():
    if(areWeThere() == True):
        return
    else:
        sceneFolderExists()
        os.chdir(getTargetPath())
        return


# Are we already in the right folder?
def areWeThere():
    if(os.getcwd() == getTargetPath()):
        return True
    else:
        return False
    

# Change Directory to one Corresponding to Current Scene, Create if non-existent.
def sceneFolderExists():
    dir_contents = os.listdir(getProjectPath())
    
    output = False
    
    for entry in dir_contents:
        if(entry == getSceneName()):
            output = True
            
    if(output == False):
        os.mkdir(getProjectPath() + '/' + getSceneName())
        
    return output


# Get Name of a Marker at the current frame:
def getCurrentMarkerName():
    markerName = "NULL"
    
    project_path = getProjectPath()
    current_scene = getCurrentScene()
    scene_name = getSceneName()
    target_path = getTargetPath()
    
    # Get current frame #:
    current_frame = current_scene.frame_current
    
    
    markers = bpy.data.scenes[scene_name].timeline_markers.keys()
    # Find the Marker at the current point
    for marker in markers:
        ## TODO: Should check if there is a marker to start with
        if(bpy.data.scenes[scene_name].timeline_markers[marker].frame == current_frame):
            markerName = bpy.data.scenes[scene_name].timeline_markers[marker].name

    if(markerName == "NULL"):
        markerName = "%s-%d" % (scene_name, current_frame)

    print(markerName)

    return markerName

## Enumerate Duplicate Marker Names
    # Go through list of markers in the Scene by Index (NOT NAME)
        # IF 2 or more entries have the same names:
            # Put them into their own list
            # Append their (new list) index number (plus 1) onto their name
            
#def enumDuplicateMarkers():
#    numMarkers = len(bpy.data.scenes[scene_name].timeline_markers)
#    for index in range(0,numMarkers):
#        name = bpy.data.scenes[scene_name].timeline_markers[index].name
#        new_name = "%s_%d" % (name, index)
        
        
## Alternative: For every time a new name is encountered: add it to the list with a value of 1
    # IF a duplicate is encountered: increase the value of the K:V pair by 1
def enumDuplicateMarkers():
    
    project_path = getProjectPath()
    current_scene = getCurrentScene()
    scene_name = getSceneName()
    target_path = getTargetPath()
    
    numMarkers = len(bpy.data.scenes[scene_name].timeline_markers)
    timelineMarkerKeys = bpy.data.scenes[scene_name].timeline_markers.keys()
    
    # Creates a dictionary consisting of the unique (non-repeating) keys from the list of markers
    testDict = {}        
    testDict = testDict.fromkeys(bpy.data.scenes[scene_name].timeline_markers.keys(), 0)
    
    duplicateDict = {}  # For tracking (in advance) which Markers have duplicate keys
    duplicateDict = testDict.fromkeys(bpy.data.scenes[scene_name].timeline_markers.keys(), 0)
    
    for key in duplicateDict.keys():
        # How many list entries are there?
        duplicateDict[key] = timelineMarkerKeys.count(key)
        

    for index in reversed(range(0, numMarkers)):
        # Name of Marker, being selected via index# (not marker name directly)
        name = bpy.data.scenes[scene_name].timeline_markers[index].name
        
        # Re-Name ONLY IF there are duplicate entries of this key
        if(duplicateDict[name] > 1):
            # Assign new name to Marker
            bpy.data.scenes[scene_name].timeline_markers[index].name = "%s_%d" % (name, testDict[name] + 1)
        
        # Increment testDict's corresponding K:V entry by 1
        testDict[name] += 1
        
    ## DEBUG CODE: ## ( for enumDuplicateMarkers() )    
#    print()
#    print(str(duplicateDict))
#    print(str(testDict))
    return

    
    
class snapMarkers(bpy.types.Operator):
    bl_idname = "marker.snapmarker"
    bl_label = "Render Snapshots of Frames at each Selected Marker"
    
    ## Main Functions: snapshotMarkers, snapSequence [doesn't rely on markers to traverse], nav2TargetFolder
    def execute(self, context):
        snapSelectedMarkers()
        print(target_path)
        return {'FINISHED'} 


        
def register():
    bpy.utils.register_class(snapMarkers)
    
def unregister():
    bpy.utils.unregister_class(snapMarkers)
    
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
