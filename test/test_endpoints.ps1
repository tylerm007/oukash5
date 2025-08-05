# PowerShell script to test all API endpoints
# Generated automatically from database models

#$BaseUrl = "http://localhost:5656/api"
$BaseUrl = "http://172.30.3.133:5656/api"

Write-Host "🚀 Testing API endpoints with PowerShell..." -ForegroundColor Green

# Array of all endpoints
$endpoints = @(
    "AchAuthToken",
    "AchPlaidLambdaResponse",
    "AchStripePayment",
    "AchStripePaymentDetail",
    "BarCode",
    "Billing",
    "CompanyPlantOption",
    "CompanycontactsTb",
    "COMPANYADDRESSTB",
    "COMPANYCERTDETAIL",
    "COMPANYCOMMENT",
    "COMPANYFEECOMMENT",
    "COMPANYFEESTRUCTURE",
    "COMPANYHOLDTB",
    "COMPANYOTHERNAME",
    "COMPANYSTATUSTB",
    "COMPANYTB",
    "CoPackerFacilitiesCategory",
    "CoPackerFacilitiesLocation",
    "CoPackerFacility",
    "COPRIVATELABELFEEDETAIL",
    "FormulaComponent",
    "FormulaProduct",
    "FormulaSubmissionComponent",
    "FormulaSubmissionPlant",
    "INVOICEFEE",
    "INVOICEFEESDETAIL",
    "LabelBarcode",
    "LabelComment",
    "LabelOption",
    "LabelTb",
    "MERCHCOMMENT",
    "MERCHOTHERNAME",
    "MERCHTB",
    "MiniCRMAction",
    "OWNSTB",
    "PENDINGINFOTB",
    "PERSONADDRESSTB",
    "PERSONJOBSTATUSTB",
    "PERSONJOBTB",
    "PERSONTB",
    "PLANTADDRESSTB",
    "PLANTCERTDETAIL",
    "PLANTCOMMENT",
    "PLANTFEECOMMENT",
    "PLANTFEESTRUCTURE",
    "PLANTFEESTRUCTUREOUT",
    "PLANTHOLDTB",
    "PLANTTB",
    "PRIVATELABELBILL",
    "PrivateLabelTemplate",
    "ProducedIn1Tb",
    "ProductJob",
    "ProductJobLineItem",
    "PurchaseOrder",
    "RCTB",
    "StripeCustomer",
    "ThirdPartyBillingCompany",
    "USEDIN1TB",
    "VISIT",
    "VISITSCOMMENT",
    "YoshonInfo"
)

$successful = 0
$failed = 0
$results = @()

# Test each endpoint
foreach ($endpoint in $endpoints) {
    Write-Host "Testing $endpoint... " -NoNewline
    
    $url = "$BaseUrl/$endpoint"
    
    try {
        $response = Invoke-RestMethod -Uri '$url/page[limit]=1' -Method GET -TimeoutSec 10
        
        $recordCount = 0
        if ($response -is [Array]) {
            $recordCount = $response.Count
        } elseif ($response.data -is [Array]) {
            $recordCount = $response.data.Count
        } elseif ($response.data) {
            $recordCount = 1
        }
        
        Write-Host "✅ Success ($recordCount records)" -ForegroundColor Green
        $successful++
        
        $results += [PSCustomObject]@{
            Endpoint = $endpoint
            Status = "Success"
            RecordCount = $recordCount
            Error = $null
        }
    }
    catch {
        Write-Host "❌ Failed ($($_.Exception.Message))" -ForegroundColor Red
        $failed++
        
        $results += [PSCustomObject]@{
            Endpoint = $endpoint
            Status = "Failed"
            RecordCount = 0
            Error = $_.Exception.Message
        }
    }
    
    Start-Sleep -Milliseconds 100  # Small delay
}

# Print summary
Write-Host ""
Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "========" -ForegroundColor Yellow
Write-Host "Total endpoints: $($endpoints.Count)"
Write-Host "Successful: $successful" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red
Write-Host "Success rate: $([math]::Round(($successful / $endpoints.Count) * 100, 2))%"

# Save results to CSV
$results | Export-Csv -Path "api_test_results.csv" -NoTypeInformation
Write-Host ""
Write-Host "Results saved to api_test_results.csv" -ForegroundColor Cyan

# Show failed endpoints
if ($failed -gt 0) {
    Write-Host ""
    Write-Host "Failed Endpoints:" -ForegroundColor Red
    Write-Host "=================" -ForegroundColor Red
    $results | Where-Object { $_.Status -eq "Failed" } | Format-Table -AutoSize
}
