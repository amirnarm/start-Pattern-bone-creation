import bpy
import math

# create bone in star pattern
def Bone_Creator(obj,angle,rows):
    bpy.ops.object.mode_set(mode='EDIT')      
    arm = obj.data
    
    #clear the object
    for bone in arm.edit_bones:
        arm.edit_bones.remove(bone)
     
    x = 1
    y = 1
    bones =[]
    # calculate the number of start corners for example if you input 60 degree in function argument you get 6 side star
    number_angels = math.ceil(int(360/angle))

    # define first row of star, other row of bones follow size of this bones and their vectors to create themselves
    for i in range(number_angels):
        bone = arm.edit_bones.new("mainBone")
        bone.head[:]= 0.00,0.00,0.0
        bone.tail[:]= math.sin(math.radians(angle * i))* x , math.cos(math.radians(angle* i))* y ,0.0
        bone.roll = 0.0000
        bone.use_connect = False
        bones.append(bone)
     
        
    # create bones from row 2 
    for i in range(1,rows,1):
        for j in range(number_angels):
            bone = arm.edit_bones.new("Bone_row_"+ str(i) + "_" + "Bone_num_" + str(j) )
            bone.head[:]= bones[(j% number_angels) +( (i-1) * number_angels) ].tail
            bone.tail[:]= bones[(j% number_angels) ].tail[0] + bones[ (j% number_angels) +( (i-1) * number_angels) ].tail[0],bones[(j% number_angels) ].tail[1] + bones[ (j% number_angels) +( (i-1) * number_angels) ].tail[1],bones[(j% number_angels) ].tail[2] + bones[ (j% number_angels) +( (i-1) * number_angels) ].tail[2]
            bone.roll = 0.0000
            bone.use_connect = False
            bones.append(bone)
    bpy.ops.object.mode_set(mode='EDIT')
    
    #deselect all bones
    for bone in arm.edit_bones:
        bone.select = False
        bone.select_head = False
        bone.select_tail = False
    
    
if __name__ == "__main__":
    # create Armature object
    bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    
    
    # function to Create bone, second argument is the angle between bones, and thirt argument is number of necessary bones
    Bone_Creator(bpy.context.active_object,60,5)
    