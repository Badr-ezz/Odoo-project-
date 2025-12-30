$configPath = "C:\Program Files\Odoo 17.0.20251228\server\odoo.conf"
$content = Get-Content $configPath
$newContent = @()

foreach ($line in $content) {
    if ($line -match "^addons_path = ") {
        $newContent += "addons_path = C:\Program Files\Odoo 17.0.20251228\server\odoo\addons,C:\Users\Anas\Desktop\Projet Odoo\odoo_custom_addons"
    } else {
        $newContent += $line
    }
}

$newContent | Set-Content $configPath
Write-Host "odoo.conf updated successfully!"
