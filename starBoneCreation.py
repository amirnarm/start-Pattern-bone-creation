
# blender StarBoneCreationAddon
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
        "name": "Star PatternBone Creator",
        "description": "create Armature in star pattern",
        "author": "amirnarm <amirshnarm@gmail.com>",
        "version": (1, 0),
        "blender": (2, 93, 0),
        "location": "VIEW3d > Properties > AmirNarm",
        "warning": "", # used for warning icon and text in add-ons panel
        "wiki_url": "http://some.url",
        "tracker_url": "http://tracker.url",
        "support": "COMMUNITY",
        "category": "Rigging"
        }


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


class StarArmature(bpy.types.Operator):
    
    """Tooltip"""
    bl_idname = "object.star_armature"
    bl_label = "Star Armature"
    bl_option = {'REGISTER' , 'UNDO'}
    
    angle : bpy.props.IntProperty( name = 'angle', description = 'the angle between two star sides', default = 60, min=1,soft_max=360)
    row : bpy.props.IntProperty( name = 'row', description = 'the number of row in star bones', default = 5, min=1 , soft_max=10 )

    def execute(self, context):
        #main(context,self.angle,self.row)
        bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        # function to Create bone, second argument is the angle between bones, and thirt argument is number of necessary bones
        Bone_Creator(bpy.context.active_object,self.angle,self.row)
        
        return {'FINISHED'}
    
    #def invoke(self, context,event):
     #   pass
    #def modal(self, context,event):
     #   pass    

#def menu_func(self, context):
#    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)


class StarBoneCreatorLayout(bpy.types.Panel):

    bl_label = "Star Bone Creator Addon"
    bl_idname = "Star_Bone_Creator_Addon"
    bl_space_type = 'VIEW_3D'
    #bl_space_type = 'PROPERTIES'
    bl_region_type = 'UI'
    bl_category= "AmirNarm"
    #bl_context = "render"

    def draw(self, context):
        layout = self.layout
        props = layout.operator('object.star_armature', text = 'init Star Armature', icon = 'ARMATURE_DATA')
        
        layout.label(text=" Properties:")
        row = layout.row(align=True)
        row.prop(props, 'angle')
        row.prop(props, 'row')        
        
            
#        scene = context.scene
#        #angle = bpy.props.FloatProperty(name = "angle:")
#        #row = bpy.props.IntProperty(name = "row:")

#        # Create a simple row.
#        layout.label(text=" Simple Row:")

#        row = layout.row()
#        row.prop(scene, "frame_start")
#        row.prop(scene, "frame_end")

#        # Create an row where the buttons are aligned to each other.
#        layout.label(text=" Aligned Row:")

#        row = layout.row(align=True)
#        row.prop(scene, "frame_start")
#        row.prop(scene, "frame_end")

#        # Create two columns, by using a split layout.
#        split = layout.split()

#        # First column
#        col = split.column()
#        col.label(text="Column One:")
#        col.prop(scene, "frame_end")
#        col.prop(scene, "frame_start")

#        # Second column, aligned
#        col = split.column(align=True)
#        col.label(text="Column Two:")
#        col.prop(scene, "frame_start")
#        col.prop(scene, "frame_end")

#        # Big render button
#        layout.label(text="Big Button:")
#        row = layout.row()
#        row.scale_y = 2.0
#        row.operator("object.star_armature")

#        # Different sizes in a row
#        layout.label(text="Different button sizes:")
#        row = layout.row(align=True)
#        row.operator("object.star_armature")

#        sub = row.row()
#        sub.scale_x = 2.0
#        sub.operator("render.render")

#        row.operator("object.star_armature")

def add_star_armature_menu_draw(self,context):
    self.layout.operator('object.star_armature')



def register():
    bpy.utils.register_class(StarArmature)

    bpy.utils.register_class(StarBoneCreatorLayout)
    bpy.types.VIEW3D_MT_armature_add.append(add_star_armature_menu_draw)


def unregister():
    bpy.utils.unregister_class(StarArmature)
    bpy.utils.unregister_class(StarBoneCreatorLayout)
    bpy.types.VIEW3D_MT_armature_add.remove(add_star_armature_menu_draw)


if __name__ == "__main__":
    register()
    
    #testCall
    #bpy.ops.object.star_armature()
