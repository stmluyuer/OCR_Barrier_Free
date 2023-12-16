# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys
from typing import List
from alibabacloud_ocr_api20210707.client import Client as ocr_api20210707Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ocr_api20210707 import models as ocr_api_20210707_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient
import json
import dotenv

# 加载 .env 文件
dotenv.load_dotenv()
ALIBABA_CLOUD_ACCESS_KEY_ID = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

print(ALIBABA_CLOUD_ACCESS_KEY_ID,ALIBABA_CLOUD_ACCESS_KEY_SECRET)
class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> ocr_api20210707Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/ocr-api
        config.endpoint = f'ocr-api.cn-hangzhou.aliyuncs.com'
        return ocr_api20210707Client(config)

    @staticmethod
    def create_client_with_sts(
        access_key_id: str,
        access_key_secret: str,
        security_token: str,
    ) -> ocr_api20210707Client:
        """
        使用STS鉴权方式初始化账号Client，推荐此方式。
        @param access_key_id:
        @param access_key_secret:
        @param security_token:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret,
            # 必填，您的 Security Token,
            security_token=security_token,
            # 必填，表明使用 STS 方式,
            type='sts'
        )
        # Endpoint 请参考 https://api.aliyun.com/product/ocr-api
        config.endpoint = f'ocr-api.cn-hangzhou.aliyuncs.com'
        return ocr_api20210707Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        image_path = input("请输入图片路径: ")
        image_path = f'img/{image_path}.jpg'  # 替换成你的图片路径
        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()
        client = Sample.create_client(ALIBABA_CLOUD_ACCESS_KEY_ID,ALIBABA_CLOUD_ACCESS_KEY_SECRET)
        recognize_general_request = ocr_api_20210707_models.RecognizeGeneralRequest(
            body=image_content
        )
        runtime = util_models.RuntimeOptions()
        resp = client.recognize_general_with_options(recognize_general_request, runtime)
        json_str = UtilClient.to_jsonstring(resp)

        data = json.loads(json_str)
        ocr_data = json.loads(data['body']['Data'])
        # ocr_data ={"algo_version":"97dbd70e1abbbe1ae999d4f0e30898b2f1c26b39","content":"第二届世界互联网大会将于2015年12月16日至18日在浙江省嘉兴市桐乡市乌 镇举行。大会的主题是\"互联互通、共享共治，共建网络空间命运共同体”。中国政府对此次大会高度重 视，中共中央总书记、中国国家主席习近平将出席大会，并发表主旨演讲。 ","height":137,"orgHeight":137,"orgWidth":935,"prism_version":"1.0.9","prism_wnum":3,"prism_wordsInfo":[{"angle":0,"direction":0,"height":20,"pos":[{"x":33,"y":11},{"x":699,"y":9},{"x":699,"y":30},{"x":34,"y":32}],"prob":99,"width":666,"word":"第二届世界互联网大会将于2015年12月16日至18日在浙江省嘉兴市桐乡市乌","x":33,"y":10},{"angle":-90,"direction":0,"height":878,"pos":[{"x":10,"y":52},{"x":889,"y":51},{"x":889,"y":73},{"x":10,"y":74}],"prob":99,"width":21,"word":"镇举行。大会的主题是\"互联互通、共享共治，共建网络空间命运共同体”。中国政府对此次大会高度重","x":438,"y":-376},{"angle":-90,"direction":0,"height":635,"pos":[{"x":10,"y":95},{"x":645,"y":93},{"x":645,"y":115},{"x":10,"y":117}],"prob":99,"width":22,"word":"视，中共中央总书记、中国国家主席习近平将出席大会，并发表主旨演讲。","x":316,"y":-212}],"width":935}
        # 获取词块信息
        # words_info = ocr_data["prism_wordsInfo"]
        # print(words_info)

        def process_text_by_height(ocr_result): #排序函数
            words_info = ocr_result["prism_wordsInfo"]

            # 根据 y 坐标对词块进行排序
            words_info.sort(key=lambda x: x["pos"][0]["y"])

            # 用于存储处理后的文本段落
            paragraphs = []
            current_paragraph = ""

            # 阈值，用于决定何时开始新的段落
            y_threshold = 10
            last_y = 0

            for word_info in words_info:
                # 获取词块的起始y坐标
                y_coord = word_info["pos"][0]["y"]

                # 如果当前词块与上一个词块的y坐标差超过阈值，则开始新的段落
                if y_coord - last_y > y_threshold and current_paragraph:
                    paragraphs.append(current_paragraph.strip())
                    current_paragraph = ""

                current_paragraph += word_info["word"] + " "
                last_y = y_coord

            # 添加最后一个段落
            if current_paragraph:
                paragraphs.append(current_paragraph.strip())

            # 打印处理后的段落
            for paragraph in paragraphs:
                print(paragraph)
        process_text_by_height(ocr_data)
        input("按任意键关闭程序...")


    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client(ALIBABA_CLOUD_ACCESS_KEY_ID,ALIBABA_CLOUD_ACCESS_KEY_SECRET)
        with open('图片文件路径', 'rb') as image_file:
            image_content = image_file.read()
        recognize_general_request = ocr_api_20210707_models.RecognizeGeneralRequest(
            image_url=image_content
        )
        runtime = util_models.RuntimeOptions()
        resp = await client.recognize_general_with_options_async(recognize_general_request, runtime)
        # ConsoleClient.log(UtilClient.to_jsonstring(resp))
        ocr_data = json.loads(resp["body"]["Data"])["prism_wordsInfo"]
        # print(resp)
        # print("\n",ocr_data)


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
