# Архиватор файлов делал на задании

import os
import pickle
import struct
from collections import Counter

class SimpleArchiver:
    def __init__(self, compression_mode='rle+huffman'):
        valid_modes = {'rle', 'huffman', 'rle+huffman', 'lz77'}
        if compression_mode not in valid_modes:
            raise ValueError(f"Недопустимый режим сжатия: {compression_mode}. "
                             f"Допустимые: {', '.join(valid_modes)}")
        self.compression_mode = compression_mode

    # ========================
    # Битовые утилиты (только для битовых строк '0101...')
    # ========================
    def bitstring_to_bytes(self, s):
        if not s:
            return b''
        padding = (8 - len(s) % 8) % 8
        s_padded = s + '0' * padding
        byte_arr = bytearray()
        for i in range(0, len(s_padded), 8):
            byte_val = int(s_padded[i:i+8], 2)
            byte_arr.append(byte_val)
        return bytes(byte_arr)

    def bytes_to_bitstring(self, b):
        return ''.join(f'{byte:08b}' for byte in b)

    # ========================
    # RLE
    # ========================
        # ========================
    # RLE
    # ========================
    def rle_encode(self, data):
        if not data:
            return ""
        encoded = []
        i = 0
        n = len(data)
        while i < n:
            count = 1
            current = data[i]
            while i + count < n and data[i + count] == current:
                count += 1
            encoded.append(current + str(count))
            i += count
        return ''.join(encoded)

    def rle_decode(self, data):
        if not data:
            return ""
        decoded = []
        i = 0
        n = len(data)
        while i < n:
            char = data[i]
            i += 1
            num_str = ''
            while i < n and data[i].isdigit():
                num_str += data[i]
                i += 1
            count = int(num_str) if num_str else 1
            decoded.append(char * count)
        return ''.join(decoded)

    # ========================
    # Хаффман
    # ========================
    def huffman_encode(self, text):
        if not text:
            return "", {}
        freq = Counter(text)
        heap = [[weight, [char, ""]] for char, weight in freq.items()]
        while len(heap) > 1:
            heap.sort(key=lambda x: x[0])
            lo = heap.pop(0)
            hi = heap.pop(0)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heap.append([lo[0] + hi[0]] + lo[1:] + hi[1:])
        huff_dict = {char: code for char, code in heap[0][1:]}
        encoded = ''.join(huff_dict[char] for char in text)
        return encoded, huff_dict

    def huffman_decode(self, bitstring, codes):
        if not bitstring or not codes:
            return ""
        reverse_map = {v: k for k, v in codes.items()}
        decoded = []
        current = ""
        for bit in bitstring:
            current += bit
            if current in reverse_map:
                decoded.append(reverse_map[current])
                current = ""
        return ''.join(decoded)

    # ========================
    # LZ77 (упрощённый)
    # ========================
    def lz77_encode(self, data, window_size=20, lookahead=15):
        if not data:
            return []
        result = []
        i = 0
        n = len(data)
        while i < n:
            best_len = 0
            best_offset = 0
            search_start = max(0, i - window_size)
            for j in range(search_start, i):
                length = 0
                while (i + length < n and
                       j + length < i and
                       data[j + length] == data[i + length] and
                       length < lookahead):
                    length += 1
                if length > best_len:
                    best_len = length
                    best_offset = i - j
            next_char = data[i + best_len] if i + best_len < n else ''
            result.append((best_offset, best_len, next_char))
            i += best_len + (1 if next_char else 0)
        return result

    def lz77_decode(self, encoded):
        if not encoded:
            return ""
        result = []
        for offset, length, next_char in encoded:
            if length > 0:
                start = len(result) - offset
                for k in range(length):
                    result.append(result[start + k])
            if next_char:
                result.append(next_char)
        return ''.join(result)

    # ========================
    # Сжатие файла
    # ========================
    def compress_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise ValueError(f"Не удалось прочитать файл {filepath} как UTF-8 текст: {e}")

        original_size = len(content)

        if self.compression_mode == 'rle':
            comp = self.rle_encode(content)
            return comp, {}, original_size
        elif self.compression_mode == 'huffman':
            bits, codes = self.huffman_encode(content)
            return bits, codes, original_size
        elif self.compression_mode == 'rle+huffman':
            rle = self.rle_encode(content)
            bits, codes = self.huffman_encode(rle)
            return bits, codes, original_size
        elif self.compression_mode == 'lz77':
            lz = self.lz77_encode(content)
            return lz, {}, original_size
        else:
            raise RuntimeError("Недопустимый режим")

    def decompress_file(self, compressed_data, codes, original_size):
        if self.compression_mode == 'rle':
            return self.rle_decode(compressed_data)
        elif self.compression_mode == 'huffman':
            return self.huffman_decode(compressed_data, codes)
        elif self.compression_mode == 'rle+huffman':
            rle = self.huffman_decode(compressed_data, codes)
            return self.rle_decode(rle)
        elif self.compression_mode == 'lz77':
            return self.lz77_decode(compressed_data)
        else:
            raise RuntimeError("Недопустимый режим")

    # ========================
    # Создание архива
    # ========================
    def create_archive(self, archive_name, filepaths):
        if not filepaths:
            raise ValueError("Список файлов пуст")

        mode_map = {'rle': 0, 'huffman': 1, 'rle+huffman': 2, 'lz77': 3}
        mode_byte = mode_map[self.compression_mode]

        valid_files = []
        for fp in filepaths:
            if not os.path.isfile(fp):
                print(f"⚠️ Пропускаем (не файл или не существует): {fp}")
                continue
            valid_files.append(fp)

        if not valid_files:
            raise ValueError("Нет валидных файлов для архивации")

        os.makedirs(os.path.dirname(os.path.abspath(archive_name)) or '.', exist_ok=True)

        with open(archive_name, 'wb') as arc:
            arc.write(struct.pack('B', mode_byte))
            arc.write(struct.pack('B', len(valid_files)))

            for fp in valid_files:
                filename = os.path.basename(fp)
                comp_data, codes, orig_size = self.compress_file(fp)

                arc.write(struct.pack('B', len(filename)))
                arc.write(filename.encode('utf-8'))
                arc.write(struct.pack('I', orig_size))

                if self.compression_mode == 'lz77':
                    data_bytes = pickle.dumps(comp_data)
                    arc.write(struct.pack('I', len(data_bytes)))
                    arc.write(data_bytes)
                    arc.write(struct.pack('I', 0))  # no codes

                elif self.compression_mode == 'rle':
                    # RLE: сохраняем как UTF-8 строку
                    data_bytes = comp_data.encode('utf-8')
                    arc.write(struct.pack('I', len(data_bytes)))
                    arc.write(data_bytes)
                    arc.write(struct.pack('I', 0))  # no codes

                else:  # huffman or rle+huffman
                    bit_data = comp_data  # строка из '0' и '1'
                    byte_data = self.bitstring_to_bytes(bit_data)
                    arc.write(struct.pack('I', len(byte_data)))
                    arc.write(byte_data)
                    codes_bytes = pickle.dumps(codes)
                    arc.write(struct.pack('I', len(codes_bytes)))
                    arc.write(codes_bytes)

    # ========================
    # Распаковка архива
    # ========================
    def extract_archive(self, archive_name, extract_to):
        if not os.path.isfile(archive_name):
            raise FileNotFoundError(f"Архив не найден: {archive_name}")

        os.makedirs(extract_to, exist_ok=True)
        extract_abs = os.path.abspath(extract_to)

        with open(archive_name, 'rb') as arc:
            mode_byte = struct.unpack('B', arc.read(1))[0]
            mode_rev = {0: 'rle', 1: 'huffman', 2: 'rle+huffman', 3: 'lz77'}
            if mode_byte not in mode_rev:
                raise ValueError("Повреждённый архив: неизвестный режим")
            self.compression_mode = mode_rev[mode_byte]

            num_files = struct.unpack('B', arc.read(1))[0]
            if num_files == 0:
                print("Архив пуст")
                return

            metadata = []
            for _ in range(num_files):
                name_len = struct.unpack('B', arc.read(1))[0]
                name = arc.read(name_len).decode('utf-8')
                orig_size = struct.unpack('I', arc.read(4))[0]
                data_len = struct.unpack('I', arc.read(4))[0]
                codes_len = struct.unpack('I', arc.read(4))[0] if self.compression_mode not in ('rle', 'lz77') else 0
                pos = arc.tell()
                metadata.append((name, orig_size, data_len, codes_len, pos))
                arc.seek(data_len + (codes_len if self.compression_mode not in ('rle', 'lz77') else 0), 1)

            for name, orig_size, data_len, codes_len, pos in metadata:
                arc.seek(pos)
                if self.compression_mode == 'lz77':
                    data_bytes = arc.read(data_len)
                    comp_data = pickle.loads(data_bytes)
                    codes = {}
                elif self.compression_mode == 'rle':
                    data_bytes = arc.read(data_len)
                    comp_data = data_bytes.decode('utf-8')
                    codes = {}
                else:  # huffman or rle+huffman
                    byte_data = arc.read(data_len)
                    bitstring = self.bytes_to_bitstring(byte_data)
                    comp_data = bitstring
                    codes_bytes = arc.read(codes_len)
                    codes = pickle.loads(codes_bytes) if codes_bytes else {}

                try:
                    content = self.decompress_file(comp_data, codes, orig_size)
                except Exception as e:
                    print(f"❌ Ошибка декомпрессии {name}: {e}")
                    continue

                out_path = os.path.abspath(os.path.join(extract_to, name))
                # Защита от path traversal
                if not out_path.startswith(extract_abs + os.sep) and out_path != extract_abs:
                    raise ValueError(f"Попытка выхода за пределы: {out_path}")

                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Извлечено: {name}")


# ========================
# Вспомогательные функции ввода
# ========================
def create_test_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Файл {filename} создан.")

def get_user_input():
    print("\n=== Создание тестовых файлов ===")
    files = []
    while True:
        name = input("Введите имя файла (или 'готово' для завершения): ").strip()
        if name.lower() in ('готово', 'done', ''):
            break
        if not name:
            print("Имя не может быть пустым.")
            continue
        content = input(f"Введите содержимое для {name}: ")
        create_test_file(name, content)
        files.append(name)
    return files

def choose_compression_mode():
    modes = {
        '1': 'rle',
        '2': 'huffman',
        '3': 'rle+huffman',
        '4': 'lz77'
    }
    print("\nВыберите режим сжатия:")
    print("1. RLE")
    print("2. Хаффман")
    print("3. RLE + Хаффман")
    print("4. LZ77")
    while True:
        choice = input("Ваш выбор (1-4): ").strip()
        if choice in modes:
            return modes[choice]
        print("Неверный выбор. Попробуйте снова.")


# ========================
# Основная программа
# ========================
def main():
    test_files = []
    archive_name = "my_archive.sa"
    extract_dir = "extracted"

    try:
        test_files = get_user_input()
        if not test_files:
            print("Нет файлов для архивации. Завершение.")
            return

        mode = choose_compression_mode()
        print(f"\nВыбран режим: {mode}")

        archiver = SimpleArchiver(compression_mode=mode)
        archiver.create_archive(archive_name, test_files)
        print(f"\nАрхив {archive_name} успешно создан!")

        archiver.extract_archive(archive_name, extract_dir)
        print(f"\nФайлы распакованы в папку: {extract_dir}")

        print("\n🔍 Проверка целостности:")
        all_ok = True
        for fname in test_files:
            with open(fname, 'r', encoding='utf-8') as f1:
                orig = f1.read()
            with open(os.path.join(extract_dir, fname), 'r', encoding='utf-8') as f2:
                extracted = f2.read()
            if orig == extracted:
                print(f"✅ {fname} — совпадает")
            else:
                print(f"❌ {fname} — НЕ совпадает!")
                all_ok = False

        if all_ok:
            print("\n🎉 Все файлы успешно сжаты и восстановлены!")
        else:
            print("\n⚠️ Обнаружены расхождения!")

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

    finally:
        cleanup = input("\nУдалить тестовые файлы и архив? (y/n): ").strip().lower()
        if cleanup == 'y':
            for f in test_files:
                if os.path.exists(f):
                    os.remove(f)
            if os.path.exists(archive_name):
                os.remove(archive_name)
            if os.path.exists(extract_dir):
                import shutil
                shutil.rmtree(extract_dir)
            print("Файлы удалены.")


if __name__ == "__main__":
    main()