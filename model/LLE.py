from keras.layers import Input, Conv2D, Conv2DTranspose, Concatenate
from keras.applications.vgg19 import VGG19
from keras.models import Model
import keras
import cv2
import numpy as np


class LLE:
    def __init__(self, input_shape=None, weights=None):
        self.model = self.build_mbllen(input_shape or (None, None, 3))
        self.model.load_weights(weights or './weights.h5')
        opt = keras.optimizers.Adam(lr=2 * 1e-04, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
        self.model.compile(loss='mse', optimizer=opt)


    def EM(self, input, kernal_size, channel):
        conv_1 = Conv2D(channel, (3, 3), activation='relu',
                        padding='same', data_format='channels_last')(input)
        conv_2 = Conv2D(channel, (kernal_size, kernal_size), activation='relu',
                        padding='valid', data_format='channels_last')(conv_1)
        conv_3 = Conv2D(channel*2, (kernal_size, kernal_size), activation='relu',
                        padding='valid', data_format='channels_last')(conv_2)
        conv_4 = Conv2D(channel*4, (kernal_size, kernal_size), activation='relu',
                        padding='valid', data_format='channels_last')(conv_3)
        conv_5 = Conv2DTranspose(channel*2, (kernal_size, kernal_size),
                                    activation='relu', padding='valid', data_format='channels_last')(conv_4)
        conv_6 = Conv2DTranspose(channel, (kernal_size, kernal_size), activation='relu',
                                    padding='valid', data_format='channels_last')(conv_5)
        res = Conv2DTranspose(3, (kernal_size, kernal_size), activation='relu',
                                padding='valid', data_format='channels_last')(conv_6)
        return res

    def build_vgg(self):
        vgg_model = VGG19(include_top=False, weights='imagenet')
        vgg_model.trainable = False
        return Model(inputs=vgg_model.input, outputs=vgg_model.get_layer('block3_conv4').output)

    def build_mbllen(self, input_shape):
        inputs = Input(shape=input_shape)
        FEM = Conv2D(32, (3, 3), activation='relu', padding='same', data_format='channels_last')(inputs)
        EM_com = self.EM(FEM, 5, 8)

        for j in range(3):
            for i in range(3):
                FEM = Conv2D(32, (3, 3), activation='relu', padding='same', data_format='channels_last')(FEM)
                EM1 = self.EM(FEM, 5, 8)
                EM_com = Concatenate(axis=3)([EM_com, EM1])

        outputs = Conv2D(3, (1, 1), activation='relu', padding='same', data_format='channels_last')(EM_com)
        return Model(inputs, outputs)

    def predict(self, img, lowpercent = 5, highpercent = 95, maxrange = 0.8, hsvgamma = 0.8):
        img_in = img / 255.
        b, g, r = cv2.split(img_in)
        img_in = cv2.merge([r, g, b])
        img_in = img_in[np.newaxis, :]

        out_pred = self.model.predict(img_in)

        fake_B = out_pred[0, :, :, :3]
        gray_fake_B = fake_B[:, :, 0] * 0.299 + fake_B[:, :, 1] * 0.587 + fake_B[:, :, 1] * 0.114
        percent_max = sum(sum(gray_fake_B >= maxrange))/sum(sum(gray_fake_B <= 1.0))
        max_value = np.percentile(gray_fake_B[:], highpercent)

        if percent_max < (100-highpercent)/100.:
            scale = maxrange / max_value
            fake_B = fake_B * scale
            fake_B = np.minimum(fake_B, 1.0)

        gray_fake_B = fake_B[:,:,0]*0.299 + fake_B[:,:,1]*0.587 + fake_B[:,:,1]*0.114
        sub_value = np.percentile(gray_fake_B[:], lowpercent)
        fake_B = (fake_B - sub_value)*(1./(1-sub_value))
        imgHSV = cv2.cvtColor(fake_B, cv2.COLOR_RGB2HSV)
        
        H, S, V = cv2.split(imgHSV)
        S = np.power(S, hsvgamma)
        imgHSV = cv2.merge([H, S, V])
        fake_B = cv2.cvtColor(imgHSV, cv2.COLOR_HSV2RGB)
        fake_B = np.minimum(fake_B, 1.0)

        outputs = fake_B
        outputs = np.minimum(outputs, 1.0)
        outputs = np.maximum(outputs, 0.0)

        r, g, b = cv2.split(outputs*255)
        img_out = cv2.merge([b, g, r])
        return img_out
        

    

    
