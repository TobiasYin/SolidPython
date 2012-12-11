#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys, os

from solid import *

# Import OpenSCAD code and call it from Python code.
# Note that the path given to use() (or include())    
# needs to be absolute to be robust
# must either be absolute or relative to the directory
# this python file is run from.
def demo_scad_include():
    abs_path = os.path.abspath( os.path.join( os.curdir, 'scad_to_include.scad'))
    use( abs_path)
    
    # scad_to_include.scad includes a module called steps()
    # use( "./scad_to_include.scad") #  could also use 'include', but that has side-effects
    return steps(5)


if __name__ == '__main__':    
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'scad_include_example.scad')
    
    a = demo_scad_include()
    
    print "%(__file__)s: SCAD file written to: %(file_out)s \n"%vars()
    
    scad_render_to_file( a, file_out)  