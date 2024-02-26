def clean_text(input_file_path, output_file_path):

    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # for exaple “www.ztcprep.com”
        cleaned_content = content.replace('www.ztcprep.com', '')
        
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)
            
        print("text cleaned")
    except Exception as e:
        print(f"error：{e}")


input_file_path = 'salmpe.txt'
output_file_path = 'cleaned_text/input.txt'

clean_text(input_file_path, output_file_path)
