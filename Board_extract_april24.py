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

def find_board_edge_size(corners):
	p1 = corners[0]
	p2 = corners[1]
	p3 = corners[2]
	p4 = corners[3]

	return max (length(p1,p2),length(p1,p3),length(p2,p4),length(p3,p4))

def findExtremeCorners(corners):
	lengths=[]
	xvalues=[]
	for index, point in enumerate(corners):
		length=np.sqrt(point[0]**2+point[1]**2)
		lengths.append((length,index))

	max_len=max(lengths[0][0],lengths[1][0],lengths[2][0],lengths[3][0])
	min_len=min(lengths[0][0],lengths[1][0],lengths[2][0],lengths[3][0])
	for point in lengths:
		if max_len==point[0]:
			bottom_right=point[1]

		elif min_len==point[0]:
			top_left=point[1]
	for index,x in enumerate(corners):
		if (index!=top_left and index!=bottom_right):
			xvalues.append((x[0],index))
	minx=min(xvalues[0][0],xvalues[1][0])
	for point in xvalues:
		if minx==point[0]:
			bottom_left=point[1]
		else:
			top_right=point[1]


	return top_left,top_right,bottom_left,bottom_right

def findHoughlines(mask):
	edges=cv2.Canny(mask, 100,200)

	thresh=120
	
	while (True):

		old_lines = cv2.HoughLines(edges,1,np.pi/180,thresh)


		lines=old_lines[0]

		for index,line in enumerate(lines):
			for index_2 in range(index+1, len(lines)):
				if ((abs(line[0]-lines[index_2][0])<thresh1) and (abs(line[1]-lines[index_2][1])<thresh2)):
					line[0]=(line[0]+lines[index_2][0])/2
					line[1]=(line[1]+lines[index_2][1])/2
					to_delete.append(index_2)

		new_lines=np.delete(lines,list(set(to_delete)),axis=0)
		if (len(new_lines))==4:
			break
		else:
			thresh=thresh+10
		if (thresh==180):
			print "Your image sucks"
			break

	return new_lines

def extract_squares(warped):
	l,w,_=warped.shape
	images=[]

	for vertical in range(8):
		for horizontal in range(8):
			images.append(cv2.cvtColor(cv2.getRectSubPix(warped,(int(l/8),int(w/8)),((l/16)+horizontal*(l/8),(w/16)+vertical*(w/8))),cv2.COLOR_BGR2GRAY))

	return images


img = cv2.imread('fixed_cam_new1.png')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_red = np.array([-10,100,100])
upper_red = np.array([10,255,255])
    
mask = cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(img,img, mask= mask)

thresh1=50
thresh2=0.1
to_delete=[]

new_lines = findHoughlines(mask)

horz=[]
vert=[]

for line in new_lines:
	if abs(np.sin(line[1]))>0.5:
		vert.append((line[0],line[1]))
	else:
		horz.append((line[0],line[1]))

# print horz
# print vert 

corners=[]

for hor_line in horz:
	for vert_line in vert:
		corners.append(find_interection(hor_line,vert_line))
#print corners

for point in corners:
	cv2.circle(img,point,5,thickness=5,color=1)

image_side_length = int(find_board_edge_size(corners))

top_left, top_right,bottom_left,bottom_right=findExtremeCorners(corners)
src=np.array([corners[top_left],corners[top_right],corners[bottom_left],corners[bottom_right]],np.float32)
dst=np.array([[0,0],[image_side_length-1,0],[0,image_side_length-1],[image_side_length-1,image_side_length-1]],np.float32)

perspective=cv2.getPerspectiveTransform(src,dst)

warped=cv2.warpPerspective(img,perspective,(image_side_length-1,image_side_length-1))

# new_individualSquares = findHoughlines(warped)

# edgy = cv2.Canny(warped, 100, 200)

# indivSquares = cv2.HoughLines(edgy,1,np.pi/180,180)
# individualSquares = indivSquares[0]

# to_delete_2=[]
# for index,line in enumerate(individualSquares):
# 	for index_2 in range(index+1, len(individualSquares)):
# 		if ((abs(line[0]-individualSquares[index_2][0])<thresh1) and (abs(line[1]-individualSquares[index_2][1])<thresh2)):
# 			line[0]=(line[0]+individualSquares[index_2][0])/2
# 			line[1]=(line[1]+individualSquares[index_2][1])/2
# 			to_delete.append(index_2)

# new_individualSquares=np.delete(individualSquares,list(set(to_delete)),axis=0)

# for rho,theta in new_lines:
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*rho
#     y0 = b*rho
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))

#     cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

list_of_images=extract_squares(warped)

# print list_of_images[1].shape

fig=plt.figure()
for x in range(64):

	plt.subplot(8,8,x+1)
	plt.imshow(list_of_images[x],cmap='gray')
# fig.axes.get_xaxis().set_visible(False)
# fig.axes.get_yaxis().set_visible(False)
# plt.show()

fig2=plt.figure()
for index,square in enumerate(list_of_images):
	plt.subplot(8,8,index+1)
	plt.hist(square.ravel(),256,[0,256]); 
plt.show()

# cv2.imshow('dst',warped)
# if cv2.waitKey(0) & 0xff == 27:
#     cv2.destroyAllWindows()

