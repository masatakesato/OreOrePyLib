import bpy

# access scene objects
print("//############### Blender Mesh Boject traverse program ##################//")



for ob in bpy.data.objects:
    print( "Object Name: ", ob.name )
    print( "Type: ", ob.type)
    
    # process mesh only 
    if ob.type == "MESH":
        
        # get materials
        print("//============ Material info =============//")
        if ob.material_slots != None:
            for mat_slot in ob.material_slots:
                mat = mat_slot.material
                print("Material Name:", mat_slot.name )
                print(" diffuse shader(",  mat.diffuse_shader, ") = (", end="" )
                print( mat.diffuse_color.r, ",", mat.diffuse_color.g, ",", mat.diffuse_color.b, ")" )
                print(" specular shader(",  mat.specular_shader, ") = (", end="" )
                print( mat.specular_color.r, ",", mat.specular_color.g, ",", mat.specular_color.b, ")" )
        
        # get vertices
        print("//=========== Vertex info ==============//")
        counter = 0
        for vertex in ob.data.vertices:
            print( "position =(", vertex.co.x, ",", vertex.co.y, ",", vertex.co.z, ")" )
            print( "normal =(", vertex.normal.x, ",", vertex.normal.y, ",", vertex.normal.z, ")" )
            print("")
            counter += 1
            
        # get faces
        print("//=========== Face info =============//")
        for face in ob.data.faces:
            print( "material index :", face.material_index )
            print( "vertex index :", end="" )
            for vert_idx in face.vertices: print( vert_idx, ",", end="")
            print( "face normal =(", face.normal.x, ",", face.normal.y, ",", face.normal.z, ")" )
            
            
            print("")
        
            
        # get children
        for child_obj in ob.children:
            print( "  child name: ", child_obj.name )
            