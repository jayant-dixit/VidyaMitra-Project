import google.generativeai as genai

genai.configure(api_key="AIzaSyA1HK1yyPkZ1psx6nMdzzIwi9ZReksQfOo")

for m in genai.list_models():
    print(m.name)
    print(m.supported_generation_methods)
    print(m.supported_generation_methods)