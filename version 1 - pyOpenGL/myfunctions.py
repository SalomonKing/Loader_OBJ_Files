import sys, os
from PyQt4 import QtGui, QtCore, uic
#import numpy as np
import Image
from PyQt4.QtOpenGL import *
from OpenGL.GL import *
#from OpenGL.GLU import *

class OBJ(object):
  def __init__(self, filename):
    vertexs = []  
    normals = []
    tcoords = []
    colors = []
    
    faces_vertexs = []
    faces_normals = []
    faces_tcoords = []
    face_colors   = []
    npoligons     = 0
      
    ## load materials
    color_temp = [0.0,0.0,0.0]
    colorObj = open(filename + '.mtl', "r")   
    materiales = {}   
    for line in colorObj:     
        cline = line.split()
        if len(cline) > 0:         
            if cline[0] == 'newmtl':
                material = cline[1]
            if cline[0] == 'Kd':
                color  =  map(float,cline[1:4])
                materiales[material] = color  
      
    ## load mesh data   
    fileobj = open(filename + '.obj', "r") 
    for line in fileobj:       
        vals = line.split()       
        if vals[0] == "v":  
            v = map(float, vals[1:4])
            vertexs.append(v)

        if vals[0] == "vt":
            t = map(float, vals[1:3])
            tcoords.append(t)
            
        if vals[0] == "vn":  
            n = map(float, vals[1:4])  
            normals.append(n)
           
        if vals[0] == 'usemtl':
            color_temp = materiales[vals[1]]             
        if vals[0] == 'f':
            
            for v in vals[1:]:
                v = v.split('/')
                faces_vertexs.extend(vertexs[int(v[0])-1])            
                faces_tcoords.extend(tcoords[int(v[1])-1])             
                faces_normals.extend(normals[int(v[2])-1])
                face_colors.extend(color_temp)
                

    npoligons = len(faces_vertexs) / 3

    # convert to OpenGL / ctypes arrays:
    faces_vertexs = (GLfloat * len(faces_vertexs))(*faces_vertexs)
    faces_normals = (GLfloat * len(faces_normals))(*faces_normals)   
    faces_tcoords = (GLfloat * len(faces_tcoords))(*faces_tcoords)   
    face_colors =  (GLfloat * len(face_colors))(*face_colors)
    
    # build the list
    self.list = glGenLists(1)
    glNewList(self.list, GL_COMPILE)

    glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
    
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)    
    glEnableClientState(GL_COLOR_ARRAY)
    
    glVertexPointer(3, GL_FLOAT, 0, faces_vertexs)
    glNormalPointer(GL_FLOAT, 0, faces_normals)   
    glColorPointer(3,GL_FLOAT,0, face_colors)
    glTexCoordPointer(2,GL_FLOAT,0,faces_tcoords)
    
    glDrawArrays(GL_TRIANGLES,0,npoligons)
    
    glPopClientAttrib()    
    glEndList()
    
  def Draw(self):
    glCallList(self.list)
