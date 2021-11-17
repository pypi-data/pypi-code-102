from PIL import Image
import numpy as np


class ArrayPil(object):
	
	@classmethod
	def ConvImgArray(self, imgdir, conv='RGB'):
		self.im1 = np.asarray(Image.open(imgdir).convert(conv))
		return self.im1
	
	@classmethod
	def ImgSave(self, imgarray, dirsave, conv='RGB'):
	   	self.im2 = Image.fromarray(imgarray, conv)
	   	self.im2.save(dirsave)
	  
	@classmethod
	def ConvPilArray(self, imgpil, conv='RGB'):
		self.im3 = np.asarray(imgpil.convert(conv))
		return self.im3
	
	@classmethod
	def ConvImgPil(self, imgarray, conv='RGB'):
		self.im4 = Image.fromarray(imgarray, conv)
		return self.im4


		
		
#testing
#obj = ArrayPil()
#a1 = obj.ConvImgArray('image1.jpg')
#print(a1)
#
#b1 = ArrayPil.ConvImgArray('image1.jpg')
#print(b1)
#
#ArrayPil.ImgSave(a1, 'res1.jpg')
#
#obj.ImgSave(a1, 'res2.jpg')
#
#b2 = ArrayPil.ConvImgPil(b1)
#print(b2)
#
#a2 = obj.ConvImgPil(a1)
#print(a2)
#
#b3 = ArrayPil.ConvPilArray(b2)
#print(b3)
#
#a3 = obj.ConvPilArray(a2)
#print(a3)
