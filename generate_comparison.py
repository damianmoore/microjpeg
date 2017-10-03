from collections import defaultdict
import os
from generate_header import generate_header
from generate_microjpeg import generate_microjpeg
from generate_jpeg import generate_jpeg


def generate_comparison():
    dirname = 'samples'
    conversions = defaultdict(list)

    process_options = [
        # qtable, size
        ('c7_', 32),  # 30%
        ('S03', 32),  # 25%
    ]

    for qtable, size in process_options:
        generate_header(qtable=qtable)

    for filename in os.listdir(dirname):
        for qtable, size in process_options:
            microjpeg_fn, microjpeg_size = generate_microjpeg(os.path.join(dirname, filename), qtable, size)
            jpeg_fn, jpeg_size = generate_jpeg('{}.microjpeg'.format(os.path.splitext(microjpeg_fn)[0]), qtable, size)
            conversions[filename].append((microjpeg_fn, microjpeg_size, jpeg_fn, jpeg_size))

    with open('comparison.html', 'w') as output:
        output.write('<html><body><table>')
        for key, val in conversions.items():
            output.write('<tr><td><img src="samples/{}" style="width: 240px" /><br/>{}</td>'.format(key, key))
            for i, item in enumerate(val):
                output.write('<td><img src="{}" style="width: 240px; image-rendering: -moz-crisp-edges; filter: blur(5px)" /><br/>{} - {} bytes</td>'.format(item[2], process_options[i], item[1]))
            output.write('</tr>'.format(key))
        output.write('</table></body></html>')


if __name__ == '__main__':
    generate_comparison()
