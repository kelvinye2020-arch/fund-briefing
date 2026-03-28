# 双推脚本：同时推送到 GitHub 和工蜂

Write-Host "正在推送到 GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host "正在推送到工蜂..." -ForegroundColor Yellow
git push gitcode main

Write-Host "✅ 双线推送完成！" -ForegroundColor Green
Write-Host "GitHub: https://github.com/kelvinye2020-arch/fund-briefing"
Write-Host "工蜂:   https://git.woa.com/kelvinyye/fund-briefing"
