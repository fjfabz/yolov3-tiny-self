from tiny_yolo_top import tiny_yolov3
import numpy as np
import tensorflow as tf
from tiny_config import cfg
from PIL import Image, ImageDraw, ImageFont
from draw_boxes import draw_boxes
import matplotlib.pyplot as plt


# IMG_ID ='008957'
# image_test = Image.open('/home/raytroop/Dataset4ML/VOC2007/VOCdevkit/VOC2007/JPEGImages/{}.jpg'.format(IMG_ID))


image_test = Image.open('image/000941.jpg')
# image_test = Image.open('image/000001.jpg')
# image_test = Image.open('image/000020.jpg')
# resized_image = image_test.resize((512, 288), Image.BICUBIC)
resized_image = image_test.resize((416, 416), Image.BICUBIC)
image_data = np.array(resized_image, dtype='float32')

imgs_holder = tf.placeholder(tf.float32, shape=[1, 416, 416, 3])
# imgs_holder = tf.placeholder(tf.float32, shape=[1, 512, 288, 3])
istraining = tf.constant(False, tf.bool)
cfg.batch_size = 1
cfg.scratch = True

model = tiny_yolov3(imgs_holder, None, istraining)
img_hw = tf.placeholder(dtype=tf.float32, shape=[2])
boxes, scores, classes = model.pedict(img_hw, iou_threshold=0.7, score_threshold=0.7)
saver = tf.train.Saver()
# ckpt_dir = './ckpt_all_100_512_288/'
ckpt_dir = './ckpt/814/'
# ckpt_dir = './ckpt/ckpt_demo_416_class3/'

with tf.Session() as sess:
    ckpt = tf.train.get_checkpoint_state(ckpt_dir)
    print(ckpt.model_checkpoint_path)
    saver.restore(sess, ckpt.model_checkpoint_path)
    boxes_, scores_, classes_ = sess.run([boxes, scores, classes],
                                         feed_dict={
                                                    img_hw: [image_test.size[1], image_test.size[0]],
                                                    # img_hw: [image_test.size[0], image_test.size[1]],
                                                    imgs_holder: np.reshape(image_data / 255, [1, 416, 416, 3])})
    # print(boxes_)
    # print(scores_)
    # print(classes_)

    image_draw = draw_boxes(np.array(image_test, dtype=np.float32) / 255, boxes_, classes_, cfg.names, scores=scores_)
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0, 0, 1, 1])
    # ax = plt.Axes(fig)
    ax.set_axis_off()
    fig.add_axes(ax)
    plt.imshow(image_draw)
    fig.savefig('prediction.jpg')
    plt.show()

