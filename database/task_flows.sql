
-- Lane: Initial

EXEC sp_add_flow @from_name = 'Start_Application_Submitted', @to_name = 'Init Lane start', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Init Lane start', @to_name = 'AssignNCRC', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'All Verified Gateway', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'All Verified Gateway', @to_name = 'to Withdrawn Y/N', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'End', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Contact Customer', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Start NDA', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Assign Product', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Assign Ingredients', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Start Inspection', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Assign Product', @to_name = 'Start Products Stage', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Assign Product', @to_name = 'Initial Collector', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Assign Ingredients', @to_name = 'Start Ingredients Stage', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Assign Ingredients', @to_name = 'Initial Collector', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Contact Customer', @to_name = 'Initial Collector', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Initial Collector', @to_name = 'Init App End', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Stage Collector', @to_name = 'Start Contract Stage', @condition = 'None'; 

GO

-- Lane: NDA

EXEC sp_add_flow @from_name = 'Start NDA', @to_name = 'Needs NDA', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Needs NDA', @to_name = 'Send NDA', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Needs NDA', @to_name = 'NDA End', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Send NDA', @to_name = 'NDA Executed by Legal', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'NDA Executed by Legal', @to_name = 'NDA Completed', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'NDA Completed', @to_name = 'NDA End', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'NDA End', @to_name = 'Stage Collector', @condition = 'None'; 

GO

-- Lane: Inspection

EXEC sp_add_flow @from_name = 'Start Inspection', @to_name = 'Is Inspection Needed', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Is Inspection Needed', @to_name = 'End Inspection', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Is Inspection Needed', @to_name = 'Assign Fee Structure', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Assign Fee Structure', @to_name = 'Select RFR', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Select RFR', @to_name = 'Assign Invoice Amount', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Assign Invoice Amount', @to_name = 'Generated Invoice and Send', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Generated Invoice and Send', @to_name = 'Mark Invoice Paid', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Mark Invoice Paid', @to_name = 'Schedule Inspection', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Schedule Inspection', @to_name = 'Inspection Report Submitted to IAR', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Inspection Report Submitted to IAR', @to_name = 'Withdraw Application', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Withdraw Application', @to_name = 'End Inspection', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Withdraw Application', @to_name = 'End', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'End Inspection', @to_name = 'Stage Collector', @condition = 'None'; 

GO

-- Lane: Ingredients

EXEC sp_add_flow @from_name = 'Start Ingredients Stage', @to_name = 'Upload Ingredients to KASH DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Upload Ingredients to KASH DB', @to_name = 'Verify Ingredients in DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Verify Ingredients in DB', @to_name = 'End Ingredients', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'End Ingredients', @to_name = 'Stage Collector', @condition = 'None'; 

GO

-- Lane: Products

EXEC sp_add_flow @from_name = 'Start Products Stage', @to_name = 'Upload Product to KASH DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Upload Product to KASH DB', @to_name = 'Verify Products in DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Verify Products in DB', @to_name = 'End Products', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'End Products', @to_name = 'Stage Collector', @condition = 'None'; 

GO

-- Lane: Contract

EXEC sp_add_flow @from_name = 'Start Contract Stage', @to_name = 'Prepare Contract', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Prepare Contract', @to_name = 'Send Contract', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Send Contract', @to_name = 'Contract Signed Y/N', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Contract Signed Y/N', @to_name = 'End Contract', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Contract Signed Y/N', @to_name = 'End', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'End Contract', @to_name = 'Start Certification Stage', @condition = 'None'; 

GO

-- Lane: Certification

EXEC sp_add_flow @from_name = 'Start Certification Stage', @to_name = 'Issue Certificate', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Issue Certificate', @to_name = 'Notify Customer', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Notify Customer', @to_name = 'End Certification', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'End Certification', @to_name = 'End', @condition = 'None'; 

GO
