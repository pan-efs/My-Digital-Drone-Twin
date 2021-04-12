from joints_dataframe import JointsDataframe
from joints_numpys import JointsNumpys
from joints_list import JointsList
from filters.digital_filter import DigitalFilter
from biomechanics.biomechanics3D import AngularKinematics, Magnitude, Cadence
from matplotlib import pyplot as plt
import numpy as np

# Starting point
jDF = JointsDataframe().__repr__()
jNps = JointsNumpys().__repr__()

jl = JointsList()
jLs = jl.__repr__()

joints = []

for i in range(0, len(jLs), 3):
    x = jl._converter_to_list(jLs[i], jLs[i+1], jLs[i+2])
    joints.append(x)

ur8, ur9, ur10 = jl._get_same_length(joints[8], joints[9], joints[10])
ur11, ur12, ur13 = jl._get_same_length(joints[11], joints[12], joints[13])

a = AngularKinematics()

# Calculate theta angle for right knee (unfiltered coordinates)
un_theta_right, un_theta_left = ([] for i in range(2))
for i in range(0, len(ur8) - 1):
    un_th_right = a.calculate_3d_angle(np.asarray(ur8[i]), np.asarray(ur9[i]), np.asarray(ur10[i]))
    un_theta_right.append(un_th_right)

# Calculate theta angle for left knee (unfiltered coordinates)
for i in range(0, len(ur11) - 1):
    un_th_left = a.calculate_3d_angle(np.asarray(ur11[i]), np.asarray(ur12[i]), np.asarray(ur13[i]))
    un_theta_left.append(un_th_left)

# Visualize right and left knee angle (unfiltered data)
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.plot(un_theta_right)
ax1.set_title('Knee Right (unfiltered)')
ax1.set(xlabel = 'Frames', ylabel = 'Knee angle (degrees)')

ax2.plot(un_theta_left)
ax2.set_title('Knee Left (unfiltered)')
ax2.set(xlabel = 'Frames', ylabel = 'Knee angle (degrees)')

plt.show()

f = DigitalFilter()
# BW
z8x, z2_8x, y8x = f.digital_filter(jLs[24], 3)
z8y, z2_8y, y8y = f.digital_filter(jLs[25], 3)
z8z, z2_8z, y8z = f.digital_filter(jLs[26], 3)

z9x, z2_9x, y9x = f.digital_filter(jLs[27], 3)
z9y, z2_9y, y9y = f.digital_filter(jLs[28], 3)
z9z, z2_9z, y9z = f.digital_filter(jLs[29], 3)

z10x, z2_10x, y10x = f.digital_filter(jLs[30], 3)
z10y, z2_10y, y10y = f.digital_filter(jLs[31], 3)
z10z, z2_10z, y10z = f.digital_filter(jLs[32], 3)

z11x, z2_11x, y11x = f.digital_filter(jLs[33], 3)
z11y, z2_11y, y11y = f.digital_filter(jLs[34], 3)
z11z, z2_11z, y11z = f.digital_filter(jLs[35], 3)

z12x, z2_12x, y12x = f.digital_filter(jLs[36], 3)
z12y, z2_12y, y12y = f.digital_filter(jLs[37], 3)
z12z, z2_12z, y12z = f.digital_filter(jLs[38], 3)

z13x, z2_13x, y13x = f.digital_filter(jLs[39], 3)
z13y, z2_13y, y13y = f.digital_filter(jLs[40], 3)
z13z, z2_13z, y13z = f.digital_filter(jLs[41], 3)

# Create lists with x,y,z coords together (filtered BW coordinates)
arr8, arr9, arr10, arr11, arr12, arr13 = ([] for i in range(6))

for i in range(0, len(y8x) - 1):
    a8 = [y8x[i], y8y[i], y8z[i]]
    arr8.append(a8)

for i in range(0, len(y9x) - 1):   
    a9 = [y9x[i], y9y[i], y9z[i]]
    arr9.append(a9)

for i in range(0, len(y10x) - 1):
    a10 = [y10x[i], y10y[i], y10z[i]]
    arr10.append(a10)

for i in range(0, len(y11x) - 1):
    a11 = [y11x[i], y11y[i], y11z[i]]
    arr11.append(a11)

for i in range(0, len(y12x) - 1):
    a12 = [y12x[i], y12y[i], y12z[i]]
    arr12.append(a12)

for i in range(0, len(y13x) - 1):
    a13 = [y13x[i], y13y[i], y13z[i]]
    arr13.append(a13)

# Get the same length (filtered BW coordinates) 
r8, r9, r10 = jl._get_same_length(arr8, arr9, arr10)
r11, r12, r13 = jl._get_same_length(arr11, arr12, arr13)

# Calculate theta angle for right knee (filtered BW coordinates)
theta_right, theta_left = ([] for i in range(2))
for i in range(0, len(r8)):
    th_right = a.calculate_3d_angle(np.asarray(r8[i]), np.asarray(r9[i]), np.asarray(r10[i]))
    theta_right.append(th_right)

# Calculate theta angle for left knee (filtered BW coordinates)
for i in range(0, len(r11)):
    th_left = a.calculate_3d_angle(np.asarray(r11[i]), np.asarray(r12[i]), np.asarray(r13[i]))
    theta_left.append(th_left)
    
# Visualize right and left knee angle (filtered data)
fig, (ax3,ax4) = plt.subplots(1,2)
ax3.plot(theta_right)
ax3.set_title('Knee Right BW')
ax3.set(xlabel = 'Frames', ylabel = 'Knee angle (degrees)')

ax4.plot(theta_left)
ax4.set_title('Knee Left BW')
ax4.set(xlabel = 'Frames', ylabel = 'Knee angle (degrees)')

plt.show()

####################################
### Calculate cadence of cycling ###
####################################
m_rk = Magnitude(arr9)
m_ak = Magnitude(arr12)

# Knees are more reliable instead of ankle
mg_rk = m_rk.calculate_magnitude()
mg_ak = m_ak.calculate_magnitude()

c_rk = Cadence(mg_rk)
c_ak = Cadence(mg_ak)

plt.plot(arr9)
plt.plot(arr12)
plt.show()

max_rk, min_rk = m_rk.find_visualize_local_max_min('KR, BW, Cycling', True)
cadence_rk, duration_rk = c_rk.calculate_cadence(max_rk)

max_ak, min_ak = m_ak.find_visualize_local_max_min('KL, BW, Cycling', True)
cadence_ak, duration_ak = c_ak.calculate_cadence(max_ak)

print("="*40, 'Local max-min of right knee', "="*40)
print('.'*10, "="*30, 'max: ', max_rk, '='*30, '.'*10)
print('.'*10, "="*30, 'min: ', min_rk, '='*30, '.'*10)
print('.'*10, "="*30, 'time: ', duration_rk, 'sec', '='*30, '.'*10)
print('.'*10, "="*30, 'RPM: ', cadence_rk, '='*30, '.'*10)

print("="*40, 'Local max-min of left knee', "="*40)
print('.'*10, "="*30, 'max: ', max_ak, '='*30, '.'*10)
print('.'*10, "="*30, 'min: ', min_ak, '='*30, '.'*10)
print('.'*10, "="*30, 'time: ', duration_ak, 'sec', '='*30, '.'*10)
print('.'*10, "="*30, 'RPM: ', cadence_ak,'='*30, '.'*10)
