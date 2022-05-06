import sys
import os       

from fbx import *
import FbxCommon



print("//############### FbxMesh test program ##################//")


# initialize fbx scene manager, and fbx scene
lSdkManager = None
lScene = None

(lSdkManager, lScene) = FbxCommon.InitializeSdkObjects()

info = FbxDocumentInfo.Create(lSdkManager, "SceneInfo")
info.mTitle = "hoge title"
info.mSubject = "hoge subject"
info.mAuthor = "uimac fbx exporter"
info.mRevision = "rev. 1.0"
info.mKeywords = "hoge keywords"
info.mComment = "hoge comment"
lScene.SetSceneInfo(info)


# initialize mesh information
numfaces = 2
numverts = 4


# create fbxnode object
print("Create FbxNode...")
fbx_node = FbxNode.Create(lSdkManager, "meshNode") #Cannot create without SceneManager object

# test func
#print(fbx_node.GetChildCount())


#create fbxmesh object (quad plane)

# create instance
print("Create FbxMesh....")
fbx_mesh = FbxMesh.Create(lSdkManager, "test")

# init vertices
fbx_mesh.InitControlPoints(numverts)

# Add Vertices
fbx_mesh.SetControlPointAt( FbxVector4(-10.0, -10.0, 0.0), 0 )
fbx_mesh.SetControlPointAt( FbxVector4(+10.0, -10.0, 0.0), 1 )
fbx_mesh.SetControlPointAt( FbxVector4(+10.0, +10.0, 0.0), 2 )
fbx_mesh.SetControlPointAt( FbxVector4(-10.0, +10.0, 0.0), 3 )


# init normal vectors
fbx_normal = FbxLayerElementNormal.Create(fbx_mesh, "NormalLayer")
fbx_normal.SetMappingMode(FbxLayerElement.eByControlPoint)
fbx_normal.SetReferenceMode(FbxLayerElement.eDirect)
fbx_normal.GetDirectArray().Resize(numverts)

# Add Normals
fbx_normal.GetDirectArray().SetAt(0, FbxVector4(0, 0, 1) )
fbx_normal.GetDirectArray().SetAt(1, FbxVector4(0, 0, 1) )
fbx_normal.GetDirectArray().SetAt(2, FbxVector4(0, 0, 1) )
fbx_normal.GetDirectArray().SetAt(3, FbxVector4(0, 0, 1) )



# init uv coordinates
fbx_tex_uv = FbxLayerElementUV.Create(fbx_mesh, "TexcoordLayer")
fbx_tex_uv.SetMappingMode(FbxLayerElement.eByPolygonVertex )#eByControlPoint)
fbx_tex_uv.SetReferenceMode(FbxLayerElement.eIndexToDirect)#eDirect
fbx_tex_uv.GetIndexArray().Resize(numverts)

# Add Texture UV
fbx_tex_uv.GetDirectArray().Add(FbxVector2(0, 0))
fbx_tex_uv.GetDirectArray().Add(FbxVector2(1, 0))
fbx_tex_uv.GetDirectArray().Add(FbxVector2(1, 1))
fbx_tex_uv.GetDirectArray().Add(FbxVector2(0, 1))


fbx_tex_uv.GetIndexArray().SetAt(0, 0)
fbx_tex_uv.GetIndexArray().SetAt(1, 1)
fbx_tex_uv.GetIndexArray().SetAt(2, 2)
fbx_tex_uv.GetIndexArray().SetAt(3, 3)
                                                


# Add Material
fbx_material = FbxLayerElementMaterial.Create(fbx_mesh, "Material")
fbx_material.SetMappingMode(FbxLayerElement.eByPolygon) # assign matertial for each polygon
fbx_material.SetReferenceMode(FbxLayerElement.eIndexToDirect)
fbx_material.GetIndexArray().SetCount(numfaces)


# FbxSurfacePhong material
material1 =  FbxSurfacePhong.Create(lSdkManager, "Material_Phong")
material1.Diffuse.Set(FbxDouble3(1.0, 0.0, 0.0))
material1.DiffuseFactor.Set(0.4)
material1.Specular.Set(FbxDouble3(0.0, 0.0, 0.25))
material1.SpecularFactor.Set(0.0122)
#material1.Shininess.Set()
#material1.Ambient.Set()
material1.AmbientFactor.Set(1.0)
#material1.Emissive.Set()
material1.EmissiveFactor.Set(0.00001)
material1.Reflection.Set(FbxDouble3(0.8, 0.8, 0.85))


# FbxSurfaceLambert material
material2 = FbxSurfaceLambert.Create(lSdkManager, "Material_Lambert")
material2.Diffuse.Set(FbxDouble3(0.0, 1.0, 0.0))
material2.DiffuseFactor.Set(0.4)
material2.Ambient.Set(0.3)
material2.AmbientFactor.Set(1.0)
material2.Emissive.Set(FbxDouble3(1.3, 1.3, 1.3) )
material2.EmissiveFactor.Set(0.00001)



fbx_node.AddMaterial( material1 )
fbx_node.AddMaterial( material2 )


# assign layers
layer = fbx_mesh.GetLayer(0)
if layer == None:
    fbx_mesh.CreateLayer()
    layer  = fbx_mesh.GetLayer(0)
                       
layer.SetNormals(fbx_normal)
layer.SetUVs(fbx_tex_uv, FbxLayerElement.eTextureDiffuse)
layer.SetMaterials(fbx_material)



#================ Add polygon 1 ===================//
fbx_mesh.BeginPolygon(-1, -1, -1)

# assign material
fbx_material.GetIndexArray().SetAt(0, 1)


# assign vertex indices
fbx_mesh.AddPolygon(0)
fbx_mesh.AddPolygon(1)
fbx_mesh.AddPolygon(2)

fbx_mesh.EndPolygon()



#============== Add polygon 2 =====================//
fbx_mesh.BeginPolygon(-1, -1, -1)

# assign material
fbx_material.GetIndexArray().SetAt(1, 0)


# assign vertex indices
fbx_mesh.AddPolygon(3)
fbx_mesh.AddPolygon(0)
fbx_mesh.AddPolygon(2)

fbx_mesh.EndPolygon()



# print
print( "num polygons:", fbx_mesh.GetPolygonCount())
print( "num verts:", fbx_mesh.GetControlPointsCount())



# set node attributes to FbxNode
print("Add FbxMesh to FbxNode....")
fbx_node.SetNodeAttribute(fbx_mesh)

#print( "attribute type: ", fbx_node.GetNodeAttribute().GetAttributeType())


lScene.GetRootNode().AddChild(fbx_node)


FbxCommon.SaveScene(lSdkManager, lScene, "d:\\test.fbx", 1)