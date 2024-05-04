# from transformers import AutoTokenizer, AutoModel
#
# # Define file paths using raw strings or double backslashes
# tokenizer_path = r"D:\Desktop\FYP\chatglm-6b-int4"
# model_path = r"D:\Desktop\FYP\chatglm-6b-int4"
#
# # Load tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True, revision="")
# model = AutoModel.from_pretrained(model_path, trust_remote_code=True, revision="").half().cuda()
#
# # Apply quantization to the model's weights
# model = model.quantize(bits=4, kernel_file=r"D:\Desktop\FYP\chatglm-6b-int4\quantization_kernels.so")
#
# # Set the model to evaluation mode
# model = model.eval()
#
# # Perform inference
# response, history = model.chat(tokenizer, "你好", history=[])
# print(response)
# response, history = model.chat(tokenizer, "晚上睡不着该怎么办", history=[])
# print(response)\\
model_path = "D:\Desktop\FYP\chatglm-6b-int4"

from langchain_community.llms import ChatGLM

endpoint_url = "http://127.0.0.1:8000"
llm = ChatGLM(endpoint_url=endpoint_url, max_token=80000,
              top_p=0.9)
