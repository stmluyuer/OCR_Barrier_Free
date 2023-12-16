# 简单的OCR无障碍应用。
## 使用的 API

-  RecognizeGeneral
-  pytesseract

## 使用说明

OCR_Barrier_Free下有2个版本，本地和云端版本，云端版本需要自行配置env，使用的是RecognizeGeneral，阿里云的通用识别,需要使用ALIBABA_CLOUD_ACCESS_KEY_ID和ALIBABA_CLOUD_ACCESS_KEY_SECRET。
本地版本需要本地机存在pytesseract，及自行训练的识别模型，位置模型。

云端效果较好，但采用的阿里云api，需要付费，作为教育产品可能较贵
本地版本部署难度大，需要自行完成部署。

目前正尝试将我训练好的模型部署到云端上以供使用，缺陷是云端CPU局限性太大，GPU价格昂贵。

