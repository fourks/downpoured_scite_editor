
others='''
#import abaqus
!import ada
!import asm
#import asn1
#import au3
!import ave
!import baan
#import freebasic
#import blitzbasic
#import bullant
!import caml
!import conf
#import cobol
import cpp
#import cmake
#import csound
import css
!import d
!import eiffel
!import erlang
!import escript
#import flagship
#import forth
!import fortran
#import gap
import html
#import inno
#import kix
import lisp
!import lot
#import lout
!import lua
!import matlab
!import metapost
!import mmixal
#import modula3
#import nimrod
#import nncrontab
#import nsis
#import opal
import others
!import pascal
!import perl
!import pov
#import powerpro
#import powershell
!import ps
#import purebasic
import python
#import r
#import rebol
import ruby
#import scriptol
#import smalltalk
#import spice
!import sql
#import specman
#import tacl
#import tal
!import tcl
#import txt2tags
!import tex
!import vb
!import yaml
#import verilog
#import vhdl
'''
import sys; sys.path.append(r'C:\pydev\dev\downpoured_scite_editor\tools\python_printval'); from printval import *
fe=open('others_enabled.properties', 'w')
fd=open('others_disabled.properties', 'w')
for item in others.split('\n'):
    item=item.strip()
    if not item: continue
    gooditem = item.replace('#','').replace('!','').replace('import ','')+'.properties'
    if item.startswith('#'):
        fd.write('##########============================================================\n')
        fd.write('##%s\n'%gooditem)
        fd.write('##########============================================================\n')
        fd.write(readfile(gooditem))
        fd.write('\n\n')
        print 'deleting ',gooditem
        os.unlink(gooditem)
    elif item.startswith('!'):
        fe.write('##########============================================================\n')
        fe.write('##%s\n'%gooditem)
        fe.write('##########============================================================\n')
        fe.write(readfile(gooditem))
        fe.write('\n\n')
        os.unlink(gooditem)
        print 'deleting ',gooditem
    else:
        print 'saving ',item

fe.close()
fd.close()
