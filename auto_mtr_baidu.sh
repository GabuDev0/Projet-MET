#!/bin/bash
# ============================================
# 文件路径
OUTPUT_FILE="$HOME/Desktop/MET/reports.json"

# 如果文件不存在，先创建一个空 JSON 词典
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "[]" > "$OUTPUT_FILE"
fi

# 每小时循环执行
while true
do
    # 当前时间
    current_time=$(date +"%Y-%m-%d_%Hh%M")

    echo "Executing mtr at $current_time ..."

    # 获取 mtr JSON 输出
    MTR_JSON=$(sudo mtr -n -r -c 10 --json baidu.com)

    # 构建带时间戳的新 JSON 条目
    NEW_ENTRY=$(jq -n --arg time "$current_time" --argjson report "$MTR_JSON" \
        '{($time): $report}')


    # 使用 jq 将新条目追加到原 JSON 数组
    TMP_FILE=$(mktemp)
    jq ". += [$NEW_ENTRY]" "$OUTPUT_FILE" > "$TMP_FILE" && mv "$TMP_FILE" "$OUTPUT_FILE"

    echo "Report saved to $OUTPUT_FILE"

    # 等待 1 小时
    sleep 3600
done
