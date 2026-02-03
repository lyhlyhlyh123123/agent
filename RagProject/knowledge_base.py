import hashlib
import os
from datetime import datetime

import config_data as config
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
def check_md3(md5str: str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            if line.strip() == md5str:
                return True

        return False



def save_md3(md5str: str):
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5str + '\n')


def get_string_md5(string: str):
    return hashlib.md5(string.encode('utf-8')).hexdigest()

class KnowledgeBaseService:

    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)

        self.chroma = Chroma(
            persist_directory=config.persist_directory,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4",dashscope_api_key="apikey"),
            collection_name=config.collection_name,
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )


    def upload_by_str(self,data,file_name):
        if check_md3(get_string_md5(data)):
            return "[跳过]内容已存在"
        if len(data)>config.max_split_char_number:
            knowledge_chucks = self.splitter.split_text(data)
        else:
            knowledge_chucks = [data]


        meta_data = {
            "source": file_name,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "admin",
        }

        self.chroma.add_texts(texts=knowledge_chucks,metadatas=[meta_data for _ in knowledge_chucks])

        save_md3(get_string_md5(data))

        return "[完成]上传成功"


if __name__ == '__main__':
    kbs = KnowledgeBaseService()
    print(kbs.upload_by_str('123456','123456'))

    # save_md3(get_string_md5('123456'))
    # print(check_md3(get_string_md5('123456')))

    # print(get_string_md5('123456'))
    # print(get_string_md5('123456'))
    # print(get_string_md5('123456'))
    # print(get_string_md5('1234567'))
