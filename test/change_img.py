from PIL import Image
import os.path


def change_img(img_file,  width=706, height=400):
    img = Image.open(img_file)
    try:
        new_img = img.resize((width, height), Image.ANTIALIAS)
        # new_img.save(os.path.join(out_dir, os.path.basename(img_file)))
        new_img.save(img_file)
    except Exception as e:
        print(e)


file4 = r'C:\Users\16529\Mygit\Mongo_API\images\mongo4.png'
file5 = r'C:\Users\16529\Mygit\Mongo_API\images\mongo3.png'
file6 = r'C:\Users\16529\Mygit\Mongo_API\images\mong7.png'

if __name__ == '__main__':
    change_img(file6, width=555, height=455)

