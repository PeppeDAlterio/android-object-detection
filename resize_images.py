from PIL import Image
from absl import app, flags, logging
from absl.flags import FLAGS

import os

flags.DEFINE_string('imageExt', 'jpg', 'Images extension')
flags.DEFINE_string('dir', '', 'Directory with images')
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
    img.resize( (FLAGS.resizeWidth, FLAGS.resizeHeight), Image.ANTIALIAS ).save(image, quality=95)
    img.close()

if __name__ == '__main__':
    app.run(main)
