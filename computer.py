    # -*- coding: utf-8 -*-

############################################################################
#import all libraries

#Math libraries
import numpy as np
from sympy import *
init_printing(use_latex=true, wrap_line=true)
from sympy.vector import *
import sympy.functions.elementary.complexes as sym
from sympy.physics.vector import vlatex
from math import *
import mpmath
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
import ast
import getpass

import os
import platform
import os.path
import glob
import re
import shutil
import sys
sys.setrecursionlimit(100000)


import subprocess



############################################################################
def calcul_algo():

    def Build_Matrix():
        Tab = np.chararray((nb_tensors,3, 3),itemsize=12,unicode=True)
        k=0
        for n in range (0,nb_tensors):
            for i in range (0,3):
                for j in range (0,3):
                    Tab[n,i,j]=Str_Tab[i,j+k]

            k+=3

        for i in range(0,nb_tensors):

            globals()['tensor_'+str(i)]= Matrix([[sympify(Tab[i,0,0]),sympify(Tab[i,0,1]),sympify(Tab[i,0,2])],[sympify(Tab[i,0+1,0]),sympify(Tab[i,0+1,1]),sympify(Tab[i,0+1,2])],[sympify(Tab[i,0+2,0]),sympify(Tab[i,0+2,1]),sympify(Tab[i,0+2,2])]])
            #print(globals()['tensor_'+str(i)])

    def Build_Pointing():

        if pointing_vector == "a = (1,0,0)":
            pointing = Matrix([1,0,0])
        if pointing_vector == "b = (0,1,0)":
            pointing = Matrix([0,1,0])
        if pointing_vector == "c = (0,0,1)":
            pointing = Matrix([0,0,1])

        #print(pointing)
        
        if pointing_vector == "Other":
            x=float(pointing_vector_x)
            y=float(pointing_vector_y)
            z=float(pointing_vector_z)
            pointing= Matrix([x,y,z])
        
        return pointing

    def Build_Crystal():

        if ref_axis == "a = (1,0,0)":
            crystal = Matrix([1,0,0])
        if ref_axis == "b = (0,1,0)":
            crystal = Matrix([0,1,0])
        if ref_axis == "c = (0,0,1)":
            crystal = Matrix([0,0,1])
        
        if ref_axis == "Other":
            x=float(ref_axis_x)
            y=float(ref_axis_y)
            z=float(ref_axis_z)
            crystal= Matrix([x,y,z])
       
        return crystal

    def verifypointing(pointing,crist_axis) :
        scalar = pointing.dot(crist_axis)
        bool = True
        try:
            scalar
            assert scalar == 0
        except AssertionError:
            bool = False
            return bool
        finally :
            return bool


    def Rotate(polar,theta_d):

        #theta= (theta_d*pi)/180
        theta = radians(theta_d)

        if pointing_vector == "a = (1,0,0)":
            mat_rot =  rot_axis1(theta)
            #print(mat_rot)
        elif pointing_vector == "b = (0,1,0)":
            mat_rot =  rot_axis2(theta)
        elif pointing_vector == "c = (0,0,1)":
            mat_rot =  rot_axis3(theta)
        
        elif pointing_vector == "Other" :
            ct = cos(theta)
            st = sin(theta)
            pointing= Build_Pointing()
            ux = pointing[0]
            uy = pointing[1]
            uz = pointing[2]

            lil = ((ux*ux*(1-ct)+ct, ux*uy*(1-ct)-uz*st , ux*uz*(1-ct)+uy*st),
                    (ux*uy*(1-ct)+uz*st, uy*uy*(1-ct)+ct, uy*uz*(1-ct)-ux*st),
                    (ux*uz*(1-ct)-uy*st, uy*uz*(1-ct)+ux*st, uz*uz*(1-ct)+ct))

            #lil = ((ux*ux- ux*ux*ct+ct, ux*uy-ux*uy*ct-uz*st, ux*uz-ux*uz*ct+uy*st),
                #   (ux*uy-ux*uy*ct+uz*st, uy*uy-uy*uy*ct+ct, uy*uz-uy*uz*ct-ux*st),
                    #  (ux*uz-ux*uz*ct-uy*st, uy*uz-uy*uz*ct+ux*st, uz*uz-uz*uz*ct+ct))
            mat_rot = Matrix(lil)
    
        #print(mat_rot*polar)
        return mat_rot*polar

    def Calcul_coeff(P_in,P_out):
        resultats = ""
        Tab = np.chararray((nb_tensors),itemsize=100,unicode=True)
        #print(Tab)
        for i in range(0,nb_tensors):

            a = simplify(abs(adjoint(P_out)*eval('tensor_{}'.format(str(i)))*P_in)**2)
            
            test_0= str(a[0,0])
            #print("avant",test_0)
            index_test_0 = test_0.find("e-")
            if index_test_0 != -1:
                test_0=test_0.replace("e-","*0*")
                #a = Matrix([0])
            #b=str(simplify(N(a[0,0],5)))
            b=str(simplify(N(test_0,5)))
            Tab[i] = b
            #print("après",test_0)
            #print("simplifié",b)
            #resultats+= b
            #if i < nb_tensors-1:
             #   resultats+= "\t"
        
        res_tab = sympify(Tab)
       
        return res_tab
    
 
    #get parameter from UI
    space_group = sys.argv[1]
    pointing_vector = sys.argv[2]
    ref_axis = sys.argv[3]
    polar_in = sys.argv[4]
    polar_out = sys.argv[5]
    angle = sympify(sys.argv[6])

    pointing_vector_x = sys.argv[7]
    pointing_vector_y = sys.argv[8]
    pointing_vector_z = sys.argv[9]

    ref_axis_x = sys.argv[10]
    ref_axis_y = sys.argv[11]
    ref_axis_z = sys.argv[12]

    database = sys.argv[13]
    point_group_str=""

    if (database == "Loudon"):
        point_group_str = "Point_Group_Loudon"
    elif (database == "Bilbao"):
        point_group_str = "Point_Group_Bilbao"
    
    #get database path
    path = os.getcwd()
    test_str=path
    if platform.system() == 'Windows':
        test_str+= "\\public\\db\\"
        test_str+= point_group_str 
        test_str+= "\\"
    else:
        test_str+="/public/db/"
        test_str+=point_group_str
        test_str+="/"

    full_name = test_str + space_group + ".txt"

    #load database matrix
    Str_Tab = np.loadtxt(full_name,dtype='str')
    length = Str_Tab.shape[1]
    nb_tensors=int(length/3)
    Build_Matrix()

    #build pointing vector
    pointing= Build_Pointing()
    #build ref axis
    crist_axis = Build_Crystal()

    if verifypointing(pointing,crist_axis)==False:
        print("true")
        return
    else:
        print("false")
    #build polar ref
    vec_global_V = crist_axis/crist_axis.norm()
    #print(vec_global_V)
    vec_global_H_temp = vec_global_V.cross(pointing)
    vec_global_H = vec_global_H_temp/vec_global_H_temp.norm()

    R_c= 1/sqrt(2)*Matrix([1,-I,0])
    L_c = 1/sqrt(2)*Matrix([1,I,0])
    
    crs=  Matrix([0,0,1])

    A = CoordSys3D('A')

    v_pointing = matrix_to_vector(pointing,A)
    v_crs= matrix_to_vector(crs,A)

    alpha = acos((crs.dot(pointing))/(crs.norm()*pointing.norm()))
    B = A.orient_new_axis('B',alpha,pointing[0]*A.i + pointing[1]*A.j +pointing[2]*A.k)

    Rot_point = B.rotation_matrix(A)


    #definition of symbolic variables
    a, b, d, c, e ,f ,g ,h ,i = symbols('a b d c e f g h i')
    theta = symbols('theta')
    
    #build true circular polar
    if pointing_vector == "a = (1,0,0)":
        vec_4 = 1/sqrt(2)*Matrix([0,1,-I])
        vec_5 = 1/sqrt(2)*Matrix([0,1,I])
    elif pointing_vector == "b = (0,1,0)":
        vec_4 = 1/sqrt(2)*Matrix([1,0,-I])
        vec_5 = 1/sqrt(2)*Matrix([1,0,I])
    elif pointing_vector == "c = (0,0,1)":
        vec_4 = 1/sqrt(2)*Matrix([1,-I,0])
        vec_5 = 1/sqrt(2)*Matrix([1,I,0])
    
    elif pointing_vector == "Other":
        vec_4 = Rot_point*R_c
        vec_5 = Rot_point*L_c
    

    #Definition of in/out polarisations with respect to user choice & angle
    #using global polarisations

    if polar_in == "Vertical" and  angle== 0.:
        vec_temp_1 = vec_global_V
        In_polar = polar_in[0]
    elif polar_in == "Vertical"  and  angle != 0.:
        vec_temp_1 = Rotate(vec_global_V,angle)
        In_polar = polar_in[0] + "_{" +str(angle) +"}"
    elif polar_in == "Horizontal"  and  angle== 0.:
        vec_temp_1 = vec_global_H
        In_polar = polar_in[0]
    elif polar_in == "Horizontal"  and  angle != 0.:
        vec_temp_1 = Rotate(vec_global_H,angle)
        In_polar = polar_in[0] + "_{" +str(angle) +"}"

    elif polar_in == "Circular Right":
        vec_temp_1 = vec_4
        In_polar = "R"
    elif polar_in == "Circular Left":
        vec_temp_1 = vec_5
        In_polar= "L"

    if polar_out == "Vertical" and  angle== 0.:
        vec_temp_2 = vec_global_V
        Out_polar = polar_out[0]
    elif polar_out == "Vertical"  and  angle != 0.:
        vec_temp_2 = Rotate(vec_global_V,angle)
        Out_polar = polar_out[0] + "_{" +str(angle) +"}"
    elif polar_out == "Horizontal"  and  angle== 0.:
        vec_temp_2 = vec_global_H
        Out_polar = polar_out[0]
    elif polar_out == "Horizontal"  and  angle != 0.:
        vec_temp_2 = Rotate(vec_global_H,angle)
        Out_polar = polar_out[0]  + "_{" +str(angle) +"}"

    elif polar_out == "Circular Right":
        vec_temp_2 = vec_4
        Out_polar = "R"
    elif polar_out == "Circular Left":
        vec_temp_2 = vec_5
        Out_polar = "L"

    
    if( pointing_vector == "Other"):
        In_vector = "(" + pointing_vector_x +"," + pointing_vector_y + "," + pointing_vector_z + ")"
        Out_vector =  "(-" + pointing_vector_x +", -" + pointing_vector_y + ", -" + pointing_vector_z + ")"
    else:  
        In_vector=pointing_vector[0] 
        Out_vector = "-" + In_vector
    config=In_vector+"("+Out_polar+","+In_polar+")"+Out_vector + " &"

    print(config)
    resultats_str = Calcul_coeff(vec_temp_1,vec_temp_2)
    resultats = latex(sympify(resultats_str))
    print(resultats)
 
    #print(vec_temp_1,vec_temp_2)

############################################################################
if __name__ == "__main__":
 
    
    calcul_algo()