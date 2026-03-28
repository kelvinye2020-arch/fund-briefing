#!/bin/bash
# 双推脚本：同时推送到 GitHub 和工蜂

echo "正在推送到 GitHub..."
git push origin main

echo "正在推送到工蜂..."
git push gitcode main

echo "✅ 双线推送完成！"
echo "GitHub: https://github.com/kelvinye2020-arch/fund-briefing"
echo "工蜂:   https://git.woa.com/kelvinyye/fund-briefing"
