# Removes local source files for the sample fields and layouts deleted from the org
# by manifest/cleanup-fields and manifest/cleanup-layouts. Run from C:\Lumenfield-accord
# AFTER both destructive deploys succeed, so the repo matches the org.

$fields = @(
  'Account\fields\Active__c', 'Account\fields\CustomerPriority__c', 'Account\fields\NumberofLocations__c',
  'Account\fields\SLAExpirationDate__c', 'Account\fields\SLASerialNumber__c',
  'Account\fields\UpsellOpportunity__c',
  'Case\fields\EngineeringReqNumber__c', 'Case\fields\PotentialLiability__c', 'Case\fields\Product__c',
  'Case\fields\SLAViolation__c',
  'Contact\fields\Languages__c', 'Contact\fields\Level__c',
  'Lead\fields\CurrentGenerators__c', 'Lead\fields\NumberofLocations__c', 'Lead\fields\Primary__c',
  'Lead\fields\ProductInterest__c', 'Lead\fields\SICCode__c',
  'Opportunity\fields\CurrentGenerators__c', 'Opportunity\fields\DeliveryInstallationStatus__c',
  'Opportunity\fields\MainCompetitors__c', 'Opportunity\fields\OrderNumber__c',
  'ServiceContract\fields\Production_estimate_given_at_signing_Wh__c'
)
$base = 'force-app\main\default'
foreach ($f in $fields) {
  $p = Join-Path $base "objects\$f.field-meta.xml"
  if (Test-Path $p) { Remove-Item $p; Write-Host "removed $p" }
}
$other = @(
  'layouts\Account-Account %28Marketing%29 Layout.layout-meta.xml',
  'layouts\Account-Account %28Sales%29 Layout.layout-meta.xml',
  'layouts\Account-Account %28Support%29 Layout.layout-meta.xml',
  'layouts\Case-Case %28Marketing%29 Layout.layout-meta.xml',
  'layouts\Case-Case %28Sales%29 Layout.layout-meta.xml',
  'layouts\Case-Case %28Support%29 Layout.layout-meta.xml',
  'permissionsets\Experience_Profile_Manager.permissionset-meta.xml'
)
foreach ($o in $other) {
  $p = Join-Path $base $o
  if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p; Write-Host "removed $p" }
}
Write-Host "Done. Layouts that still list a deleted field: re-retrieve them with"
Write-Host "  sf project retrieve start -o lumenfield -m Layout"
