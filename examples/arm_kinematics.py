"""
This code is intended as an example for the use of the generalized screw formalism in general and the GScrew package in particular. It provides a numerical solution to the forward kinematics of a robotic arm, composed of a number of successive revolute joints.
"""

import numpy as np
import gscrew
from gscrew.geometric_algebra import GeometricAlgebra
from gscrew.screw import CoScrew

algebra = GeometricAlgebra(3) # create a 3D geometric algebra
locals().update(algebra.blades) # create the GA canonical basis

O = 0 * s  # the origin of the reference frame

# Setting the arm geometry

nb_joints = 6 # number of revolute joints in the arm
end_effector = 40*e3 # position of the end effector
rotation_centers = np.array([10*e3, 10*e3, 20*e3, 30*e3, 30*e3, 30*e3]) # positions of the revolute joints in the reference frame and canonical basis
rotation_planes = np.array([e12, - e13, - e13, e12, - e13, e12]) # unit bivectors representing the oriented planes of rotation

# Setting the motion parameters

rotation_angles = np.array([0, 90, 0, 90, 45, 0]) * np.pi/180 # rotation angles in radians

# Creating the joint comotors

joint_comotors = [] # list of comotors associated with the joints

for index in range(nb_joints):
    resultant = np.cos(rotation_angles[index]/2) + np.sin(rotation_angles[index]/2) * rotation_planes[index] # rotor representing the indexed rotation
    comotor = CoScrew(rotation_centers[index], resultant, 0*s) # comotor representing the indexed motion
    joint_comotors.append(comotor)

# Computing the total motion

total_comotor = joint_comotors[-1] # initialization of the total motion's comotor

for index in range(1, nb_joints-1):
    total_comotor = total_comotor.composition(joint_comotors[nb_joints - index - 1])

# Extracting the results

total_rotor = total_comotor.resultant
print(f"total rotor = {total_rotor}")

total_comotor.change_point(O)
total_translation = total_comotor.moment # total translation at the origin

final_position = ~total_rotor * end_effector * total_rotor + 2 * ~total_rotor * total_translation # final position of the end effector
print(f"final position = {final_position(1)}") # eliminate the small pseudoscalar component, due to numerical error
