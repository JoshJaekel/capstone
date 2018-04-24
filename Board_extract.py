import cv2
from matplotlib import pyplot as plt
import numpy as np

def find_interection(line1,line2):
	p1 = line1[0]
	theta1 = line1[1]
	p2 = line2[0]
	theta2 = line2[1]
	
	m1=-(np.cos(theta1)/np.sin(theta1))
	m2=-(np.cos(theta2)/np.sin(theta2))
	b1=p1/np.sin(theta1)
	b2=p2/np.sin(theta2)
	x=(b2-b1)/(m1-m2)

	y=m1*x+b1

	return (x,y)
def length(p1,p2):
	return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def find_board_edges(corners):
	p1 = corners[0]
	p2 = corners[1]
	p3 = corners[2]
	p4 = corners[3]

	return max (length(p1,p2),length(p1,p3),length(p2,p4),length(p3,p4))
	


img = cv2.imread('red_centered.png')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_red = np.array([-10,100,100])
upper_red = np.array([10,255,255])
    
mask = cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(img,img, mask= mask)

edges=cv2.Canny(mask, 100,200)



old_lines = cv2.HoughLines(edges,1,np.pi/180,180)


thresh1=25
thresh2=0.1

lines=old_lines[0]

to_delete=[]
for index,line in enumerate(lines):
	for index_2 in range(index+1, len(lines)):
		if ((abs(line[0]-lines[index_2][0])<thresh1) and (abs(line[1]-lines[index_2][1])<thresh2)):
			line[0]=(line[0]+lines[index_2][0])/2
			line[1]=(line[1]+lines[index_2][1])/2
			to_delete.append(index_2)

new_lines=np.delete(lines,list(set(to_delete)),axis=0)


horz=[]
vert=[]

for line in new_lines:
	if abs(np.sin(line[1]))>0.5:
		vert.append((line[0],line[1]))
	else:
		horz.append((line[0],line[1]))

print horz
print vert 

corners=[]

for hor_line in horz:
	for vert_line in vert:
		corners.append(find_interection(hor_line,vert_line))
print corners

for point in corners:
	cv2.circle(img,point,5,thickness=5,color=1)




# for rho,theta in new_lines[0]:
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*rho
#     y0 = b*rho
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))

#     cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()


image_side_length = find_board_edges(corners)



