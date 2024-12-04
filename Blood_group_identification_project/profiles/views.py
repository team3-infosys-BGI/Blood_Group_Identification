# import base64
# from django.shortcuts import render
# from django.core.files.storage import FileSystemStorage
# import cv2
# import numpy as np

# def profiles(request):
#     if request.method == "POST" and request.FILES.get('abo_image'):
#         # Get the uploaded image
#         img_file = request.FILES['abo_image']
        
#         # Save the image to a temporary location
#         fs = FileSystemStorage()
#         filename = fs.save(img_file.name, img_file)
#         img_path = fs.path(filename)
        
#         # Identify process the image(morphed image)
#         morph_image,blood_type = identify_blood_group(img_path)
        
#         # Convert the morphological image to Base64
#         _, buffer = cv2.imencode('.png', morph_image)
#         morph_image_base64 = base64.b64encode(buffer).decode('utf-8') # the morphed image is in binary ,needs to be converted to string to be displayed in html
        
#         # img_url = fs.url(filename)
        
#         return render(request, 'profiles.html', {
#             'morph_image': morph_image_base64,
#             'blood_type': blood_type
#         })
#     return render(request, 'profiles.html', {})
    
   

# def identify_blood_group(img_path):
#     # Read the uploaded image
#     abo_image = cv2.imread(img_path)
    
#     # Convert the image from color to grayscale
#     gray = cv2.cvtColor(abo_image, cv2.COLOR_BGR2GRAY)
    
#     # blur the image using Gaussian Blur (smoothning the image for more accurate blood cell Image)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
#    # blurred to threshold to calculate the threshold values for the given images and will return the image and its value
#     # val, threshold = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)# sets pixels to either black or white
    
#    # finding the contours(continuous curve along the boundary) to find the curved edges of the blood cells in the image
#     # contours,val2 = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# 2nd parameter is for considering only the outer contour and not any of its inside child contour

#     enhanced_img = cv2.equalizeHist(blur)

#     #morphological operations
#     var, bin_image = cv2.threshold(enhanced_img, 0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#     #morphological operations
#     #step-1: creating the kernel
#     kernel_imp = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

#     #convert the threshold image into morphological structured image 
#     bin_img = cv2.morphologyEx(bin_image, cv2.MORPH_OPEN, kernel_imp)
#     bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel_imp)

#     h,w = bin_img.shape
#     mid_width = int(w/2)

#     region_A = bin_img[0:mid_width]
#     region_B = bin_img[mid_width:2*mid_width]
#     region_D = bin_img[2*mid_width:]

#     print(region_A)
#     print(region_B)
#     print(region_D)


#     def cal_agglutination(region):
#         num_labels,labels,stats,var = cv2.connectedComponentsWithStats(region,connectivity=8)
#         return num_labels-1
    
#     num_region_A = cal_agglutination(region_A)
#     num_region_B = cal_agglutination(region_B)
#     num_region_D = cal_agglutination(region_D)

#     print(num_region_A,num_region_B,num_region_D)
    
#     is_positive = None
#     blood_type = None

#     if num_region_D>0:
#         is_positive ='+'
#     else:
#         is_positive ='-'

#     if num_region_A and num_region_B==0:
#         blood_type ='A'

#     elif num_region_A==0 and num_region_B>0:
#         blood_type='B'

#     elif num_region_A>0 and num_region_B>0:
#         blood_type='AB'

#     elif num_region_A==0 and num_region_B==0:
#         blood_type='O'

#     else:
#         blood_type='unknown'                

#     print(blood_type+is_positive)

#     return bin_img, blood_type+is_positive

  

import base64
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np

def profiles(request):
    if request.method == "POST" and request.FILES.get('abo_image'):
        # Get the uploaded image
        img_file = request.FILES['abo_image']
        
        # Save the image to a temporary location
        fs = FileSystemStorage()
        filename = fs.save(img_file.name, img_file)
        img_path = fs.path(filename)
        
        try:
            # Identify process the image(morphed image)
            morph_image, blood_type = identify_blood_group(img_path)
            
            # Convert the morphological image to Base64
            _, buffer = cv2.imencode('.png', morph_image)
            morph_image_base64 = base64.b64encode(buffer).decode('utf-8')  # the morphed image is in binary, needs to be converted to string to be displayed in HTML
            
            return render(request, 'profiles.html', {
                'morph_image': morph_image_base64,
                'blood_type': blood_type
            })
        
        except cv2.error as e:
            print(f"OpenCV error: {e}")
            error_message = "The uploaded image could not be processed. Please ensure it is a valid blood smear image."
            return render(request, 'profiles.html', {'error_message': error_message})
        
        except Exception as e:
            print(f"Error: {e}")
            error_message = "An unexpected error occurred while processing the image."
            return render(request, 'profiles.html', {'error_message': error_message})
    
    return render(request, 'profiles.html', {})


def identify_blood_group(img_path):
    try:
        # Read the uploaded image
        abo_image = cv2.imread(img_path)
        
        if abo_image is None:
            raise ValueError("Invalid image file")
        
        # Convert the image from color to grayscale
        gray = cv2.cvtColor(abo_image, cv2.COLOR_BGR2GRAY)
        
        # Blur the image using Gaussian Blur (smoothing the image for more accurate blood cell Image)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Enhance the image contrast
        enhanced_img = cv2.equalizeHist(blur)

        # Apply thresholding
        _, bin_image = cv2.threshold(enhanced_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Perform morphological operations
        kernel_imp = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        bin_img = cv2.morphologyEx(bin_image, cv2.MORPH_OPEN, kernel_imp)
        bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel_imp)

        # Divide the image into regions
        h, w = bin_img.shape
        mid_width = w // 2

        region_A = bin_img[0:mid_width]
        region_B = bin_img[mid_width:2 * mid_width]
        region_D = bin_img[2 * mid_width:]

        def cal_agglutination(region):
            num_labels, _, _, _ = cv2.connectedComponentsWithStats(region, connectivity=8)
            return num_labels - 1

        num_region_A = cal_agglutination(region_A)
        num_region_B = cal_agglutination(region_B)
        num_region_D = cal_agglutination(region_D)

        is_positive = '+' if num_region_D > 0 else '-'

        if num_region_A > 0 and num_region_B == 0:
            blood_type = 'A'
        elif num_region_A == 0 and num_region_B > 0:
            blood_type = 'B'
        elif num_region_A > 0 and num_region_B > 0:
            blood_type = 'AB'
        elif num_region_A == 0 and num_region_B == 0:
            blood_type = 'O'
        else:
            blood_type = 'unknown'

        return bin_img, blood_type + is_positive
    
    except Exception as e:
        print(f"Error in identify_blood_group: {e}")
        raise

