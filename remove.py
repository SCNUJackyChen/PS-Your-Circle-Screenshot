from PIL import Image
import cv2

class HappyShareCircle:
    def __init__(self,pic_path):
        self.path = pic_path
        self.picture = cv2.imread(self.path)
        self.height, self.width, self.channel = self.picture.shape

    def __isBlank(self, line):
        '''
        判断当前行是否为全白
        :param line: 行坐标
        :return: True/False
        '''
        for w in range(self.width):
            RGB = self.picture[line,w]
            if RGB.sum()<255*3:
                return False
        return True

    def divide(self):
        '''
        图像分割
        :return: ordinates：list，元素为二元组，表示图片每个部分的上下界
        '''
        begin = end = 0
        flag = False # flag为真表示当前在某个区间中
        ordinates = []
        for h in range(self.height):
            if not self.__isBlank(h) and not flag:
                begin = h
                flag = True
            elif self.__isBlank(h) and flag:
                end = h
                flag = False
                ordinates.append((begin,end))
        if end < begin:
            end = self.height+1
            ordinates.append((begin, end))
        return ordinates

    def setBlank(self, interval:tuple):
        '''
        删除图片某个区间的图像
        :param interval: 区间，二元组
        :return: 新的图像
        '''
        picture = self.picture.copy()
        picture[interval[0]:interval[1],:] = 255
        return picture


if __name__ == '__main__':
    picture = HappyShareCircle('test.jpg')
    retrivals = picture.divide()
    print(retrivals)
    new_picture = picture.setBlank(retrivals[-1])
    cv2.imwrite('output_ipad.jpg',new_picture)
    #图像叠加
    image = Image.open('output_ipad.jpg')
    button = Image.open('button.png')
    image.paste(button,(image.size[0]-button.size[0]-20,retrivals[-2][0]-10),None)
    image.save('output_ipad2.jpg')
