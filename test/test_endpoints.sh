#!/bin/bash
# Curl script to test all API endpoints
# Generated automatically from database models

BASE_URL="http://localhost:5656/api"

echo "🚀 Testing API endpoints with curl..."

# Array of all endpoints
endpoints=(
    "AchAuthToken"
    "AchPlaidLambdaResponse"
    "AchStripePayment"
    "AchStripePaymentDetail"
    "BarCode"
    "Billing"
    "CompanyPlantOption"
    "CompanycontactsTb"
    "COMPANYADDRESSTB"
    "COMPANYCERTDETAIL"
    "COMPANYCOMMENT"
    "COMPANYFEECOMMENT"
    "COMPANYFEESTRUCTURE"
    "COMPANYHOLDTB"
    "COMPANYOTHERNAME"
    "COMPANYSTATUSTB"
    "COMPANYTB"
    "CoPackerFacilitiesCategory"
    "CoPackerFacilitiesLocation"
    "CoPackerFacility"
    "COPRIVATELABELFEEDETAIL"
    "FormulaComponent"
    "FormulaProduct"
    "FormulaSubmissionComponent"
    "FormulaSubmissionPlant"
    "INVOICEFEE"
    "INVOICEFEESDETAIL"
    "LabelBarcode"
    "LabelComment"
    "LabelOption"
    "LabelTb"
    "MERCHCOMMENT"
    "MERCHOTHERNAME"
    "MERCHTB"
    "MiniCRMAction"
    "OWNSTB"
    "PENDINGINFOTB"
    "PERSONADDRESSTB"
    "PERSONJOBSTATUSTB"
    "PERSONJOBTB"
    "PERSONTB"
    "PLANTADDRESSTB"
    "PLANTCERTDETAIL"
    "PLANTCOMMENT"
    "PLANTFEECOMMENT"
    "PLANTFEESTRUCTURE"
    "PLANTFEESTRUCTUREOUT"
    "PLANTHOLDTB"
    "PLANTTB"
    "PRIVATELABELBILL"
    "PrivateLabelTemplate"
    "ProducedIn1Tb"
    "ProductJob"
    "ProductJobLineItem"
    "PurchaseOrder"
    "RCTB"
    "StripeCustomer"
    "ThirdPartyBillingCompany"
    "USEDIN1TB"
    "VISIT"
    "VISITSCOMMENT"
    "YoshonInfo"
)

successful=0
failed=0

# Test each endpoint
for endpoint in "${endpoints[@]}"; do
    echo -n "Testing $endpoint... "
    
    response=$(curl -s -w "%{http_code}" -o /tmp/response.json "$BASE_URL/$endpoint")
    
    if [ "$response" -eq 200 ]; then
        record_count=$(jq '. | if type=="object" and has("data") then .data | length else if type=="array" then length else 0 end end' /tmp/response.json 2>/dev/null || echo "0")
        echo "✅ Success ($record_count records)"
        ((successful++))
    else
        echo "❌ Failed (HTTP $response)"
        ((failed++))
    fi
    
    sleep 0.1  # Small delay
done

# Print summary
echo ""
echo "Summary:"
echo "========"
echo "Total endpoints: ${#endpoints[@]}"
echo "Successful: $successful"
echo "Failed: $failed"
echo "Success rate: $(( (successful * 100) / ${#endpoints[@]} ))%"

# Clean up
rm -f /tmp/response.json
