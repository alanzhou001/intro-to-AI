def right_justified(s):
    # 每行最大字符数
    max_length = 72
    # 结果列表
    result_lines = []

    # 按72个字符为一行进行分割
    for i in range(0, len(s), max_length):
        line = s[i:i + max_length]
        # 计算需要填充的空格数量
        spaces_needed = max_length - len(line)
        # 右对齐当前行
        result_lines.append(' ' * spaces_needed + line)

    # 将所有右对齐的行合并为一个字符串
    result = '\n'.join(result_lines)
    return result