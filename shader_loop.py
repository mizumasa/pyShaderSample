#!/usr/local/bin python
import numpy as np
import sys
import time
from PIL import Image
import math
import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# PyOpenGL 3.0.1 introduces this convenience module...
from OpenGL.GL.shaders import *

vertices = None
indices = None
program = None
startTime = 0.

def InitGL( vertex_shade_code, fragment_shader_code,w_size):
    glClearColor(0.0, 0.0, 0.0, 0.0)

    texture_id = glGenTextures( 1 )
    glPixelStorei( GL_UNPACK_ALIGNMENT, 1 )
    glActiveTexture( GL_TEXTURE0 )
    glBindTexture( GL_TEXTURE_2D, texture_id )

    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )

    global program
    program = compileProgram(
        compileShader( vertex_shade_code,GL_VERTEX_SHADER),
        compileShader( fragment_shader_code,GL_FRAGMENT_SHADER),)
    glUseProgram(program)
    glUniform1f( glGetUniformLocation( program, "texture_width" ), float( w_size[ 0 ] ) )
    glUniform1f( glGetUniformLocation( program, "texture_height" ), float( w_size[ 1 ] ) )

    global startTime
    startTime = time.time()
    global vertices
    global indices
    position_vertices = [ -1.0,  1.0, 0.0,
                          -1.0, -1.0, 0.0,
                           1.0, -1.0, 0.0,
                           1.0,  1.0, 0.0, ]
    texture_vertices = [ 0.0, 0.0,
                         0.0, w_size[ 1 ],
                         w_size[ 0 ], w_size[ 1 ],
                         w_size[ 0 ], 0.0 ]

    indices = [ 0, 1, 2, 0, 2, 3 ]

    position_loc = glGetAttribLocation( program, 'a_position' )
    glVertexAttribPointer( position_loc,
                           3,
                           GL_FLOAT,
                           GL_FALSE,
                           3 * 4,
                           np.array( position_vertices, np.float32 ) )

    tex_loc = glGetAttribLocation( program, 'a_texCoord' )
    glVertexAttribPointer( tex_loc,
                           2,
                           GL_FLOAT,
                           GL_FALSE,
                           2 * 4,
                           np.array( texture_vertices, np.float32 ) )
    glEnableVertexAttribArray( position_loc )
    glEnableVertexAttribArray( tex_loc )
    glUniform1f( glGetUniformLocation( program, "time" ), time.time() - startTime)

def ReSizeGLScene(Width, Height):
    glViewport(0, 0, Width, Height)

# The main drawing function.
def DrawGLScene():
    glUniform1f( glGetUniformLocation( program, "time" ), time.time() - startTime)
    #print "time",time.time() - startTime
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_TEXTURE_2D)
    glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_SHORT, np.array( indices, np.uint16 ) )
    glDisable(GL_TEXTURE_2D)
    glutSwapBuffers()

def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == '\x1b':
        data = glReadPixels(0, 0, 500, 500, GL_RGBA, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (500, 500), data)
        image.save("output.png")
        sys.exit()

def usage():
    print "usage:%s vertex_shader_file fragment_shader_file" % sys.argv[ 0 ]

def main():
    try:
        vertex_shader_file = sys.argv[ 1 ]
        fragment_shader_file = sys.argv[ 2 ]
    except IndexError:
        usage()
        sys.exit( -1 )
    vertex_shade_code = '\n'.join( open( vertex_shader_file, 'r' ).readlines() )
    fragment_shader_code = '\n'.join( open( fragment_shader_file, 'r' ).readlines() )
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

    window_width,window_height = (800,800)
    glutInitWindowSize( window_width, window_height )
    glutInitWindowPosition(0, 0)
    glutCreateWindow( sys.argv[ 0 ] )
    glutDisplayFunc(DrawGLScene)
    #glutFullScreen()
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL( vertex_shade_code, fragment_shader_code, ( window_width, window_height ) )
    glutMainLoop()

if __name__ == "__main__":
    print "Hit ESC key to quit."
    main()