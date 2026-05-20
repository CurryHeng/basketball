$apiKey = "5e23e236-ba97-4690-b126-79495db71fd5"
$headers = @{
    "Authorization" = $apiKey
}
$response = Invoke-RestMethod -Uri "https://api.balldontlie.io/v1/players?per_page=100" -Headers $headers -Method Get
$response | ConvertTo-Json -Depth 10
