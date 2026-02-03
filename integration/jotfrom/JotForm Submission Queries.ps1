<#
# Function Name: Truncate-String
# Parameters:
#   - str   : [string]     String to display
#   - len   : [int]        Length to cap
# Returns:
#   - Truncated string or original if shorter than len
# Description:
#   If the string length is less than or equal to len, return the complete string.
#   Otherwise, truncate the string after len characters
#>
Function Truncate-String {
    param(
        [string]$str,
        [int]$len
    )
 
    if ($str -eq $null) { return '' }
    if ($str.Length -le $len) { 
        return $str 
    } else {
        return $str.Substring(0,$len)
    }
}

# JotForm API key
$apiKey = $env:JotFormAPIKey

# JotForm base URL
$baseUrl = "https://ou.jotform.com"

# ID of Kashrus team
$teamID = "240425799590063"

$headers = @{
    'jf-team-id' = $teamID
    'apiKey' = $apiKey
}

# ID of the PROD Kashrus Application form
$formID = "243646438272058"

# ID of TEST application form
#$formID = "253065393574867"

# get form info
$formUrl = "$($baseUrl)/API/form/$($formID)?&apiKey=$($apiKey)"
$formResponse = Invoke-RestMethod -Uri $formUrl -Method Get -Headers $headers
$formResponse.content

# get form properties - including HTML
$propertiesUrl = "$baseUrl/API/form/$($formID)/properties?limit=1000&apiKey=$($apiKey)"
$propertiesResponse = Invoke-RestMethod -Uri $propertiesUrl -Method Get -Headers $headers
#$propertiesResponse.content

# form submissions 
$submissionsUrl = "$baseUrl/API/form/$($formID)/submissions?limit=1000&apiKey=$($apiKey)"
$submissionsResponse = Invoke-RestMethod -Uri $submissionsUrl -Method Get -Headers $headers
#$submissionsResponse.content

# given a JotForm submission, display ALL fields of the submission (except the types below)

# example of a submission after the JotForm API call above
$submission = $submissionsResponse.content[0]

$subList = @()
$submission.answers.PSObject.Properties.Value | ForEach-Object {
    if ($_.type -notmatch "control_(text$|head|button|widget|pagebreak|collapse)$") {
        if ($_.type -eq 'control_fullname') {
            $subList += [PSCustomObject]@{ Order = [int]$_.order; Name  = 'contactFirst'; Type  = $_.type; Answer = $_.answer.first; Text  = Truncate-String $_.text 350 }
            $subList += [PSCustomObject]@{ Order = [int]$_.order; Name  = 'contactLast'; Type  = $_.type; Answer = $_.answer.last; Text  = Truncate-String $_.text 350 }
        } else {
            $subList += [PSCustomObject]@{ Order = [int]$_.order; Name  = $_.name; Type  = $_.type; Answer = $_.answer; Text  = Truncate-String $_.text 350 } 
        }
    }
}

$sublist | select Name, text, answer | ft -AutoSize