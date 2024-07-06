import csv

def ucs2_to_binary_string(text):
    # Encode the text into UCS-2 (UTF-16) bytes
    ucs2_bytes = text.encode('utf-16be')

    # Convert each byte to binary representation
    binary_string = ''.join(format(byte, '08b') for byte in ucs2_bytes)

    return binary_string

def sms_encoding_info(text):
    # Define GSM-7 characters and extended characters
    gsm_7_chars = set(
        '@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1BÆæßÉ !"#¤%&\'()*+,-./0123456789:;<=>?'
        '¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà'
    )
    gsm_7_extended_chars = set('^{}\\[~]|€')

    # Check if the text can be encoded in GSM-7
    can_use_gsm_7 = all(char in gsm_7_chars or char in gsm_7_extended_chars for char in text)

    # Prepare the CSV data
    csv_data = []

    if can_use_gsm_7:
        encoding = "GSM-7"
        bit_length = 0
        char_count = 0
        segment = 1

        for char in text:
            if char in gsm_7_extended_chars:
                byte_size = 2  # 14 bits = 2 bytes
                bit_length += 14
            else:
                byte_size = 1  # 7 bits = 1 byte
                bit_length += 7

            # Append to CSV data
            hex_repr = f"0x{ord(char):04X}"
            csv_data.append([char, hex_repr, encoding, byte_size, segment])

            # Update character count and segment if necessary
            char_count += byte_size
            if char_count >= 160:
                segment += 1
                char_count = 0

        # Calculate the number of SMS segments needed
        if bit_length <= 1120:
            sms_count = 1
        else:
            sms_count = (bit_length + 105) // 106

    else:
        encoding = "UCS-2"
        bit_length = 0
        char_count = 0
        segment = 1

        # Convert text to UCS-2 binary string
        binary_string = ucs2_to_binary_string(text)

        # Calculate bit length based on UCS-2 encoding
        bit_length = len(binary_string)

        i = 0
        while i < len(text):
            char = text[i]
            if 0xD800 <= ord(char) >= 0xDBFF:
                # Surrogate pair (two 16-bit code units)
                byte_size = 4  # 32 bits = 4 bytes
                hex_repr = 'U+{:X}'.format(ord(char))
                csv_data.append([char, hex_repr, encoding, byte_size, segment])
                  # Move to the next character pair
            else:
                byte_size = 2  # 16 bits = 2 bytes
                hex_repr = f"0x{ord(char):04X}"
                csv_data.append([char, hex_repr, encoding, byte_size, segment])

            i += 1

            # Update character count and segment if necessary
            char_count += byte_size // 2
            if char_count >= 70:
                segment += 1
                char_count = 0

        # Calculate the number of SMS segments needed
        if bit_length <= 1120:
            sms_count = 1
        else:
            sms_count = (bit_length + 1119) // 1120

    # Save CSV data to file
    with open('sms_encoding_info.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([f'Number of SMS: {sms_count}'])
        csv_writer.writerow(['Character', 'Hex', 'Encoding', 'Byte', 'Segment'])
        csv_writer.writerows(csv_data)

    return encoding, bit_length

# Example usage:
if __name__ == "__main__":
    text_ucs_2 = "Rumors say there will be free healthy smoothies at the Twilio booth 🥤🍓🍍"
    text_gsm_7 = "Ahoy World"
    encoding, bit_length = sms_encoding_info(text_ucs_2)
    print(f"Encoding: {encoding}, Bit length: {bit_length}")

    #encoding, bit_length = sms_encoding_info(text_gsm_7)
    #print(f"Encoding: {encoding}, Bit length: {bit_length}")
