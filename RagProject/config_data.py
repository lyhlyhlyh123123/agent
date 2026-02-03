md5_path = "./md5.text"

#chroma
collection_name = "rag"
persist_directory = "./chroma_db"


chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "", ".","。", "!", "?", "!","？","！"]
max_split_char_number = 1000


similarity_threshold = 2


embedding_model_name  = "text-embedding-v4"
chat_model_name = "qwen-max"
dashscope_api_key  = "sk-54c5cde195864e09a43673ca5a930b43"
tongyi_api_key = "sk-54c5cde195864e09a43673ca5a930b43"


session_config = {
        "configurable": {
            "session_id": "user_2"
        }
    }