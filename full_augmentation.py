# pip install pillow absl-py

# Usage example
# data augmentation on jpg images in /my/directory/with/data and resize to 300x300
# python data_augmentation --dir=/my/directory/with/data --imageExt=jpg --resizeWidth=300 --resizeHeight=300

import xml.etree.ElementTree as ET
import math

from PIL import Image
from absl import app, flags, logging
from absl.flags import FLAGS

import os

flags.DEFINE_string('imageExt', 'jpg', 'Images extension')
flags.DEFINE_string('dir', '', 'Directory with images')

def rotatePoint(angle, x, y, img_width, img_height):
    """
    Clockwise rotation
    """

    x = int(x)
    y = int(y)
    img_width = int(img_width)
    img_height = int(img_height)

    if angle==180:
        x90, y90 = rotatePoint(90, x, y, img_width, img_height)
        x2, y2 = rotatePoint(90, x90, y90, img_width, img_height)
        return str(x2), str(y2)

    a = angle * math.pi / 180

    print('Rotating ('+ str(x) +', '+ str(y) +') by ' + str(angle) + '° ...')

    xm = img_width/2
    ym = img_height/2

    x2 = int( (x - xm) * math.cos(a) - (y - ym) * math.sin(a) + xm )
    y2 = int( (x - xm) * math.sin(a) - (y - ym) * math.cos(a) + ym )

    print('.. result: ('+ str(x2) +', '+ str(y2) +').')

    return str(x2), str(y2)


def main(_argv):

  ext_len = len(FLAGS.imageExt)
  
  if not FLAGS.dir:
    dir = os.getcwd()
  else:
    dir = FLAGS.dir
    
  for image in os.listdir(dir):
  
    if(not image.endswith(FLAGS.imageExt)):
        continue
        
    if dir.endswith(str(os.path.sep)) :
        image = dir + image
    else:
        image = dir + os.path.sep + image
    
    image_name_length = len(image)
    # + 1 per includere il punto
    image_name = image[:image_name_length-(ext_len+1)]
    logging.info('Working on: ' + image)
        
    img = Image.open(image)

    image_xml_filename = image.replace('.'+FLAGS.imageExt, '.xml')

    if not os.path.exists(image_xml_filename):
        raise ValueError('missing XML')

    for angle in [90, 180, 270]:
        tree = ET.parse(image_xml_filename)
        root = tree.getroot()

        original_filename = root.find('filename').text
        file_ext = original_filename.split('.')[-1]

        new_filename = original_filename[0:-(len(file_ext)+1)] + '_' + str(angle) + '.' + file_ext
        
        root.find('filename').text = new_filename

        root.find('path').text = root.find('path').text.replace(original_filename, new_filename)

        print(root.find('filename').text)

        img_width = root.find('size').find('width').text
        img_height = root.find('size').find('height').text

        for item in root.iter('object'):
            object_name = str(item.find('name').text)
            print(object_name)
            for bndbox in item.iter('bndbox'):
                
                xmin = bndbox.find('xmin').text
                ymax = bndbox.find('ymax').text

                bndbox.find('xmin').text, bndbox.find('ymax').text = rotatePoint(angle, xmin, ymax, img_width, img_height)

                xmax = bndbox.find('xmax').text
                ymin = bndbox.find('ymin').text

                bndbox.find('xmax').text, bndbox.find('ymin').text = rotatePoint(angle, xmax, ymin, img_width, img_height)

        img.rotate(360-int(angle)).save(image_name+ '_' + str(angle) + '.' + FLAGS.imageExt, quality=95)
        tree.write(original_filename[0:-(len(file_ext)+1)] + '_' + str(angle) + '.xml', encoding='utf-8')
    
    # Horizontal flip
    # Vertical flip
    for flip in ['HF', 'VF']:
        tree = ET.parse(image_xml_filename)
        root = tree.getroot()

        original_filename = root.find('filename').text
        file_ext = original_filename.split('.')[-1]

        new_filename = original_filename[0:-(len(file_ext)+1)] + '_' + str(flip) + '.' + file_ext
        
        root.find('filename').text = new_filename

        root.find('path').text = root.find('path').text.replace(original_filename, new_filename)

        print(root.find('filename').text)

        img_width = root.find('size').find('width').text
        img_height = root.find('size').find('height').text

        for item in root.iter('object'):
            object_name = str(item.find('name').text)
            print(object_name)
            for bndbox in item.iter('bndbox'):
                
                xmin = bndbox.find('xmin').text
                ymax = bndbox.find('ymax').text

                xmax = bndbox.find('xmax').text
                ymin = bndbox.find('ymin').text

                if flip == 'HF':
                    bndbox.find('xmin').text = str( int(img_width) - int(xmin) )
                    bndbox.find('xmax').text = str( int(img_width) - int(xmax) )
                elif flip == 'VF':
                    bndbox.find('ymax').text = str( int(img_height) - int(ymax) )
                    bndbox.find('ymin').text = str( int(img_height) - int(ymin) )

        if flip == 'HF':
            tree.write(original_filename[0:-(len(file_ext)+1)] + '_HF.xml', encoding='utf-8')
            img.transpose(Image.FLIP_LEFT_RIGHT).save(image_name+'_HF' + '.' + FLAGS.imageExt, quality=95)
        elif flip == 'VF':
            tree.write(original_filename[0:-(len(file_ext)+1)] + '_VF.xml', encoding='utf-8')
            img.transpose(Image.FLIP_TOP_BOTTOM).save(image_name+'_VF' + '.' + FLAGS.imageExt, quality=95)

    # Close original
    img.close()

if __name__ == '__main__':
    app.run(main)
