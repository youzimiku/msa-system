Add-Type -AssemblyName System.Drawing
$src = 'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\_flowchart.png'
$img = [System.Drawing.Image]::FromFile($src)
$w = 1200
$h = [int]($img.Height * $w / $img.Width)
$bmp = New-Object System.Drawing.Bitmap($w, $h)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.InterpolationMode = 'HighQualityBicubic'
$g.DrawImage($img, 0, 0, $w, $h)
$out = 'C:\Users\youzi\Doubao\chats\2026-09-03\new-chat\MSA系统\_flowchart_small.jpg'
$bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$g.Dispose()
$bmp.Dispose()
$img.Dispose()
Write-Output ('saved ' + (Get-Item $out).Length)
