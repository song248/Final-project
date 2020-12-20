import tensorflow as tf
import torch, torchvision, os, json
from efficientnet_pytorch import EfficientNet

def model_load(): 
    global model_name,model,labels_map,MEAN_RGB,STDDEV_RGB,CROP_PADDING,image_size
    
    # 모델 초기 정의 
    model_name = 'efficientnet-b4'
    model = EfficientNet.from_pretrained(model_name, num_classes=38)

    # 모델로드 
    model.load_state_dict(torch.load('president_model_b4_1210.pt'))
    # 모델 사용 선언 1
    model.eval()

    # 클래스명 로드 (필수)
    labels_map = json.load(open('labels_map_final.txt'))
    labels_map = [labels_map[str(i)] for i in range(39)]

    # 텐서로 이미지 전처리 
    tf.executing_eagerly()

    # 이미지 콘텐츠 
    MEAN_RGB = [0.485 * 255, 0.456 * 255, 0.406 * 255]
    STDDEV_RGB = [0.229 * 255, 0.224 * 255, 0.225 * 255]
    CROP_PADDING = 32
    image_size = 224
    return 
    
# 처리함수 
def _decode_and_center_crop(image_bytes, image_size):
    shape = tf.image.extract_jpeg_shape(image_bytes)
    image_height = shape[0]
    image_width = shape[1]
    padded_center_crop_size = tf.cast(
      ((image_size / (image_size + CROP_PADDING)) *
       tf.cast(tf.minimum(image_height, image_width), tf.float32)),
      tf.int32)
    offset_height = ((image_height - padded_center_crop_size) + 1) // 2
    offset_width = ((image_width - padded_center_crop_size) + 1) // 2
    crop_window = tf.stack([offset_height, offset_width, padded_center_crop_size, padded_center_crop_size])
    image = tf.image.decode_and_crop_jpeg(image_bytes, crop_window, channels=3)
    image = tf.image.resize([image], [image_size, image_size])[0]
    return image    

def testfunction(img):
    global preds ,label, prob
    tf_img_bytes = tf.io.read_file(img)
    tf_img = _decode_and_center_crop(tf_img_bytes, image_size)
    tf_img = tf.image.resize([tf_img], [image_size, image_size])[0] # ok it matches up to here
    use_bfloat16 = 224 # bug in the original repo! 
    tf_img = tf.image.convert_image_dtype(tf_img, dtype=tf.bfloat16 if use_bfloat16 else tf.float32)
    tf_img = tf.cast(tf_img, tf.float32)
    tf_img = (tf_img - MEAN_RGB) / (STDDEV_RGB)  # this is exactly the input to the model
    img = torch.from_numpy(tf_img.numpy()).unsqueeze(0).permute((0,3,1,2))
    with torch.no_grad():
        logits = model(img)
    preds = torch.topk(logits, k=5).indices.squeeze(0).tolist()
    print('pred: ', preds[0])
    print(preds)
    print(type(preds[0]))

    print('*'*100)
    percen_list = []
    for idx in preds:
        label = labels_map[idx]
        prob = torch.softmax(logits, dim=1)[0, idx].item()
        percen = round(prob*100, 2)
        print('{:<75} ({:.2f}%)'.format(label, prob*100))
        percen_list.append(percen)
    print('percent: ', percen_list[0],'%')
    print('*'*100)

    if percen_list[0] < 70:
        print('*****classification error*****')
        preds[0] = 38
        print(preds)

def Selected_Place():
    global place
    place=[]
    for idx in preds:
        k=labels_map[idx]
        place.append(k)

def execute_model(img):
    model_load()
    testfunction(img)
    Selected_Place() 
    return place[0]
