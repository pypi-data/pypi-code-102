class Explanations:
    def __init__(self,img,model,class_names,img_list,img_shape=224,r=10) -> None:
        self.explanation_list={"Anchor":None,
                    "LIME":None,
                    "IG":None,
                    "SHAP":None}
        self.model = model
        self.image = img
        self.img_list = img_list
        self.img_shape = img_shape
        self.class_names = class_names
        self.r = r
        self.pred_class = self.getPredictions()

    def anchor_explanations(self,n_segments,compactness,sigma,image,model,segmentation_fn="slic",
                            threshold=.95, p_sample=.5, tau=0.25,image_shape=(224,224,3)):
        
        global explanation_list
        from alibi.explainers import AnchorImage
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt


        predict_fn = lambda x: model.predict(x)
        image = np.array(image)
        #felzenszwalb, slic and quick shift
        # not for felzenszwalb 
        if segmentation_fn == "slic":
            kwargs = {'n_segments': n_segments, 'compactness': compactness, 'sigma': sigma}
            explainer = AnchorImage(predict_fn, image_shape=image_shape, segmentation_fn=segmentation_fn,
                                    segmentation_kwargs=kwargs, images_background=None)
        else:
            explainer = AnchorImage(predict_fn, image_shape=image_shape, segmentation_fn=segmentation_fn,
                                    images_background=None)
        np.random.seed(0)
        explanation = explainer.explain(image, threshold, p_sample, tau)
        

        fig = plt.figure(figsize=(10, 7))
        # setting values to rows and column variables
        rows = 1
        columns = 2

        fig.add_subplot(rows, columns, 1)
        plt.imshow(explanation.anchor)
        plt.axis('off')
        plt.savefig("AnchorExpalanation.png")

        fig.add_subplot(rows, columns, 2)
        plt.imshow(explanation.segments)
        plt.axis('off')
        plt.savefig("AnchorSegmentation.png")
        self.explanation_list["Anchor"]=explanation.anchor
        


    def LIME_explanations(self,model,image,prediction,class_name=None,positive_only=True,num_features=10000,
                        hide_rest=False,min_weight=0.1, hide_color=None, num_samples=None):
        """
            model:CNN
            image:The image that we want LIME to explain.
            prediction:Your image classier prediction.
            class_name:Real Prediction if avaiable
            num_samples:to determine the amount of artificial data points similar to our input that will be generated by LIME.
            hide_color: is the color for a superpixel turned OFF. Alternatively, if it is NONE, the superpixel will be replaced by the average of its pixels. 
                        (in the representation used by inception model, 0 means gray)
            positive_only:Bool show only the positive part
            num_features:Number of features in the positive need to show
            hide_rest:Bool rest of the image need to hide or not
            min_weight: such as 0.1 to be taken as value for the prediction
        """
        
        global explanation_list
       
        from lime import lime_image
        from skimage.segmentation import mark_boundaries
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        image=np.array(image,dtype=np.double)
        explainer = lime_image.LimeImageExplainer(random_state=42)

        explanation = explainer.explain_instance(image, model.predict, hide_color, num_samples)
        
        plt.title(f"Prediction: {prediction} Actual: {class_name}")
        
        plt.imshow((image * 255).astype(np.uint8))
         
        if positive_only==False and hide_rest==False:
            image, mask = explanation.get_image_and_mask(model.predict(image.reshape((1,224,224,3))).argmax(axis=1)[0],
                                                            positive_only=positive_only,hide_rest=hide_rest,
                                                            num_features=num_features,min_weight=min_weight)
        else:
            image, mask = explanation.get_image_and_mask(model.predict(image.reshape((1,224,224,3))).argmax(axis=1)[0],
                                                            positive_only=positive_only,hide_rest=hide_rest,
                                                            num_features=num_features,min_weight=min_weight)
        plt.axis('off')
        plt.imshow(mark_boundaries(image, mask))
        plt.savefig("LimeExplanation.png")
        self.explanation_list["LIME"]=mask
        

    def integrated_Gradients(self,model,img,prediction,class_name="Not given",n_steps=20,internal_batch_size=20,
                             Random_baseline=False,method = "gausslegendre",Scale_Factor=1):
        

        global explanation_list
        from alibi.explainers import IntegratedGradients
        from alibi.utils.visualization import visualize_image_attr
        import tensorflow as tf
        import numpy as np
        from PIL import Image
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import tensorflow.python.ops.numpy_ops.np_config as np_config
        np_config.enable_numpy_behavior()
        tf.executing_eagerly()

        ig  = IntegratedGradients(model,n_steps=n_steps,method=method,internal_batch_size=internal_batch_size)

        instance = np.expand_dims(img, axis=0)
        if Random_baseline:
            baselines = np.random.random_sample(instance.shape)
        else:
            baselines=None

        predictions = model(instance).numpy().argmax(axis=1)

        image = np.array(img)
        explanation = ig.explain(instance,baselines=baselines,target=predictions)
        
        attrs = explanation.attributions[0]
        
        # scaling attribute values
        attrs = attrs.squeeze()*Scale_Factor
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
        plt.axis('off')

        visualize_image_attr(attr=None, original_image=(image * 255).astype(np.uint8), method='original_image',
                            title=f'Prediction {prediction}, Actual {class_name}', plt_fig_axis=(fig, ax[0]), 
                            use_pyplot=False);

        visualize_image_attr(attr=attrs.squeeze(), original_image=image, method='blended_heat_map',
                            sign='all', show_colorbar=True, title='Overlaid Attributions',
                            plt_fig_axis=(fig, ax[1]), use_pyplot=True);
        fig.savefig("IGExplanation.png")
     
        self.explanation_list["IG"]=attrs
        

    def Shape_Gradient_Explainer(self,model,images_list):
        global explanation_list
        
        import numpy as np
        import shap
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        # get the length of the image list
        k = len(images_list)

        # since we have two inputs we pass a list of inputs to the explainer
        images_list = np.array(images_list)  
        explainer = shap.GradientExplainer(model,images_list)

        # we explain the model's predictions on the first three samples of the test set
        shap_values = explainer.shap_values(images_list[0:k])
        
        print(len(shap_values))
        shap.image_plot(shap_values, images_list[0:k],width=60,aspect=0.1,hspace=0.1, show=False)
        plt.savefig("SHAPExplanation.png")
        self.explanation_list["SHAP"]=shap_values
        
       
    def FFT(self,img,dst,dst_I):
        import numpy as np
        import cv2
        from matplotlib import pyplot as plt

        # fft to convert the image to freq domain 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # fft to convert the image to freq domain 
        f = np.fft.fft2(img)

        # shift the center
        fshift = np.fft.fftshift(f)

        rows, cols = img.shape
        crow,ccol = int(rows/2) , int(cols/2)

        # remove the low frequencies by masking with a rectangular window of size 60x60
        # High Pass Filter (HPF)
        rows, cols = img.shape
        crow, ccol = int(rows / 2), int(cols / 2)

        mask = np.ones((rows, cols), np.uint8)
        center = [crow, ccol]
        x, y = np.ogrid[:rows, :cols]
        mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= self.r*self.r
        mask[mask_area] = 0
        fshift = fshift * mask

        # shift back (we shifted the center before)
        f_ishift = np.fft.ifftshift(fshift)

        # inverse fft to get the image back 
        img_back = np.fft.ifft2(f_ishift)

        img_back = np.abs(img_back)

        magnitude_spectrum = 20*np.log(np.abs(fshift))
        from matplotlib.pyplot import figure
        figure(num=None, figsize=(18, 16), dpi=80, facecolor='w', edgecolor='k')
        plt.subplot(141),plt.imshow(magnitude_spectrum, cmap = 'gray')
        plt.title('magnitude_spectrum after filtering'), plt.xticks([]), plt.yticks([])
        plt.subplot(142),plt.imshow(img, cmap = 'gray')
        plt.title('Input Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(143),plt.imshow(img_back, cmap = 'gray')
        plt.title('Image after HPF'), plt.xticks([]), plt.yticks([])
        plt.subplot(144),plt.imshow(dst)
        plt.title('LISA Explanation Union'), plt.xticks([]), plt.yticks([])
        plt.subplot(241),plt.imshow(dst_I)
        plt.title('LISA Explanation Intersection'), plt.xticks([]), plt.yticks([])
        plt.subplot(242),plt.imshow(img_back)
        plt.title('LISA Explanation Boundary'), plt.xticks([]), plt.yticks([])
        plt.show()
        plt.savefig("FFTExplanation.png")


    def LISA(self,input_image):
        import numpy as np
        import cv2

        Anchor=self.explanation_list.get("Anchor")
        LIME=self.explanation_list.get("LIME")
        IG=self.explanation_list.get("IG")
        SHAP=self.explanation_list.get("SHAP")
 
        # # SHAP
        # Convert SHAP to numpy array
        SHAP_np = np.array(SHAP)
        
        # Access the shaply value of explained image
        # SHAP_np[0][2]
        SHAP_np_target = SHAP_np[0][2]
        
        # extract positive shape values
        SHAP_np_target_positive = np.where(SHAP_np_target>0,SHAP_np_target,0)
        SHAP_np_target_positive_replace = SHAP_np_target_positive.copy()
        # get the shape value if any present in R or B pixcel line which are positive shapley values and replace with G
        SHAP_np_target_positive_replace = np.where(((SHAP_np_target_positive_replace[...,0]>0).any() | 
                                                    (SHAP_np_target_positive_replace[...,1]>0).any() | 
                                                    (SHAP_np_target_positive_replace[...,2]>0).any())
                                                    ,SHAP_np_target_positive_replace[...,1],0)
        
        # using opencv
        # convert to cv2 gray scale images
        im_shap = np.array(SHAP_np_target_positive_replace * 255, dtype = np.uint8)
        threshed_shap = cv2.adaptiveThreshold(im_shap, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0)
        
        # Add colour to shap
        img_shap = np.zeros((224,224,3),dtype = np.float32)
        img_shap[:,:,0]=threshed_shap* 255./255. 
        img_shap[:,:,1]=threshed_shap* 0/255.
        img_shap[:,:,2]=threshed_shap* 0/255.

        # Apply green color mask to lime explanations
        im_lime = np.array(LIME * 255, dtype = np.uint8)
        # create 3 channel image
        img_lime = np.zeros((224,224,3),dtype = np.float32)
        img_lime[:,:,0]=im_lime*0/255.
        img_lime[:,:,1]=im_lime*255./255.
        img_lime[:,:,2]=im_lime*0/255.
        
        im_IG=np.array(IG, dtype = np.uint8)
        gray_IG = cv2.cvtColor(im_IG, cv2.COLOR_BGR2GRAY)
        # create 3 channel image
        img_IG = np.zeros((224,224,3),dtype = np.float32)
        img_IG[:,:,0]=gray_IG*0/255.
        img_IG[:,:,1]=gray_IG*0/255.
        img_IG[:,:,2]=gray_IG*1.
        
        #Anchor
        Anchor_np = np.array(Anchor, dtype = np.uint8)
        gray_Anchor = cv2.cvtColor(Anchor_np, cv2.COLOR_BGR2GRAY)
        threshed_anchor = cv2.adaptiveThreshold(gray_Anchor, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0)
        
        img_anchor = np.zeros((224,224,3),dtype = np.float32)
        img_anchor[:,:,0]=threshed_anchor*255./255.
        img_anchor[:,:,1]=threshed_anchor*223./255.
        img_anchor[:,:,2]=threshed_anchor*0/255.

        mask = img_shap + img_lime + img_IG  + img_anchor
        # normalize the mask
        img_mask = (mask/np.float(np.max(mask)) )*255.

        # open cv alpha blending with weights
        # convert input image to array
        input_image_array = np.array(input_image*255.,dtype=np.float32)

        dst = cv2.addWeighted(input_image_array, 1, img_mask, 0.8, 0)
        dst_I = cv2.bitwise_and(input_image_array,img_mask,input_image_array)
        self.FFT(input_image_array,dst,dst_I)
    

    def callForMethods(self):
        # get model prdictions
        pred_class= self.getPredictions()
        self.anchor_explanations(7,20,0.5,self.image,self.model,"slic")
        self.LIME_explanations(self.model,self.image,pred_class,self.class_names,min_weight=0.05)
        self.integrated_Gradients(self.model,self.image,pred_class,self.pred_class)
        self.Shape_Gradient_Explainer(self.model,self.img_list)
        self.LISA(self.image)
   

    def getPredictions(self):
        import tensorflow as tf
        import matplotlib.pyplot as plt
        
        pred_prob = self.model.predict(tf.expand_dims(self.image,axis=0))
        pred_class = self.class_names[pred_prob[0].argmax()]
        return pred_class
      
    