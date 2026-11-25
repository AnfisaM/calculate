from PIL import Image
import math
import sys
from datetime import datetime

blur_kernel = [1, 1, 1,
          1, 1, 1,
          1, 1, 1]
sharp_kernel=[0, -1, 0,
             -1, 5, -1,
             0, -1, 0]


def convolution(image, kernel, scale):
    width, height = image.size
    result = image.copy()
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            top_left = image.getpixel((x - 1, y - 1))
            top = image.getpixel((x, y - 1))
            top_right = image.getpixel((x + 1, y - 1))

            left = image.getpixel((x - 1, y))
            center = image.getpixel((x, y))
            right = image.getpixel((x + 1, y))

            bottom_left = image.getpixel((x - 1, y + 1))
            bottom = image.getpixel((x, y + 1))
            bottom_right = image.getpixel((x + 1, y + 1))

            pixels = [top_left, top, top_right,left, center, right,bottom_left, bottom, bottom_right]
            r = 0
            g = 0
            b = 0

            for i in range(9):
                r += pixels[i][0] * kernel[i]
                g += pixels[i][1] * kernel[i]
                b += pixels[i][2] * kernel[i]

            r = round(r / scale)
            g = round(g / scale)
            b = round(b / scale)

            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            result.putpixel((x, y), (r, g, b))
    return result

def calculate_mean(image):
    width, height = image.size
    total_pixels = width * height

    r_sum = 0
    g_sum = 0
    b_sum = 0
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))

            r_sum += r
            g_sum += g
            b_sum += b

    r_mean = r_sum / total_pixels
    g_mean = g_sum / total_pixels
    b_mean = b_sum / total_pixels

    return r_mean, g_mean, b_mean

#Стандартное отклонение
def calculate_std(image, mean):
    width, height = image.size
    total_pixels = width * height

    r_mean, g_mean, b_mean = mean

    r_sum = 0
    g_sum = 0
    b_sum = 0
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))

            r_sum+= (r-r_mean)**2
            g_sum+= (g-g_mean)**2
            b_sum+= (b-b_mean)**2

    r_std= math.sqrt(r_sum/total_pixels)
    g_std= math.sqrt(g_sum/total_pixels)
    b_std= math.sqrt(b_sum/total_pixels)

    return r_std, g_std, b_std

def color_correction(image, template):
    mean = calculate_mean(image)
    std = calculate_std(image, mean)

    template_mean = calculate_mean(template)
    template_std = calculate_std(template, template_mean)
    r_mean, g_mean, b_mean = mean
    r_std, g_std, b_std = std

    r_template_mean, g_template_mean, b_template_mean = template_mean
    r_template_std, g_template_std, b_template_std = template_std
    
    width, height = image.size
    result = image.copy()
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            if r_std != 0:
                r_new = (r - r_mean) * (r_template_std / r_std) + r_template_mean
            else:
                r_new = r_template_mean

            r_new = round(r_new)
            r_new = max(0, min(255, r_new))

            if g_std != 0:
                g_new = (g - g_mean) * (g_template_std / g_std) + g_template_mean
            else:
                g_new = g_template_mean

            g_new = round(g_new)
            g_new = max(0, min(255, g_new))

            if b_std != 0:
                b_new = (b - b_mean) * (b_template_std / b_std) + b_template_mean
            else:
                b_new =b_template_mean 

            b_new = round(b_new)
            b_new = max(0, min(255, b_new))

            result.putpixel((x, y), (r_new, g_new, b_new))
    return result

def write_log(filename, algorithm, status):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open("logs/history.txt", "a", encoding="utf-8") as file:
            file.write(f"[{date}] Файл: {filename} | Фильтр: {algorithm} | Статус: {status}\n")

    except OSError:
        print("Ошибка: не удалось записать данные в журнал")
   
# Открываем изображение
def open_image(path):
    filename = path.split("/")[-1]
    try:
        with Image.open(path) as image:
            return image.convert("RGB")

    except FileNotFoundError:
        print("Ошибка: Файл не найден")
        write_log(filename, "Открытие", "Ошибка: файл не найден")
        sys.exit(1)

    except PermissionError:
        print(f"Ошибка: Нет прав на чтение файла {filename}. Обратитесь к администратору")
        write_log(filename, "Открытие", "Ошибка доступа")
        sys.exit(1)

    except OSError:
        print("Ошибка: Не удалось прочитать изображение")
        write_log(filename, "Открытие", "Ошибка чтения")
        sys.exit(1)

# Сохранение изображения и обработка ошибок

def save_image(image, path, filename, algorithm):
    try:
        image.save(path)

    except OSError:
        print("Не удалось сохранить изображение")
        write_log(filename, algorithm, "Ошибка сохранения")
        sys.exit(1)

    write_log(filename, algorithm, "Успешно")

# Запрашиваем название изображения
filename = input("Введите название изображения: ")
image_path = "data/input/" + filename

image = open_image(image_path)
template = open_image("data/input/image2.png")

# Выбор фильтра
print("Выберите фильтр для итогового изображения:")
print("1 — Размытие")
print("2 — Повышение резкости")

choice = input("Введите номер фильтра: ")

if choice != "1" and choice != "2":
    print("Ошибка: неизвестный фильтр")
    sys.exit(1)

# Отдельная цветокоррекция
corrected_image = color_correction(image, template)
save_image(corrected_image, "data/output/corrected.png", filename, "Цветокоррекция")

# Отдельное размытие
blurred_image = convolution(image, blur_kernel, 9)
save_image(blurred_image, "data/output/blurred.png", filename, "Размытие")

# Отдельное повышение резкости
sharp_image = convolution(image, sharp_kernel, 1)
save_image(sharp_image, "data/output/sharp.png",filename, "Повышение резкости")

# Выбираем изображение для итоговой обработки
if choice == "1":
    filtered_image = blurred_image
    algorithm = "Размытие"

else:
    filtered_image = sharp_image
    algorithm = "Повышение резкости"

# Итоговая обработка
result_image = color_correction(filtered_image, template)

save_image(result_image, "data/output/result.jpg", filename, algorithm + " + Цветокоррекция")

# Выводим информацию
print("Размер изображения:", result_image.size)
print("Цветовой режим:", result_image.mode)
print("Обработка завершена")