import os
import cv2

def get_item_quantity(class_name, item_est_area_cm):
    
    '''
    To calculate volume and weight for food item
    - input: class_name, item_est_area_cm (area calculated from mask pixel in cm2)
    - output: volume in ml, weight in gm
    
    NOTE: values in items_avg_hts_cm and items_density_gm_per_cm3 list are taken from internet
    '''

  #items_act_vols_ml = {'beet':120, 'chicken sandwich':'1 sandwich (tongs)', 'macaroni':180}
    items_avg_hts_cm = {'beet':3.8, 'chicken sandwich':4.5, 'macaroni':3.5}

    items_density_gm_per_cm3 = {'beet':0.76,'chicken sandwich':0.65,'macaroni':0.51}

  # Volume = Area * Height
    item_est_vol_cm = item_est_area_cm*items_avg_hts_cm[class_name]

  # Weight = Volume * Density
    item_est_wgt_gms = items_density_gm_per_cm3[class_name]*item_est_vol_cm

    return round(item_est_vol_cm,2), round(item_est_wgt_gms,2)
          

def get_items_measures(unit_pxl_area, class_ids, masks, scores):
  detected_class = set([class_id for class_id, score in zip(class_ids, scores) if score>0.5])

  item_details = {}
  def get_item_count_area_vol(item, class_ids, instance_masks, scores):
    item_count_area_vol = {'count':None, 'accuracy_score':[], 'cm2_area':[], 'cm3_vol':[], 'cm3_total_vol':None, 'gm_wegt':None}
    
    item_total_vol = 0
    item_count = 0
    for class_id, object_contours, score in zip(class_ids, instance_masks, scores):
        if score>=0.5 and classes[class_id]==item:
          item_count+=1
          object_contours[object_contours > 0] = 255
          thresh = cv2.threshold(object_contours,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
          mask_pxl = cv2.countNonZero(thresh)

          area_cm2 = round(mask_pxl/unit_pxl_area, 2)
          vol_cm3, weight_gm = get_item_quantity(item, area_cm2)
          item_count_area_vol['accuracy_score'].append(round(score, 2))
          item_count_area_vol['cm2_area'].append(area_cm2)
          item_count_area_vol['cm3_vol'].append(vol_cm3)
          item_total_vol+=vol_cm3

          object_contours[object_contours > 0] = 1

    item_count_area_vol['count'] = item_count
    item_count_area_vol['cm3_total_vol'] = round(item_total_vol, 2)
    item_count_area_vol['gm_wegt'] = weight_gm

    return item_count_area_vol

  classes = {1:'beet', 2:'chicken sandwich', 3:'macaroni'}

  for item in [classes[det] for det in detected_class]:
    item_details[item] = get_item_count_area_vol(item, class_ids, masks, scores)

  return item_details
  
  
# step 2 : setting function to calculate items area and volume from mask area

def get_detection_measures(image, total_detection, class_ids, masks, scores, mask_dir=None):

  '''
  1. 1 cm2 = 38x38 = 1444 pxl; 2.20% of 256x256

  2. A demo referance: if 78x78 pixel = 1 cmsq (taking 1024x576 px image)
     1 unit cmsq will be 1.03149414062% of entire image,
     so unit area in cmsq for our image(256x256) is 1.03149414062% of image's total area, i.e 1.031494140625 * (256x256) / 100 = 676 pxls
  '''

  #classes = {1:'beet', 2:'chicken sandwich', 3:'macaroni'}
  image_measures = {}
  items_area_vol = {}
  if bool(image_measures) and bool(items_area_vol):
    print('Dict is not empty!')

  w1, h1, _ = image.shape
  image_area_in_pxl = w1*h1

  unit_pxl_area = (1.031494140625 * image_area_in_pxl) / 100
  #unit_pxl_area = (2.20 * image_area_in_pxl) / 100
  image_area_in_cm = round(image_area_in_pxl/unit_pxl_area, 2)
  image_measures['image_area_cm'] = image_area_in_cm

  mask_pxl_total = 0
  for i, class_id, object_contours, score in zip(range(total_detection), class_ids, masks, scores):
    if score>=0.5:
      object_contours[object_contours > 0] = 255
      if mask_dir!=None:
          cv2.imwrite(os.path.join(mask_dir, 'mask{}.jpg'.format(i)), object_contours)

      thresh = cv2.threshold(object_contours,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]
      mask_pxl_total += cv2.countNonZero(thresh)

      object_contours[object_contours > 0] = 1
    
  items_acc_area_vol = get_items_measures(unit_pxl_area, class_ids, masks, scores)

  mask_ratio_in_pxl = (mask_pxl_total / image_area_in_pxl) * 100
  image_measures['total_mask_proportion'] = round(mask_ratio_in_pxl, 2)
  image_measures['total_mask_area_cm'] = round(image_area_in_cm*mask_ratio_in_pxl / 100, 2)

  return image_measures, items_acc_area_vol