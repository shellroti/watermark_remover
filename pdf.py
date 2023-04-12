import re
import time
import sys
import PyPDF2

def loading_animation():
    animation = "|/-\\"
    for i in range(50):
        time.sleep(0.1)
        sys.stdout.write("\r" + "Loading" + animation[i % len(animation)])
        sys.stdout.flush()

def remove_watermark(input_file, watermark_text, output_file):
    with open(input_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            content = page.extract_text()
            content = re.sub(watermark_text, "", content)

            page_data = b"".join(filter(lambda x: isinstance(x, bytes), page.get_contents())).decode("utf-8")

            new_page_data = re.sub(watermark_text, "", page_data)

            if new_page_data != page_data:
                page.__setitem__(PyPDF2.generic.NameObject("/Contents"),
                                 PyPDF2.generic.TextStringObject(new_page_data))

            writer.add_page(page)

        with open(output_file, "wb") as output:
            writer.write(output)

if __name__ == "__main__":
    input_pdf = "input.pdf"  
    watermark_text = "text"  
    output_pdf = "output.pdf" 

    loading_animation()
    remove_watermark(input_pdf, watermark_text, output_pdf)
    print("\rComplete!")