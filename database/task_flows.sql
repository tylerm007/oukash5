
-- Lane: Initial

EXEC sp_add_flow @from_name = 'Start_Application_Submitted', @to_name = 'AssignNCRC', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Company', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Plant', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Product', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Ingredients', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Contact', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'verify Company', @to_name = 'All Verified Gateway', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'verify Plant', @to_name = 'All Verified Gateway', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'verify Contact', @to_name = 'All Verified Gateway', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'verify Product', @to_name = 'All Verified Gateway', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'verify Ingredients', @to_name = 'All Verified Gateway', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'All Verified Gateway', @to_name = 'to Withdrawn Y/N', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'All Verified Gateway', @to_name = 'to Withdrawn Y/N', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Initial Collector', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Assign Product', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Assign Ingredients', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Contact Customer', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Assign Product', @to_name = 'Initial Collector', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Assign Ingredients', @to_name = 'Initial Collector', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Contact Customer', @to_name = 'Initial Collector', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Initial Collector', @to_name = 'Start NDA', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Initial Collector', @to_name = 'Inspection Needed', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Initial Collector', @to_name = 'Start Ingredients Stage', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Initial Collector', @to_name = 'Start Products Stage', @condition = 'None'; 

GO

-- Lane: NDA

EXEC sp_add_flow @from_name = 'Start NDA', @to_name = 'Needs NDA', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Needs NDA', @to_name = 'Send NDA', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Needs NDA', @to_name = 'NDA Completed', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Send NDA', @to_name = 'NDA Executed by Legal', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'NDA Executed by Legal', @to_name = 'NDA Completed', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'NDA Completed', @to_name = 'NDA End', @condition = 'NO'; 

GO

-- Lane: Inspection

EXEC sp_add_flow @from_name = 'Inspection Needed', @to_name = 'End Inspection', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Inspection Needed', @to_name = 'Set Inspection Fee', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Set Inspection Fee', @to_name = 'Send KIM Invoice', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Send KIM Invoice', @to_name = 'Invoice Paid', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Invoice Paid', @to_name = 'Assign RFR', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Invoice Paid', @to_name = 'Payment Overdue', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Assign RFR', @to_name = 'RFR Assigned', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'RFR Assigned', @to_name = 'EIR Received/Reviewed', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'EIR Received/Reviewed', @to_name = 'Notify IAR of EIR', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Notify IAR of EIR', @to_name = 'End Inspection', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'End Inspection', @to_name = 'End Inspection', @condition = 'None'; 

GO

-- Lane: Ingredients

EXEC sp_add_flow @from_name = 'Start Ingredients Stage', @to_name = 'Upload to KASH DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Upload to KASH DB', @to_name = 'Verify Ingredients in DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Verify Ingredients in DB', @to_name = 'End Ingredients', @condition = 'None'; 

GO

-- Lane: Products

EXEC sp_add_flow @from_name = 'Start Products Stage', @to_name = 'Upload to KASH DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Upload to KASH DB', @to_name = 'Verify Products in DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Verify Products in DB', @to_name = 'End Products', @condition = 'None'; 

GO

-- Lane: Contract


GO

-- Lane: Certification


GO
