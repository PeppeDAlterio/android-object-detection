# pip install pillow absl-py

# Usage example
# data augmentation on jpg images in /my/directory/with/data and resize to 300x300
# python data_augmentation --dir=/my/directory/with/data --imageExt=jpg --resizeWidth=300 --resizeHeight=300

from PIL import Image
from absl import app, flags, logging
from absl.flags import FLAGS

import os

flags.DEFINE_string('imageExt', 'jpg', 'Images extension')
flags.DEFINE_string('dir', '', 'Images extension')
flags.DEFINE_integer('resizeWidth', 300, 'Images resize width')
flags.DEFINE_integer('resizeHeight', 300, 'Images resize height')

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
    # 90
    img.rotate(90).resize( (FLAGS.resizeWidth, FLAGS.resizeHeight) ).save(image_name+'_90' + '.' + FLAGS.imageExt)
    # 180
    img.rotate(180).resize( (FLAGS.resizeWidth, FLAGS.resizeHeight) ).save(image_name+'_180' + '.' + FLAGS.imageExt)
    # 270
    img.rotate(270).resize( (FLAGS.resizeWidth, FLAGS.resizeHeight) ).save(image_name+'_270' + '.' + FLAGS.imageExt)
    # Horizontal flip
    im.transpose(PIL.Image.FLIP_LEFT_RIGHT).resize( (FLAGS.resizeWidth, FLAGS.resizeHeight) ).save(image_name+'_HF' + '.' + FLAGS.imageExt)
    # Vertical flip
    im.transpose(PIL.Image.FLIP_TOP_BOTTOM).resize( (FLAGS.resizeWidth, FLAGS.resizeHeight) ).save(image_name+'_VF' + '.' + FLAGS.imageExt)
    
    # Resize and close original
    img.resize( (FLAGS.resizeWidth, FLAGS.resizeHeight) ).save(image)
    img.close()

if __name__ == '__main__':
    app.run(main)
