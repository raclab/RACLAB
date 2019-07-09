import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO

from matplotlib import pyplot as plt
from PIL import Image                                                       # Gerekli kütüphaneler dahşl edildi.

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):                  # Eğer tensorflow sürümü 1.9.0'dan küçük ise,
  raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')  # Bu  hata fırlatılır.

from utils import label_map_util
from utils import visualization_utils as vis_util                           # Diğer kütüphaneler dahil edildi.

MODEL_NAME = 'faster_rcnn_resnet101_coco_2018_01_28'                        # Hangi model kullanmak istiyorsak onun ismi verilmelidir.

MODEL_FILE = MODEL_NAME + '.tar.gz'                                         # İndilen modelin uzantısı.
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'   # Modelin indirileceği adres.

PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'            # Dondurulmuş modelin adresi değişkene gönderildi.

# Her kutuya doğru etiket eklemek için kullanılan dizelerin listesi. (label_map dosyası ve adresi)
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

# Eğer nesnne tanıma yapılacak model daha önce indirilmiş ise aşağıdaki kodlar yorum satırı haline getirlebilir.
#-----------------------------------------------------------------------------------------------
opener = urllib.request.URLopener()                                         # Bir defa program çalıştırıldıktan
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)                     # sonra model
tar_file = tarfile.open(MODEL_FILE)                                         # iner. Bir
for file in tar_file.getmembers():                                          # daha bu
  file_name = os.path.basename(file.name)                                   # satırları
  if 'frozen_inference_graph.pb' in file_name:                              # çalıştırmaya
    tar_file.extract(file, os.getcwd())                                     # gerek yok.
#------------------------------------------------------------------------------------------------

# Model hafızaya yükleniyor.
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

# Sonra tüm etiketleri yükleyeceğiz.
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

# Görüntü verilerinin işlemesi için dizilere dönüştürülecek.
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

PATH_TO_TEST_IMAGES_DIR = 'test_images'                                     # Nesne tanıma yapılacak görüntülerin bulunduğu konum.
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 3) ]
                                                                            # Nesne tanıma yapılacak görüntülerin yolu.

IMAGE_SIZE = (12, 8)                                                        # Çıktı resimlerinin inç cinsinden boyutu.

# Bu kod, nesneleri algıladığı, kutuları oluşturduğu ve o nesnenin sınıfını ve sınıf puanını sağlayan tek bir görüntünün çıkarımını çalıştırır.
def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      # Çıktı resimlerinin inç cinsinden boyutu.
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
      if 'detection_masks' in tensor_dict:
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: np.expand_dims(image, 0)})

      # Tüm çıkışlar float32 numpy dizileridir, dolayısıyla tipleri uygun şekilde dönüştürülmelidir.
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict

# Bu kısımda gerekli tespitler yapıldıktan sonra görselleştimenin yapıldığığı ksımdır.
for image_path in TEST_IMAGE_PATHS:
  image = Image.open(image_path)
  image_np = load_image_into_numpy_array(image)
  image_np_expanded = np.expand_dims(image_np, axis=0)
  output_dict = run_inference_for_single_image(image_np, detection_graph)
  # Algılama bu komut ile görselleştirildi.
  vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      category_index,
      instance_masks=output_dict.get('detection_masks'),
      use_normalized_coordinates=True,
      line_thickness=8)

  plt.figure(figsize=IMAGE_SIZE)                                            # Görüntülerin ekranda gösterilmesi için bir boşluk oluşturuldu.
  plt.imshow(image_np)                                                      # Görüntü ekrana getirildi.
  plt.show()                                                                # Görüntü ekranda tutuldu.


