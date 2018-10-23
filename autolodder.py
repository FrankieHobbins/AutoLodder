import bpy
print("--Adding LODS to objects--")

scn = bpy.context.scene
objs = bpy.context.selected_objects

def moveModifier(obj):
    armindex = -1
    decindex = -1
    decname = "none"
    
    #check all modifiers in object to work out where the armature is and how far to move decimate
    for x in range(len(obj.modifiers)):
        if obj.modifiers[x].type == "DECIMATE" and "LOD" in obj.name:
            decindex = x
            decname = obj.modifiers[x].name
        if obj.modifiers[x].type == "ARMATURE":
            armindex = x

    #move the decimate modifier so its above the armature modifier
    moveAmount = decindex - armindex
    if moveAmount > 0:
        for x in range(moveAmount):
            bpy.ops.object.modifier_move_up(modifier=decname)
    return

def newObject(obj, number, ratio):
    #duplicate and name 
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()
    new_obj.animation_data_clear()
    scn.objects.link(new_obj)
    new_obj.name = obj.name + "_LOD" + str(number)

    #apply modifiers
    modifier = new_obj.modifiers.new(name = "LOD" + str(number) + "decimate", type='DECIMATE')
    modifier.ratio = ratio
    
    #move modifier before armature
    moveModifier(new_obj)
    return

#add lods to selected objects
for obj in objs:
    #only work on objects that dont already have lods setup
    if "_LOD" not in obj.name:
        newObject(obj, 1, 0.66)
        newObject(obj, 2, 0.33)
        obj.name = obj.name + "_LOD0"
