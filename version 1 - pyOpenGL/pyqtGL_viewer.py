# -*- coding: utf-8 -*-
from myfunctions import *

# load image
image = Image.open('marble.bmp')	
imag_X = image.size[0]
imag_Y = image.size[1]
imag_data  = image.tostring("raw", "RGBX",0,-1)

def vec(*args): return (GLfloat * len(args))(*args)
        
class Viewer3DWidget(QGLWidget):
    
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.ang    = 0
        self.texID  = 0

    def paintGL(self):      
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)      
        glEnable(GL_LIGHT0);
        
        glEnable(GL_COLOR_MATERIAL);        
        glLoadIdentity()
        glMatrixMode( GL_MODELVIEW );       
        self.draw()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_COLOR_MATERIAL);
        glDisable(GL_LIGHT0);
        
        
        glFlush()
        
    def draw(self):
        glOrtho(-2,2,-1,1,-1,1)

        glPushMatrix()
        glTranslatef(-1.0,0.0,0.0)
        glRotated(self.ang,0,1,0)      
        self.modelo1.Draw()
        glPopMatrix()

        glEnable(GL_TEXTURE_2D);
        
        glPushMatrix()
        glTranslatef(1.0,0.0,0.0)
        glRotated(self.ang,0,1,0)    
        self.modelo2.Draw()
        glPopMatrix()

        
        
    def resizeGL(self, widthInPixels, heightInPixels):
        glViewport(0, 0, widthInPixels, heightInPixels)       

    def initializeGL(self):
        glClearColor(0.8, 0.8, 0.8, 1.0)
        
        glClearDepth(1.0)
        
        ## load model
        self.modelo1 = OBJ('pato')
        self.modelo2 = OBJ('monkey')
        
        ## lighting        
        glEnable(GL_LIGHTING)       
        ambientLight  = vec( 0.4, 0.4, 0.4, 1.0 )
        diffuseLight  = vec( 1.0, 1.0, 1.0, 1.0 )
        specularLight = vec( 1.0, 1.0, 1.0, 1.0 )
        lightPos = vec( -5.0, 0.0, -5.0, 1.0 )        
        glLightfv(GL_LIGHT0, GL_AMBIENT,  ambientLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE,  diffuseLight)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specularLight)    
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

        # Texture        
        glEnable(GL_TEXTURE_2D);
        glBindTexture(GL_TEXTURE_2D, self.texID) 
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, imag_X, imag_Y, 0, GL_RGBA, GL_UNSIGNED_BYTE, imag_data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glGenerateMipmap(GL_TEXTURE_2D)
        
         
class MainApp(QtGui.QMainWindow):
   def __init__(self):
      QtGui.QMainWindow.__init__(self)
      self.ui = uic.loadUi('OpenGLViewer.ui')
      self.viewer3D = Viewer3DWidget(self)
      self.ui.OpenGLLayout1.addWidget( self.viewer3D );
      self.ui.show()      
      self.timer = QtCore.QTimer()
      self.timer.start() 
      self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.Timer1_actualizar)
      
           
   def Timer1_actualizar(self):
       self.viewer3D.ang += 1
       if(self.viewer3D.ang > 360):
           self.viewer3D.ang = 0
       self.viewer3D.updateGL()  
    
if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   win = MainApp()
   sys.exit(app.exec_())
