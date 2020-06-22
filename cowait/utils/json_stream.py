import json


def json_stream(stream):
    buffer = ''
    for log in stream:
        buffer += str(log, encoding='utf-8')

        while '\n' in buffer:
            split = buffer.find('\n')
            chunk = buffer[:split]
            buffer = buffer[split+1:]

            if len(chunk) == 0:
                continue

            yield json.loads(chunk)
